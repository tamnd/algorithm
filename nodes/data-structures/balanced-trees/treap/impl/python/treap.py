# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap/. The authors are listed in prov/S6DS4V.jsonl.

from __future__ import annotations

import random
from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    __slots__ = ("key", "pri", "left", "right")

    def __init__(self, key: K, pri: float) -> None:
        self.key = key
        self.pri = pri
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None


def rotate_right(t: Node[K]) -> Node[K]:
    """Lift t.left above t. O(1)."""
    x = t.left
    assert x is not None
    t.left = x.right
    x.right = t
    return x


def rotate_left(t: Node[K]) -> Node[K]:
    """Lift t.right above t. O(1)."""
    x = t.right
    assert x is not None
    t.right = x.left
    x.left = t
    return x


def insert(t: Node[K] | None, k: K, p: float) -> Node[K]:
    """Insert key k with priority p below t; return the new subtree root.

    Precondition: t is a treap (search order on keys, max-heap order on
    priorities). Cost O(depth of k).
    """
    if t is None:  # @line L1
        return Node(k, p)
    if k < t.key:  # @line L2
        t.left = insert(t.left, k, p)
        if t.left.pri > t.pri:  # @line L3
            t = rotate_right(t)
    elif t.key < k:  # @line L4
        t.right = insert(t.right, k, p)
        if t.right.pri > t.pri:  # @line L5
            t = rotate_left(t)
    return t  # @line L6


def delete(t: Node[K] | None, k: K) -> Node[K] | None:
    """Delete k from the treap t; return the new subtree root.

    The node of k is rotated down, always lifting the child of larger
    priority, until it has at most one child. Cost O(depth of k + the
    lengths of the two spines below it).
    """
    if t is None:  # @line L7
        return None
    if k < t.key:  # @line L8
        t.left = delete(t.left, k)
    elif t.key < k:  # @line L9
        t.right = delete(t.right, k)
    elif t.left is None:  # @line L10
        return t.right
    elif t.right is None:  # @line L11
        return t.left
    elif t.left.pri > t.right.pri:  # @line L12
        t = rotate_right(t)
        t.right = delete(t.right, k)
    else:  # @line L13
        t = rotate_left(t)
        t.left = delete(t.left, k)
    return t  # @line L14


class Treap(Generic[K]):
    """An ordered set kept as a treap with random priorities.

    Keys must be totally ordered. Search, insertion and deletion take
    O(log n) expected time, over the random priorities, for every input.
    """

    def __init__(self, seed: int | None = None) -> None:
        self.root: Node[K] | None = None
        self.size = 0
        self._rng = random.Random(seed)

    def contains(self, k: K) -> bool:
        """Return whether k is in the set. O(log n) expected."""
        t = self.root
        while t is not None:
            if k < t.key:
                t = t.left
            elif t.key < k:
                t = t.right
            else:
                return True
        return False

    def insert(self, k: K, priority: float | None = None) -> bool:
        """Add k; return False if it was present. A priority may be given
        for tests; by default it is drawn uniformly from [0, 1)."""
        if self.contains(k):
            return False
        p = self._rng.random() if priority is None else priority
        self.root = insert(self.root, k, p)
        self.size += 1
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n) expected."""
        if not self.contains(k):
            return False
        self.root = delete(self.root, k)
        self.size -= 1
        return True

    def keys(self) -> Iterator[K]:
        """Yield the keys in increasing order. O(n)."""
        stack: list[Node[K]] = []
        t = self.root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def height(self) -> int:
        """The number of nodes on the longest downward path."""
        best = 0
        stack: list[tuple[Node[K], int]] = [(self.root, 1)] if self.root else []
        while stack:
            t, d = stack.pop()
            best = max(best, d)
            for c in (t.left, t.right):
                if c is not None:
                    stack.append((c, d + 1))
        return best

    def __len__(self) -> int:
        return self.size

    def check_invariant(self) -> None:
        """Raise AssertionError unless keys are in search order and each
        priority is at least the priorities of its children."""
        count = 0
        stack: list[tuple[Node[K], K | None, K | None]] = (
            [(self.root, None, None)] if self.root else []
        )
        while stack:
            t, lo, hi = stack.pop()
            count += 1
            assert lo is None or lo < t.key
            assert hi is None or t.key < hi
            for c in (t.left, t.right):
                if c is not None:
                    assert c.pri <= t.pri, "heap order on priorities"
            if t.left is not None:
                stack.append((t.left, lo, t.key))
            if t.right is not None:
                stack.append((t.right, t.key, hi))
        assert count == self.size
