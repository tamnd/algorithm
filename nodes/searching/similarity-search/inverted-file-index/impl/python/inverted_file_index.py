# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverted-file-index/. The authors are listed in prov/B1PB10.jsonl.

import heapq
import math
import random
from collections.abc import Sequence

Vector = tuple[float, ...]


def sq_dist(x: Sequence[float], y: Sequence[float]) -> float:
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def lloyd(points: Sequence[Vector], m: int, iters: int, rng: random.Random) -> list[Vector]:
    """Lloyd's k-means: m centroids from m distinct random points, then iters rounds. O(iters n m d)."""
    distinct = list(dict.fromkeys(points))
    cent = rng.sample(distinct, min(m, len(distinct)))
    for _ in range(iters):
        groups: list[list[Vector]] = [[] for _ in cent]
        for x in points:
            groups[nearest_centroid(cent, x)].append(x)
        cent = [
            tuple(sum(c) / len(g) for c in zip(*g)) if g else cent[j] for j, g in enumerate(groups)
        ]
    return cent


def nearest_centroid(cent: Sequence[Vector], x: Sequence[float]) -> int:
    """Index of the nearest centroid, ties to the smallest index."""
    return min(range(len(cent)), key=lambda j: (sq_dist(x, cent[j]), j))


class IVFIndex:
    """Inverted file index: a list of point ids per k-means cell.

    Build O(t n m d) for t Lloyd rounds. Search O(m d + s d + s log k), s = points in the probed lists.
    """

    def __init__(
        self,
        points: Sequence[Vector],
        m: int,
        iters: int = 10,
        rng: random.Random | None = None,
        centroids: Sequence[Vector] | None = None,
    ) -> None:
        rng = rng if rng is not None else random.Random()
        self.points: list[Vector] = list(points)
        if centroids is not None:
            self.cent = list(centroids)
        else:
            self.cent = lloyd(self.points, m, iters, rng) if self.points else []  # @line L1
        self.lists: list[list[int]] = [[] for _ in self.cent]
        for i, x in enumerate(self.points):
            self.lists[nearest_centroid(self.cent, x)].append(i)  # @line L2

    def insert(self, x: Vector) -> int:
        """Add x to the list of its nearest centroid; return its id."""
        self.points.append(x)
        self.lists[nearest_centroid(self.cent, x)].append(len(self.points) - 1)
        return len(self.points) - 1

    def search(self, q: Vector, k: int, nprobe: int) -> list[tuple[float, int]]:
        """Return up to k pairs (squared distance, id), nearest first, from the nprobe nearest cells."""
        order = sorted(range(len(self.cent)), key=lambda j: (sq_dist(q, self.cent[j]), j))
        probe = order[:nprobe]  # @line L3
        heap: list[tuple[float, int]] = []  # @line L4
        for j in probe:  # @line L5
            for i in self.lists[j]:
                item = (-sq_dist(q, self.points[i]), -i)
                if len(heap) < k:
                    heapq.heappush(heap, item)
                elif item > heap[0]:
                    heapq.heapreplace(heap, item)
        return sorted((-a, -b) for a, b in heap)  # @line L6

    def search_exact(self, q: Vector, k: int) -> list[tuple[float, int]]:
        """Exact k nearest: probe cells by centroid distance, stop when the bisector bound fails."""
        if not self.cent:
            return []
        dq = [sq_dist(q, c) for c in self.cent]
        a = min(range(len(self.cent)), key=lambda j: (dq[j], j))

        def bound(j: int) -> float:
            if j == a:
                return 0.0
            gap = math.sqrt(sq_dist(self.cent[a], self.cent[j]))
            return max(0.0, (dq[j] - dq[a]) / (2 * gap)) if gap > 0 else 0.0

        cells = sorted(range(len(self.cent)), key=lambda j: (bound(j), j))
        heap: list[tuple[float, int]] = []
        for j in cells:
            if len(heap) == k and bound(j) ** 2 > -heap[0][0]:
                break
            for i in self.lists[j]:
                item = (-sq_dist(q, self.points[i]), -i)
                if len(heap) < k:
                    heapq.heappush(heap, item)
                elif item > heap[0]:
                    heapq.heapreplace(heap, item)
        return sorted((-a2, -b) for a2, b in heap)
