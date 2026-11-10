# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-source-extractor/. The authors are listed in prov/20AZMB.jsonl.

"""Exact checks of the inner product two-source extractor on small sources.

A string in {0,1}^n is an int whose bit j is x_j. A source is a dict from ints to
Fractions that sum to 1. The extractor is IP(x, y) = <x, y> mod 2.
"""

from fractions import Fraction
from itertools import combinations
from typing import Dict, Iterable, Sequence, Tuple

Source = Dict[int, Fraction]


def ip(x: int, y: int) -> int:
    """<x, y> mod 2."""
    return bin(x & y).count("1") & 1


def sign(x: int, y: int) -> int:
    """The entry H[x][y] = (-1)^<x, y> of the Hadamard matrix."""
    return -1 if ip(x, y) else 1


def flat(support: Iterable[int]) -> Source:
    s = list(support)
    return {x: Fraction(1, len(s)) for x in s}


def rectangle_sum(a: Sequence[int], b: Sequence[int]) -> int:
    """The sum of H over the rectangle A x B."""
    return sum(sign(x, y) for x in a for y in b)


def bias(p: Source, q: Source) -> Fraction:
    """|Pr[IP(X, Y) = 0] - Pr[IP(X, Y) = 1]| for independent X ~ p and Y ~ q.

    The output bit is at distance bias / 2 from a uniform bit."""
    return abs(sum((pa * qb * sign(x, y) for x, pa in p.items() for y, qb in q.items()), Fraction(0)))


def strong_bias(p: Source, q: Source) -> Fraction:
    """E over y ~ q of the bias of IP(X, y): the error when y is revealed, times 2."""
    total = Fraction(0)
    for y, qb in q.items():
        total += qb * abs(sum((pa * sign(x, y) for x, pa in p.items()), Fraction(0)))
    return total


def collision(p: Source) -> Fraction:
    """||p||_2^2, the collision probability of p."""
    return sum((v * v for v in p.values()), Fraction(0))


def bound_squared(n: int, k1: int, k2: int) -> Fraction:
    """The square of the Chor-Goldreich bound 2^((n - k1 - k2)/2) on the bias."""
    e = n - k1 - k2
    return Fraction(1 << e) if e >= 0 else Fraction(1, 1 << -e)


def worst_flat_bias(n: int, k1: int, k2: int) -> Tuple[Fraction, Tuple[int, ...], Tuple[int, ...]]:
    """The largest bias over all flat sources with supports of size 2^k1 and 2^k2."""
    best = (Fraction(-1), (), ())
    universe = range(1 << n)
    for a in combinations(universe, 1 << k1):
        for b in combinations(universe, 1 << k2):
            v = Fraction(abs(rectangle_sum(a, b)), len(a) * len(b))
            if v > best[0]:
                best = (v, a, b)
    return best
