# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-transform-sampling/. The authors are listed in prov/FC22KF.jsonl.

"""Inverse transform sampling.

X = F^{-1}(U) with the generalized inverse F^{-1}(u) = inf{x : F(x) >= u}
has distribution function F when U is uniform on (0, 1). For a discrete law
with integer weights, a uniform integer t in [0, W) and a search in the
prefix sums give the exact law. The real-valued forms are exact only in
exact arithmetic.
"""

import bisect
import math
import random
from typing import Callable, List, Sequence


def inverse_transform(f_inv: Callable[[float], float], rng: random.Random) -> float:
    """Return F^{-1}(U) for U uniform on (0, 1)."""
    u = rng.random()  # @line L1
    while u == 0.0:  # @line L1
        u = rng.random()  # @line L1
    return f_inv(u)  # @line L2


def exponential(rate: float, rng: random.Random) -> float:
    """F(x) = 1 - exp(-rate x); F^{-1}(u) = -ln(1 - u) / rate."""
    return inverse_transform(lambda u: -math.log1p(-u) / rate, rng)


def cauchy(rng: random.Random) -> float:
    """F(x) = 1/2 + arctan(x) / pi; F^{-1}(u) = tan(pi (u - 1/2))."""
    return inverse_transform(lambda u: math.tan(math.pi * (u - 0.5)), rng)


def generalized_inverse(values: Sequence, cdf: Sequence, u) -> object:
    """inf{x : F(x) >= u} for a step function F with F(values[i]) = cdf[i].

    values is increasing, cdf is non-decreasing and ends at 1, and 0 < u <= 1.
    """
    i = bisect.bisect_left(cdf, u)
    return values[i]


def prefix_sums(weights: Sequence[int]) -> List[int]:
    out, s = [], 0
    for w in weights:
        if w < 0:
            raise ValueError("weights must be non-negative")
        s += w
        out.append(s)
    if s == 0:
        raise ValueError("the total weight must be positive")
    return out


def discrete_inverse(prefix: Sequence[int], rng: random.Random) -> int:
    """Exact discrete inversion: index i with probability weights[i] / W."""
    t = rng.randrange(prefix[-1])  # @line L3
    return bisect.bisect_right(prefix, t)  # @line L4


def discrete_inverse_float(probs: Sequence[float], rng: random.Random) -> int:
    """Sequential search with a float uniform; exact only in exact arithmetic."""
    u = rng.random()
    s = 0.0
    for i, p in enumerate(probs):
        s += p
        if u < s:
            return i
    return len(probs) - 1
