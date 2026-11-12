# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rand-index/. The authors are listed in prov/C0AH5H.jsonl.
"""The Rand index of two partitions of the same n items, from the contingency table."""

from collections import Counter
from fractions import Fraction
from typing import Hashable, Sequence


def comb2(m: int) -> int:
    """The number of unordered pairs in a set of m items."""
    return m * (m - 1) // 2


def pair_counts(u: Sequence[Hashable], v: Sequence[Hashable]) -> tuple[int, int, int, int]:
    """Return (a, b, c, d) for two labelings of the same items.

    a: pairs together in u and together in v
    b: pairs together in u and apart in v
    c: pairs apart in u and together in v
    d: pairs apart in u and apart in v
    The counts come from the contingency table in O(n) time.
    """
    if len(u) != len(v):
        raise ValueError("the two labelings must have the same length")
    n = len(u)
    s = sum(comb2(m) for m in Counter(zip(u, v)).values())
    su = sum(comb2(m) for m in Counter(u).values())
    sv = sum(comb2(m) for m in Counter(v).values())
    a = s
    b = su - s
    c = sv - s
    d = comb2(n) - a - b - c
    return a, b, c, d


def rand_index(u: Sequence[Hashable], v: Sequence[Hashable]) -> Fraction:
    """(a + d) / C(n, 2). By convention the index is 1 when n < 2 (no pairs)."""
    a, b, c, d = pair_counts(u, v)
    total = a + b + c + d
    if total == 0:
        return Fraction(1)
    return Fraction(a + d, total)


def rand_index_naive(u: Sequence[Hashable], v: Sequence[Hashable]) -> Fraction:
    """The definition: look at each of the C(n, 2) pairs. O(n^2) time."""
    n = len(u)
    agree = 0
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            pairs += 1
            if (u[i] == u[j]) == (v[i] == v[j]):
                agree += 1
    return Fraction(1) if pairs == 0 else Fraction(agree, pairs)
