# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-three-four-tree/. The authors are listed in prov/0AZZFQ.jsonl.

from __future__ import annotations

from bisect import bisect_left
from typing import Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A 2-node, 3-node or 4-node: 1, 2 or 3 sorted keys.

    A leaf has no children; an internal node has len(keys) + 1 children.
    """

    __slots__ = ("keys", "kids")

    def __init__(self, keys: list[K], kids: list[Node[K]] | None = None) -> None:
        self.keys = keys
        self.kids: list[Node[K]] = kids if kids is not None else []

    def is_leaf(self) -> bool:
        return not self.kids


class TwoThreeFourTree(Generic[K]):
    """An ordered set kept as a 2-3-4 tree, updated top-down in one pass.

    Every internal node has 2, 3 or 4 children and all leaves are at the
    same depth. Keys must be totally ordered. Search, insertion and
    deletion cost O(log n) time in the worst case and O(1) extra space.
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
    @staticmethod
    def _split_child(t: Node[K], i: int) -> None:
        """Split the 4-node t.kids[i]; t must not be a 4-node. O(1)."""
        c = t.kids[i]  # @line L10
        a = Node(c.keys[:1], c.kids[:2])
        b = Node(c.keys[2:], c.kids[2:])
        t.keys.insert(i, c.keys[1])  # @line L11
        t.kids[i : i + 1] = [a, b]

    def insert(self, k: K) -> bool:
        """Add k; return False if it was already present. O(log n)."""
        if self.root is None:  # @line L1
            self.root = Node([k])
            self.size = 1
            return True
        if len(self.root.keys) == 3:  # @line L2
            self.root = Node([], [self.root])
            self._split_child(self.root, 0)
        t = self.root  # @line L3
        while True:  # @line L4
            i = bisect_left(t.keys, k)  # @line L5
            if i < len(t.keys) and not (k < t.keys[i]):  # @line L6
                return False
            if t.is_leaf():  # @line L7
                t.keys.insert(i, k)
                self.size += 1
                return True
            if len(t.kids[i].keys) == 3:  # @line L8
                self._split_child(t, i)
                if not (k < t.keys[i]) and not (t.keys[i] < k):
                    return False
                if t.keys[i] < k:
                    i += 1
            t = t.kids[i]  # @line L9

    # deletion ---------------------------------------------------------
    @staticmethod
    def _merge(t: Node[K], i: int) -> None:
        """Merge t.kids[i], t.keys[i] and t.kids[i + 1] into one 4-node.

        Both children must be 2-nodes. O(1).
        """
        a, b = t.kids[i], t.kids[i + 1]  # @line L26
        a.keys = a.keys + [t.keys.pop(i)] + b.keys
        a.kids = a.kids + b.kids
        del t.kids[i + 1]

    def _fill(self, t: Node[K], i: int) -> int:
        """Make the 2-node t.kids[i] a 3-node or 4-node; return the index of
        the child that now holds its keys. O(1)."""
        c = t.kids[i]
        if i > 0 and len(t.kids[i - 1].keys) >= 2:  # @line L23
            s = t.kids[i - 1]
            c.keys.insert(0, t.keys[i - 1])
            t.keys[i - 1] = s.keys.pop()
            if s.kids:
                c.kids.insert(0, s.kids.pop())
            return i
        if i + 1 < len(t.kids) and len(t.kids[i + 1].keys) >= 2:  # @line L24
            s = t.kids[i + 1]
            c.keys.append(t.keys[i])
            t.keys[i] = s.keys.pop(0)
            if s.kids:
                c.kids.append(s.kids.pop(0))
            return i
        if i + 1 < len(t.kids):  # @line L25
            self._merge(t, i)
            return i
        self._merge(t, i - 1)
        return i - 1

    def delete(self, k: K) -> bool:
        """Remove k; return False if it was absent. O(log n)."""
        if self.root is None:
            return False
        found_any = False
        t = self.root  # @line L12
        while True:  # @line L13
            i = bisect_left(t.keys, k)  # @line L14
            if t.is_leaf():  # @line L15
                if i < len(t.keys) and not (k < t.keys[i]):
                    del t.keys[i]
                    found_any = True
                break
            if i < len(t.keys) and not (k < t.keys[i]):  # @line L16
                if len(t.kids[i].keys) >= 2:  # @line L17
                    p = t.kids[i]
                    while p.kids:
                        p = p.kids[-1]
                    k = t.keys[i] = p.keys[-1]
                    t = t.kids[i]
                elif len(t.kids[i + 1].keys) >= 2:  # @line L18
                    s = t.kids[i + 1]
                    while s.kids:
                        s = s.kids[0]
                    k = t.keys[i] = s.keys[0]
                    t = t.kids[i + 1]
                else:  # @line L19
                    self._merge(t, i)
                    t = t.kids[i]
                continue
            if len(t.kids[i].keys) == 1:  # @line L20
                i = self._fill(t, i)
            t = t.kids[i]  # @line L21
        if not self.root.keys:  # @line L22
            self.root = self.root.kids[0] if self.root.kids else None
        if found_any:
            self.size -= 1
        return found_any

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
        """Raise AssertionError unless the tree is a valid 2-3-4 tree."""
        if self.root is None:
            assert self.size == 0
            return
        depths: set[int] = set()
        count = 0

        def walk(t: Node[K], d: int, lo: K | None, hi: K | None) -> None:
            nonlocal count
            assert 1 <= len(t.keys) <= 3, "a node has 1, 2 or 3 keys"
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
