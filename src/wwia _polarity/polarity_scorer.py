import numpy as np
from typing import List
from .embedder import Embedder

class PolarityScorer:
    def __init__(self, embedder: Embedder | None = None, target_country: str | None = None):
        self.embedder = embedder or Embedder()
        self.target_country = target_country

        if target_country:
            pos = [
                f"{target_country} is a reliable partner and force for stability",
                f"cooperation and constructive relations with {target_country}",
            ]
            neg = [
                f"{target_country} is a threat and aggressive actor",
                f"hostility and confrontation against {target_country}",
            ]
            self.axis = self.embedder.build_axis(neg, pos)
        else:
            left = ["social justice equity climate action progressive taxation"]
            right = ["free market capitalism strong borders traditional values national security"]
            self.axis = self.embedder.build_axis(left, right)

    def score_texts(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        emb = self.embedder.encode(texts)
        raw = emb @ self.axis
        z = (raw - raw.mean()) / (raw.std() + 1e-8)
        return np.tanh(z)
