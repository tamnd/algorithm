# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-tree/. The authors are listed in prov/XGPFAM.jsonl.

"""A static d-dimensional range tree (Bentley 1979, de Berg et al., Sections 5.3 and 5.4).

The level for coordinate j is a balanced binary tree over the points sorted by (p[j], index).
A node covers a contiguous block [lo, hi) of that order and stores an associated structure for
coordinate j + 1 over the points of the block. The level for the last coordinate is a sorted
array. Nodes are numbered as in a heap (root 1, children 2v and 2v + 1), and all traversals use
explicit stacks; only the dimension recursion is a Python call, of depth d.

Query boxes are closed: lo[j] <= p[j] <= hi[j] for every j.

Cost, for n points in d >= 2 dimensions: build O(n log^(d-1) n) time and space;
report O(log^d n + k) time; count O(log^d n) time, all in the worst case.
"""

from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Sequence, Tuple


class _Level:
    """The structure for coordinates j, j+1, ..., d-1 over a list of point indices."""

    __slots__ = ("j", "order", "keys", "assoc", "m")

    def __init__(self, pts: List[tuple], d: int, j: int, order: List[int]) -> None:
        # order: indices sorted by (pts[i][j], i).
        self.j = j
        self.order = order
        self.keys = [pts[i][j] for i in order]
        self.m = len(order)
        self.assoc: Dict[int, "_Level"] = {}
        if j == d - 1 or self.m == 0:  # @line L1
            return
        nxt = j + 1
        key = lambda i: (pts[i][nxt], i)
        # Post-order over the implicit tree: Y(v) is the merge of Y(2v) and Y(2v + 1).
        ylist: Dict[int, List[int]] = {}
        stack = [(1, 0, self.m, False)]  # @line L2
        while stack:  # @line L3
            v, lo, hi, done = stack.pop()
            if hi - lo == 1:
                ylist[v] = [order[lo]]  # @line L4
            elif not done:
                mid = (lo + hi) // 2
                stack.append((v, lo, hi, True))
                stack.append((2 * v + 1, mid, hi, False))
                stack.append((2 * v, lo, mid, False))
                continue
            else:
                a, b = ylist[2 * v], ylist[2 * v + 1]
                merged = []
                p = q = 0
                while p < len(a) and q < len(b):
                    if key(a[p]) <= key(b[q]):
                        merged.append(a[p])
                        p += 1
                    else:
                        merged.append(b[q])
                        q += 1
                merged.extend(a[p:])
                merged.extend(b[q:])
                ylist[v] = merged
            self.assoc[v] = _Level(pts, d, nxt, ylist[v])  # @line L5
        # @line L6: the tree of this level is the implicit node numbering plus self.assoc.

    def canonical(self, a: int, b: int) -> List[int]:
        """The maximal nodes whose blocks lie inside positions [a, b), left to right."""
        out: List[int] = []
        if a >= b:
            return out
        stack = [(1, 0, self.m)]
        while stack:
            v, lo, hi = stack.pop()
            if b <= lo or hi <= a:
                continue
            if a <= lo and hi <= b:
                out.append(v)
                continue
            mid = (lo + hi) // 2
            stack.append((2 * v + 1, mid, hi))
            stack.append((2 * v, lo, mid))
        return out


class RangeTree:
    """A static range tree on points of a fixed dimension d >= 1 (repeats allowed)."""

    def __init__(self, points: Sequence[Sequence] = (), d: Optional[int] = None) -> None:
        self.points: List[tuple] = [tuple(p) for p in points]
        if d is None:
            d = len(self.points[0]) if self.points else 2
        self.d = d
        pts = self.points
        order = sorted(range(len(pts)), key=lambda i: (pts[i][0], i))
        self.top = _Level(pts, d, 0, order)

    def __len__(self) -> int:
        return len(self.points)

    def _search(self, lo: Sequence, hi: Sequence, sink, stats: Optional[dict]) -> None:
        canon = 0
        # Each task: a level and the coordinate it handles.
        tasks = [self.top]
        while tasks:
            s = tasks.pop()
            j = s.j
            a = bisect_left(s.keys, lo[j])  # @line L7
            b = bisect_right(s.keys, hi[j])
            if a >= b:
                continue
            if j == self.d - 1:  # @line L8
                sink(s, a, b)
                continue
            for v in s.canonical(a, b):  # @line L9
                canon += 1
                tasks.append(s.assoc[v])  # @line L10
        if stats is not None:
            stats["canonical"] = canon

    def report(self, lo: Sequence, hi: Sequence, stats: Optional[dict] = None) -> List[tuple]:
        """Points p with lo[j] <= p[j] <= hi[j] for all j. O(log^d n + k) worst case."""
        out: List[tuple] = []
        pts = self.points

        def sink(s: _Level, a: int, b: int) -> None:
            out.extend(pts[i] for i in s.order[a:b])

        self._search(lo, hi, sink, stats)
        return out

    def count(self, lo: Sequence, hi: Sequence, stats: Optional[dict] = None) -> int:
        """Number of points in the closed box. O(log^d n) worst case."""
        total = [0]

        def sink(s: _Level, a: int, b: int) -> None:
            total[0] += b - a

        self._search(lo, hi, sink, stats)
        return total[0]

    def size(self) -> int:
        """Total number of point entries stored in all levels (the space measure)."""
        total = 0
        stack = [self.top]
        while stack:
            s = stack.pop()
            total += s.m
            stack.extend(s.assoc.values())
        return total

    def check_invariant(self) -> bool:
        """Each level is sorted by its coordinate, and each associated structure holds
        exactly the points of its node's block."""
        pts = self.points
        stack = [self.top]
        while stack:
            s = stack.pop()
            j = s.j
            keyed = [(pts[i][j], i) for i in s.order]
            if keyed != sorted(keyed):
                return False
            if j < self.d - 1 and s.m > 0:
                nodes = [(1, 0, s.m)]
                while nodes:
                    v, lo, hi = nodes.pop()
                    sub = s.assoc.get(v)
                    if sub is None or sorted(sub.order) != sorted(s.order[lo:hi]):
                        return False
                    stack.append(sub)
                    if hi - lo > 1:
                        mid = (lo + hi) // 2
                        nodes.append((2 * v, lo, mid))
                        nodes.append((2 * v + 1, mid, hi))
        return True
