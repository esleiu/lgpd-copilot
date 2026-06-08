from __future__ import annotations

import html
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.observability.trace import JsonlTracer
from src.pipeline.cache import ResponseCache
from src.pipeline.routing import ModelRouter
from src.pipeline.tools import TOOL_SCHEMA, LgpdTools

load_dotenv()


@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float
    page_hint: str


class CorpusStore:
    def __init__(self, corpus_dir: str | Path = "data/corpus", chunk_size: int = 1200, overlap: int = 0) -> None:
        self.corpus_dir = Path(corpus_dir)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.raw_text = self._load_text()
        self.chunks = self._chunk_text(self.raw_text)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode")
        self.matrix = self.vectorizer.fit_transform([chunk.text for chunk in self.chunks])

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            RetrievedChunk(
                text=self.chunks[idx].text,
                source=self.chunks[idx].source,
                score=float(scores[idx]),
                page_hint=self.chunks[idx].page_hint,
            )
            for idx in top_indices
            if scores[idx] > 0
        ]

    def _load_text(self) -> str:
        parts: list[str] = []
        for path in sorted(self.corpus_dir.glob("*")):
            if path.suffix.lower() not in {".md", ".txt", ".html", ".htm"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if path.suffix.lower() in {".html", ".htm"}:
                text = self._html_to_text(text)
            parts.append(f"\n\n[Fonte: {path.name}]\n{text}")
        if not parts:
            raise FileNotFoundError(f"Nenhum corpus encontrado em {self.corpus_dir}")
        return "\n".join(parts)

    def _chunk_text(self, text: str) -> list[RetrievedChunk]:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks: list[RetrievedChunk] = []
        current = ""
        source = "corpus"
        page_hint = "sem pagina"

        for paragraph in paragraphs:
            if paragraph.startswith("[Fonte:"):
                source = paragraph.removeprefix("[Fonte:").removesuffix("]").strip()
                continue
            if paragraph.lower().startswith("## pagina"):
                page_hint = paragraph.replace("## ", "").strip()
            if len(current) + len(paragraph) + 2 > self.chunk_size and current:
                chunks.append(RetrievedChunk(current.strip(), source, 0.0, page_hint))
                prefix = current[-self.overlap :].strip() + "\n\n" if self.overlap else ""
                current = prefix + paragraph
            else:
                current = f"{current}\n\n{paragraph}".strip()

        if current:
            chunks.append(RetrievedChunk(current.strip(), source, 0.0, page_hint))
        return chunks

    @staticmethod
    def _html_to_text(document: str) -> str:
        document = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", document, flags=re.IGNORECASE)
        document = re.sub(r"<[^>]+>", " ", document)
        document = html.unescape(document)
        return re.sub(r"\s+", " ", document)


class LgpdRagPipeline:
    def __init__(
        self,
        corpus: CorpusStore | None = None,
        cache: ResponseCache | None = None,
        router: ModelRouter | None = None,
        tracer: JsonlTracer | None = None,
    ) -> None:
        self.corpus = corpus or CorpusStore()
        self.cache = cache or ResponseCache()
        self.router = router or ModelRouter()
        self.tools = LgpdTools(self.corpus.raw_text)
        self.tracer = tracer or JsonlTracer()
        self.top_k = int(os.getenv("RETRIEVAL_TOP_K", "5"))

    def ask(self, question: str) -> dict[str, Any]:
        cache_hit = self.cache.get(question)
        if cache_hit:
            self.tracer.log("cache_hit", kind=cache_hit.kind, similarity=cache_hit.similarity)
            return {
                "answer": cache_hit.answer,
                "sources": [],
                "route": "cache",
                "cache_hit": cache_hit.kind,
                "cache_similarity": cache_hit.similarity,
            }

        retrieved = self.corpus.retrieve(question, self.top_k)
        route = self.router.route(question)
        answer = self._answer_with_llm(question, retrieved, route.model)
        if not answer:
            answer = self._fallback_answer(question, retrieved)

        self.cache.set(question, answer)
        self.tracer.log(
            "answer_generated",
            route=route.tier,
            model=route.model,
            retrieved=len(retrieved),
            estimated_context_chars=sum(len(chunk.text) for chunk in retrieved),
        )
        return {
            "answer": answer,
            "sources": self._format_sources(retrieved),
            "route": route.tier,
            "model": route.model,
            "route_reason": route.reason,
            "cache_hit": None,
        }

    def _answer_with_llm(self, question: str, retrieved: list[RetrievedChunk], model: str) -> str | None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None

        try:
            from openai import OpenAI
        except ImportError:
            return None

        context = "\n\n---\n\n".join(
            f"Fonte: {chunk.source} | {chunk.page_hint} | score={chunk.score:.3f}\n{chunk.text}"
            for chunk in retrieved
        )
        client = OpenAI(api_key=api_key)
        messages = [
            {
                "role": "system",
                "content": (
                    "Voce e um assistente de compliance LGPD para times de software. "
                    "Responda em portugues, cite artigos quando relevantes, diga limites e nunca substitua parecer juridico."
                ),
            },
            {
                "role": "user",
                "content": f"Pergunta: {question}\n\nContexto recuperado:\n{context}",
            },
        ]

        first = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[TOOL_SCHEMA],
            tool_choice="auto",
            temperature=0.2,
        )
        msg = first.choices[0].message
        if not msg.tool_calls:
            return msg.content or None

        messages.append(msg.model_dump())
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            result = self.tools.execute(call.function.name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": result.name,
                    "content": result.result,
                }
            )

        final = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
        return final.choices[0].message.content

    def _fallback_answer(self, question: str, retrieved: list[RetrievedChunk]) -> str:
        article_match = re.search(r"art(?:igo)?\.?\s*(\d+)", question.lower())
        tool_note = ""
        if article_match:
            tool_note = "\n\nTrecho recuperado pela ferramenta cite_article:\n" + self.tools.cite_article(int(article_match.group(1)))

        if not retrieved:
            return "Nao encontrei contexto suficiente no corpus para responder com seguranca."

        bullets = "\n".join(f"- {chunk.text[:500].strip()}..." for chunk in retrieved[:3])
        return (
            "Resposta baseada no corpus local (modo sem API key):\n\n"
            f"{bullets}"
            f"{tool_note}\n\n"
            "Limite: valide a decisao com responsavel juridico/encarregado antes de producao."
        )

    @staticmethod
    def _format_sources(retrieved: list[RetrievedChunk]) -> list[dict[str, Any]]:
        return [
            {
                "source": chunk.source,
                "page_hint": chunk.page_hint,
                "score": round(chunk.score, 3),
                "preview": chunk.text[:260],
            }
            for chunk in retrieved
        ]
