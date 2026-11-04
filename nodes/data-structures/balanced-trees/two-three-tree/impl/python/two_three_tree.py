# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-three-tree/. The authors are listed in prov/3W4BM4.jsonl.

from __future__ import annotations

from bisect import bisect_left
from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A 2-node (one key) or a 3-node (two keys).

    A leaf has no children; an internal node has len(keys) + 1 children.
    During an update a node may hold 0 keys (underflow) or 3 keys (overflow)
    for a moment.
    """

    __slots__ = ("keys", "kids")

    def __init__(self, keys: list[K], kids: list[Node[K]] | None = None) -> None:
        self.keys = keys
        self.kids: list[Node[K]] = kids if kids is not None else []

    def is_leaf(self) -> bool:
        return not self.kids


Split = tuple[K, Node[K], Node[K]]


class TwoThreeTree(Generic[K]):
    """An ordered set kept as a 2-3 tree: every internal node has 2 or 3
    children and all leaves are at the same depth.

    Keys must be totally ordered. Search, insertion and deletion cost
    O(log n) time in the worst case; the height is at most lg(n + 1).
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.size = 0

    # search -----------------------------------------------------------
    def contains(self, k: K) -> bool:
        """Return whether k is in the set. O(log n)."""
        t = self.root
        while t is not None:
            i = bisect_left(t.keys, k)
            if i < len(t.keys) and not (k < t.keys[i]):
                return True
            t = t.kids[i] if t.kids else None
        return False

    # insertion --------------------------------------------------------
    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present. O(log n)."""
        if self.root is None:  # @line L1
            self.root = Node([k])
            self.size = 1
            return True
        before = self.size
        r = self._ins(self.root, k)  # @line L2
        if r is not None:  # @line L3
            m, a, b = r
            self.root = Node([m], [a, b])
        return self.size > before

    def _ins(self, t: Node[K], k: K) -> Split[K] | None:
        i = bisect_left(t.keys, k)  # @line L7
        if i < len(t.keys) and not (k < t.keys[i]):  # @line L4
            return None
        if t.is_leaf():  # @line L5
            t.keys.insert(i, k)
            self.size += 1
        else:  # @line L6
            r = self._ins(t.kids[i], k)  # @line L8
            if r is None:  # @line L9
                return None
            m, a, b = r
            t.keys.insert(i, m)  # @line L10
            t.kids[i : i + 1] = [a, b]
        if len(t.keys) == 3:  # @line L11
            x, y, z = t.keys
            if t.is_leaf():  # @line L12
                return (y, Node([x]), Node([z]))
            return (y, Node([x], t.kids[:2]), Node([z], t.kids[2:]))
        return None  # @line L13

    # deletion ---------------------------------------------------------
    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n)."""
        if self.root is None:  # @line L14
            return False
        before = self.size
        self._del(self.root, k)  # @line L15
        if not self.root.keys:  # @line L16
            self.root = self.root.kids[0] if self.root.kids else None
        return self.size < before

    def _del(self, t: Node[K], k: K) -> None:
        i = bisect_left(t.keys, k)
        found = i < len(t.keys) and not (k < t.keys[i])
        if t.is_leaf():  # @line L17
            if found:
                del t.keys[i]
                self.size -= 1
            return
        if found:  # @line L18
            s = t.kids[i + 1]  # @line L19
            while s.kids:
                s = s.kids[0]
            t.keys[i] = s.keys[0]
            k = s.keys[0]
            i += 1
        self._del(t.kids[i], k)  # @line L20
        if not t.kids[i].keys:  # @line L21
            self._fix(t, i)

    def _fix(self, t: Node[K], i: int) -> None:
        c = t.kids[i]
        # prefer the left sibling, else the right one
        if i > 0 and len(t.kids[i - 1].keys) == 2:  # @line L22
            s = t.kids[i - 1]
            c.keys.insert(0, t.keys[i - 1])  # @line L23
            t.keys[i - 1] = s.keys.pop()
            if s.kids:
                c.kids.insert(0, s.kids.pop())
            return
        if i + 1 < len(t.kids) and len(t.kids[i + 1].keys) == 2:
            s = t.kids[i + 1]
            c.keys.append(t.keys[i])
            t.keys[i] = s.keys.pop(0)
            if s.kids:
                c.kids.append(s.kids.pop(0))
            return
        if i > 0:  # @line L24
            s = t.kids[i - 1]
            s.keys.append(t.keys.pop(i - 1))  # @line L25
            s.kids.extend(c.kids)
            del t.kids[i]
        else:
            s = t.kids[1]
            s.keys.insert(0, t.keys.pop(0))
            s.kids[0:0] = c.kids
            del t.kids[0]

    # queries ----------------------------------------------------------
    def keys(self) -> Iterator[K]:
        """Yield the keys in increasing order. O(n)."""

        def walk(t: Node[K]) -> Iterator[K]:
            if t.is_leaf():
                yield from t.keys
                return
            for j, key in enumerate(t.keys):
                yield from walk(t.kids[j])
                yield key
            yield from walk(t.kids[-1])

        if self.root is not None:
            yield from walk(self.root)

    def height(self) -> int:
        """The number of nodes on a root-to-leaf path (0 when empty)."""
        h, t = 0, self.root
        while t is not None:
            h += 1
            t = t.kids[0] if t.kids else None
        return h

    def __len__(self) -> int:
        return self.size

    def check_invariant(self) -> None:
        """Raise AssertionError unless the tree is a valid 2-3 tree."""
        if self.root is None:
            assert self.size == 0
            return
        depths: set[int] = set()
        count = 0

        def walk(t: Node[K], d: int, lo: K | None, hi: K | None) -> None:
            nonlocal count
            assert 1 <= len(t.keys) <= 2, "a node has 1 or 2 keys"
            assert all(t.keys[j] < t.keys[j + 1] for j in range(len(t.keys) - 1))
            for key in t.keys:
                assert lo is None or lo < key
                assert hi is None or key < hi
            count += len(t.keys)
            if t.is_leaf():
                depths.add(d)
                return
            assert len(t.kids) == len(t.keys) + 1, "children = keys + 1"
            bounds = [lo, *t.keys, hi]
            for j, kid in enumerate(t.kids):
                walk(kid, d + 1, bounds[j], bounds[j + 1])

        walk(self.root, 1, None, None)
        assert len(depths) == 1, "all leaves at the same depth"
        assert count == self.size
