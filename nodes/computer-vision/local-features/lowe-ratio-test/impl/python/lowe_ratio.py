# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lowe-ratio-test/. The authors are listed in prov/GBD07V.jsonl.

"""Lowe's ratio test on top of exact nearest neighbor search (Lowe 2004, Section 7.1).

For each descriptor a_i of A, find the nearest descriptor b_j of B, at
Euclidean distance d1, and the distance d2 to the second nearest. Keep the
pair (i, j) only when d1 < r * d2. The test compares squared distances with r^2,
which gives the same result and needs no square root.

Precondition: B has at least two descriptors, all of the same length as those
of A, and 0 < r <= 1. Cost: O(|A| |B| D) time for descriptors of length D, with
exact search; O(1) extra space per query. Ties for the nearest go to the
smaller index of B.
"""

from typing import List, Sequence, Tuple

Vec = Sequence[float]


def sqdist(a: Vec, b: Vec) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def nearest_two(a: Vec, B: Sequence[Vec]) -> Tuple[int, float, float]:
    """Return (j1, d1^2, d2^2): the nearest index and the two smallest squared distances."""
    j1, best, second = -1, float("inf"), float("inf")
    for j, b in enumerate(B):
        d = sqdist(a, b)
        if d < best:
            j1, best, second = j, d, best
        elif d < second:
            second = d
    return j1, best, second


def ratio_test_match(A: Sequence[Vec], B: Sequence[Vec], r: float = 0.8) -> List[Tuple[int, int, float, float]]:
    """Return the kept pairs as (i, j, d1, d2) with Euclidean distances d1 < r * d2."""
    if len(B) < 2:
        raise ValueError("the ratio test needs at least two descriptors in B")
    if not 0.0 < r <= 1.0:
        raise ValueError("the ratio r must be in (0, 1]")
    out = []
    for i, a in enumerate(A):  # @line L1
        j, d1, d2 = nearest_two(a, B)  # @line L2
        if d1 < r * r * d2:  # @line L3
            out.append((i, j, d1 ** 0.5, d2 ** 0.5))  # @line L4
    return out
