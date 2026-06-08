from __future__ import annotations

import re
from dataclasses import dataclass


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "cite_article",
        "description": "Retorna o trecho do artigo da LGPD encontrado no corpus local.",
        "parameters": {
            "type": "object",
            "properties": {
                "article_number": {
                    "type": "integer",
                    "description": "Numero do artigo da LGPD. Exemplo: 7 para Art. 7.",
                }
            },
            "required": ["article_number"],
        },
    },
}


@dataclass
class ToolResult:
    name: str
    result: str


class LgpdTools:
    def __init__(self, corpus_text: str) -> None:
        self.corpus_text = corpus_text

    def cite_article(self, article_number: int) -> str:
        pattern = re.compile(
            rf"(Art\.\s*{article_number}\.?[\s\S]*?)(?=\n\n+Art\.\s*\d+\.?|\n\n+## Pagina|\Z)",
            re.IGNORECASE,
        )
        match = pattern.search(self.corpus_text)
        if not match:
            return f"Art. {article_number} nao encontrado no corpus local."
        return match.group(1).strip()

    def execute(self, name: str, arguments: dict) -> ToolResult:
        if name != "cite_article":
            return ToolResult(name, f"Ferramenta desconhecida: {name}")
        article_number = int(arguments["article_number"])
        return ToolResult(name, self.cite_article(article_number))
