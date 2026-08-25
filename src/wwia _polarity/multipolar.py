from typing import Dict, List, Any
import numpy as np
import pandas as pd
from .data_collector import collect_posts
from .polarity_scorer import PolarityScorer
from .aggregator import weighted_mean, der_polarization
from .config import load_config

COUNTRY_ALIASES = {
    "IL": ["israel", "israeli", "tel aviv", "netanyahu"],
    "IR": ["iran", "iranian", "tehran", "hormuz"],
    "SA": ["saudi", "saudi arabia", "riyadh"],
    "YE": ["yemen", "houthi", "sanaa"],
    "US": ["united states", "america", "usa", "washington", "trump"],
    "UA": ["ukraine", "ukrainian", "kyiv", "zelensky"],
    "RU": ["russia", "russian", "moscow", "putin"],
    "TR": ["turkey", "türkiye", "turkish", "ankara"],
    "PK": ["pakistan", "pakistani", "islamabad"],
    "CN": ["china", "chinese", "beijing", "xi"],
    "TW": ["taiwan", "taipei"],
}

def extract_directed_corpus(posts: List[Dict], target: str) -> List[Dict]:
    aliases = COUNTRY_ALIASES.get(target.upper(), [target.lower()])
    return [p for p in posts if any(a in p["text"].lower() for a in aliases)]

def compute_directed_bias(
    source: str, target: str,
    posts: List[Dict] | None = None,
    kappa: float | None = None, alpha: float | None = None,
) -> Dict[str, Any]:
    cfg = load_config()
    kappa = kappa if kappa is not None else cfg.get("kappa", 1.0)
    alpha = alpha if alpha is not None else cfg.get("alpha", 0.5)

    if posts is None:
        posts = collect_posts(source)

    directed = extract_directed_corpus(posts, target)
    if len(directed) < cfg.get("min_posts", 3):
        return {
            "source": source.upper(), "target": target.upper(),
            "B_ij": 0.0, "mu": 0.0, "Pi": 0.0,
            "n_posts": len(directed), "status": "insufficient_mentions",
        }

    texts = [p["text"] for p in directed]
    engagements = np.array([p.get("engagement", 1) for p in directed], dtype=float)

    scorer = PolarityScorer(target_country=target)
    polarities = scorer.score_texts(texts)

    mu = weighted_mean(polarities, engagements)
    Pi = der_polarization(polarities, alpha=alpha, weights=engagements)
    B = float(np.clip(mu * (1.0 + kappa * Pi), -1.0, 1.0))

    return {
        "source": source.upper(), "target": target.upper(),
        "B_ij": B, "mu": float(mu), "Pi": float(Pi),
        "n_posts": len(directed), "status": "ok",
    }

def build_multipolar_matrix(
    countries: List[str],
    posts_cache: Dict[str, List[Dict]] | None = None,
) -> pd.DataFrame:
    n = len(countries)
    mat = np.zeros((n, n))
    for i, src in enumerate(countries):
        src_posts = (posts_cache or {}).get(src) or collect_posts(src)
        for j, tgt in enumerate(countries):
            if i == j:
                continue
            res = compute_directed_bias(src, tgt, posts=src_posts)
            mat[i, j] = res["B_ij"]
    return pd.DataFrame(mat, index=[c.upper() for c in countries], columns=[c.upper() for c in countries])
