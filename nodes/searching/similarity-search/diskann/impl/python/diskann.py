# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diskann/. The authors are listed in prov/KR79N8.jsonl.
"""The Vamana graph of DiskANN: greedy search, robust pruning and graph construction."""

import math
import random
from typing import Callable, Optional, Sequence

Point = Sequence[float]


def euclidean(a: Point, b: Point) -> float:
    return math.dist(a, b)


class Vamana:
    def __init__(self, points: Sequence[Point],
                 dist: Callable[[Point, Point], float] = euclidean) -> None:
        self.points = list(points)
        self.dist = dist
        self.adj: list[list[int]] = [[] for _ in self.points]
        self.start = self.medoid()

    def d(self, i: int, x: Point) -> float:
        return self.dist(self.points[i], x)

    def medoid(self) -> int:
        n = len(self.points)
        if n == 0:
            return -1
        return min(range(n), key=lambda i: (sum(self.d(i, p) for p in self.points), i))

    def greedy_search(self, q: Point, k: int, L: int,
                      start: Optional[int] = None) -> tuple[list[int], set[int]]:
        """Returns the k nearest of the final list and the set of expanded (read) nodes."""
        s = self.start if start is None else start
        cand = {s}  # @line L1
        visited: set[int] = set()
        while True:
            open_ = [p for p in cand if p not in visited]  # @line L2
            if not open_:
                break
            p = min(open_, key=lambda i: (self.d(i, q), i))  # @line L3
            visited.add(p)
            cand.update(self.adj[p])  # @line L4
            if len(cand) > L:
                cand = set(sorted(cand, key=lambda i: (self.d(i, q), i))[:L])
        return sorted(cand, key=lambda i: (self.d(i, q), i))[:k], visited  # @line L5

    def robust_prune(self, p: int, cands: set[int], alpha: float, R: int) -> None:
        pts = self.points
        v = (set(cands) | set(self.adj[p])) - {p}  # @line L6
        out: list[int] = []
        while v:  # @line L7
            best = min(v, key=lambda i: (self.dist(pts[p], pts[i]), i))  # @line L8
            out.append(best)
            if len(out) == R:  # @line L9
                break
            v = {x for x in v
                 if alpha * self.dist(pts[best], pts[x]) > self.dist(pts[p], pts[x])}  # @line L10
        self.adj[p] = out

    def build(self, R: int, L: int, alpha: float, rng: Optional[random.Random] = None) -> None:
        """Vamana: a random R-regular start, then two passes (alpha = 1, then alpha)."""
        rng = rng or random.Random()
        n = len(self.points)
        for i in range(n):  # @line L11
            others = [j for j in range(n) if j != i]
            self.adj[i] = rng.sample(others, min(R, len(others)))
        for a in (1.0, alpha):
            order = list(range(n))
            rng.shuffle(order)
            for i in order:  # @line L12
                _, visited = self.greedy_search(self.points[i], 1, L)
                self.robust_prune(i, visited, a, R)  # @line L13
                for j in self.adj[i]:  # @line L14
                    if i in self.adj[j]:
                        continue
                    if len(self.adj[j]) + 1 > R:
                        self.robust_prune(j, set(self.adj[j]) | {i}, a, R)  # @line L15
                    else:
                        self.adj[j].append(i)

    def build_full(self, alpha: float) -> None:
        """Slow preprocessing: prune each point against all others with no degree limit."""
        n = len(self.points)
        for i in range(n):
            self.adj[i] = []
            self.robust_prune(i, set(range(n)), alpha, n)
