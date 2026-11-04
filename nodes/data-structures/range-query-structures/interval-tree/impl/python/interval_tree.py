# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-tree/. The authors are listed in prov/8H8C9B.jsonl.

import random
from typing import Optional


class _Node:
    __slots__ = ("lo", "hi", "uid", "prio", "left", "right", "max")

    def __init__(self, lo: int, hi: int, uid: int, prio: float) -> None:
        self.lo = lo
        self.hi = hi
        self.uid = uid
        self.prio = prio
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None
        self.max = hi


def _mx(x: Optional[_Node]) -> float:
    return x.max if x is not None else float("-inf")


def _pull(x: _Node) -> _Node:
    x.max = max(x.hi, _mx(x.left), _mx(x.right))
    return x


def _key(x: _Node) -> tuple[int, int, int]:
    return (x.lo, x.hi, x.uid)


def _split(t: Optional[_Node], key: tuple[int, int, int]) -> tuple[Optional[_Node], Optional[_Node]]:
    """Split t into the nodes with key < key and those with key >= key."""
    if t is None:
        return None, None
    if _key(t) < key:
        a, b = _split(t.right, key)
        t.right = a
        return _pull(t), b
    a, b = _split(t.left, key)
    t.left = b
    return a, _pull(t)


def _merge(a: Optional[_Node], b: Optional[_Node]) -> Optional[_Node]:
    """Merge two treaps where all keys of a are below all keys of b."""
    if a is None:
        return b
    if b is None:
        return a
    if a.prio > b.prio:
        a.right = _merge(a.right, b)
        return _pull(a)
    b.left = _merge(a, b.left)
    return _pull(b)


class IntervalTree:
    """A dynamic multiset of closed intervals [lo, hi] in a treap keyed by lo,
    with the largest right end of each subtree in the field max.

    insert, delete and search take O(log n) expected time; report takes
    O((k + 1) log n) expected time for k results. Space O(n).
    """

    def __init__(self, seed: int = 0) -> None:
        self.root: Optional[_Node] = None
        self._rng = random.Random(seed)
        self._next = 0
        self.size = 0

    def insert(self, lo: int, hi: int) -> None:
        """Add the interval [lo, hi]; requires lo <= hi."""
        if lo > hi:
            raise ValueError("lo must be at most hi")
        node = _Node(lo, hi, self._next, self._rng.random())
        self._next += 1
        a, b = _split(self.root, _key(node))
        self.root = _merge(_merge(a, node), b)
        self.size += 1

    def delete(self, lo: int, hi: int) -> bool:
        """Remove one copy of [lo, hi]; return False if there is none."""
        a, rest = _split(self.root, (lo, hi, -1))
        mid, b = _split(rest, (lo, hi + 1, -1))
        found = mid is not None
        if mid is not None:
            # every node of mid holds [lo, hi]; drop its root
            mid = _merge(mid.left, mid.right)
            self.size -= 1
        self.root = _merge(_merge(a, mid), b)
        return found

    def search(self, a: int, b: int) -> Optional[tuple[int, int]]:
        """One stored interval that overlaps [a, b], or None. O(height)."""
        x = self.root  # @line L1
        while x is not None and not (x.lo <= b and a <= x.hi):  # @line L2
            if x.left is not None and x.left.max >= a:  # @line L3
                x = x.left
            else:  # @line L4
                x = x.right
        return (x.lo, x.hi) if x is not None else None  # @line L5

    def report(self, a: int, b: int) -> list[tuple[int, int]]:
        """All stored intervals that overlap [a, b], in order of (lo, hi)."""
        out: list[tuple[int, int]] = []
        stack: list[tuple[Optional[_Node], bool]] = [(self.root, False)]
        while stack:
            x, expanded = stack.pop()
            if x is None:
                continue
            if not expanded:
                if x.max < a:  # @line L6
                    continue
                if x.lo <= b:  # @line L9
                    stack.append((x.right, False))
                stack.append((x, True))
                stack.append((x.left, False))  # @line L7
            elif x.lo <= b and a <= x.hi:  # @line L8
                out.append((x.lo, x.hi))
        return out

    def check_invariant(self) -> None:
        """Check the search order, the heap order of priorities, the max
        fields and the size."""
        count = 0
        stack: list[tuple[Optional[_Node], Optional[tuple[int, int, int]], Optional[tuple[int, int, int]]]] = [
            (self.root, None, None)
        ]
        while stack:
            x, low, high = stack.pop()
            if x is None:
                continue
            count += 1
            k = _key(x)
            assert low is None or low < k, "search order"
            assert high is None or k < high, "search order"
            assert x.lo <= x.hi, "empty interval"
            for c in (x.left, x.right):
                if c is not None:
                    assert c.prio <= x.prio, "heap order"
            assert x.max == max(x.hi, _mx(x.left), _mx(x.right)), "max field"
            stack.append((x.left, low, k))
            stack.append((x.right, k, high))
        assert count == self.size, "size"
