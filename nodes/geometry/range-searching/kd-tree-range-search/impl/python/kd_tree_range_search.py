# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-range-search/. The authors are listed in prov/XJ7XNM.jsonl.

"""Orthogonal range reporting with a two-dimensional kd-tree (de Berg et al., Section 5.2).

The tree is leaf based: every leaf holds one point and every internal node has two children.
The split at depth t uses the composite key (p[a], p[1 - a], index) with a = t mod 2, so equal
coordinates are split evenly. Every node stores the bounding box of the points below it, in the
original coordinates; the query compares these boxes with the closed query box.

Cost: build O(n log n) time and O(n) space (presorted lists, partitioned at each level);
a query reports the k points of the closed box [x1, x2] x [y1, y2] in O(n^(1/2) + k) time
in the worst case. Coordinates are integers or Fractions; all comparisons are exact.
"""

from typing import List, Optional, Sequence, Tuple

Point = Tuple[object, object]


class KDTree:
    """A static two-dimensional kd-tree over a list of points (repeats allowed)."""

    def __init__(self, points: Sequence[Point] = ()) -> None:
        self.points: List[Point] = [tuple(p) for p in points]
        n = len(self.points)
        # Node arrays. leaf_point[v] is a point index for a leaf and -1 for an internal node.
        self.left: List[int] = []
        self.right: List[int] = []
        self.leaf_point: List[int] = []
        self.box: List[Tuple[object, object, object, object]] = []
        self.size: List[int] = []
        self.root: int = -1
        if n == 0:
            return
        pts = self.points
        by_x = sorted(range(n), key=lambda i: (pts[i][0], pts[i][1], i))
        by_y = sorted(range(n), key=lambda i: (pts[i][1], pts[i][0], i))
        self.root = self._new_node()
        # Task: (node, list sorted by the split axis of this depth, list sorted by the other, depth)
        tasks = [(self.root, by_x, by_y, 0)]
        while tasks:
            v, first, second, depth = tasks.pop()
            xs = [pts[i][0] for i in first]
            ys = [pts[i][1] for i in first]
            self.box[v] = (min(xs), max(xs), min(ys), max(ys))
            self.size[v] = len(first)
            if len(first) == 1:
                self.leaf_point[v] = first[0]
                continue
            half = (len(first) + 1) // 2
            left_set = set(first[:half])
            l_first, r_first = first[:half], first[half:]
            l_second = [i for i in second if i in left_set]
            r_second = [i for i in second if i not in left_set]
            lc, rc = self._new_node(), self._new_node()
            self.left[v], self.right[v] = lc, rc
            # The children split on the other axis, so the two lists swap roles.
            tasks.append((lc, l_second, l_first, depth + 1))
            tasks.append((rc, r_second, r_first, depth + 1))

    def _new_node(self) -> int:
        self.left.append(-1)
        self.right.append(-1)
        self.leaf_point.append(-1)
        self.box.append((0, 0, 0, 0))
        self.size.append(0)
        return len(self.left) - 1

    def __len__(self) -> int:
        return len(self.points)

    def _report_subtree(self, v: int, out: List[Point], stats: dict) -> None:
        stack = [v]
        while stack:
            u = stack.pop()
            stats["reported_nodes"] += 1
            if self.leaf_point[u] >= 0:
                out.append(self.points[self.leaf_point[u]])
            else:
                stack.append(self.right[u])
                stack.append(self.left[u])

    def query(self, x1, x2, y1, y2, stats: Optional[dict] = None) -> List[Point]:
        """Return the points p with x1 <= p[0] <= x2 and y1 <= p[1] <= y2 (closed box).

        If stats is a dict, stats["search_nodes"] counts the nodes on which the search
        recursed and stats["reported_nodes"] the nodes inside reported subtrees.
        Time O(n^(1/2) + k) in the worst case.
        """
        st = {"search_nodes": 0, "reported_nodes": 0}
        out: List[Point] = []
        if self.root >= 0 and x1 <= x2 and y1 <= y2:
            stack = [self.root]
            while stack:
                v = stack.pop()
                st["search_nodes"] += 1
                if self.leaf_point[v] >= 0:  # @line L1
                    p = self.points[self.leaf_point[v]]
                    if x1 <= p[0] <= x2 and y1 <= p[1] <= y2:  # @line L2
                        out.append(p)
                    continue
                for c in (self.right[v], self.left[v]):  # @line L3
                    bx1, bx2, by1, by2 = self.box[c]
                    if x1 <= bx1 and bx2 <= x2 and y1 <= by1 and by2 <= y2:  # @line L4
                        self._report_subtree(c, out, st)
                    elif bx1 <= x2 and x1 <= bx2 and by1 <= y2 and y1 <= by2:  # @line L5
                        stack.append(c)
        if stats is not None:
            stats.update(st)
        return out

    def check_invariant(self) -> bool:
        """Every node's box is the bounding box of its points, and sizes add up."""
        if self.root < 0:
            return len(self.points) == 0
        stack = [self.root]
        seen = 0
        while stack:
            v = stack.pop()
            if self.leaf_point[v] >= 0:
                p = self.points[self.leaf_point[v]]
                if self.box[v] != (p[0], p[0], p[1], p[1]) or self.size[v] != 1:
                    return False
                seen += 1
                continue
            a, b = self.left[v], self.right[v]
            if self.size[v] != self.size[a] + self.size[b]:
                return False
            if abs(self.size[a] - self.size[b]) > 1:
                return False
            ba, bb = self.box[a], self.box[b]
            want = (min(ba[0], bb[0]), max(ba[1], bb[1]), min(ba[2], bb[2]), max(ba[3], bb[3]))
            if self.box[v] != want:
                return False
            stack.extend((a, b))
        return seen == len(self.points)
