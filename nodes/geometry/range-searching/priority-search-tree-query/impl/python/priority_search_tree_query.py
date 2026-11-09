# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-search-tree-query/. The authors are listed in prov/ZHWQH0.jsonl.

"""The three-sided query on a priority search tree, in the form of de Berg et al. (Section 10.2).

The tree: points sorted by (x, y, index), position j is the j-th point; node v (heap numbering,
root 1) covers the block [lo(v), hi(v)) of positions, children split it in the middle, and v
stores the position with the smallest key (y, x, position) among the positions of its block not
stored at a proper ancestor (or nothing).

The query for [x1, x2] x (-inf, y0] walks the search paths to the leaves of the positions lo and
hi, tests the point stored at every node on them, and calls REPORT-IN-SUBTREE on every subtree
that hangs between the two paths. REPORT-IN-SUBTREE descends while the stored points are low
enough, which is output sensitive because of the heap order.

Cost: O(log n + k) time in the worst case, O(n) space.
"""

from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[object, object]


class PrioritySearchTree:
    """A static priority search tree with the split-path three-sided query."""

    def __init__(self, points: Sequence[Point] = ()) -> None:
        pts = [tuple(p) for p in points]
        self.n = len(pts)
        order = sorted(range(self.n), key=lambda i: (pts[i][0], pts[i][1], i))
        self.pts = [pts[i] for i in order]
        self.xs = [p[0] for p in self.pts]
        self.node: Dict[int, int] = {}
        stack = [(1, 0, self.n, list(range(self.n)))] if self.n else []
        while stack:
            v, lo, hi, rest = stack.pop()
            if not rest:
                continue
            j = min(rest, key=lambda r: (self.pts[r][1], self.pts[r][0], r))
            self.node[v] = j
            if hi - lo > 1:
                mid = (lo + hi) // 2
                stack.append((2 * v, lo, mid, [r for r in rest if r != j and r < mid]))
                stack.append((2 * v + 1, mid, hi, [r for r in rest if r != j and r >= mid]))

    def _report_in_subtree(self, u: int, y0, out: List[Point], st: dict) -> None:
        stack = [u]  # @line L6
        while stack:  # @line L7
            u = stack.pop()
            st["subtree_visits"] += 1
            if u not in self.node or self.pts[self.node[u]][1] > y0:  # @line L8
                continue
            out.append(self.pts[self.node[u]])  # @line L9
            stack.append(2 * u + 1)
            stack.append(2 * u)

    def query(self, x1, x2, y0, stats: Optional[dict] = None) -> List[Point]:
        """Points with x1 <= x <= x2 and y <= y0. O(log n + k) worst case."""
        out: List[Point] = []
        st = {"path_nodes": 0, "subtree_visits": 0, "subtrees": 0}
        lo = bisect_left(self.xs, x1)  # @line L1
        hi = bisect_right(self.xs, x2) - 1
        if self.n and lo <= hi:
            # Each walker is (node, block start, block end, which path): 0 shared, 1 to lo, 2 to hi.
            walkers = [(1, 0, self.n, 0)]
            while walkers:  # @line L2
                v, a, b, side = walkers.pop()
                if v not in self.node:
                    continue
                st["path_nodes"] += 1
                j = self.node[v]
                if lo <= j <= hi and self.pts[j][1] <= y0:  # @line L3
                    out.append(self.pts[j])
                if b - a == 1:
                    continue
                mid = (a + b) // 2
                if side == 0:
                    if hi < mid:
                        walkers.append((2 * v, a, mid, 0))
                    elif lo >= mid:
                        walkers.append((2 * v + 1, mid, b, 0))
                    else:  # v is the split node
                        walkers.append((2 * v + 1, mid, b, 2))
                        walkers.append((2 * v, a, mid, 1))
                elif side == 1:
                    if lo < mid:  # @line L4
                        st["subtrees"] += 1
                        self._report_in_subtree(2 * v + 1, y0, out, st)
                        walkers.append((2 * v, a, mid, 1))
                    else:
                        walkers.append((2 * v + 1, mid, b, 1))
                else:
                    if hi >= mid:  # @line L5
                        st["subtrees"] += 1
                        self._report_in_subtree(2 * v, y0, out, st)
                        walkers.append((2 * v + 1, mid, b, 2))
                    else:
                        walkers.append((2 * v, a, mid, 2))
        if stats is not None:
            stats.update(st)
        return out
