# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gnat/. The authors are listed in prov/2746FY.jsonl.
"""Geometric near-neighbor access tree (Brin): range and nearest neighbor search."""

import math
from typing import Callable, Optional, Sequence

Point = Sequence[float]


def euclidean(a: Point, b: Point) -> float:
    return math.dist(a, b)


class Node:
    __slots__ = ("splits", "ranges", "kids", "bucket")

    def __init__(self) -> None:
        self.splits: list[int] = []
        self.ranges: list[list[tuple[float, float]]] = []
        self.kids: list[Optional["Node"]] = []
        self.bucket: list[int] = []


class GNAT:
    def __init__(self, points: Sequence[Point], m: int = 3, leaf_size: int = 3,
                 dist: Callable[[Point, Point], float] = euclidean) -> None:
        if m < 2:
            raise ValueError("m must be at least 2")
        self.points = list(points)
        self.m, self.leaf_size, self.dist = m, max(leaf_size, 1), dist
        self.evals = 0
        self.root = self._build(list(range(len(self.points))))

    def _d(self, a: Point, b: Point) -> float:
        self.evals += 1
        return self.dist(a, b)

    def _build(self, ids: list[int]) -> Optional[Node]:
        if not ids:
            return None
        node = Node()
        if len(ids) <= self.leaf_size:  # @line L1
            node.bucket = ids
            return node
        pts = self.points
        splits = [ids[0]]  # @line L2
        near = {x: self._d(pts[x], pts[ids[0]]) for x in ids}
        while len(splits) < min(self.m, len(ids)):
            far = max((x for x in ids if x not in splits), key=lambda x: (near[x], -x))
            splits.append(far)
            for x in ids:
                near[x] = min(near[x], self._d(pts[x], pts[far]))
        rest = [x for x in ids if x not in splits]
        dto = {x: [self._d(pts[x], pts[s]) for s in splits] for x in rest}
        groups: list[list[int]] = [[] for _ in splits]
        for x in rest:  # @line L3
            groups[min(range(len(splits)), key=lambda j: (dto[x][j], j))].append(x)
        k = len(splits)
        ranges = [[(0.0, 0.0)] * k for _ in range(k)]
        for i in range(k):  # @line L4
            for j in range(k):
                ds = [self._d(pts[splits[i]], pts[splits[j]])] + [dto[x][i] for x in groups[j]]
                ranges[i][j] = (min(ds), max(ds))
        node.splits, node.ranges = splits, ranges
        node.kids = [self._build(g) for g in groups]  # @line L5
        return node

    def range(self, q: Point, r: float) -> list[int]:
        out: list[int] = []
        self._range(self.root, q, r, out)
        return sorted(out)

    def _range(self, node: Optional[Node], q: Point, r: float, out: list[int]) -> None:
        if node is None:
            return
        if node.bucket:  # @line L6
            out.extend(x for x in node.bucket if self._d(q, self.points[x]) <= r)
            return
        alive = [True] * len(node.splits)  # @line L7
        for i, s in enumerate(node.splits):  # @line L8
            if not alive[i]:
                continue
            d = self._d(q, self.points[s])
            if d <= r:
                out.append(s)
            for j in range(len(node.splits)):  # @line L9
                lo, hi = node.ranges[i][j]
                if alive[j] and (d + r < lo or d - r > hi):
                    alive[j] = False
        for j, kid in enumerate(node.kids):  # @line L10
            if alive[j]:
                self._range(kid, q, r, out)

    def nearest(self, q: Point) -> Optional[tuple[float, int]]:
        best = [math.inf, -1]
        self._nearest(self.root, q, best)
        return None if best[1] < 0 else (best[0], best[1])

    def _offer(self, best: list, d: float, x: int) -> None:
        if (d, x) < (best[0], best[1]) or best[1] < 0:
            best[0], best[1] = d, x

    def _nearest(self, node: Optional[Node], q: Point, best: list) -> None:
        if node is None:
            return
        if node.bucket:
            for x in node.bucket:
                self._offer(best, self._d(q, self.points[x]), x)
            return
        k = len(node.splits)
        alive = [True] * k
        dist = [math.inf] * k
        for i, s in enumerate(node.splits):  # @line L11
            if not alive[i]:
                continue
            dist[i] = self._d(q, self.points[s])
            self._offer(best, dist[i], s)
            for j in range(k):
                lo, hi = node.ranges[i][j]
                if alive[j] and (dist[i] + best[0] < lo or dist[i] - best[0] > hi):
                    alive[j] = False
        order = sorted((j for j in range(k) if alive[j]), key=lambda j: dist[j])
        for j in order:  # @line L12
            lo_bound = max(max(dist[i] - node.ranges[i][j][1], node.ranges[i][j][0] - dist[i])
                           for i in range(k) if dist[i] < math.inf)
            if lo_bound <= best[0]:
                self._nearest(node.kids[j], q, best)
