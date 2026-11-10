# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leftover-hash-lemma/. The authors are listed in prov/T7RZCY.jsonl.

"""Exact checks of the leftover hash lemma on small sources.

A string in {0,1}^n is an int whose bit j is x_j. A source is a dict from ints to
Fractions that sum to 1. A hash family is a list of functions from ints to ints
below 2^m, used with the uniform distribution on the list.
"""

from fractions import Fraction
from typing import Callable, Dict, List, Sequence

Source = Dict[int, Fraction]
Hash = Callable[[int], int]


def toeplitz_hash(t: int, n: int, m: int) -> Hash:
    """x -> Tx over GF(2), where T is the m x n Toeplitz matrix with T[i][j] = bit (i - j + n - 1) of t.

    t has n + m - 1 bits, one for each diagonal."""

    def h(x: int) -> int:
        y = 0
        for i in range(m):
            bit = 0
            for j in range(n):
                if (x >> j) & 1:
                    bit ^= (t >> (i - j + n - 1)) & 1
            y |= bit << i
        return y

    return h


def toeplitz_family(n: int, m: int) -> List[Hash]:
    return [toeplitz_hash(t, n, m) for t in range(1 << (n + m - 1))]


def prefix_family(n: int, m: int) -> List[Hash]:
    """x -> (first m bits of x) XOR a, for all a. Not universal when m < n."""
    mask = (1 << m) - 1
    return [lambda x, a=a: (x & mask) ^ a for a in range(1 << m)]


def collision_rate(family: Sequence[Hash], x: int, y: int) -> Fraction:
    """Pr over h in the family of h(x) = h(y)."""
    return Fraction(sum(1 for h in family if h(x) == h(y)), len(family))


def is_universal(family: Sequence[Hash], n: int, m: int) -> bool:
    """True if Pr[h(x) = h(y)] <= 2^-m for all x != y in {0,1}^n."""
    bound = Fraction(1, 1 << m)
    return all(collision_rate(family, x, y) <= bound for x in range(1 << n) for y in range(x + 1, 1 << n))


def flat_source(support: Sequence[int]) -> Source:
    w = Fraction(1, len(support))
    return {x: w for x in support}


def min_entropy_at_least(source: Source, k: int) -> bool:
    """True if every probability is at most 2^-k."""
    return max(source.values()) * (1 << k) <= 1


def collision_probability(source: Source) -> Fraction:
    return sum((p * p for p in source.values()), Fraction(0))


def extraction_distance(family: Sequence[Hash], source: Source, m: int) -> Fraction:
    """The exact statistical distance between (H, H(X)) and (H, U_m).

    It equals the average over h of the distance between h(X) and U_m."""
    u = Fraction(1, 1 << m)
    total = Fraction(0)
    for h in family:
        out: Dict[int, Fraction] = {}
        for x, p in source.items():
            y = h(x)
            out[y] = out.get(y, Fraction(0)) + p
        total += sum((abs(out.get(y, Fraction(0)) - u) for y in range(1 << m)), Fraction(0)) / 2
    return total / len(family)


def joint_collision_probability(family: Sequence[Hash], source: Source) -> Fraction:
    """The collision probability of (H, H(X))."""
    total = Fraction(0)
    for h in family:
        out: Dict[int, Fraction] = {}
        for x, p in source.items():
            y = h(x)
            out[y] = out.get(y, Fraction(0)) + p
        total += sum((p * p for p in out.values()), Fraction(0))
    return total / (len(family) ** 2)


def lhl_bound_squared(k: int, m: int) -> Fraction:
    """The square of the bound (1/2) sqrt(2^(m-k)) of the leftover hash lemma."""
    return Fraction(1 << m, 1 << k) / 4
