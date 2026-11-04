# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap-merge/. The authors are listed in prov/J8TN0B.jsonl.

from __future__ import annotations

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


def build(pairs: list[tuple[K, float]]) -> Node[K] | None:
    """Build the treap of distinct (key, priority) pairs.

    Sorts by key and keeps the right spine on a stack, as for a Cartesian
    tree. O(n log n) for the sort, O(n) after it.
    """
    spine: list[Node[K]] = []
    for k, p in sorted(pairs, key=lambda kp: kp[0]):
        x = Node(k, p)
        last: Node[K] | None = None
        while spine and spine[-1].pri < p:
            last = spine.pop()
        x.left = last
        if spine:
            spine[-1].right = x
        spine.append(x)
    return spine[0] if spine else None


def keys(t: Node[K] | None) -> Iterator[K]:
    """Yield the keys of t in increasing order. O(size of t)."""
    stack: list[Node[K]] = []
    while stack or t is not None:
        while t is not None:
            stack.append(t)
            t = t.left
        t = stack.pop()
        yield t.key
        t = t.right


def check_treap(t: Node[K] | None) -> int:
    """Raise AssertionError unless t has search order on keys and max-heap
    order on priorities; return its number of nodes."""
    count = 0
    stack: list[tuple[Node[K], K | None, K | None]] = [(t, None, None)] if t else []
    while stack:
        x, lo, hi = stack.pop()
        count += 1
        assert lo is None or lo < x.key
        assert hi is None or x.key < hi
        if x.left is not None:
            assert x.left.pri <= x.pri
            stack.append((x.left, lo, x.key))
        if x.right is not None:
            assert x.right.pri <= x.pri
            stack.append((x.right, x.key, hi))
    return count


def merge(a: Node[K] | None, b: Node[K] | None) -> Node[K] | None:
    """Merge two treaps into one, when every key of a is less than every
    key of b. The nodes are reused.

    Precondition: a and b are treaps with keys(a) < keys(b). Cost
    O(length of the right spine of a + length of the left spine of b),
    which is O(log n) expected for random priorities.
    """
    if a is None:  # @line L1
        return b
    if b is None:  # @line L2
        return a
    if a.pri > b.pri:  # @line L3
        a.right = merge(a.right, b)  # @line L4
        return a  # @line L5
    b.left = merge(a, b.left)  # @line L6
    return b  # @line L7
