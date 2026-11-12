# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjusted-rand-index/. The authors are listed in prov/W19B99.jsonl.
"""The adjusted Rand index of Hubert and Arabie (1985), in exact arithmetic."""

from collections import Counter
from fractions import Fraction
from typing import Hashable, Sequence


def comb2(m: int) -> int:
    return m * (m - 1) // 2


def contingency(u: Sequence[Hashable], v: Sequence[Hashable]):
    """Return (cells, row sums, column sums) of the contingency table of u and v."""
    if len(u) != len(v):
        raise ValueError("the two labelings must have the same length")
    return Counter(zip(u, v)), Counter(u), Counter(v)


def adjusted_rand_index(u: Sequence[Hashable], v: Sequence[Hashable]) -> Fraction:
    """ARI = (S - E) / (M - E) with

    S = sum over cells of C(n_ij, 2)
    E = (sum_i C(a_i, 2)) (sum_j C(b_j, 2)) / C(n, 2), the mean of S under the permutation model
    M = (sum_i C(a_i, 2) + sum_j C(b_j, 2)) / 2, the upper bound of Hubert and Arabie

    M = E only when both partitions are one cluster, or both are all singletons
    (this includes n < 2). Then the two partitions are equal, and the function returns 1.
    """
    cells, rows, cols = contingency(u, v)
    n = len(u)
    s = sum(comb2(m) for m in cells.values())
    su = sum(comb2(m) for m in rows.values())
    sv = sum(comb2(m) for m in cols.values())
    pairs = comb2(n)
    if pairs == 0:
        return Fraction(1)
    expected = Fraction(su * sv, pairs)
    maximum = Fraction(su + sv, 2)
    if maximum == expected:
        return Fraction(1)
    return (s - expected) / (maximum - expected)
