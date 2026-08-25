"""Range of Multipolarity metrics – core of v0.4.0"""
from typing import List, Dict
import numpy as np
import pandas as pd

def multipolar_range(M: pd.DataFrame, countries: List[str]) -> float:
    """R(S) for any set of nations (ideally ≥3)."""
    if len(countries) < 2:
        return 0.0
    countries = [c.upper() for c in countries]
    missing = [c for c in countries if c not in M.index]
    if missing:
        return 0.0
    sub = M.loc[countries, countries]
    mask = ~np.eye(len(countries), dtype=bool)
    vals = sub.values[mask]
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return 0.0
    return float(np.max(vals) - np.min(vals))

def country_range(M: pd.DataFrame, country: str) -> float:
    """R_C – range of all directed polarities involving country C."""
    country = country.upper()
    if country not in M.index:
        return 0.0
    outgoing = M.loc[country].drop(country, errors="ignore").values
    incoming = M[country].drop(country, errors="ignore").values
    vals = np.concatenate([outgoing, incoming])
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return 0.0
    return float(np.max(vals) - np.min(vals))

def compute_all_country_ranges(M: pd.DataFrame) -> Dict[str, float]:
    return {c: country_range(M, c) for c in M.index}
