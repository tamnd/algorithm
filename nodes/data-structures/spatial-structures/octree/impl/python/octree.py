# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree/. The authors are listed in prov/AKGCFN.jsonl.

from typing import Optional

Point = tuple[int, int, int]
Box = tuple[Point, Point]


class Node:
    """A cell of the octree: a cube with corner (x, y, z) and side size.

    A leaf has children None and holds up to B points in points.
    An internal node has eight children, indexed by the octant number
    o = bx + 2*by + 4*bz, where bx is 1 for the upper half in x, and so on.
    count is the number of points in the subtree.
    """

    __slots__ = ("x", "y", "z", "size", "points", "children", "count")

    def __init__(self, x: int, y: int, z: int, size: int) -> None:
        self.x, self.y, self.z, self.size = x, y, z, size
        self.points: list[Point] = []
        self.children: Optional[list[Node]] = None
        self.count = 0

    def octant(self, p: Point) -> int:
        """The index of the child cell that holds p. O(1)."""
        h = self.size // 2
        return (
            (1 if p[0] >= self.x + h else 0)
            | (2 if p[1] >= self.y + h else 0)
            | (4 if p[2] >= self.z + h else 0)
        )

    def holds(self, p: Point) -> bool:
        return (
            self.x <= p[0] < self.x + self.size
            and self.y <= p[1] < self.y + self.size
            and self.z <= p[2] < self.z + self.size
        )


class Octree:
    """A point-region (PR) octree with leaf capacity B over the cube [0, 2^depth)^3.

    Points have integer coordinates and are stored as a set. Cells split at
    their centers, so the shape depends only on the set of points, not on the
    order of insertion. Invariant: a leaf holds at most B points, an internal
    node holds more than B points in its subtree, and each point lies in the
    cell of its leaf. With distinct integer points, a cell of side 1 holds at
    most one point, so the height is at most depth.
    """

    def __init__(self, depth: int, capacity: int = 1) -> None:
        if depth < 0 or capacity < 1:
            raise ValueError("need depth >= 0 and capacity >= 1")
        self.depth = depth
        self.capacity = capacity
        self.root = Node(0, 0, 0, 1 << depth)

    def __len__(self) -> int:
        return self.root.count

    def _check_point(self, p: Point) -> Point:
        q = (int(p[0]), int(p[1]), int(p[2]))
        if not self.root.holds(q):
            raise ValueError("the point is outside the root cube")
        return q

    def _leaf(self, p: Point) -> tuple[Node, list[Node]]:
        """The leaf whose cell holds p, and the path of nodes above it. O(depth)."""
        u = self.root
        path: list[Node] = []
        while u.children is not None:
            path.append(u)
            u = u.children[u.octant(p)]
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
        while len(u.points) > B:  # @line L4: overflow; a cell of side 1 never overflows
            h = u.size // 2
            u.children = [  # @line L5
                Node(u.x + (o & 1) * h, u.y + (o >> 1 & 1) * h, u.z + (o >> 2 & 1) * h, h)
                for o in range(8)
            ]
            for r in u.points:  # @line L6
                c = u.children[u.octant(r)]
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

    def range_search(self, lo: Point, hi: Point) -> list[Point]:
        """The stored points p with lo[i] <= p[i] <= hi[i] for each axis.

        Visits each node whose cell meets the box; an explicit stack is used.
        """
        out: list[Point] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            if (  # @line L9
                hi[0] < u.x or lo[0] >= u.x + u.size
                or hi[1] < u.y or lo[1] >= u.y + u.size
                or hi[2] < u.z or lo[2] >= u.z + u.size
            ):
                continue
            if u.children is None:  # @line L10
                for p in u.points:
                    if all(lo[i] <= p[i] <= hi[i] for i in range(3)):
                        out.append(p)
                continue
            stack.extend(u.children)  # @line L11
        return out

    def delete(self, p: Point) -> bool:
        """Remove p; return False if it is not stored. O(depth + B)."""
        q = self._check_point(p)
        u, path = self._leaf(q)  # @line L12
        if q not in u.points:
            return False
        u.points.remove(q)  # @line L13
        u.count -= 1
        for v in path:
            v.count -= 1
        B = self.capacity
        for v in reversed(path):  # @line L14: merge upward while the subtree is small
            if v.count > B:
                break
            assert v.children is not None
            pts: list[Point] = []
            for c in v.children:
                pts.extend(c.points)  # all children are leaves here
            v.points = pts
            v.children = None
        return True  # @line L15

    def points(self) -> list[Point]:
        """All stored points. O(number of nodes)."""
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
        """The number of levels below the root (0 for a single leaf)."""
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
        """Raise AssertionError if the structure is broken. O(number of nodes)."""
        seen: set[Point] = set()
        stack = [self.root]
        while stack:
            u = stack.pop()
            if u.children is None:
                assert len(u.points) <= self.capacity
                assert u.count == len(u.points)
                for p in u.points:
                    assert u.holds(p)
                    assert p not in seen
                    seen.add(p)
            else:
                assert not u.points and len(u.children) == 8 and u.size >= 2
                h = u.size // 2
                total = 0
                for o, c in enumerate(u.children):
                    assert (c.x, c.y, c.z, c.size) == (
                        u.x + (o & 1) * h, u.y + (o >> 1 & 1) * h, u.z + (o >> 2 & 1) * h, h)
                    total += c.count
                    stack.append(c)
                assert u.count == total
                assert u.count > self.capacity
        assert len(seen) == self.root.count
