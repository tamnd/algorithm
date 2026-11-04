# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadtree/. The authors are listed in prov/K3B2RT.jsonl.

import heapq
from typing import Optional

Point = tuple[int, int]


class Node:
    """A cell of the quadtree: the square [x, x + size) x [y, y + size).

    A leaf has children None and holds up to B points in points. An internal
    node has four children, indexed by the quadrant number q = bx + 2*by, where
    bx is 1 for the right half and by is 1 for the upper half.
    count is the number of points in the subtree.
    """

    __slots__ = ("x", "y", "size", "points", "children", "count")

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x, self.y, self.size = x, y, size
        self.points: list[Point] = []
        self.children: Optional[list[Node]] = None
        self.count = 0

    def quadrant(self, p: Point) -> int:
        """The index of the child cell that holds p. O(1)."""
        h = self.size // 2
        return (1 if p[0] >= self.x + h else 0) | (2 if p[1] >= self.y + h else 0)

    def holds(self, p: Point) -> bool:
        return self.x <= p[0] < self.x + self.size and self.y <= p[1] < self.y + self.size

    def dist2(self, q: Point) -> int:
        """Squared Euclidean distance from q to the closed cell. O(1)."""
        dx = max(self.x - q[0], 0, q[0] - (self.x + self.size - 1))
        dy = max(self.y - q[1], 0, q[1] - (self.y + self.size - 1))
        return dx * dx + dy * dy


class QuadTree:
    """A point-region (PR) quadtree with leaf capacity B over [0, 2^depth)^2.

    Points have integer coordinates and are stored as a set. Cells split at
    their centers, so the shape depends only on the set of points.
    Invariant: a leaf holds at most B points, an internal node holds more
    than B points below it, and each point lies in the cell of its leaf.
    The height is at most depth.
    """

    def __init__(self, depth: int, capacity: int = 1) -> None:
        if depth < 0 or capacity < 1:
            raise ValueError("need depth >= 0 and capacity >= 1")
        self.depth = depth
        self.capacity = capacity
        self.root = Node(0, 0, 1 << depth)

    def __len__(self) -> int:
        return self.root.count

    def _check_point(self, p: Point) -> Point:
        q = (int(p[0]), int(p[1]))
        if not self.root.holds(q):
            raise ValueError("the point is outside the root square")
        return q

    def _leaf(self, p: Point) -> tuple[Node, list[Node]]:
        """The leaf whose cell holds p, and the path of nodes above it. O(depth)."""
        u = self.root
        path: list[Node] = []
        while u.children is not None:
            path.append(u)
            u = u.children[u.quadrant(p)]
        return u, path

    def contains(self, p: Point) -> bool:
        """Whether p is stored. O(depth + B)."""
        q = self._check_point(p)
        u, _ = self._leaf(q)
        return q in u.points

    def insert(self, p: Point) -> bool:
        """Add p; return False if it was already there. O(depth * B) worst."""
        q = self._check_point(p)
        u, path = self._leaf(q)  # @line L1
        if q in u.points:
            return False
        for v in path:  # @line L2
            v.count += 1
        u.points.append(q)  # @line L3
        u.count += 1
        B = self.capacity
        while len(u.points) > B:  # @line L4: a cell of side 1 never overflows
            h = u.size // 2
            u.children = [Node(u.x + (k & 1) * h, u.y + (k >> 1) * h, h) for k in range(4)]  # @line L5
            for r in u.points:  # @line L6
                c = u.children[u.quadrant(r)]
                c.points.append(r)
                c.count += 1
            u.points = []
            nxt = None
            for c in u.children:  # @line L7: at most one child can overflow
                if len(c.points) > B:
                    nxt = c
            if nxt is None:
                break
            u = nxt
        return True  # @line L8

    def delete(self, p: Point) -> bool:
        """Remove p; return False if it is not stored. O(depth + B) amortized over merges."""
        q = self._check_point(p)
        u, path = self._leaf(q)  # @line L12
        if q not in u.points:
            return False
        u.points.remove(q)  # @line L13
        u.count -= 1
        for v in path:
            v.count -= 1
        for v in reversed(path):  # @line L14: merge upward while the subtree is small
            if v.count > self.capacity:
                break
            assert v.children is not None
            pts: list[Point] = []
            for c in v.children:
                pts.extend(c.points)  # all children are leaves here
            v.points = pts
            v.children = None
        return True  # @line L15

    def range_search(self, lo: Point, hi: Point) -> list[Point]:
        """The stored points p with lo[i] <= p[i] <= hi[i]; an explicit stack is used."""
        out: list[Point] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            if hi[0] < u.x or lo[0] >= u.x + u.size or hi[1] < u.y or lo[1] >= u.y + u.size:  # @line L9
                continue
            if u.children is None:  # @line L10
                out.extend(p for p in u.points if lo[0] <= p[0] <= hi[0] and lo[1] <= p[1] <= hi[1])
                continue
            stack.extend(u.children)  # @line L11
        return out

    def nearest(self, q: tuple[int, int]) -> Optional[Point]:
        """A stored point closest to q (Euclidean), or None if the tree is empty.

        Best-first search: cells come out of a heap in order of their distance
        to q, so the search stops when the closest cell left is farther than
        the best point found.
        """
        if self.root.count == 0:
            return None
        best: Optional[Point] = None
        best_d = -1
        heap: list[tuple[int, int, Node]] = [(self.root.dist2(q), 0, self.root)]
        tick = 1
        while heap:
            d, _, u = heapq.heappop(heap)  # @line L18
            if best is not None and d >= best_d:  # @line L19
                break
            if u.children is None:  # @line L20
                for p in u.points:
                    dp = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
                    if best is None or dp < best_d:
                        best, best_d = p, dp
            else:
                for c in u.children:  # @line L21
                    if c.count:
                        heapq.heappush(heap, (c.dist2(q), tick, c))
                        tick += 1
        return best

    def points(self) -> list[Point]:
        out: list[Point] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            if u.children is None:
                out.extend(u.points)
            else:
                stack.extend(u.children)
        return out

    def height(self) -> int:
        best = 0
        stack = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            best = max(best, d)
            if u.children is not None:
                stack.extend((c, d + 1) for c in u.children)
        return best

    def node_count(self) -> int:
        n = 0
        stack = [self.root]
        while stack:
            u = stack.pop()
            n += 1
            if u.children is not None:
                stack.extend(u.children)
        return n

    def check_invariant(self) -> None:
        """Raise AssertionError if the structure is broken."""
        seen: set[Point] = set()
        stack = [self.root]
        while stack:
            u = stack.pop()
            if u.children is None:
                assert len(u.points) <= self.capacity
                assert u.count == len(u.points)
                for p in u.points:
                    assert u.holds(p) and p not in seen
                    seen.add(p)
            else:
                assert not u.points and u.size >= 2
                assert u.count > self.capacity
                assert u.count == sum(c.count for c in u.children)
                h = u.size // 2
                for k, c in enumerate(u.children):
                    assert (c.x, c.y, c.size) == (u.x + (k & 1) * h, u.y + (k >> 1) * h, h)
                stack.extend(u.children)
        assert len(seen) == self.root.count
