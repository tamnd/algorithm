# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loose-octree/. The authors are listed in prov/7DA53Q.jsonl.

from typing import Optional

Vec = tuple[int, int, int]
Box = tuple[Vec, Vec]  # closed box [lo, hi] with integer corners, lo <= hi on each axis


class Node:
    """A cell of side size with corner (i*size, j*size, k*size) and looseness 2.

    The loose cell is the cell grown by size/2 on every side, so it has side
    2*size. children[o] is the child for octant o = bx + 2*by + 4*bz, or None.
    """

    __slots__ = ("index", "size", "boxes", "children")

    def __init__(self, index: Vec, size: int) -> None:
        self.index, self.size = index, size
        self.boxes: list[Box] = []
        self.children: list[Optional[Node]] = [None] * 8

    def loose_meets(self, q: Box) -> bool:
        """Whether the closed loose cell meets the closed box q, in doubled coordinates."""
        s = self.size
        for a in range(3):
            lo2 = 2 * self.index[a] * s - s
            hi2 = 2 * (self.index[a] + 1) * s + s
            if 2 * q[1][a] < lo2 or 2 * q[0][a] > hi2:
                return False
        return True

    def loose_holds(self, b: Box) -> bool:
        s = self.size
        for a in range(3):
            if 2 * b[0][a] < 2 * self.index[a] * s - s or 2 * b[1][a] > 2 * (self.index[a] + 1) * s + s:
                return False
        return True


def meets(a: Box, b: Box) -> bool:
    return all(a[0][i] <= b[1][i] and b[0][i] <= a[1][i] for i in range(3))


class LooseOctree:
    """A loose octree with looseness 2 over [0, 2^depth)^3.

    Invariant: a box with largest extent e is stored at the depth whose cell
    side s is the least power of two with s >= max(e, 1), in the cell that holds
    its center. Then the box lies in the loose cell of its node. A node exists
    only if it or a node below it stores a box. The node of a box is found from
    its size and center alone, with no search.
    """

    def __init__(self, depth: int) -> None:
        if depth < 0:
            raise ValueError("need depth >= 0")
        self.depth = depth
        self.root = Node((0, 0, 0), 1 << depth)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _norm(self, b: Box) -> Box:
        lo = tuple(int(v) for v in b[0])
        hi = tuple(int(v) for v in b[1])
        side = 1 << self.depth
        if len(lo) != 3 or len(hi) != 3 or not all(0 <= lo[i] <= hi[i] < side for i in range(3)):
            raise ValueError("need 0 <= lo <= hi < 2^depth on each axis")
        return lo, hi  # type: ignore[return-value]

    def place(self, b: Box) -> tuple[int, Vec]:
        """The depth and cell index of the node of b. O(1) word operations plus a bit length."""
        lo, hi = self._norm(b)
        e = max(hi[i] - lo[i] for i in range(3))  # @line L1
        s = 1
        while s < e:  # @line L2
            s *= 2
        t = self.depth - (s.bit_length() - 1)
        index = tuple((lo[i] + hi[i]) // (2 * s) for i in range(3))  # @line L3
        return t, index  # type: ignore[return-value]

    def _path(self, t: int, index: Vec, create: bool) -> tuple[Optional[Node], list[tuple[Node, int]]]:
        u = self.root
        path: list[tuple[Node, int]] = []
        for d in range(t):  # @line L4
            bit = t - d - 1
            o = ((index[0] >> bit) & 1) | (((index[1] >> bit) & 1) << 1) | (((index[2] >> bit) & 1) << 2)
            c = u.children[o]
            if c is None:
                if not create:
                    return None, path
                h = u.size // 2
                c = Node(tuple(2 * u.index[i] + ((o >> i) & 1) for i in range(3)), h)  # type: ignore[arg-type]
                u.children[o] = c
            path.append((u, o))
            u = c
        return u, path

    def insert(self, b: Box) -> bool:
        """Store b. Returns False if it was stored. O(depth) to make the path."""
        b = self._norm(b)
        t, index = self.place(b)
        u, _ = self._path(t, index, True)
        assert u is not None
        if b in u.boxes:
            return False
        u.boxes.append(b)  # @line L5
        self.size += 1
        return True

    def query(self, q: Box) -> list[Box]:
        """All stored boxes that meet the closed box q."""
        q = self._norm(q)
        out: list[Box] = []
        stack = [self.root]
        while stack:  # @line L6
            u = stack.pop()
            if not u.loose_meets(q):  # @line L7
                continue
            for b in u.boxes:  # @line L8
                if meets(b, q):
                    out.append(b)  # @line L9
            for c in u.children:  # @line L10
                if c is not None:
                    stack.append(c)
        return out

    def delete(self, b: Box) -> bool:
        """Remove b. Returns False if it was not stored. Removes the nodes left empty."""
        b = self._norm(b)
        t, index = self.place(b)
        u, path = self._path(t, index, False)  # @line L11
        if u is None or b not in u.boxes:  # @line L12
            return False
        u.boxes.remove(b)
        self.size -= 1
        while path and not u.boxes and all(c is None for c in u.children):  # @line L13
            parent, o = path.pop()
            parent.children[o] = None  # @line L14
            u = parent
        return True

    def move(self, b: Box, nb: Box) -> bool:
        """Replace b by nb, as when an object moves. Returns False if b was not stored."""
        if not self.delete(b):
            return False
        self.insert(nb)
        return True

    def boxes(self) -> list[Box]:
        out: list[Box] = []
        stack = [self.root]
        while stack:
            u = stack.pop()
            out.extend(u.boxes)
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
        seen: set[Box] = set()
        stack: list[tuple[Node, int]] = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            assert u.size == 1 << (self.depth - d), "wrong side for the depth"
            for b in u.boxes:
                assert b not in seen, "box stored twice"
                seen.add(b)
                assert self.place(b) == (d, u.index), "box at the wrong node"
                assert u.loose_holds(b), "box outside the loose cell"
            for o, c in enumerate(u.children):
                if c is None:
                    continue
                assert c.index == tuple(2 * u.index[i] + ((o >> i) & 1) for i in range(3)), "child is not an octant"
                assert c.boxes or any(cc is not None for cc in c.children), "empty node"
                stack.append((c, d + 1))
        assert len(seen) == self.size, "size is wrong"
