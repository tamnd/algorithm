# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-quadtree/. The authors are listed in prov/C2HX1P.jsonl.

from typing import Optional, Sequence

Point = tuple[float, float]


def quadrant(p: Point, q: Point) -> int:
    """The quadrant of q relative to p: 0 SW, 1 SE, 2 NW, 3 NE. O(1).

    East means q.x >= p.x and north means q.y >= p.y.
    """
    return (1 if q[0] >= p[0] else 0) | (2 if q[1] >= p[1] else 0)


class Node:
    __slots__ = ("point", "child")

    def __init__(self, point: Point) -> None:
        self.point = point
        self.child: list[Optional[Node]] = [None, None, None, None]


class PointQuadtree:
    """Finkel and Bentley's point quadtree for a set of points in the plane.

    Each node holds one point, and its four children hold the points of the
    four quadrants around it. Invariant: every point in child[i] of a node
    with point p has quadrant(p, q) == i. Points are stored as a set.
    """

    def __init__(self, points: Sequence[Sequence[float]] = ()) -> None:
        """Build by median splits on x: with distinct x coordinates the height
        is at most floor(lg n) + 1. O(n log n) time with sorting."""
        pts = sorted({(float(p[0]), float(p[1])) for p in points})
        self.size = len(pts)
        self.root: Optional[Node] = None
        # Each task: (points sorted by (x, y), parent, quadrant index).
        stack: list[tuple[list[Point], Optional[Node], int]] = [(pts, None, 0)]
        while stack:
            group, parent, qi = stack.pop()
            if not group:
                continue
            p = group[len(group) // 2]  # the median by x
            t = Node(p)
            if parent is None:
                self.root = t
            else:
                parent.child[qi] = t
            parts: list[list[Point]] = [[], [], [], []]
            for q in group:
                if q != p:
                    parts[quadrant(p, q)].append(q)  # each part stays sorted
            for i in range(4):
                stack.append((parts[i], t, i))

    def __len__(self) -> int:
        return self.size

    def contains(self, q: Sequence[float]) -> bool:
        """Whether q is stored. O(h)."""
        p = (float(q[0]), float(q[1]))
        t = self.root
        while t is not None:
            if t.point == p:
                return True
            t = t.child[quadrant(t.point, p)]
        return False

    def insert(self, q: Sequence[float]) -> bool:
        """Add q as a new leaf; return False if it is already stored. O(h)."""
        p = (float(q[0]), float(q[1]))
        if self.root is None:  # @line L1
            self.root = Node(p)
            self.size = 1
            return True
        t = self.root
        while True:
            if t.point == p:  # @line L2
                return False
            i = quadrant(t.point, p)  # @line L3
            c = t.child[i]
            if c is None:  # @line L4
                t.child[i] = Node(p)
                self.size += 1
                return True
            t = c  # @line L5

    def range_search(self, lo: Sequence[float], hi: Sequence[float]) -> list[Point]:
        """The points p with lo[0] <= p.x <= hi[0] and lo[1] <= p.y <= hi[1]."""
        out: list[Point] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is None:  # @line L6
                continue
            x, y = t.point
            if lo[0] <= x <= hi[0] and lo[1] <= y <= hi[1]:  # @line L7
                out.append(t.point)
            west, east = lo[0] < x, hi[0] >= x  # @line L8
            south, north = lo[1] < y, hi[1] >= y
            if south and west:  # @line L9
                stack.append(t.child[0])
            if south and east:
                stack.append(t.child[1])
            if north and west:
                stack.append(t.child[2])
            if north and east:
                stack.append(t.child[3])
        return out

    def delete(self, q: Sequence[float]) -> bool:
        """Remove q: cut out its node and reinsert the points below it.

        O(s h) time, where s is the size of the subtree of the node.
        """
        p = (float(q[0]), float(q[1]))
        parent: Optional[Node] = None
        pi = 0
        t = self.root
        while t is not None and t.point != p:  # @line L10
            parent, pi = t, quadrant(t.point, p)
            t = t.child[pi]
        if t is None:
            return False
        rest: list[Point] = []  # @line L11
        stack = [c for c in t.child if c is not None]
        while stack:
            u = stack.pop()
            rest.append(u.point)
            stack.extend(c for c in u.child if c is not None)
        if parent is None:  # @line L12
            self.root = None
        else:
            parent.child[pi] = None
        self.size -= 1 + len(rest)
        for r in rest:  # @line L13
            self.insert(r)
        return True

    def points(self) -> list[Point]:
        out: list[Point] = []
        stack = [self.root]
        while stack:
            t = stack.pop()
            if t is not None:
                out.append(t.point)
                stack.extend(t.child)
        return out

    def height(self) -> int:
        best = 0
        stack = [(self.root, 1)]
        while stack:
            t, d = stack.pop()
            if t is not None:
                best = max(best, d)
                stack.extend((c, d + 1) for c in t.child)
        return best

    def check_invariant(self) -> None:
        """Each point lies in the quadrant of each ancestor that its path takes."""
        count = 0
        seen: set[Point] = set()
        stack: list[tuple[Optional[Node], list[tuple[Point, int]]]] = [(self.root, [])]
        while stack:
            t, path = stack.pop()
            if t is None:
                continue
            count += 1
            assert t.point not in seen
            seen.add(t.point)
            for a, i in path:
                assert quadrant(a, t.point) == i and a != t.point
            for i in range(4):
                stack.append((t.child[i], path + [(t.point, i)]))
        assert count == self.size
