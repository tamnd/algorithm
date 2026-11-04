# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-treap/. The authors are listed in prov/XM4DVE.jsonl.

"""A persistent treap: an ordered set built by split, merge and path copying.

No node is changed after it is made. Each update copies the nodes on
O(log n) expected paths and shares the rest, so every old version stays
valid. Recursion depth equals the tree depth, which is O(log n) expected.
"""

import random
from typing import Iterator, List, Optional, Tuple


class _Node:
    __slots__ = ("key", "prio", "left", "right", "size")

    def __init__(
        self, key: int, prio: float, left: "Optional[_Node]", right: "Optional[_Node]"
    ) -> None:
        self.key = key
        self.prio = prio
        self.left = left
        self.right = right
        self.size = 1 + _size(left) + _size(right)


def _size(t: Optional[_Node]) -> int:
    return 0 if t is None else t.size


def _split(t: Optional[_Node], k: int) -> Tuple[Optional[_Node], Optional[_Node]]:
    """Keys < k and keys >= k. Copies one node per level of one path."""
    if t is None:  # @line L1
        return None, None
    if t.key < k:  # @line L2
        a, b = _split(t.right, k)
        return _Node(t.key, t.prio, t.left, a), b
    a, b = _split(t.left, k)  # @line L3
    return a, _Node(t.key, t.prio, b, t.right)


def _merge(a: Optional[_Node], b: Optional[_Node]) -> Optional[_Node]:
    """Join two treaps; every key of a must be less than every key of b."""
    if a is None:  # @line L4
        return b
    if b is None:  # @line L5
        return a
    if a.prio > b.prio:  # @line L6
        return _Node(a.key, a.prio, a.left, _merge(a.right, b))
    return _Node(b.key, b.prio, _merge(a, b.left), b.right)  # @line L7


def _ins(t: Optional[_Node], k: int, p: float) -> _Node:
    # Called only when k is not in t.
    if t is None or p > t.prio:  # @line L10
        a, b = _split(t, k)
        return _Node(k, p, a, b)
    if k < t.key:  # @line L11
        return _Node(t.key, t.prio, _ins(t.left, k, p), t.right)
    return _Node(t.key, t.prio, t.left, _ins(t.right, k, p))  # @line L12


def _delete(t: Optional[_Node], k: int) -> Optional[_Node]:
    # Called only when k is in t.
    assert t is not None
    if k < t.key:  # @line L15
        return _Node(t.key, t.prio, _delete(t.left, k), t.right)
    if k > t.key:  # @line L16
        return _Node(t.key, t.prio, t.left, _delete(t.right, k))
    return _merge(t.left, t.right)  # @line L17


class PersistentTreap:
    """An immutable ordered set of integers. Every update returns a new set.

    All sets made from one another share one random source for priorities.
    """

    __slots__ = ("_root", "_rng")

    def __init__(self, seed: Optional[int] = None) -> None:
        """The empty set. Cost: O(1)."""
        self._root: Optional[_Node] = None
        self._rng = random.Random(seed)

    def _make(self, root: Optional[_Node]) -> "PersistentTreap":
        t = PersistentTreap.__new__(PersistentTreap)
        t._root = root
        t._rng = self._rng
        return t

    def __len__(self) -> int:
        """Number of keys. Cost: O(1)."""
        return _size(self._root)

    def contains(self, k: int) -> bool:
        """Whether k is in the set. Cost: O(log n) expected."""
        t = self._root
        while t is not None:  # @line L18
            if k == t.key:  # @line L19
                return True
            t = t.left if k < t.key else t.right  # @line L20
        return False  # @line L21

    def insert(self, k: int, prio: Optional[float] = None) -> "PersistentTreap":
        """The set with k added. ``prio`` fixes the priority (for examples).

        Cost: O(log n) expected time and new nodes.
        """
        if self.contains(k):  # @line L8
            return self
        p = self._rng.random() if prio is None else prio
        return self._make(_ins(self._root, k, p))  # @line L9

    def delete(self, k: int) -> "PersistentTreap":
        """The set with k removed. Cost: O(log n) expected time and new nodes."""
        if not self.contains(k):  # @line L13
            return self
        return self._make(_delete(self._root, k))  # @line L14

    def split(self, k: int) -> Tuple["PersistentTreap", "PersistentTreap"]:
        """The keys < k and the keys >= k. Cost: O(log n) expected."""
        a, b = _split(self._root, k)
        return self._make(a), self._make(b)

    def merge(self, other: "PersistentTreap") -> "PersistentTreap":
        """Join with ``other``, whose keys must all be greater.

        Cost: O(log n) expected, n the total size.
        """
        if self._root is not None and other._root is not None:
            if self.max() >= other.min():
                raise ValueError("merge needs every key of self below every key of other")
        return self._make(_merge(self._root, other._root))

    def min(self) -> int:
        """Least key. Cost: O(log n) expected."""
        t = self._root
        if t is None:
            raise ValueError("empty set")
        while t.left is not None:
            t = t.left
        return t.key

    def max(self) -> int:
        """Greatest key. Cost: O(log n) expected."""
        t = self._root
        if t is None:
            raise ValueError("empty set")
        while t.right is not None:
            t = t.right
        return t.key

    def kth(self, i: int) -> int:
        """The key of rank i (0-based). Cost: O(log n) expected."""
        if not 0 <= i < len(self):
            raise IndexError("rank out of range")
        t = self._root
        while t is not None:
            ls = _size(t.left)
            if i < ls:
                t = t.left
            elif i == ls:
                return t.key
            else:
                i -= ls + 1
                t = t.right
        raise AssertionError("unreachable")

    def keys(self) -> List[int]:
        """Keys in increasing order. Cost: Θ(n)."""
        return list(iter(self))

    def __iter__(self) -> Iterator[int]:
        stack: List[_Node] = []
        t = self._root
        while stack or t is not None:
            while t is not None:
                stack.append(t)
                t = t.left
            t = stack.pop()
            yield t.key
            t = t.right

    def height(self) -> int:
        """Number of nodes on the longest root-to-leaf path. Cost: Θ(n)."""
        best = 0
        stack = [(self._root, 1)]
        while stack:
            t, d = stack.pop()
            if t is not None:
                best = max(best, d)
                stack.append((t.left, d + 1))
                stack.append((t.right, d + 1))
        return best

    def check_invariant(self) -> None:
        """Check search order, heap order on priorities, and sizes. Cost: Θ(n)."""
        stack = [(self._root, None, None, float("inf"))]
        while stack:
            t, lo, hi, cap = stack.pop()
            if t is None:
                continue
            assert lo is None or t.key > lo
            assert hi is None or t.key < hi
            assert t.prio <= cap
            assert t.size == 1 + _size(t.left) + _size(t.right)
            stack.append((t.left, lo, t.key, t.prio))
            stack.append((t.right, t.key, hi, t.prio))


def count_nodes(*sets: PersistentTreap) -> int:
    """Distinct nodes reachable from the given sets. Cost: linear in that count."""
    seen = set()
    stack = [s._root for s in sets]
    while stack:
        t = stack.pop()
        if t is not None and id(t) not in seen:
            seen.add(id(t))
            stack.append(t.left)
            stack.append(t.right)
    return len(seen)
