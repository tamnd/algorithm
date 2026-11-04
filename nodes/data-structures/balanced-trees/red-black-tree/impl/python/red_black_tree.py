# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/red-black-tree/. The authors are listed in prov/WQME6V.jsonl.

from __future__ import annotations

from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)

RED, BLACK = True, False


class Node:
    __slots__ = ("key", "color", "left", "right", "p")

    def __init__(self, key: Any, color: bool, nil: "Node | None") -> None:
        self.key = key
        self.color = color
        self.left: Node = nil if nil is not None else self
        self.right: Node = nil if nil is not None else self
        self.p: Node = nil if nil is not None else self


class RedBlackTree(Generic[K]):
    """An ordered set of keys kept in a red-black tree (CLRS style, with a sentinel).

    contains, insert and delete take O(log n) time in the worst case for n keys.
    An insertion does at most 2 rotations and a deletion at most 3. Keys must be
    totally ordered by <; equal keys are stored once. No recursion is used.
    """

    def __init__(self) -> None:
        self.nil = Node(None, BLACK, None)
        self.root: Node = self.nil
        self.n = 0
        self.rotations = 0

    def __len__(self) -> int:
        return self.n

    # -- rotations ---------------------------------------------------------
    def _left_rotate(self, x: Node) -> None:
        self.rotations += 1
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.p = x
        y.p = x.p
        if x.p is self.nil:
            self.root = y
        elif x is x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def _right_rotate(self, y: Node) -> None:
        self.rotations += 1
        x = y.left
        y.left = x.right
        if x.right is not self.nil:
            x.right.p = y
        x.p = y.p
        if y.p is self.nil:
            self.root = x
        elif y is y.p.left:
            y.p.left = x
        else:
            y.p.right = x
        x.right = y
        y.p = x

    # -- search ------------------------------------------------------------
    def _find(self, k: K) -> Node:
        x = self.root
        while x is not self.nil:
            if k < x.key:
                x = x.left
            elif x.key < k:
                x = x.right
            else:
                return x
        return self.nil

    def contains(self, k: K) -> bool:
        return self._find(k) is not self.nil

    # -- insertion ---------------------------------------------------------
    def insert(self, k: K) -> bool:
        """Insert k. Return True if k was not present."""
        y, x = self.nil, self.root  # @line L1
        while x is not self.nil:  # @line L2
            y = x  # @line L3
            if k < x.key:  # @line L4
                x = x.left
            elif x.key < k:
                x = x.right
            else:
                return False
        z = Node(k, RED, self.nil)  # @line L5
        z.p = y
        if y is self.nil:  # @line L6
            self.root = z
        elif k < y.key:  # @line L7
            y.left = z
        else:
            y.right = z
        self.n += 1
        self._insert_fixup(z)  # @line L8
        return True

    def _insert_fixup(self, z: Node) -> None:
        while z.p.color == RED:  # @line L9
            if z.p is z.p.p.left:  # @line L10
                u = z.p.p.right  # @line L11
                if u.color == RED:  # @line L12
                    z.p.color = BLACK  # @line L13
                    u.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:  # @line L14
                    if z is z.p.right:  # @line L15
                        z = z.p
                        self._left_rotate(z)
                    z.p.color = BLACK  # @line L16
                    z.p.p.color = RED
                    self._right_rotate(z.p.p)  # @line L17
            else:  # @line L18
                u = z.p.p.left
                if u.color == RED:
                    z.p.color = BLACK
                    u.color = BLACK
                    z.p.p.color = RED
                    z = z.p.p
                else:
                    if z is z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p.color = BLACK
                    z.p.p.color = RED
                    self._left_rotate(z.p.p)
        self.root.color = BLACK  # @line L19

    # -- deletion ----------------------------------------------------------
    def _transplant(self, u: Node, v: Node) -> None:
        if u.p is self.nil:
            self.root = v
        elif u is u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p

    def delete(self, k: K) -> bool:
        """Delete k. Return True if k was present."""
        z = self._find(k)
        if z is self.nil:
            return False
        y = z
        y_color = y.color
        if z.left is self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = z.right
            while y.left is not self.nil:
                y = y.left
            y_color = y.color
            x = y.right
            if y is not z.right:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            else:
                x.p = y
            self._transplant(z, y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        self.n -= 1
        if y_color == BLACK:
            self._delete_fixup(x)
        return True

    def _delete_fixup(self, x: Node) -> None:
        while x is not self.root and x.color == BLACK:
            if x is x.p.left:
                w = x.p.right
                if w.color == RED:  # case 1
                    w.color = BLACK
                    x.p.color = RED
                    self._left_rotate(x.p)
                    w = x.p.right
                if w.left.color == BLACK and w.right.color == BLACK:  # case 2
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color == BLACK:  # case 3
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color  # case 4
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color == RED:
                    w.color = BLACK
                    x.p.color = RED
                    self._right_rotate(x.p)
                    w = x.p.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.p)
                    x = self.root
        x.color = BLACK

    # -- inspection --------------------------------------------------------
    def keys(self) -> list[K]:
        out: list[K] = []
        stack: list[Node] = []
        x = self.root
        while stack or x is not self.nil:
            while x is not self.nil:
                stack.append(x)
                x = x.left
            x = stack.pop()
            out.append(x.key)
            x = x.right
        return out

    def height(self) -> int:
        """The number of nodes on the longest path from the root down."""
        best = 0
        stack = [(self.root, 0)]
        while stack:
            x, d = stack.pop()
            if x is self.nil:
                best = max(best, d)
            else:
                stack.append((x.left, d + 1))
                stack.append((x.right, d + 1))
        return best

    def black_height(self) -> int:
        """The number of black nodes below the root on a path to a leaf."""
        bh, x = 0, self.root
        while x is not self.nil:
            x = x.left
            if x.color == BLACK:
                bh += 1
        return bh

    def check_invariant(self) -> None:
        """Raise AssertionError unless the four red-black properties and the order hold."""
        assert self.nil.color == BLACK
        assert self.root.color == BLACK
        assert self.root is self.nil or self.root.p is self.nil
        count = 0
        # iterative post-order: returns the black-height of each subtree
        stack: list[tuple[Node, Any, Any, bool]] = [(self.root, None, None, False)]
        bh: dict[int, int] = {}
        while stack:
            x, lo, hi, done = stack.pop()
            if x is self.nil:
                continue
            if not done:
                assert lo is None or lo < x.key
                assert hi is None or x.key < hi
                if x.color == RED:
                    assert x.left.color == BLACK and x.right.color == BLACK, "red node with a red child"
                for c in (x.left, x.right):
                    assert c is self.nil or c.p is x, "bad parent pointer"
                stack.append((x, lo, hi, True))
                stack.append((x.left, lo, x.key, False))
                stack.append((x.right, x.key, hi, False))
            else:
                count += 1
                sides = []
                for c in (x.left, x.right):
                    b = 0 if c is self.nil else bh[id(c)]
                    sides.append(b + (1 if c.color == BLACK else 0))
                assert sides[0] == sides[1], "unequal black-heights"
                bh[id(x)] = sides[0]
        assert count == self.n
