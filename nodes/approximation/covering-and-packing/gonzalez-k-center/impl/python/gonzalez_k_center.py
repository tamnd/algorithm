# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gonzalez-k-center/. The authors are listed in prov/FMYANK.jsonl.

from typing import Callable, Sequence, TypeVar

P = TypeVar("P")


def gonzalez_k_center(points: Sequence[P], k: int, dist: Callable[[P, P], object], first: int = 0):
    """Choose at most k centers by farthest-first traversal.

    Return (centers, radius): centers is a list of distinct 0-based indices
    into points, in the order of choice, and radius is the largest distance
    from a point to its nearest center. dist must be a metric. Ties go to the
    smallest index. The loop stops early when the radius is 0.
    """
    n = len(points)
    if n == 0:
        raise ValueError("points must not be empty")
    if k < 1:
        raise ValueError("k must be at least 1")
    if not 0 <= first < n:
        raise ValueError("first must be an index of points")
    centers = [first]  # @line L1
    near = [dist(p, points[first]) for p in points]  # @line L2
    for _ in range(k - 1):  # @line L3
        c = max(range(n), key=lambda v: (near[v], -v))  # @line L4
        if near[c] == 0:  # @line L5
            break
        centers.append(c)  # @line L6
        for v in range(n):  # @line L7
            d = dist(points[v], points[c])
            if d < near[v]:
                near[v] = d
    return centers, max(near)  # @line L8
