# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavl-tree/. The authors are listed in prov/9VPK2S.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    __slots__ = ("key", "rank", "left", "right", "parent")

    def __init__(self, key: K, parent: Node[K] | None) -> None:
        self.key = key
        self.rank = 0
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.parent = parent


def rank(t: Node[K] | None) -> int:
    """The rank of a node; a missing node has rank -1."""
    return -1 if t is None else t.rank


def is_leaf(t: Node[K]) -> bool:
    return t.left is None and t.right is None


class WAVLTree(Generic[K]):
    """An ordered set kept as a weak AVL tree (Haeupler, Sen and Tarjan).

    Every rank difference is 1 or 2, and every leaf has rank 0. Search,
    insertion and deletion take O(log n) time, and each update does at most
    two rotations.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.n = 0
        self.rotations = 0  # total rotations, for the tests

    def _rotate(self, x: Node[K]) -> None:
        """Rotate x above its parent. O(1)."""
        p = x.parent
        assert p is not None
        g = p.parent
        if x is p.left:
            p.left = x.right
            if x.right is not None:
                x.right.parent = p
            x.right = p
        else:
            p.right = x.left
            if x.left is not None:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g is None:
            self.root = x
        elif g.left is p:
            g.left = x
        else:
            g.right = x
        self.rotations += 1

    def contains(self, k: K) -> bool:
        t = self.root
        while t is not None:
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return True
        return False

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present."""
        p: Node[K] | None = None
        t = self.root
        while t is not None:  # @line L1
            p = t
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return False
        x = Node(k, p)
        self.n += 1
        if p is None:
            self.root = x
            return True
        if k < p.key:
            p.left = x
        else:
            p.right = x
        while p is not None and p.rank == x.rank:  # @line L2
            s = p.right if x is p.left else p.left
            if p.rank - rank(s) == 1:  # @line L3
                p.rank += 1
                x, p = p, p.parent
                continue
            y = x.right if x is p.left else x.left  # inner child of x
            if x.rank - rank(y) == 2:  # @line L4
                self._rotate(x)
                p.rank -= 1
            else:  # @line L5
                assert y is not None
                self._rotate(y)
                self._rotate(y)
                y.rank += 1
                x.rank -= 1
                p.rank -= 1
            break  # @line L6
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent."""
        z = self.root
        while z is not None and (k < z.key or z.key < k):  # @line L7
            z = z.left if k < z.key else z.right
        if z is None:
            return False
        if z.left is not None and z.right is not None:
            s = z.right
            while s.left is not None:
                s = s.left
            z.key = s.key
            z = s
        x = z.left if z.left is not None else z.right
        p = z.parent
        if x is not None:
            x.parent = p
        if p is None:
            self.root = x
        elif p.left is z:
            p.left = x
        else:
            p.right = x
        self.n -= 1
        if p is not None and is_leaf(p) and p.rank == 1:  # @line L8
            p.rank = 0  # a 2,2 leaf
            x, p = p, p.parent
        while p is not None and p.rank - rank(x) == 3:  # @line L9
            x_left = (x is p.left) if x is not None else (p.left is None)
            y = p.right if x_left else p.left
            assert y is not None
            if p.rank - y.rank == 2:  # @line L10
                p.rank -= 1
                x, p = p, p.parent
                continue
            if y.rank - rank(y.left) == 2 and y.rank - rank(y.right) == 2:  # @line L11
                p.rank -= 1
                y.rank -= 1
                x, p = p, p.parent
                continue
            outer = y.right if x_left else y.left
            inner = y.left if x_left else y.right
            if y.rank - rank(outer) == 1:  # @line L12
                self._rotate(y)
                y.rank += 1
                p.rank -= 1
                if is_leaf(p):
                    p.rank -= 1
            else:  # @line L13
                assert inner is not None
                self._rotate(inner)
                self._rotate(inner)
                inner.rank += 2
                y.rank -= 1
                p.rank -= 2
            break  # @line L14
        return True

    def __contains__(self, k: K) -> bool:
        return self.contains(k)

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[K]:
        stack: list[Node[K]] = []
        t = self.root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def keys(self) -> list[K]:
        return list(self)

    def height(self) -> int:
        def h(t: Node[K] | None) -> int:
            return -1 if t is None else 1 + max(h(t.left), h(t.right))
        return h(self.root)

    def check_invariant(self) -> None:
        """Assert order, parent links and the WAVL rank rules."""
        def go(t: Node[K] | None, parent: Node[K] | None) -> int:
            if t is None:
                return 0
            assert t.parent is parent, "parent link"
            for c in (t.left, t.right):
                assert t.rank - rank(c) in (1, 2), "rank difference"
            if is_leaf(t):
                assert t.rank == 0, "leaf rank"
            return 1 + go(t.left, t) + go(t.right, t)
        assert go(self.root, None) == self.n, "count"
        ks = self.keys()
        assert all(a < b for a, b in zip(ks, ks[1:])), "order"
