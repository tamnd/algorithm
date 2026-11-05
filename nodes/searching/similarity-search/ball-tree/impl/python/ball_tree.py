# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ball-tree/. The authors are listed in prov/DT55WY.jsonl.

import heapq
import math
from collections.abc import Callable, Sequence
from typing import Generic, TypeVar

P = TypeVar("P")


def euclidean(x: Sequence[float], y: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) * (a - b) for a, b in zip(x, y)))


class Node(Generic[P]):
    __slots__ = ("center", "radius", "points", "left", "right")

    def __init__(self, center: int, radius: float) -> None:
        self.center = center
        self.radius = radius
        self.points: list[int] | None = None
        self.left: Node[P] | None = None
        self.right: Node[P] | None = None


class BallTree(Generic[P]):
    """Metric ball tree. Each node has a center point and a radius that covers its subtree.

    Build: O(n log n) distance evaluations, height ceil(lg(n/b)) + 1. Queries: O(n) worst case.
    """

    def __init__(
        self,
        points: Sequence[P],
        dist: Callable[[P, P], float] = euclidean,
        leaf_size: int = 2,
    ) -> None:
        if leaf_size < 1:
            raise ValueError("leaf_size must be at least 1")
        self.points = list(points)
        self.dist = dist
        self.b = leaf_size
        self.root = self._build(list(range(len(self.points)))) if self.points else None

    def _build(self, ids: list[int]) -> Node[P]:
        d = self.dist
        pts = self.points
        c = ids[0]  # @line L2
        node = Node(c, max(d(pts[c], pts[i]) for i in ids))
        if len(ids) <= self.b:  # @line L1
            node.points = ids
            return node
        a = max(ids, key=lambda i: d(pts[c], pts[i]))  # @line L3
        z = max(ids, key=lambda i: d(pts[a], pts[i]))
        ids = sorted(ids, key=lambda i: (d(pts[i], pts[a]) - d(pts[i], pts[z]), i))  # @line L4
        h = len(ids) // 2
        node.left = self._build(ids[:h])  # @line L5
        node.right = self._build(ids[h:])
        return node

    def knn(self, q: P, k: int) -> list[tuple[float, int]]:
        """Return the k pairs (distance, index) nearest to q, nearest first."""
        heap: list[tuple[float, int]] = []

        def tau() -> float:
            return -heap[0][0] if len(heap) == k else math.inf

        def visit(t: Node[P], dc: float) -> None:
            if dc - t.radius >= tau():  # @line L6
                return
            if t.points is not None:  # @line L7
                for i in t.points:
                    di = self.dist(q, self.points[i])
                    if len(heap) < k:
                        heapq.heappush(heap, (-di, -i))
                    elif (-di, -i) > heap[0]:
                        heapq.heapreplace(heap, (-di, -i))
                return
            assert t.left is not None and t.right is not None
            dl = self.dist(q, self.points[t.left.center])  # @line L8
            dr = self.dist(q, self.points[t.right.center])
            if dl <= dr:
                visit(t.left, dl)
                visit(t.right, dr)
            else:
                visit(t.right, dr)
                visit(t.left, dl)

        if self.root is not None and k > 0:
            visit(self.root, self.dist(q, self.points[self.root.center]))
        return sorted((-a, -b) for a, b in heap)

    def range(self, q: P, r: float) -> list[int]:
        """Return the indices of all points within distance r of q."""
        out: list[int] = []
        stack = [self.root] if self.root is not None else []
        while stack:
            t = stack.pop()
            if self.dist(q, self.points[t.center]) - t.radius > r:
                continue
            if t.points is not None:
                out.extend(i for i in t.points if self.dist(q, self.points[i]) <= r)
            else:
                stack.extend((t.left, t.right))
        return out
