from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
from .tokenizer import WWIATokenizer

class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model = SentenceTransformer(model_name)
        self.tokenizer = WWIATokenizer(model_name)

    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    def build_axis(self, neg_texts: List[str], pos_texts: List[str]) -> np.ndarray:
        neg_emb = self.encode(neg_texts).mean(axis=0)
        pos_emb = self.encode(pos_texts).mean(axis=0)
        axis = pos_emb - neg_emb
        norm = np.linalg.norm(axis)
        return axis / (norm + 1e-8)
