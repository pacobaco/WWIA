from typing import Dict, List, Any
import pandas as pd
from .config import load_config
from .formula import compute_country_bias
from .multipolar import build_multipolar_matrix

def conflict_potential(M: pd.DataFrame, i: str, j: str) -> float:
    return -min(M.loc[i, j], M.loc[j, i])

def apply_threshold_vector(
    countries: List[str] | None = None,
    M: pd.DataFrame | None = None,
) -> Dict[str, Any]:
    cfg = load_config()
    T = cfg.get("threshold", {})
    t_dom = T.get("t_dom", 0.60)
    t_Pi = T.get("t_Pi", 0.40)
    t_CP = T.get("t_CP", 0.50)
    t_hot = T.get("t_hot", 0.70)

    if countries is None:
        countries = [c.strip() for c in cfg.get("default_countries", "IL,IR,SA,YE,US,UA,RU").split(",")]
    if M is None:
        M = build_multipolar_matrix(countries)

    domestic = {c: compute_country_bias(c) for c in countries}
    flags = {"ongoing": [], "potential": [], "watch": [], "details": {}}

    for c in countries:
        d = domestic[c]
        breaches = []
        if abs(d["B_C"]) >= t_dom:
            breaches.append("t_dom")
        if d["Pi"] >= t_Pi:
            breaches.append("t_Pi")

        for other in countries:
            if c == other:
                continue
            cp = conflict_potential(M, c, other)
            if cp >= t_hot:
                flags["ongoing"].append(f"{c}-{other}")
                breaches.append("t_hot")
            elif cp >= t_CP:
                flags["potential"].append(f"{c}-{other}")
                breaches.append("t_CP")

        if breaches:
            flags["details"][c] = {"breaches": breaches, "B_C": d["B_C"], "Pi": d["Pi"]}

    flags["ongoing"] = list(set(flags["ongoing"]))
    flags["potential"] = list(set(flags["potential"]))
    return flags

def rank_countries_by_risk(countries: List[str] | None = None) -> List[Dict]:
    flags = apply_threshold_vector(countries)
    scores = {}
    for pair in flags["ongoing"]:
        a, b = pair.split("-")
        scores[a] = scores.get(a, 0) + 40
        scores[b] = scores.get(b, 0) + 40
    for pair in flags["potential"]:
        a, b = pair.split("-")
        scores[a] = scores.get(a, 0) + 20
        scores[b] = scores.get(b, 0) + 20
    for c, det in flags["details"].items():
        scores[c] = scores.get(c, 0) + 10 * len(det["breaches"])

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    result = []
    for rank, (country, score) in enumerate(ranked, 1):
        tier = "Ongoing Major" if score >= 80 else "Elevated" if score >= 50 else "Watch"
        result.append({"rank": rank, "country": country, "score": min(score, 100), "tier": tier})
    return result
