from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class CacheHit:
    answer: str
    kind: str
    similarity: float


class ResponseCache:
    def __init__(self, semantic_threshold: float | None = None) -> None:
        self.semantic_threshold = semantic_threshold or float(os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.86"))
        self._answers: dict[str, str] = {}

    def get(self, question: str) -> CacheHit | None:
        key = self._normalize(question)
        if key in self._answers:
            return CacheHit(self._answers[key], "exact", 1.0)

        if not self._answers:
            return None

        questions = list(self._answers.keys())
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode")
        matrix = vectorizer.fit_transform(questions + [key])
        scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score >= self.semantic_threshold:
            return CacheHit(self._answers[questions[best_idx]], "semantic", best_score)
        return None

    def set(self, question: str, answer: str) -> None:
        self._answers[self._normalize(question)] = answer

    def stats(self) -> dict[str, int]:
        return {"items": len(self._answers)}

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.lower().strip().split())
