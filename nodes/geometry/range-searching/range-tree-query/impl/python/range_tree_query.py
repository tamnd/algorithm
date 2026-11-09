# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-tree-query/. The authors are listed in prov/ZMJ28C.jsonl.

"""The two-dimensional range tree query of de Berg et al. (Section 5.3, 2DRANGEQUERY).

The primary tree is a balanced leaf-based tree over the points sorted by (x, y, index); node v
covers the positions [lo(v), hi(v)) of that order, with children split at the middle, numbered
as in a heap. Each node keeps its points sorted by (y, x, index) with their y-values, the
associated one-dimensional structure. The query maps [x1, x2] to the positions lo..hi (closed),
finds the split node where the paths to the leaves lo and hi separate, and walks the two paths,
querying the associated array of every subtree that hangs off the inner side of a path.

Boxes are closed. Cost: build O(n log n) time and space; report O(log^2 n + k) and count
O(log^2 n) time in the worst case.
"""

from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[object, object]


class RangeTree2D:
    """A static two-dimensional range tree (repeats allowed)."""

    def __init__(self, points: Sequence[Point] = ()) -> None:
        pts = [tuple(p) for p in points]
        self.n = len(pts)
        order = sorted(range(self.n), key=lambda i: (pts[i][0], pts[i][1], i))
        self.pts = [pts[i] for i in order]  # points in x-order
        self.xs = [p[0] for p in self.pts]
        # assoc[v] = (points of v sorted by y, their y-values)
        self.assoc: Dict[int, Tuple[List[Point], list]] = {}
        if self.n == 0:
            return
        ykey = lambda p: (p[1], p[0])
        lists: Dict[int, List[Point]] = {}
        stack = [(1, 0, self.n, False)]
        while stack:
            v, lo, hi, done = stack.pop()
            if hi - lo == 1:
                lists[v] = [self.pts[lo]]
            elif not done:
                mid = (lo + hi) // 2
                stack.append((v, lo, hi, True))
                stack.append((2 * v + 1, mid, hi, False))
                stack.append((2 * v, lo, mid, False))
                continue
            else:
                a, b = lists[2 * v], lists[2 * v + 1]
                out, i, j = [], 0, 0
                while i < len(a) and j < len(b):
                    if ykey(a[i]) <= ykey(b[j]):
                        out.append(a[i])
                        i += 1
                    else:
                        out.append(b[j])
                        j += 1
                out.extend(a[i:])
                out.extend(b[j:])
                lists[v] = out
            self.assoc[v] = (lists[v], [p[1] for p in lists[v]])

    def __len__(self) -> int:
        return self.n

    def _query_1d(self, v: int, y1, y2, sink) -> None:
        arr, ys = self.assoc[v]
        sink(arr, bisect_left(ys, y1), bisect_right(ys, y2))

    def _run(self, x1, x2, y1, y2, sink, stats: Optional[dict]) -> None:
        st = {"one_d_queries": 0, "path_nodes": 0, "split_depth": -1}
        lo = bisect_left(self.xs, x1)  # @line L1
        hi = bisect_right(self.xs, x2) - 1
        if self.n == 0 or lo > hi or y1 > y2:
            if stats is not None:
                stats.update(st)
            return

        def leaf_check(pos: int) -> None:
            p = self.pts[pos]
            if y1 <= p[1] <= y2:
                sink([p], 0, 1)

        # FIND-SPLIT-NODE: descend while both lo and hi lie in the same child.
        v, a, b, depth = 1, 0, self.n, 0  # @line L2
        while b - a > 1:
            mid = (a + b) // 2
            if hi < mid:
                v, b = 2 * v, mid
            elif lo >= mid:
                v, a = 2 * v + 1, mid
            else:
                break
            depth += 1
        st["split_depth"] = depth
        if b - a == 1:  # @line L3
            leaf_check(a)
        else:
            mid = (a + b) // 2
            u, ua, ub = 2 * v, a, mid  # @line L4
            while ub - ua > 1:  # @line L5
                st["path_nodes"] += 1
                um = (ua + ub) // 2
                if lo < um:  # @line L6
                    self._query_1d(2 * u + 1, y1, y2, sink)
                    st["one_d_queries"] += 1
                    u, ub = 2 * u, um
                else:  # @line L7
                    u, ua = 2 * u + 1, um
            leaf_check(ua)  # @line L8
            u, ua, ub = 2 * v + 1, mid, b  # @line L9
            while ub - ua > 1:
                st["path_nodes"] += 1
                um = (ua + ub) // 2
                if hi >= um:
                    self._query_1d(2 * u, y1, y2, sink)
                    st["one_d_queries"] += 1
                    u, ua = 2 * u + 1, um
                else:
                    u, ub = 2 * u, um
            leaf_check(ua)  # @line L10
        if stats is not None:
            stats.update(st)

    def report(self, x1, x2, y1, y2, stats: Optional[dict] = None) -> List[Point]:
        """Points p with x1 <= p[0] <= x2 and y1 <= p[1] <= y2. O(log^2 n + k) worst case."""
        out: List[Point] = []
        self._run(x1, x2, y1, y2, lambda arr, i, j: out.extend(arr[i:j]), stats)
        return out

    def count(self, x1, x2, y1, y2, stats: Optional[dict] = None) -> int:
        """Number of points in the closed box. O(log^2 n) worst case."""
        total = [0]

        def sink(arr, i, j):
            total[0] += j - i

        self._run(x1, x2, y1, y2, sink, stats)
        return total[0]
