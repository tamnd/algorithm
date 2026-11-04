# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ss-tree/. The authors are listed in prov/G93DHE.jsonl.
"""The SS-tree of White and Jain: a balanced tree of bounding spheres.

Points live in leaves of at most M entries; every node other than the
root has at least m. Each node keeps the centroid of all the points below
it, the number of those points, and a radius such that the sphere around
the centroid holds every point below. Insert goes to the child with the
nearest centroid. A node that overflows is split on the coordinate of
highest variance of its entries' centroids, at the cut that makes the sum
of the variances of the two sides smallest. (White and Jain also use the
forced reinsert of the R*-tree; this code does not.) Queries: points in a
ball, and the k nearest neighbors by a best-first search.
"""

from __future__ import annotations

import heapq
import math
from typing import Hashable, List, Optional, Sequence, Tuple

Point = Tuple[float, ...]


def dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


class Node:
    __slots__ = ("leaf", "entries", "center", "radius", "count", "parent")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.entries: list = []  # leaf: (point, id); internal: Node
        self.center: Point = ()
        self.radius = 0.0
        self.count = 0
        self.parent: Optional[Node] = None

    def centers(self) -> List[Point]:
        return [p for p, _ in self.entries] if self.leaf else [c.center for c in self.entries]

    def refresh(self) -> None:
        """Recompute centroid, count and radius from the entries."""
        if self.leaf:
            pts = [p for p, _ in self.entries]
            self.count = len(pts)
            d = len(pts[0])
            self.center = tuple(sum(p[t] for p in pts) / len(pts) for t in range(d))  # @line L5
            self.radius = max(dist(self.center, p) for p in pts)
        else:
            self.count = sum(c.count for c in self.entries)
            d = len(self.entries[0].center)
            self.center = tuple(sum(c.center[t] * c.count for c in self.entries) / self.count
                                for t in range(d))
            self.radius = max(dist(self.center, c.center) + c.radius for c in self.entries)  # @line L6


def variance(vals: Sequence[float]) -> float:
    mu = sum(vals) / len(vals)
    return sum((v - mu) ** 2 for v in vals) / len(vals)


def split_entries(entries: list, centers: List[Point], m: int) -> Tuple[list, list]:
    """Split on the coordinate of highest variance, at the cut that minimizes
    the sum of the variances of the two sides on that coordinate."""
    d = len(centers[0])
    axis = max(range(d), key=lambda t: (variance([c[t] for c in centers]), -t))  # @line L7
    order = sorted(range(len(entries)), key=lambda i: (centers[i][axis], i))
    vals = [centers[i][axis] for i in order]
    n = len(entries)
    best_k = min(range(m, n - m + 1),
                 key=lambda k: (variance(vals[:k]) + variance(vals[k:]), k))  # @line L8
    return [entries[i] for i in order[:best_k]], [entries[i] for i in order[best_k:]]


class SSTree:
    def __init__(self, max_entries: int = 4, min_entries: Optional[int] = None) -> None:
        if max_entries < 2:
            raise ValueError("M must be at least 2")
        self.M = max_entries
        self.m = min_entries if min_entries is not None else max(1, (2 * max_entries) // 5)
        if not 1 <= self.m <= self.M // 2:
            raise ValueError("need 1 <= m <= M/2")
        self.root: Optional[Node] = None
        self.n = 0

    # ---- insertion ----
    def insert(self, p: Sequence[float], oid: Hashable) -> None:
        p = tuple(float(x) for x in p)
        if self.root is None:
            self.root = Node(True)
        self._insert_entry((p, oid), 0)
        self.n += 1

    def _height(self) -> int:
        h, u = 0, self.root
        while not u.leaf:
            u = u.entries[0]
            h += 1
        return h

    def _insert_entry(self, e, level: int) -> None:
        """Insert a point (level 0) or a subtree whose leaves are at height level - 1."""
        u = self.root
        target = e[0] if level == 0 else e.center
        for _ in range(self._height() - level):  # @line L1
            u = min(u.entries, key=lambda c: dist(c.center, target))  # @line L2
        u.entries.append(e)  # @line L3
        if level > 0:
            e.parent = u
        while u is not None:  # @line L4
            if len(u.entries) > self.M:
                self._split(u)
            u.refresh()
            u = u.parent

    def _split(self, u: Node) -> None:
        a, b = split_entries(u.entries, u.centers(), self.m)
        u.entries = a
        v = Node(u.leaf)
        v.entries = b
        if not u.leaf:
            for c in b:
                c.parent = v
        v.refresh()
        if u.parent is None:  # @line L9
            root = Node(False)
            root.entries = [u, v]
            u.parent = v.parent = root
            self.root = root
            u.refresh()
            root.refresh()
        else:
            v.parent = u.parent
            u.parent.entries.append(v)  # @line L10

    # ---- deletion ----
    def delete(self, p: Sequence[float], oid: Hashable) -> bool:
        p = tuple(float(x) for x in p)
        leaf = self._find(self.root, p, oid) if self.root else None
        if leaf is None:
            return False
        leaf.entries.remove((p, oid))  # @line L11
        self.n -= 1
        orphans: List[Tuple[object, int]] = []
        u, h = leaf, 0
        while u.parent is not None:  # @line L12
            par = u.parent
            if len(u.entries) < self.m:
                par.entries.remove(u)
                orphans += [(e, h) for e in u.entries]
            else:
                u.refresh()
            u, h = par, h + 1
        if not self.root.entries:  # the root was a leaf with one point
            self.root = None
            return True
        self.root.refresh()
        for e, h in orphans:  # @line L13
            self._insert_entry(e, h)
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L14
            self.root = self.root.entries[0]
            self.root.parent = None
        return True

    def _find(self, u: Node, p: Point, oid) -> Optional[Node]:
        if dist(u.center, p) > u.radius + 1e-9:
            return None
        if u.leaf:
            return u if (p, oid) in u.entries else None
        for c in u.entries:
            r = self._find(c, p, oid)
            if r is not None:
                return r
        return None

    # ---- queries ----
    def ball(self, q: Sequence[float], r: float) -> List[Hashable]:
        """Ids of the points within distance r of q."""
        out: List[Hashable] = []
        if self.root is None:
            return out
        stack = [self.root]
        while stack:
            u = stack.pop()
            if dist(q, u.center) - u.radius > r:  # @line L15
                continue
            if u.leaf:
                out += [oid for p, oid in u.entries if dist(q, p) <= r]
            else:
                stack.extend(u.entries)
        return out

    def knn(self, q: Sequence[float], k: int) -> List[Tuple[float, Hashable]]:
        """The k nearest points as (distance, id), nearest first, by best-first search."""
        out: List[Tuple[float, Hashable]] = []
        if self.root is None or k <= 0:
            return out
        heap = [(max(0.0, dist(q, self.root.center) - self.root.radius), 0, 1, self.root)]
        tick = 1
        while heap and len(out) < k:  # @line L16
            d, kind, _, x = heapq.heappop(heap)
            if kind == 1:
                out.append((d, x))  # @line L17
                continue
            for e in x.entries:
                tick += 1
                if x.leaf:
                    heapq.heappush(heap, (dist(q, e[0]), 1, tick, e[1]))
                else:  # mindist of a sphere is a lower bound on the distance of its points
                    heapq.heappush(heap, (max(0.0, dist(q, e.center) - e.radius), 0, tick, e))  # @line L18
        return out

    # ---- checks ----
    def height(self) -> int:
        return -1 if self.root is None else self._height()

    def check_invariant(self) -> None:
        if self.root is None:
            assert self.n == 0
            return
        depths = set()
        total = 0

        def walk(u: Node, d: int) -> List[Point]:
            nonlocal total
            assert len(u.entries) <= self.M
            if u is not self.root:
                assert len(u.entries) >= self.m
            if u.leaf:
                depths.add(d)
                pts = [p for p, _ in u.entries]
                total += len(pts)
            else:
                assert u is self.root and len(u.entries) >= 2 or u is not self.root
                pts = []
                for c in u.entries:
                    assert c.parent is u
                    pts += walk(c, d + 1)
            assert u.count == len(pts)
            cen = tuple(sum(p[t] for p in pts) / len(pts) for t in range(len(pts[0])))
            assert dist(cen, u.center) < 1e-6
            assert all(dist(u.center, p) <= u.radius + 1e-6 for p in pts)
            return pts

        walk(self.root, 0)
        assert len(depths) == 1 and total == self.n
