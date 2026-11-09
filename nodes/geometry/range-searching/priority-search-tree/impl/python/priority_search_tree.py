# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-search-tree/. The authors are listed in prov/2MY7Y5.jsonl.

"""A static priority search tree (McCreight 1985; de Berg et al., Section 10.2).

The points are sorted by (x, y, index); position j is the j-th point of that order. The tree is
a balanced binary tree over the positions: node v covers the block [lo(v), hi(v)), children split
at the middle and are numbered as in a heap (root 1, children 2v and 2v + 1). Each node stores at
most one point: the point of its block with the smallest key (y, x, position) among the points
not stored at a proper ancestor. So the tree is a search tree on x (by blocks) and a min-heap on
y (by stored points) at the same time.

Queries are closed: three_sided(x1, x2, y0) reports the points with x1 <= x <= x2 and y <= y0.
Cost: build O(n log n), space O(n), three_sided O(log n + k), lowest_in_x_range O(log n), all in
the worst case.
"""

from bisect import bisect_left, bisect_right
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[object, object]


class PrioritySearchTree:
    """A static priority search tree on a multiset of points in the plane."""

    def __init__(self, points: Sequence[Point] = ()) -> None:
        pts = [tuple(p) for p in points]
        self.n = len(pts)
        order = sorted(range(self.n), key=lambda i: (pts[i][0], pts[i][1], i))
        self.pts = [pts[i] for i in order]  # @line L1
        self.xs = [p[0] for p in self.pts]
        self.node: Dict[int, int] = {}  # node -> position of its stored point
        if self.n == 0:
            return
        stack = [(1, 0, self.n, list(range(self.n)))]  # @line L2
        while stack:
            v, lo, hi, rest = stack.pop()
            if not rest:  # @line L3
                continue
            j = min(rest, key=self._key)  # @line L4
            self.node[v] = j
            if hi - lo > 1:  # @line L5
                mid = (lo + hi) // 2
                stack.append((2 * v, lo, mid, [r for r in rest if r != j and r < mid]))
                stack.append((2 * v + 1, mid, hi, [r for r in rest if r != j and r >= mid]))

    def _key(self, j: int):
        p = self.pts[j]
        return (p[1], p[0], j)

    def __len__(self) -> int:
        return self.n

    def three_sided(self, x1, x2, y0, stats: Optional[dict] = None) -> List[Point]:
        """Points with x1 <= x <= x2 and y <= y0. O(log n + k) worst case."""
        out: List[Point] = []
        calls = 0
        lo = bisect_left(self.xs, x1)  # @line L6
        hi = bisect_right(self.xs, x2) - 1
        stack = [(1, 0, self.n)] if self.n and lo <= hi else []
        while stack:  # @line L7
            v, a, b = stack.pop()
            calls += 1
            if v not in self.node or b <= lo or a > hi:  # @line L8
                continue
            j = self.node[v]
            if self.pts[j][1] > y0:  # @line L9
                continue
            if lo <= j <= hi:  # @line L10
                out.append(self.pts[j])
            if b - a > 1:  # @line L11
                mid = (a + b) // 2
                stack.append((2 * v + 1, mid, b))
                stack.append((2 * v, a, mid))
        if stats is not None:
            stats["calls"] = calls
        return out

    def lowest_in_x_range(self, x1, x2, stats: Optional[dict] = None) -> Optional[Point]:
        """The point with the smallest (y, x) among x1 <= x <= x2, or None. O(log n) worst case."""
        lo = bisect_left(self.xs, x1)
        hi = bisect_right(self.xs, x2) - 1
        best = None
        calls = 0
        stack = [(1, 0, self.n)] if self.n and lo <= hi else []
        while stack:
            v, a, b = stack.pop()
            calls += 1
            if v not in self.node or b <= lo or a > hi:
                continue
            j = self.node[v]
            if lo <= j <= hi and (best is None or self._key(j) < self._key(best)):
                best = j
            if lo <= a and b - 1 <= hi:
                continue  # the stored point is the lowest of the whole block
            if b - a > 1:
                mid = (a + b) // 2
                stack.append((2 * v + 1, mid, b))
                stack.append((2 * v, a, mid))
        if stats is not None:
            stats["calls"] = calls
        return None if best is None else self.pts[best]

    def check_invariant(self) -> None:
        """Each point is stored once, inside its block, and keys increase down every path."""
        assert sorted(self.node.values()) == list(range(self.n))
        stack = [(1, 0, self.n, None)] if self.n else []
        while stack:
            v, a, b, parent_key = stack.pop()
            if v not in self.node:
                for w in (2 * v, 2 * v + 1):
                    assert w not in self.node or b - a <= 1
                continue
            j = self.node[v]
            assert a <= j < b
            assert parent_key is None or parent_key < self._key(j)
            if b - a > 1:
                mid = (a + b) // 2
                stack.append((2 * v, a, mid, self._key(j)))
                stack.append((2 * v + 1, mid, b, self._key(j)))
