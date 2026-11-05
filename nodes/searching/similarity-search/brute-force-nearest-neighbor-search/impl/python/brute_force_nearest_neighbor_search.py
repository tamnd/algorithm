# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brute-force-nearest-neighbor-search/. The authors are listed in prov/VXFMJM.jsonl.

import heapq
from collections.abc import Callable, Sequence

Point = Sequence[float]


def squared_euclidean(a: Point, b: Point) -> float:
    """Return the squared Euclidean distance of two points of the same dimension."""
    return sum((x - y) * (x - y) for x, y in zip(a, b, strict=True))


def brute_force_knn(
    points: Sequence[Point],
    q: Point,
    k: int,
    dist: Callable[[Point, Point], float] = squared_euclidean,
) -> list[tuple[float, int]]:
    """Return the min(k, n) pairs (distance, index) of the points nearest to q, in increasing order.

    Ties in distance are broken by the smaller index. Precondition: k >= 1.
    Cost: n calls of dist and O(n log k) heap time; O(k) extra space.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    h: list[tuple[float, int]] = []  # @line L1: max-heap through negated pairs
    for i in range(len(points)):  # @line L2
        delta = dist(q, points[i])  # @line L3
        if len(h) < k:
            heapq.heappush(h, (-delta, -i))  # @line L4
        elif (delta, i) < (-h[0][0], -h[0][1]):
            heapq.heapreplace(h, (-delta, -i))  # @line L5
    return sorted((-nd, -ni) for nd, ni in h)  # @line L6
