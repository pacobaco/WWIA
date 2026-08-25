import numpy as np
from scipy.stats import gaussian_kde

def weighted_mean(polarities: np.ndarray, weights: np.ndarray | None = None) -> float:
    if len(polarities) == 0:
        return 0.0
    if weights is None:
        return float(np.mean(polarities))
    return float(np.average(polarities, weights=weights))

def der_polarization(polarities: np.ndarray, alpha: float = 0.5, weights: np.ndarray | None = None) -> float:
    if len(polarities) < 5:
        return 0.0
    if weights is None:
        weights = np.ones_like(polarities)
    try:
        kde = gaussian_kde(polarities, weights=weights)
    except Exception:
        return 0.0
    xs = np.linspace(polarities.min() - 0.15, polarities.max() + 0.15, 180)
    dens = kde(xs)
    dens = dens / (dens.sum() + 1e-12)
    P = 0.0
    for i, x in enumerate(xs):
        for j, y in enumerate(xs):
            P += (dens[i] ** (1 + alpha)) * dens[j] * abs(y - x)
    return float(min(P / 2.0, 1.0))
