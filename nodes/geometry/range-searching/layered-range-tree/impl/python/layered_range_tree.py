# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/layered-range-tree/. The authors are listed in prov/HMB009.jsonl.

"""A two-dimensional layered range tree (de Berg et al., Section 5.6).

The primary tree is a balanced leaf-based tree over the points sorted by (x, y, index); node v
covers the positions [lo(v), hi(v)) of that order, children split at the middle, numbered as in a
heap. Each node keeps A(v), its points sorted by the total key (y, x, index), and the cascading
array left[v], where left[v][i] is the number of entries of A(left child) among the first i
entries of A(v), for i = 0..|A(v)|. The matching count for the right child is i - left[v][i].

Because the keys are distinct, the first i entries of A(v) are exactly the entries with a key
below A(v)[i], so left[v][i] is the position in A(left child) of the first entry with a key at
least A(v)[i]. A query does its only two binary searches in A(split node) and follows these
counts down both search paths.

Boxes are closed. Cost: build O(n log n) time and space; report O(log n + k) and count
O(log n) time in the worst case.
"""

from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[object, object]


class LayeredRangeTree:
    """A static two-dimensional layered range tree (repeats allowed)."""

    def __init__(self, points: Sequence[Point] = ()) -> None:
        pts = [tuple(p) for p in points]
        self.n = len(pts)
        order = sorted(range(self.n), key=lambda i: (pts[i][0], pts[i][1], i))
        self.pts = [pts[i] for i in order]  # @line L1
        self.xs = [p[0] for p in self.pts]
        self.arr: Dict[int, List[Point]] = {}
        self.ys: Dict[int, list] = {}
        self.left: Dict[int, List[int]] = {}
        if self.n == 0:
            return
        # Key of the position j in x-order: (y, x, j); distinct for all j.
        keys: Dict[int, List[tuple]] = {}
        stack = [(1, 0, self.n, False)]
        while stack:  # @line L2
            v, lo, hi, done = stack.pop()
            if hi - lo == 1:  # @line L3
                p = self.pts[lo]
                keys[v] = [(p[1], p[0], lo)]
            elif not done:
                mid = (lo + hi) // 2
                stack.append((v, lo, hi, True))
                stack.append((2 * v + 1, mid, hi, False))
                stack.append((2 * v, lo, mid, False))
                continue
            else:
                a, b = keys[2 * v], keys[2 * v + 1]
                out, cnt, i, j = [], [0], 0, 0  # @line L4
                while i < len(a) or j < len(b):
                    if j == len(b) or (i < len(a) and a[i] < b[j]):
                        out.append(a[i])
                        i += 1
                    else:
                        out.append(b[j])
                        j += 1
                    cnt.append(i)
                keys[v] = out
                self.left[v] = cnt
                del keys[2 * v], keys[2 * v + 1]
            self.arr[v] = [self.pts[k[2]] for k in keys[v]]  # @line L5
            self.ys[v] = [k[0] for k in keys[v]]

    def __len__(self) -> int:
        return self.n

    def _run(self, x1, x2, y1, y2, sink, stats: Optional[dict]) -> None:
        st = {"binary_searches": 0, "path_nodes": 0, "canonical": 0}
        if self.n == 0 or y1 > y2:
            if stats is not None:
                stats.update(st)
            return
        lo = bisect_left(self.xs, x1)  # @line L6
        hi = bisect_right(self.xs, x2) - 1
        if lo > hi:
            if stats is not None:
                stats.update(st)
            return
        v, a, b = 1, 0, self.n  # @line L7
        while b - a > 1:
            mid = (a + b) // 2
            if hi < mid:
                v, b = 2 * v, mid
            elif lo >= mid:
                v, a = 2 * v + 1, mid
            else:
                break
        ys = self.ys[v]  # @line L8
        s, t = bisect_left(ys, y1), bisect_right(ys, y2)
        st["binary_searches"] = 2
        if b - a == 1:  # @line L9
            sink(self.arr[v], s, t)
        else:
            mid = (a + b) // 2
            lv = self.left[v]
            u, ua, ub, us, ut = 2 * v, a, mid, lv[s], lv[t]  # @line L10
            while ub - ua > 1:  # @line L11
                st["path_nodes"] += 1
                um = (ua + ub) // 2
                lu = self.left[u]
                if lo < um:  # @line L12
                    st["canonical"] += 1
                    sink(self.arr[2 * u + 1], us - lu[us], ut - lu[ut])
                    u, ub, us, ut = 2 * u, um, lu[us], lu[ut]
                else:  # @line L13
                    u, ua, us, ut = 2 * u + 1, um, us - lu[us], ut - lu[ut]
            sink(self.arr[u], us, ut)  # @line L14
            u, ua, ub = 2 * v + 1, mid, b  # @line L15
            us, ut = s - lv[s], t - lv[t]
            while ub - ua > 1:
                st["path_nodes"] += 1
                um = (ua + ub) // 2
                lu = self.left[u]
                if hi >= um:
                    st["canonical"] += 1
                    sink(self.arr[2 * u], lu[us], lu[ut])
                    u, ua, us, ut = 2 * u + 1, um, us - lu[us], ut - lu[ut]
                else:
                    u, ub, us, ut = 2 * u, um, lu[us], lu[ut]
            sink(self.arr[u], us, ut)  # @line L16
        if stats is not None:
            stats.update(st)

    def report(self, x1, x2, y1, y2, stats: Optional[dict] = None) -> List[Point]:
        """Points p with x1 <= p[0] <= x2 and y1 <= p[1] <= y2. O(log n + k) worst case."""
        out: List[Point] = []
        self._run(x1, x2, y1, y2, lambda arr, i, j: out.extend(arr[i:j]), stats)
        return out

    def count(self, x1, x2, y1, y2, stats: Optional[dict] = None) -> int:
        """Number of points in the closed box. O(log n) worst case."""
        total = [0]

        def sink(arr, i, j):
            total[0] += j - i

        self._run(x1, x2, y1, y2, sink, stats)
        return total[0]

    def check_invariant(self) -> None:
        """Every A(v) is its block sorted by (y, x, index); every cascading array is right."""
        if self.n == 0:
            return
        stack = [(1, 0, self.n)]
        while stack:
            v, lo, hi = stack.pop()
            block = sorted(range(lo, hi), key=lambda j: (self.pts[j][1], self.pts[j][0], j))
            assert self.arr[v] == [self.pts[j] for j in block]
            assert self.ys[v] == [self.pts[j][1] for j in block]
            if hi - lo > 1:
                mid = (lo + hi) // 2
                want = [0]
                for j in block:
                    want.append(want[-1] + (1 if j < mid else 0))
                assert self.left[v] == want
                stack.append((2 * v, lo, mid))
                stack.append((2 * v + 1, mid, hi))
