# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bca-bootstrap-interval/. The authors are listed in prov/HRG7H4.jsonl.

import math
import random
from fractions import Fraction
from statistics import NormalDist
from typing import Callable, Sequence

Statistic = Callable[[Sequence[float]], float]
STD_NORMAL = NormalDist()


def empirical_quantile(sorted_values: Sequence[float], p: float) -> float:
    """inf{t : G(t) >= p}: the ceil(b p)-th smallest value, or the smallest for p = 0."""
    k = max(1, math.ceil(Fraction(p) * len(sorted_values)))
    return sorted_values[k - 1]


def jackknife_acceleration(x: Sequence[float], statistic: Statistic) -> float:
    """a = sum d_i^3 / (6 (sum d_i^2)^(3/2)) with d_i = theta_(.) - theta_(i)."""
    n = len(x)
    loo = [statistic(list(x[:i]) + list(x[i + 1 :])) for i in range(n)]
    dot = math.fsum(loo) / n
    d = [dot - t for t in loo]
    s2 = math.fsum(v * v for v in d)
    if s2 == 0:
        return 0.0
    return math.fsum(v**3 for v in d) / (6.0 * s2**1.5)


def bca_levels(z0: float, a: float, alpha: float) -> tuple:
    """The adjusted levels alpha_1 and alpha_2 of Efron (1987)."""
    out = []
    for z in (STD_NORMAL.inv_cdf(alpha / 2), STD_NORMAL.inv_cdf(1 - alpha / 2)):
        w = z0 + z
        denom = 1 - a * w
        if denom <= 0:
            raise ValueError("the acceleration is too large for this level")
        out.append(STD_NORMAL.cdf(z0 + w / denom))
    return out[0], out[1]


def bca_interval(
    x: Sequence[float],
    statistic: Statistic,
    alpha: float,
    b: int,
    rng: random.Random,
    acceleration: float | None = None,
) -> tuple:
    """The 1 - alpha BCa interval [G^{-1}(alpha_1), G^{-1}(alpha_2)].

    acceleration=None estimates a by the jackknife; a number fixes it.
    Returns (lo, hi, z0, a).
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    n = len(x)
    if n < 2 or b < 1:
        raise ValueError("need n >= 2 and b >= 1")
    theta_hat = statistic(x)  # @line L1
    reps = []
    for _ in range(b):  # @line L2
        xs = [x[rng.randrange(n)] for _ in range(n)]  # @line L3
        reps.append(statistic(xs))  # @line L4
    reps.sort()
    below = sum(1 for t in reps if t < theta_hat)  # @line L5
    if below == 0 or below == b:
        raise ValueError("all replicates lie on one side of the estimate; z0 is infinite")
    z0 = STD_NORMAL.inv_cdf(below / b)  # @line L6
    a = jackknife_acceleration(x, statistic) if acceleration is None else acceleration  # @line L7
    a1, a2 = bca_levels(z0, a, alpha)  # @line L8
    return empirical_quantile(reps, a1), empirical_quantile(reps, a2), z0, a  # @line L9
