# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sr-tree/. The authors are listed in prov/PJ11JW.jsonl.
"""The SR-tree of Katayama and Satoh: a tree of spheres and rectangles.

The tree has the shape and the insertion and split rules of the SS-tree:
points live in leaves of at most M entries, insertion goes to the child
with the nearest centroid, and a full node is split on the coordinate of
highest variance. Each node keeps both a bounding sphere, around the
centroid of the points below it, and a bounding rectangle, the MBR of
those points. The region of the node is the intersection of the two. The
radius of the sphere uses the rectangles of the children to stay small:
it is the largest, over the children, of the smaller of two bounds on
the distance from the centroid to the child's points. The lower bound on
the distance from a query to a node is the larger of the distance to the
sphere and the distance to the rectangle.
"""

from __future__ import annotations

import heapq
import math
from typing import Hashable, List, Optional, Sequence, Tuple

Point = Tuple[float, ...]


def dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def far_dist(c: Sequence[float], lo: Sequence[float], hi: Sequence[float]) -> float:
    """The largest distance from c to a point of the box [lo, hi]."""
    return math.sqrt(sum(max(x - a, b - x) ** 2 for x, a, b in zip(c, lo, hi)))


def rect_mindist(q: Sequence[float], lo: Sequence[float], hi: Sequence[float]) -> float:
    """The distance from q to the box [lo, hi]."""
    return math.sqrt(sum(max(a - x, 0.0, x - b) ** 2 for x, a, b in zip(q, lo, hi)))


class Node:
    __slots__ = ("leaf", "entries", "center", "radius", "count", "parent", "lo", "hi")

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.entries: list = []  # leaf: (point, id); internal: Node
        self.center: Point = ()
        self.radius = 0.0
        self.count = 0
        self.parent: Optional[Node] = None
        self.lo: Point = ()
        self.hi: Point = ()

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
            self.lo = tuple(min(p[t] for p in pts) for t in range(d))
            self.hi = tuple(max(p[t] for p in pts) for t in range(d))
        else:
            self.count = sum(c.count for c in self.entries)
            d = len(self.entries[0].center)
            self.center = tuple(sum(c.center[t] * c.count for c in self.entries) / self.count
                                for t in range(d))
            self.lo = tuple(min(c.lo[t] for c in self.entries) for t in range(d))  # @line L6
            self.hi = tuple(max(c.hi[t] for c in self.entries) for t in range(d))
            self.radius = max(min(dist(self.center, c.center) + c.radius,
                                  far_dist(self.center, c.lo, c.hi)) for c in self.entries)  # @line L7

    def mindist(self, q: Sequence[float]) -> float:
        """A lower bound on the distance from q to every point below: the larger
        of the distances to the sphere and to the rectangle."""
        return max(dist(q, self.center) - self.radius, rect_mindist(q, self.lo, self.hi))  # @line L15


def variance(vals: Sequence[float]) -> float:
    mu = sum(vals) / len(vals)
    return sum((v - mu) ** 2 for v in vals) / len(vals)


def split_entries(entries: list, centers: List[Point], m: int) -> Tuple[list, list]:
    """Split on the coordinate of highest variance, at the cut that minimizes
    the sum of the variances of the two sides on that coordinate."""
    d = len(centers[0])
    axis = max(range(d), key=lambda t: (variance([c[t] for c in centers]), -t))  # @line L8
    order = sorted(range(len(entries)), key=lambda i: (centers[i][axis], i))
    vals = [centers[i][axis] for i in order]
    n = len(entries)
    best_k = min(range(m, n - m + 1),
                 key=lambda k: (variance(vals[:k]) + variance(vals[k:]), k))
    return [entries[i] for i in order[:best_k]], [entries[i] for i in order[best_k:]]


class SRTree:
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
        if u.parent is None:
            root = Node(False)
            root.entries = [u, v]
            u.parent = v.parent = root
            self.root = root
            u.refresh()
            root.refresh()
        else:
            v.parent = u.parent
            u.parent.entries.append(v)

    # ---- deletion ----
    def delete(self, p: Sequence[float], oid: Hashable) -> bool:
        p = tuple(float(x) for x in p)
        leaf = self._find(self.root, p, oid) if self.root else None
        if leaf is None:
            return False
        leaf.entries.remove((p, oid))  # @line L9
        self.n -= 1
        orphans: List[Tuple[object, int]] = []
        u, h = leaf, 0
        while u.parent is not None:  # @line L10
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
        for e, h in orphans:  # @line L11
            self._insert_entry(e, h)
        while not self.root.leaf and len(self.root.entries) == 1:  # @line L12
            self.root = self.root.entries[0]
            self.root.parent = None
        return True

    def _find(self, u: Node, p: Point, oid) -> Optional[Node]:
        if u.mindist(p) > 1e-9:
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
            if u.mindist(q) > r:  # @line L13
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
        heap = [(max(0.0, self.root.mindist(q)), 0, 1, self.root)]
        tick = 1
        while heap and len(out) < k:  # @line L14
            d, kind, _, x = heapq.heappop(heap)
            if kind == 1:
                out.append((d, x))
                continue
            for e in x.entries:
                tick += 1
                if x.leaf:
                    heapq.heappush(heap, (dist(q, e[0]), 1, tick, e[1]))
                else:  # mindist is a lower bound on the distance of the points below
                    heapq.heappush(heap, (max(0.0, e.mindist(q)), 0, tick, e))
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
            for t in range(len(pts[0])):
                assert u.lo[t] == min(p[t] for p in pts) and u.hi[t] == max(p[t] for p in pts)
            return pts

        walk(self.root, 0)
        assert len(depths) == 1 and total == self.n
