# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/avl-tree/. The authors are listed in prov/195NAP.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    __slots__ = ("key", "left", "right", "h")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.h = 1  # the number of nodes on the longest downward path


def height(t: Node[K] | None) -> int:
    return t.h if t is not None else 0


def update(t: Node[K]) -> None:
    t.h = 1 + max(height(t.left), height(t.right))


def bf(t: Node[K]) -> int:
    """Balance factor: height of the right subtree minus height of the left one."""
    return height(t.right) - height(t.left)


def rotate_left(x: Node[K]) -> Node[K]:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    update(x)
    update(y)
    return y


def rotate_right(y: Node[K]) -> Node[K]:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    update(y)
    update(x)
    return x


def rebalance(t: Node[K]) -> Node[K]:
    update(t)  # @line L6
    if bf(t) == 2:  # @line L7
        assert t.right is not None
        if bf(t.right) < 0:  # @line L8
            t.right = rotate_right(t.right)
        return rotate_left(t)  # @line L9
    if bf(t) == -2:  # @line L10
        assert t.left is not None
        if bf(t.left) > 0:  # @line L11
            t.left = rotate_left(t.left)
        return rotate_right(t)  # @line L12
    return t  # @line L13


def insert(t: Node[K] | None, k: K) -> Node[K]:
    if t is None:  # @line L1
        return Node(k)
    if k < t.key:  # @line L2
        t.left = insert(t.left, k)
    elif t.key < k:  # @line L3
        t.right = insert(t.right, k)
    else:
        return t  # @line L4
    return rebalance(t)  # @line L5


def delete(t: Node[K] | None, k: K) -> Node[K] | None:
    if t is None:  # @line L14
        return None
    if k < t.key:  # @line L15
        t.left = delete(t.left, k)
    elif t.key < k:  # @line L16
        t.right = delete(t.right, k)
    else:  # @line L17
        if t.left is None:  # @line L18
            return t.right
        if t.right is None:  # @line L19
            return t.left
        m = t.right  # @line L20
        while m.left is not None:
            m = m.left
        t.key = m.key  # @line L21
        t.right = delete(t.right, m.key)
    return rebalance(t)  # @line L22


class AVLTree(Generic[K]):
    """An ordered set of keys kept in an AVL tree.

    Each operation takes O(log n) time in the worst case for n keys, and the
    recursion depth is the height, at most about 1.44 lg n. Keys must be
    totally ordered by <; equal keys are stored once.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

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
        """Insert k. Return True if k was not present."""
        if self.contains(k):
            return False
        self.root = insert(self.root, k)
        self.n += 1
        return True

    def delete(self, k: K) -> bool:
        """Delete k. Return True if k was present."""
        if not self.contains(k):
            return False
        self.root = delete(self.root, k)
        self.n -= 1
        return True

    def height(self) -> int:
        return height(self.root)

    def keys(self) -> list[K]:
        out: list[K] = []
        stack: list[Node[K]] = []
        t = self.root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            out.append(t.key)
            t = t.right
        return out

    def __iter__(self) -> Iterator[K]:
        return iter(self.keys())

    def check_invariant(self) -> None:
        """Raise AssertionError unless the tree is an AVL search tree of n keys."""

        def walk(t: Node[K] | None, lo: K | None, hi: K | None) -> tuple[int, int]:
            if t is None:
                return 0, 0
            assert lo is None or lo < t.key
            assert hi is None or t.key < hi
            hl, cl = walk(t.left, lo, t.key)
            hr, cr = walk(t.right, t.key, hi)
            assert t.h == 1 + max(hl, hr), "stored height is wrong"
            assert abs(hr - hl) <= 1, "balance factor out of range"
            return t.h, cl + cr + 1

        _, count = walk(self.root, None, None)
        assert count == self.n
