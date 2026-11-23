# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-sensitivity/. The authors are listed in prov/0ZFFMP.jsonl.
"""The smooth sensitivity framework of Nissim, Raskhodnikova and Smith
(2007), for the median of values in a known range [0, lam].

Neighbors replace one value by another, so n is fixed. The local
sensitivity of the median at y is how far one change can move the median
of y. The beta-smooth sensitivity is S*(x) = max over k >= 0 of
exp(-k beta) A(k, x), where A(k, x) is the largest local sensitivity over
the datasets within k changes of x. Noise scaled to S*(x) gives privacy:
Cauchy noise for pure DP, and Laplace noise for (epsilon, delta)-DP.

The code uses random.Random so that the tests can be repeated, and float
noise. A real release needs a cryptographic source of randomness and exact
sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Sequence


def median(xs: Sequence[float]) -> float:
    """The median x_m of an odd number of values, m = (n + 1)/2 in 1-based order. Cost: O(n log n)."""
    if len(xs) % 2 == 0 or not xs:
        raise ValueError("n must be odd")
    return sorted(xs)[len(xs) // 2]


def _padded(xs: Sequence[float], lam: float):
    s = sorted(xs)
    n = len(s)

    def at(i: int) -> float:  # 1-based, with x_i = 0 for i <= 0 and x_i = lam for i > n
        if i <= 0:
            return 0.0
        if i > n:
            return float(lam)
        return float(s[i - 1])

    return at, n


def ball_sensitivity(xs: Sequence[float], k: int, lam: float) -> float:
    """A(k, x) = max over t = 0..k+1 of x_{m+t} - x_{m+t-k-1}: the largest local sensitivity within k changes.

    Precondition: n odd, values in [0, lam], k >= 0. Cost: O(n log n + k).
    """
    at, n = _padded(xs, lam)
    m = (n + 1) // 2
    return max(at(m + t) - at(m + t - k - 1) for t in range(k + 2))


def smooth_sensitivity_median(xs: Sequence[float], beta: float, lam: float) -> float:
    """The beta-smooth sensitivity of the median (NRS Proposition 3.4).

    S*(x) = max over k = 0..n of exp(-k beta) A(k, x). For k >= n, A(k, x) = lam.
    Precondition: n odd, values in [0, lam], beta > 0. Cost: O(n^2) with this direct
    formula; NRS give an O(n log n) algorithm.
    """
    if beta <= 0:
        raise ValueError("beta must be positive")
    at, n = _padded(xs, lam)
    m = (n + 1) // 2
    best = 0.0
    for k in range(n + 1):  # @line L1
        a_k = max(at(m + t) - at(m + t - k - 1) for t in range(k + 2))  # @line L2
        best = max(best, math.exp(-k * beta) * a_k)  # @line L3
    return best


def cauchy_noise(rng: random.Random) -> float:
    """One draw of the standard Cauchy law, density 1/(pi (1 + z^2)), by the inverse CDF. Cost: O(1)."""
    u = rng.random()
    while u == 0.0:
        u = rng.random()
    return math.tan(math.pi * (u - 0.5))


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF. Cost: O(1)."""
    u = rng.random() - 0.5
    while u == -0.5:
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def private_median_cauchy(xs: Sequence[float], lam: float, epsilon: float, rng: random.Random) -> float:
    """An epsilon-DP median: x_m + (6 S*/epsilon) Z, with beta = epsilon/6 and Z standard Cauchy.

    This is NRS Corollary 2.4 (1) with gamma = 2: noise 2(gamma + 1) S*/epsilon = 6 S*/epsilon,
    which needs beta <= epsilon/(2(gamma + 1)) = epsilon/6.
    Precondition: epsilon > 0, n odd, values in [0, lam]. Cost: O(n^2).
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    beta = epsilon / 6.0
    s = smooth_sensitivity_median(xs, beta, lam)
    return median(xs) + (6.0 * s / epsilon) * cauchy_noise(rng)  # @line L4


def private_median_laplace(
    xs: Sequence[float], lam: float, epsilon: float, delta: float, rng: random.Random
) -> float:
    """An (epsilon, delta)-DP median: x_m + (2 S*/epsilon) Lap(1), with beta = epsilon/(2 ln(2/delta)).

    This is NRS Corollary 2.4 (2). Precondition: epsilon > 0, 0 < delta < 1. Cost: O(n^2).
    """
    if epsilon <= 0 or not 0 < delta < 1:
        raise ValueError("need epsilon > 0 and 0 < delta < 1")
    beta = epsilon / (2.0 * math.log(2.0 / delta))
    s = smooth_sensitivity_median(xs, beta, lam)
    return median(xs) + (2.0 * s / epsilon) * laplace_noise(1.0, rng)
