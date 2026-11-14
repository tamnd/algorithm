# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cusum/. The authors are listed in prov/ST2SET.jsonl.
"""Page's CUSUM procedure for online change detection.

Before the change the observations have density f0, after it f1. With the
log likelihood ratio increments Z_t = log f1(x_t) - log f0(x_t), the CUSUM
statistic is S_0 = 0, S_t = max(0, S_(t-1) + Z_t). It equals the largest log
likelihood ratio of "the change happened at time k" over k = 1, ..., t + 1
(k = t + 1 means no change yet). An alarm sounds at the first t with S_t >= h.

Cost O(1) time and O(1) memory per observation.
"""

import math
from collections.abc import Callable, Iterable


def cusum_scores(zs: Iterable[float], h: float) -> tuple[int | None, int | None, list[float]]:
    """Run CUSUM on given increments. Returns (alarm time, change estimate, statistics).

    The alarm time is the first t (1-based) with S_t >= h, or None. The change
    estimate is the first index of the maximizing segment, that is the time of
    the last reset plus 1. Precondition: h > 0.
    """
    if h <= 0:
        raise ValueError("h must be positive")
    s = 0  # @line L1
    k = 1  # @line L1
    t = 0  # @line L1
    path = []
    for z in zs:  # @line L2
        t += 1  # @line L3
        s = s + z  # @line L4
        if s <= 0:  # @line L5
            s = 0  # @line L5
            k = t + 1  # @line L5
        path.append(s)
        if s >= h:  # @line L6
            return t, k, path  # @line L6
    return None, None, path  # @line L7


def cusum(stream: Iterable[float], log_f0: Callable[[float], float], log_f1: Callable[[float], float],
          h: float) -> tuple[int | None, int | None]:
    """CUSUM on raw observations with known pre-change and post-change log densities."""
    t, k, _ = cusum_scores((log_f1(x) - log_f0(x) for x in stream), h)
    return t, k


def gaussian_mean_shift_scores(xs: Iterable[float], mu0: float, mu1: float, sigma: float) -> list[float]:
    """Z_t for N(mu0, sigma^2) -> N(mu1, sigma^2): (mu1 - mu0) / sigma^2 * (x - (mu0 + mu1) / 2)."""
    d = (mu1 - mu0) / (sigma * sigma)
    m = 0.5 * (mu0 + mu1)
    return [d * (x - m) for x in xs]


def brute_force_statistic(zs: list[float], t: int) -> tuple[float, int]:
    """max over k in 1..t+1 of sum_(i=k)^t z_i, with the largest maximizing k (O(t^2))."""
    best, arg = 0, t + 1
    for k in range(t, 0, -1):
        total = sum(zs[k - 1:t])
        if total > best:
            best, arg = total, k
    return best, arg


def two_sided_gaussian(xs: Iterable[float], mu0: float, delta: float, sigma: float,
                       h: float) -> int | None:
    """Two CUSUMs, for a shift up by delta and down by delta. Returns the first alarm time."""
    up = down = 0.0
    for t, x in enumerate(xs, 1):
        u = (x - mu0) / sigma
        up = max(0.0, up + delta * u - 0.5 * delta * delta)
        down = max(0.0, down - delta * u - 0.5 * delta * delta)
        if up >= h or down >= h:
            return t
    return None


def gaussian_log_density(mu: float, sigma: float) -> Callable[[float], float]:
    c = -math.log(sigma * math.sqrt(2.0 * math.pi))
    return lambda x: c - 0.5 * ((x - mu) / sigma) ** 2
