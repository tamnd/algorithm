# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-nearest-neighbor-matching/. The authors are listed in prov/5K7F44.jsonl.

"""Mutual nearest neighbor matching, also called cross-check matching.

For each descriptor a_i of A find its nearest descriptor f(i) in B, and for
each descriptor b_j of B its nearest descriptor g(j) in A. Keep (i, f(i))
when g(f(i)) = i. Ties for the nearest go to the smaller index, so f and g
are functions and the result does not depend on the order of the scan.

Precondition: all vectors have the same length. Cost: O(|A| |B| D) time with
exact search over descriptors of length D, and O(|A| + |B|) extra space.
"""

from typing import List, Sequence, Tuple

Vec = Sequence[float]


def sqdist(a: Vec, b: Vec) -> float:
    return sum((x - y) * (x - y) for x, y in zip(a, b))


def nearest(a: Vec, B: Sequence[Vec]) -> int:
    """Index of the nearest vector of B to a, the smallest index on ties; -1 if B is empty."""
    best, arg = float("inf"), -1
    for j, b in enumerate(B):
        d = sqdist(a, b)
        if d < best:
            best, arg = d, j
    return arg


def mutual_nn_match(A: Sequence[Vec], B: Sequence[Vec]) -> List[Tuple[int, int]]:
    """Return the mutual nearest neighbor pairs (i, j) in increasing order of i."""
    if not A or not B:
        return []
    f = [nearest(a, B) for a in A]  # @line L1
    g = [nearest(b, A) for b in B]  # @line L2
    out = []
    for i in range(len(A)):  # @line L3
        if g[f[i]] == i:  # @line L4
            out.append((i, f[i]))
    return out
