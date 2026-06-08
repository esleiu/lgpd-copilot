from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    model: str
    tier: str
    reason: str


class ModelRouter:
    def __init__(self, cheap_model: str | None = None, strong_model: str | None = None) -> None:
        self.cheap_model = cheap_model or os.getenv("OPENAI_MODEL_CHEAP", "gpt-4.1-mini")
        self.strong_model = strong_model or os.getenv("OPENAI_MODEL_STRONG", "gpt-4.1")

    def route(self, question: str) -> RouteDecision:
        normalized = question.lower()
        complex_markers = [
            "compare",
            "risco",
            "base legal",
            "sensivel",
            "sensível",
            "incidente",
            "retenção",
            "retencao",
            "arquitetura",
            "decisão",
            "decisao",
        ]
        if len(question) > 220 or any(marker in normalized for marker in complex_markers):
            return RouteDecision(self.strong_model, "strong", "Pergunta complexa ou de maior risco juridico.")
        return RouteDecision(self.cheap_model, "cheap", "Pergunta direta; rota barata suficiente.")

    @staticmethod
    def estimate_cost_reduction(strong_calls: int, cheap_calls: int, cache_hits: int) -> float:
        total = strong_calls + cheap_calls + cache_hits
        if total == 0:
            return 0.0
        # Estimativa simples: chamada barata custa 20% da forte; cache custa 0.
        baseline = total * 1.0
        actual = strong_calls * 1.0 + cheap_calls * 0.2
        return round((1 - actual / baseline) * 100, 2)
