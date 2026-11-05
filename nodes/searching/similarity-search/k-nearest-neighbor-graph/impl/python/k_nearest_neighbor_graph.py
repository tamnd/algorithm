# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-nearest-neighbor-graph/. The authors are listed in prov/CST612.jsonl.
"""A k-nearest neighbor graph, built by brute force, with greedy beam search."""

import heapq
import math
from typing import Callable, Sequence

Point = Sequence[float]


def euclidean(a: Point, b: Point) -> float:
    return math.dist(a, b)


class KNNGraph:
    """Directed graph with an edge from each point to its k nearest other points.

    Ties in distance are broken by the smaller index.
    """

    def __init__(self, points: Sequence[Point], k: int,
                 dist: Callable[[Point, Point], float] = euclidean) -> None:
        self.points = list(points)
        self.k = k
        self.dist = dist
        self.adj: list[list[int]] = []
        n = len(self.points)
        for i in range(n):  # @line L1
            heap: list[tuple[float, int]] = []  # max-heap of (-d, -j)
            for j in range(n):  # @line L2
                if j == i:
                    continue
                d = dist(self.points[i], self.points[j])
                item = (-d, -j)
                if len(heap) < k:  # @line L3
                    heapq.heappush(heap, item)
                elif item > heap[0]:
                    heapq.heapreplace(heap, item)
            self.adj.append([-mj for _, mj in sorted(heap, reverse=True)])  # @line L4

    def neighbors(self, i: int) -> list[int]:
        return self.adj[i]

    def reverse(self) -> list[list[int]]:
        """In-neighbors of each point: the reverse k-nearest neighbor lists."""
        rev: list[list[int]] = [[] for _ in self.points]
        for i, out in enumerate(self.adj):
            for j in out:
                rev[j].append(i)
        return rev

    def search(self, q: Point, k: int, ef: int, starts: Sequence[int]) -> list[tuple[float, int]]:
        """Beam search from the start points; returns up to k (distance, index) pairs."""
        d = self.dist
        visited = set(starts)  # @line L5
        cand = [(d(q, self.points[s]), s) for s in visited]
        heapq.heapify(cand)
        best = [(-dist_s, s) for dist_s, s in heapq.nsmallest(ef, cand)]
        heapq.heapify(best)
        while cand:  # @line L6
            dc, c = heapq.heappop(cand)  # @line L7
            if dc > -best[0][0]:
                break
            for e in self.adj[c]:  # @line L8
                if e in visited:
                    continue
                visited.add(e)
                de = d(q, self.points[e])
                if len(best) < ef or de < -best[0][0]:
                    heapq.heappush(cand, (de, e))
                    heapq.heappush(best, (-de, e))
                    if len(best) > ef:
                        heapq.heappop(best)
        return sorted((-nd, e) for nd, e in best)[:k]  # @line L9
