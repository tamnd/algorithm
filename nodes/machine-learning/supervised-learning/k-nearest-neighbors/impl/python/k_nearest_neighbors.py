# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-nearest-neighbors/. The authors are listed in prov/4WACV7.jsonl.

"""Brute force k-nearest neighbors for classification and regression.

The neighbors are the k training points with the smallest keys (distance, index).
So a tie in distance goes to the point with the smaller index.
A tie in the vote goes to the tied class whose first member in the sorted
neighbor list is nearest.
"""

import heapq
import math
from typing import Callable, Hashable, Sequence

Vector = Sequence[float]


def euclidean(a: Vector, b: Vector) -> float:
    return math.sqrt(sum((u - v) * (u - v) for u, v in zip(a, b)))


def k_nearest(
    xs: Sequence[Vector], q: Vector, k: int, dist: Callable[[Vector, Vector], float] = euclidean
) -> list[tuple[float, int]]:
    """Return the k smallest pairs (distance, index), in increasing order. O(n d + n log k)."""
    if k < 1:
        raise ValueError("k must be at least 1")
    heap: list[tuple[float, int]] = []  # max-heap of (-distance, -index)  # @line L1
    for i, x in enumerate(xs):  # @line L2
        d = dist(x, q)  # @line L3
        if len(heap) < k:  # @line L4
            heapq.heappush(heap, (-d, -i))
        elif d < -heap[0][0]:  # @line L5
            heapq.heapreplace(heap, (-d, -i))  # @line L6
    return sorted((-nd, -ni) for nd, ni in heap)  # @line L7


def _weights(neigh: list[tuple[float, int]], weighted: bool) -> list[float]:
    if not weighted:
        return [1.0] * len(neigh)
    if any(d == 0 for d, _ in neigh):
        # Points that coincide with the query take all the weight, equally.
        return [1.0 if d == 0 else 0.0 for d, _ in neigh]
    return [1.0 / d for d, _ in neigh]


def knn_classify(
    xs: Sequence[Vector],
    ys: Sequence[Hashable],
    q: Vector,
    k: int,
    weighted: bool = False,
    dist: Callable[[Vector, Vector], float] = euclidean,
) -> Hashable:
    """Majority vote (or 1/distance weighted vote) of the k nearest labels."""
    neigh = k_nearest(xs, q, k, dist)
    votes: dict[Hashable, float] = {}
    first: dict[Hashable, int] = {}
    for r, ((_, i), w) in enumerate(zip(neigh, _weights(neigh, weighted))):
        votes[ys[i]] = votes.get(ys[i], 0.0) + w  # @line L9
        first.setdefault(ys[i], r)
    best = max(votes.values())
    tied = [c for c in votes if votes[c] == best]  # @line L10
    return min(tied, key=lambda c: first[c])  # @line L11


def knn_regress(
    xs: Sequence[Vector],
    ys: Sequence[float],
    q: Vector,
    k: int,
    weighted: bool = False,
    dist: Callable[[Vector, Vector], float] = euclidean,
) -> float:
    """Mean (or 1/distance weighted mean) of the k nearest targets."""
    neigh = k_nearest(xs, q, k, dist)
    ws = _weights(neigh, weighted)
    return sum(w * ys[i] for (_, i), w in zip(neigh, ws)) / sum(ws)  # @line L8


def leave_one_out_error(xs: Sequence[Vector], ys: Sequence[Hashable], k: int) -> float:
    """Fraction of points that the k-NN rule on the other n - 1 points gets wrong."""
    wrong = 0
    for j in range(len(xs)):
        rest_x = [x for i, x in enumerate(xs) if i != j]
        rest_y = [y for i, y in enumerate(ys) if i != j]
        wrong += knn_classify(rest_x, rest_y, xs[j], k) != ys[j]
    return wrong / len(xs)
