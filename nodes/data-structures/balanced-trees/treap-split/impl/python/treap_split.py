# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap-split/. The authors are listed in prov/WYJ3AW.jsonl.

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


def split(t: Node[K] | None, k: K) -> tuple[Node[K] | None, Node[K] | None]:
    """Split the treap t into (L, R): the keys less than k go to L, the
    keys at least k go to R. Both are treaps. The nodes of t are reused.

    Precondition: t is a treap. Cost O(depth of the search path of k),
    which is O(log n) expected for random priorities.
    """
    if t is None:  # @line L1
        return None, None
    if t.key < k:  # @line L2
        a, b = split(t.right, k)  # @line L3
        t.right = a  # @line L4
        return t, b  # @line L5
    # @line L6
    a, b = split(t.left, k)  # @line L7
    t.left = b  # @line L8
    return a, t  # @line L9
