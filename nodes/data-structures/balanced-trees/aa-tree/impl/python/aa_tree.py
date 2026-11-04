# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aa-tree/. The authors are listed in prov/TPBFGF.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node with its level; nil has level 0."""

    __slots__ = ("key", "left", "right", "level")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.level = 1


def level(t: Node[K] | None) -> int:
    return 0 if t is None else t.level


def skew(t: Node[K] | None) -> Node[K] | None:
    """Remove a horizontal left link at t by a right rotation. O(1)."""
    if t is not None and t.left is not None and t.left.level == t.level:  # @line L1
        l = t.left  # @line L2
        t.left = l.right
        l.right = t
        return l
    return t


def split(t: Node[K] | None) -> Node[K] | None:
    """Remove two horizontal right links in a row at t by a left rotation
    that lifts the middle node one level. O(1)."""
    if (
        t is not None
        and t.right is not None
        and t.right.right is not None
        and t.right.right.level == t.level  # @line L3
    ):
        r = t.right  # @line L4
        t.right = r.left
        r.left = t
        r.level += 1  # @line L5
        return r
    return t


def insert(t: Node[K] | None, k: K) -> Node[K]:
    """Insert k below t (k must be absent) and return the new root. O(log n)."""
    if t is None:  # @line L6
        return Node(k)
    if k < t.key:  # @line L7
        t.left = insert(t.left, k)
    else:
        t.right = insert(t.right, k)
    t = skew(t)  # @line L8
    t = split(t)
    assert t is not None
    return t


def decrease_level(t: Node[K]) -> None:
    """Lower t (and a horizontal right child) to one above its lower child."""
    should = min(level(t.left), level(t.right)) + 1  # @line L16
    if should < t.level:  # @line L17
        t.level = should
        if t.right is not None and should < t.right.level:
            t.right.level = should


def delete(t: Node[K] | None, k: K) -> Node[K] | None:
    """Delete k from below t (k must be present) and return the new root.
    O(log n)."""
    assert t is not None
    if k < t.key:  # @line L9
        t.left = delete(t.left, k)
    elif t.key < k:
        t.right = delete(t.right, k)
    elif t.left is None and t.right is None:  # @line L10
        return None
    elif t.left is None:  # @line L11
        assert t.right is not None
        s = t.right
        while s.left is not None:
            s = s.left
        t.key = s.key
        t.right = delete(t.right, s.key)
    else:  # @line L12
        p = t.left
        while p.right is not None:
            p = p.right
        t.key = p.key
        t.left = delete(t.left, p.key)
    decrease_level(t)  # @line L13
    t = skew(t)  # @line L14
    assert t is not None
    t.right = skew(t.right)
    if t.right is not None:
        t.right.right = skew(t.right.right)
    t = split(t)  # @line L15
    assert t is not None
    t.right = split(t.right)
    return t


class AATree(Generic[K]):
    """An ordered set kept as an AA tree (Andersson 1993).

    Keys must be totally ordered. Search, insertion and deletion cost
    O(log n) time in the worst case; the height is at most 2 lg(n + 1).
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.size = 0

    def contains(self, k: K) -> bool:
        """Return whether k is in the set. O(log n)."""
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
        """Add k; return False if it was already present. O(log n)."""
        if self.contains(k):
            return False
        self.root = insert(self.root, k)
        self.size += 1
        return True

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n)."""
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
        def ht(t: Node[K] | None) -> int:
            return 0 if t is None else 1 + max(ht(t.left), ht(t.right))

        return ht(self.root)

    def __len__(self) -> int:
        return self.size

    def check_invariant(self) -> None:
        """Raise AssertionError unless the tree is a valid AA tree."""
        count = 0

        def walk(t: Node[K] | None, lo: K | None, hi: K | None) -> None:
            nonlocal count
            if t is None:
                return
            count += 1
            assert lo is None or lo < t.key
            assert hi is None or t.key < hi
            if t.left is None and t.right is None:
                assert t.level == 1, "(A1) a leaf has level 1"
            assert level(t.left) == t.level - 1, "(A2) left child one level down"
            assert level(t.right) in (t.level, t.level - 1), "(A3) right child"
            if t.right is not None:
                assert level(t.right.right) < t.level, "(A4) no two horizontal links"
            if t.level > 1:
                assert t.left is not None and t.right is not None, "(A5)"
            walk(t.left, lo, t.key)
            walk(t.right, t.key, hi)

        walk(self.root, None, None)
        assert count == self.size
