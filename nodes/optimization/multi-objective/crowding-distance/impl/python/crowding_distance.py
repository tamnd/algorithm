# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crowding-distance/. The authors are listed in prov/KB59FK.jsonl.

"""Crowding distance of NSGA-II (Deb, Pratap, Agarwal and Meyarivan, 2002).

All objectives are minimized. The input is one front: a list of objective
vectors. A larger distance means a less crowded point. Time O(p l log l) for a
front of l points with p objectives. Pass fractions.Fraction values to get
exact results.
"""

import math
from typing import Sequence

Vector = Sequence[float]


def crowding_distance(front: Sequence[Vector]) -> list:
    """Return the crowding distance of each point of the front."""
    l = len(front)
    d: list = [0] * l  # @line L1
    if l == 0:
        return d
    p = len(front[0])
    for m in range(p):  # @line L2
        idx = sorted(range(l), key=lambda i: front[i][m])  # @line L3
        d[idx[0]] = math.inf  # @line L4
        d[idx[-1]] = math.inf  # @line L4
        span = front[idx[-1]][m] - front[idx[0]][m]
        if span == 0:  # @line L5
            continue
        for k in range(1, l - 1):  # @line L6
            d[idx[k]] += (front[idx[k + 1]][m] - front[idx[k - 1]][m]) / span  # @line L7
    return d  # @line L8


def truncate(front: Sequence[Vector], keep: int, recompute: bool = False) -> list[int]:
    """Return the sorted indices of `keep` points of the front, chosen by crowding distance.

    With recompute=False, keep the `keep` largest distances in one pass (NSGA-II).
    With recompute=True, remove the most crowded point one at a time and recompute
    the distances of the rest each time (the pruning of Kukkonen and Deb).
    On a tie, the point with the larger index goes first.
    """
    alive = list(range(len(front)))
    if keep >= len(alive):
        return alive
    if not recompute:
        d = crowding_distance(front)
        return sorted(sorted(alive, key=lambda i: (-d[i], i))[:keep])
    while len(alive) > keep:
        d = crowding_distance([front[i] for i in alive])
        worst = min(range(len(alive)), key=lambda k: (d[k], -alive[k]))
        alive.pop(worst)
    return alive
