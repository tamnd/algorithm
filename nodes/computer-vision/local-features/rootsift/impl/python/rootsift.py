# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rootsift/. The authors are listed in prov/5CC4QY.jsonl.

"""RootSIFT (Arandjelovic and Zisserman 2012).

Map a descriptor with non-negative entries, such as SIFT, to the square roots
of its L1-normalized entries. For L1-normalized x and y,
||sqrt(x) - sqrt(y)||^2 = 2 - 2 H(x, y) with H(x, y) = sum_i sqrt(x_i y_i),
the Hellinger kernel (the Bhattacharyya coefficient). So Euclidean nearest
neighbors of the mapped vectors are the neighbors of largest Hellinger kernel.

Precondition: all entries are non-negative. The zero vector maps to itself.
Cost: O(D) time and space for a descriptor of length D.
"""

import math
from typing import List, Sequence

Vec = Sequence[float]


def rootsift(x: Vec) -> List[float]:
    """Return the RootSIFT vector of x; it has unit Euclidean norm unless x is zero."""
    if any(t < 0 for t in x):
        raise ValueError("RootSIFT needs non-negative entries")
    s = sum(x)  # @line L1
    if s == 0:  # @line L2
        return [0.0] * len(x)
    return [math.sqrt(t / s) for t in x]  # @line L3


def hellinger_kernel(x: Vec, y: Vec) -> float:
    """H(x, y) = sum_i sqrt(x_i y_i) after L1 normalization of x and y."""
    sx, sy = sum(x), sum(y)
    return sum(math.sqrt(a * b / (sx * sy)) for a, b in zip(x, y))


def nearest_by_rootsift(q: Vec, database: Sequence[Vec]) -> int:
    """Index of the database descriptor whose RootSIFT vector is nearest to that of q."""
    rq = rootsift(q)
    best, arg = math.inf, -1
    for j, p in enumerate(database):  # @line L4
        d = math.dist(rq, rootsift(p))
        if d < best:
            best, arg = d, j
    return arg
