# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bernoulli-sampling/. The authors are listed in prov/9SBD59.jsonl.

"""Bernoulli sampling: keep each of n items independently with probability p.

bernoulli_sample jumps from one kept item to the next with geometric skips,
so it takes O(1 + n p) expected time instead of O(n). It uses floating
point logarithms, so its law is exact only in exact arithmetic.

bernoulli_sample_direct is the exact version for a rational p = a / b: one
uniform integer draw for each item, O(n) time, and no rounding at all.
"""

import math
import random
from typing import Callable, List, Optional


def geometric(p: float, rng: random.Random) -> int:
    """Number of failures before the first success, Pr[G = g] = (1 - p)^g p.

    Inversion: with U uniform in (0, 1], G = floor(ln U / ln(1 - p)).
    Precondition: 0 < p < 1. O(1) time.
    """
    u = 1.0 - rng.random()  # @line L7
    return int(math.floor(math.log(u) / math.log1p(-p)))  # @line L8


def bernoulli_sample(
    n: int,
    p: float,
    rng: random.Random,
    geo: Optional[Callable[[], int]] = None,
) -> List[int]:
    """Return the sorted list of kept positions in range(n).

    Each position is kept with probability p, independently. The optional
    geo() gives the geometric skips; by default it is geometric(p, rng).
    Expected time O(1 + n p).
    """
    if p <= 0.0:
        return []
    if p >= 1.0:
        return list(range(n))
    if geo is None:
        def geo() -> int:
            return geometric(p, rng)
    S: List[int] = []  # @line L1
    i = -1  # @line L1
    while True:  # @line L2
        G = geo()  # @line L3
        i = i + G + 1  # @line L4
        if i >= n:  # @line L5
            return S  # @line L5
        S.append(i)  # @line L6


def bernoulli_sample_direct(n: int, a: int, b: int, rng: random.Random) -> List[int]:
    """Exact Bernoulli sampling with p = a / b, 0 <= a <= b, b >= 1.

    One uniform integer in [0, b) for each item. O(n) time.
    """
    return [i for i in range(n) if rng.randrange(b) < a]
