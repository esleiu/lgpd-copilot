from src.pipeline.cache import ResponseCache
from src.pipeline.rag import CorpusStore, LgpdRagPipeline
from src.pipeline.routing import ModelRouter
from src.pipeline.tools import LgpdTools


def test_retrieval_finds_lgpd_context():
    corpus = CorpusStore()
    chunks = corpus.retrieve("Quais direitos o titular possui na LGPD?", top_k=3)
    assert chunks
    assert any("Art. 18" in chunk.text or "direito" in chunk.text.lower() for chunk in chunks)


def test_cite_article_tool_returns_article_text():
    corpus = CorpusStore()
    tools = LgpdTools(corpus.raw_text)
    result = tools.cite_article(7)
    assert "Art. 7" in result
    assert "consentimento" in result.lower()


def test_cache_exact_and_semantic_hit():
    cache = ResponseCache(semantic_threshold=0.4)
    cache.set("posso armazenar cpf?", "resposta")
    assert cache.get("posso armazenar cpf?").kind == "exact"
    assert cache.get("armazenar cpf pode?").kind == "semantic"


def test_router_uses_strong_for_risk_question():
    router = ModelRouter(cheap_model="cheap", strong_model="strong")
    assert router.route("Compare o risco e a base legal para dados sensiveis").tier == "strong"
    assert router.route("O que diz o Art. 7?").tier == "cheap"


def test_pipeline_runs_without_api_key():
    pipeline = LgpdRagPipeline()
    result = pipeline.ask("Cite o Art. 46 e explique medidas tecnicas.")
    assert result["answer"]
    assert result["sources"]
