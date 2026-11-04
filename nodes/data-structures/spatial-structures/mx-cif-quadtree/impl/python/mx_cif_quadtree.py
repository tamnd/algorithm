# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mx-cif-quadtree/. The authors are listed in prov/RHN2XW.jsonl.

from typing import Optional

Rect = tuple[int, int, int, int]  # half-open [x1, x2) x [y1, y2), written (x1, y1, x2, y2)


class Node:
    """A square cell with corner (x, y) and side size.

    rects holds the rectangles whose smallest enclosing cell is this one.
    children[o] is the child for quadrant o = bx + 2*by (0 SW, 1 SE, 2 NW,
    3 NE), or None if no rectangle is stored below it.
    """

    __slots__ = ("x", "y", "size", "rects", "children")

    def __init__(self, x: int, y: int, size: int) -> None:
        self.x, self.y, self.size = x, y, size
        self.rects: list[Rect] = []
        self.children: list[Optional[Node]] = [None, None, None, None]

    def quadrant_of(self, r: Rect) -> int:
        """The quadrant that holds all of r, or -1 if r crosses a center line or the cell has side 1."""
        if self.size == 1:
            return -1
        cx, cy = self.x + self.size // 2, self.y + self.size // 2
        if r[2] <= cx:
            bx = 0
        elif r[0] >= cx:
            bx = 1
        else:
            return -1
        if r[3] <= cy:
            by = 0
        elif r[1] >= cy:
            by = 1
        else:
            return -1
        return bx + 2 * by

    def child_cell(self, o: int) -> "Node":
        h = self.size // 2
        return Node(self.x + (o & 1) * h, self.y + (o >> 1) * h, h)

    def meets(self, q: Rect) -> bool:
        return self.x < q[2] and q[0] < self.x + self.size and self.y < q[3] and q[1] < self.y + self.size


def intersects(a: Rect, b: Rect) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


class MxCifQuadtree:
    """An MX-CIF quadtree of rectangles with integer corners in [0, 2^depth)^2.

    Invariant: each rectangle is stored once, at the smallest cell of the
    quadtree that holds it, which is the first cell on the path from the root
    where it crosses a center line (or a cell of side 1). A node exists only if
    it or a node below it stores a rectangle, so the shape depends only on the
    set of rectangles.
    """

    def __init__(self, depth: int) -> None:
        if depth < 0:
            raise ValueError("need depth >= 0")
        self.depth = depth
        self.root = Node(0, 0, 1 << depth)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _norm(self, r: Rect) -> Rect:
        x1, y1, x2, y2 = (int(v) for v in r)
        side = 1 << self.depth
        if not (0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side):
            raise ValueError("need 0 <= x1 < x2 <= 2^depth and 0 <= y1 < y2 <= 2^depth")
        return x1, y1, x2, y2

    def insert(self, r: Rect) -> bool:
        """Store r. Returns False if it was already stored. O(depth + the list at its node)."""
        r = self._norm(r)
        u = self.root  # @line L1
        o = u.quadrant_of(r)
        while o >= 0:  # @line L2
            if u.children[o] is None:  # @line L3
                u.children[o] = u.child_cell(o)
            u = u.children[o]  # type: ignore[assignment]
            o = u.quadrant_of(r)  # @line L4
        if r in u.rects:
            return False
        u.rects.append(r)  # @line L5
        self.size += 1
        return True

    def window(self, q: Rect) -> list[Rect]:
        """All stored rectangles that meet the half-open window q."""
        q = self._norm(q)
        out: list[Rect] = []
        stack = [self.root]
        while stack:  # @line L6
            u = stack.pop()
            if not u.meets(q):  # @line L7
                continue
            for r in u.rects:  # @line L8
                if intersects(r, q):
                    out.append(r)  # @line L9
            for c in u.children:  # @line L10
                if c is not None:
                    stack.append(c)
        return out

    def stab(self, p: tuple[int, int]) -> list[Rect]:
        """All stored rectangles that hold the point p. Visits one path of the tree."""
        px, py = int(p[0]), int(p[1])
        side = 1 << self.depth
        if not (0 <= px < side and 0 <= py < side):
            raise ValueError("the point is outside the root square")
        out: list[Rect] = []
        u: Optional[Node] = self.root
        while u is not None:
            out.extend(r for r in u.rects if r[0] <= px < r[2] and r[1] <= py < r[3])
            if u.size == 1:
                break
            h = u.size // 2
            u = u.children[(1 if px >= u.x + h else 0) + (2 if py >= u.y + h else 0)]
        return out

    def delete(self, r: Rect) -> bool:
        """Remove r. Returns False if it was not stored. Removes the nodes left empty."""
        r = self._norm(r)
        path: list[tuple[Node, int]] = []
        u = self.root  # @line L11
        o = u.quadrant_of(r)
        while o >= 0:
            c = u.children[o]
            if c is None:
                return False
            path.append((u, o))
            u, o = c, c.quadrant_of(r)
        if r not in u.rects:  # @line L12
            return False
        u.rects.remove(r)
        self.size -= 1
        while path and not u.rects and all(c is None for c in u.children):  # @line L13
            parent, o = path.pop()
            parent.children[o] = None  # @line L14
            u = parent
        return True

    def rects(self) -> list[Rect]:
        out: list[Rect] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            out.extend(u.rects)
            stack.extend(c for c in u.children if c is not None)
        return out

    def node_count(self) -> int:
        n, stack = 0, [self.root]
        while stack:
            u = stack.pop()
            n += 1
            stack.extend(c for c in u.children if c is not None)
        return n

    def check_invariant(self) -> None:
        seen: set[Rect] = set()
        stack = [self.root]
        while stack:
            u = stack.pop()
            for r in u.rects:
                assert r not in seen, "rectangle stored twice"
                seen.add(r)
                assert u.x <= r[0] and r[2] <= u.x + u.size and u.y <= r[1] and r[3] <= u.y + u.size, "outside its cell"
                assert u.quadrant_of(r) < 0, "rectangle fits in a child"
            for o, c in enumerate(u.children):
                if c is None:
                    continue
                e = u.child_cell(o)
                assert u.size > 1 and (c.x, c.y, c.size) == (e.x, e.y, e.size), "child is not a quadrant"
                assert c.rects or any(cc is not None for cc in c.children), "empty node"
                stack.append(c)
        assert len(seen) == self.size, "size is wrong"
