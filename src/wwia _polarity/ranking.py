"""World ranking by Range of Multipolarity."""
from typing import List, Dict, Any
import pandas as pd
from .multipolar import build_multipolar_matrix
from .multipolar_range import compute_all_country_ranges
from .config import load_config

def rank_by_multipolarity_range(
    countries: List[str] | None = None,
    M: pd.DataFrame | None = None,
) -> List[Dict[str, Any]]:
    cfg = load_config()
    tiers = cfg.get("range_tiers", {})
    extreme = tiers.get("extreme", 1.0)
    high = tiers.get("high", 0.70)
    mod_high = tiers.get("moderate_high", 0.50)
    moderate = tiers.get("moderate", 0.30)

    if countries is None:
        countries = [c.strip() for c in cfg.get("default_countries", "US,IL,IR,SA").split(",") if c.strip()]
    if M is None:
        M = build_multipolar_matrix(countries)

    ranges = compute_all_country_ranges(M)
    ranked = sorted(ranges.items(), key=lambda x: -x[1])

    result = []
    for rank, (country, r) in enumerate(ranked, 1):
        if r >= extreme:
            tier = "Extreme"
        elif r >= high:
            tier = "High"
        elif r >= mod_high:
            tier = "Moderate-High"
        elif r >= moderate:
            tier = "Moderate"
        else:
            tier = "Low"
        result.append({
            "rank": rank,
            "country": country,
            "R_C": round(float(r), 3),
            "tier": tier,
        })
    return result
