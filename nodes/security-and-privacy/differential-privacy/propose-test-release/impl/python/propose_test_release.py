# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/propose-test-release/. The authors are listed in prov/DV793R.jsonl.
"""Propose-test-release (PTR) of Dwork and Lei (2009), in the form of
Vadhan (2017, Proposition 3.2), for the median of values in [0, lam].

Neighbors replace one value by another, so n is fixed. The analyst proposes
a bound b on the local sensitivity. The mechanism computes the distance
from x to the nearest dataset whose local sensitivity is above b, tests a
noisy copy of it against ln(1/delta)/epsilon, and releases the median with
Lap(b/epsilon) noise only if the test passes. Otherwise it outputs None
(the symbol "no answer"). The whole run is (2 epsilon, delta)-DP.

The code uses random.Random so that the tests can be repeated, and float
noise. A real release needs a cryptographic source of randomness and exact
sampling (Mironov 2012; Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Optional, Sequence


def median(xs: Sequence[float]) -> float:
    """The median x_m of an odd number of values, m = (n + 1)/2 in 1-based order. Cost: O(n log n)."""
    if len(xs) % 2 == 0 or not xs:
        raise ValueError("n must be odd")
    return sorted(xs)[len(xs) // 2]


def ball_sensitivity(xs: Sequence[float], k: int, lam: float) -> float:
    """A(k, x) = max over t = 0..k+1 of x_{m+t} - x_{m+t-k-1}, with x_i = 0 for i <= 0 and lam for i > n.

    This is the largest local sensitivity of the median over the datasets within k replacements
    of x (Nissim, Raskhodnikova and Smith 2007, Proposition 3.4). Cost: O(n log n + k).
    """
    return _ball(_padded(xs, lam), (len(xs) + 1) // 2, k)


def _padded(xs: Sequence[float], lam: float) -> list[float]:
    # Index i of the list is x_{i - n - 1}: n zeros, the sorted values, then n + 2 copies of lam.
    n = len(xs)
    return [0.0] * (n + 1) + [float(v) for v in sorted(xs)] + [float(lam)] * (n + 2)


def _ball(p: list[float], m: int, k: int) -> float:
    off = (len(p) - 1) // 3  # the offset of x_0 in the padded list
    return max(p[off + m + t] - p[off + m + t - k - 1] for t in range(k + 2))


def distance_to_instability(xs: Sequence[float], b: float, lam: float) -> float:
    """The number of replacements from x to the nearest dataset whose local sensitivity is above b.

    It is the least k with A(k, x) > b, because A(k, x) grows with k. It is infinite when b >= lam.
    Precondition: n odd, values in [0, lam]. Cost: O(n log n + gamma^2).
    """
    p = _padded(xs, lam)
    m = (len(xs) + 1) // 2
    for k in range(len(xs) + 1):
        if _ball(p, m, k) > b:
            return float(k)
    return math.inf


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF. Cost: O(1)."""
    u = rng.random() - 0.5
    while u == -0.5:
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def laplace_cdf(t: float, b: float) -> float:
    """P(Lap(b) <= t). Cost: O(1)."""
    if t < 0:
        return 0.5 * math.exp(t / b)
    return 1.0 - 0.5 * math.exp(-t / b)


def pass_probability(gamma: float, epsilon: float, delta: float) -> float:
    """P(gamma + Lap(1/epsilon) > ln(1/delta)/epsilon), the chance that the test of line L3 passes. Cost: O(1)."""
    if math.isinf(gamma):
        return 1.0
    return 1.0 - laplace_cdf(math.log(1.0 / delta) / epsilon - gamma, 1.0 / epsilon)


def propose_test_release_median(
    xs: Sequence[float], lam: float, b: float, epsilon: float, delta: float, rng: random.Random
) -> Optional[float]:
    """PTR for the median. Returns None for "no answer", else median(x) + Lap(b/epsilon).

    Precondition: n odd, values in [0, lam], b > 0, epsilon > 0, 0 < delta < 1.
    Guarantee: (2 epsilon, delta)-DP for replace neighbors (Vadhan, Proposition 3.2).
    Cost: O(n^2) time and O(n) extra space.
    """
    if epsilon <= 0 or not 0 < delta < 1 or b <= 0:
        raise ValueError("need epsilon > 0, 0 < delta < 1 and b > 0")
    if len(xs) % 2 == 0:
        raise ValueError("n must be odd")
    gamma = distance_to_instability(xs, b, lam)  # @line L1
    noisy = gamma + laplace_noise(1.0 / epsilon, rng)  # @line L2
    if noisy <= math.log(1.0 / delta) / epsilon:  # @line L3
        return None
    return median(xs) + laplace_noise(b / epsilon, rng)  # @line L4
