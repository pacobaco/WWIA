from typing import Dict, List, Any
import numpy as np
from .data_collector import collect_posts
from .polarity_scorer import PolarityScorer
from .aggregator import weighted_mean, der_polarization
from .config import load_config

def compute_country_bias(
    country: str,
    posts: List[Dict] | None = None,
    kappa: float | None = None,
    alpha: float | None = None,
) -> Dict[str, Any]:
    cfg = load_config()
    kappa = kappa if kappa is not None else cfg.get("kappa", 1.0)
    alpha = alpha if alpha is not None else cfg.get("alpha", 0.5)

    if posts is None:
        posts = collect_posts(country)

    if len(posts) < cfg.get("min_posts", 5):
        return {
            "country": country.upper(),
            "B_C": 0.0, "mu": 0.0, "Pi": 0.0,
            "n_posts": len(posts), "status": "insufficient_data",
        }

    texts = [p["text"] for p in posts]
    engagements = np.array([p.get("engagement", 1) for p in posts], dtype=float)

    scorer = PolarityScorer()
    polarities = scorer.score_texts(texts)

    mu = weighted_mean(polarities, engagements if cfg.get("weight_by_engagement") else None)
    Pi = der_polarization(polarities, alpha=alpha, weights=engagements)
    B = float(np.clip(mu * (1.0 + kappa * Pi), -1.0, 1.0))

    return {
        "country": country.upper(),
        "B_C": B, "mu": float(mu), "Pi": float(Pi),
        "n_posts": len(posts), "status": "ok",
    }
