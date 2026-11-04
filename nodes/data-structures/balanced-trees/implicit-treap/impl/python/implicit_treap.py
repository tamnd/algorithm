# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-treap/. The authors are listed in prov/47AZT5.jsonl.

from __future__ import annotations

import random
from typing import Iterator


class Node:
    """A treap node keyed by position. size and total describe the subtree;
    rev means that the subtree must still be mirrored (a lazy reversal)."""

    __slots__ = ("value", "prio", "left", "right", "size", "total", "rev")

    def __init__(self, value: int, prio: float) -> None:
        self.value = value
        self.prio = prio
        self.left: Node | None = None
        self.right: Node | None = None
        self.size = 1
        self.total = value
        self.rev = False


def size(t: Node | None) -> int:
    return 0 if t is None else t.size


def total(t: Node | None) -> int:
    return 0 if t is None else t.total


def push(t: Node) -> None:
    """Apply a pending reversal at t and pass it to the children. O(1)."""
    if t.rev:
        t.left, t.right = t.right, t.left
        for c in (t.left, t.right):
            if c is not None:
                c.rev = not c.rev
        t.rev = False


def update(t: Node) -> None:
    """Recompute size and total of t from its children. O(1)."""
    t.size = size(t.left) + size(t.right) + 1
    t.total = total(t.left) + total(t.right) + t.value


def split(t: Node | None, i: int) -> tuple[Node | None, Node | None]:
    """Split t into its first i items and the rest. O(depth)."""
    if t is None:  # @line L1
        return None, None
    push(t)  # @line L2
    if size(t.left) < i:  # @line L3
        a, b = split(t.right, i - size(t.left) - 1)
        t.right = a
        update(t)
        return t, b
    a, b = split(t.left, i)  # @line L4
    t.left = b
    update(t)
    return a, t


def merge(a: Node | None, b: Node | None) -> Node | None:
    """Concatenate a and b (all of a comes first). O(depth)."""
    if a is None or b is None:  # @line L5
        return a if b is None else b
    if a.prio > b.prio:  # @line L6
        push(a)
        a.right = merge(a.right, b)
        update(a)
        return a
    push(b)  # @line L7
    b.left = merge(a, b.left)
    update(b)
    return b


class ImplicitTreap:
    """A list of integers kept as an implicit treap.

    Positions start at 0. insert, delete, get, reverse and range_sum take
    O(log n) expected time; the priorities come from rng (or are given).
    """

    def __init__(self, rng: random.Random | None = None) -> None:
        self.root: Node | None = None
        self.rng = rng if rng is not None else random.Random()

    def __len__(self) -> int:
        return size(self.root)

    def insert(self, i: int, x: int, prio: float | None = None) -> None:
        """Insert x before position i (0 <= i <= n)."""
        if not 0 <= i <= len(self):
            raise IndexError(i)
        p = self.rng.random() if prio is None else prio
        a, b = split(self.root, i)  # @line L8
        self.root = merge(merge(a, Node(x, p)), b)

    def append(self, x: int, prio: float | None = None) -> None:
        self.insert(len(self), x, prio)

    def delete(self, i: int) -> int:
        """Remove and return the item at position i."""
        if not 0 <= i < len(self):
            raise IndexError(i)
        a, b = split(self.root, i)  # @line L9
        m, c = split(b, 1)
        assert m is not None
        self.root = merge(a, c)
        return m.value

    def reverse(self, lo: int, hi: int) -> None:
        """Reverse the items at positions lo .. hi - 1."""
        if not 0 <= lo <= hi <= len(self):
            raise IndexError((lo, hi))
        a, b = split(self.root, lo)  # @line L10
        m, c = split(b, hi - lo)
        if m is not None:
            m.rev = not m.rev  # @line L11
        self.root = merge(a, merge(m, c))

    def range_sum(self, lo: int, hi: int) -> int:
        """Return the sum of the items at positions lo .. hi - 1."""
        if not 0 <= lo <= hi <= len(self):
            raise IndexError((lo, hi))
        a, b = split(self.root, lo)  # @line L12
        m, c = split(b, hi - lo)
        s = total(m)
        self.root = merge(a, merge(m, c))
        return s

    def get(self, i: int) -> int:
        """Return the item at position i, walking down one path."""
        if not 0 <= i < len(self):
            raise IndexError(i)
        t = self.root
        while t is not None:
            push(t)
            s = size(t.left)
            if i < s:
                t = t.left
            elif i > s:
                i -= s + 1
                t = t.right
            else:
                return t.value
        raise AssertionError("unreachable")

    def __iter__(self) -> Iterator[int]:
        stack: list[Node] = []
        t = self.root
        while stack or t is not None:
            while t is not None:
                push(t)
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.value
            t = t.right

    def to_list(self) -> list[int]:
        return list(self)

    def height(self) -> int:
        def h(t: Node | None) -> int:
            return -1 if t is None else 1 + max(h(t.left), h(t.right))
        return h(self.root)

    def check_invariant(self) -> None:
        """Assert the heap order on priorities and the sizes and totals."""
        def go(t: Node | None) -> None:
            if t is None:
                return
            for c in (t.left, t.right):
                assert c is None or c.prio <= t.prio, "heap order"
            assert t.size == size(t.left) + size(t.right) + 1, "size"
            assert t.total == total(t.left) + total(t.right) + t.value, "total"
            go(t.left)
            go(t.right)
        go(self.root)
