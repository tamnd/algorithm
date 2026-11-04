# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brodal-queue/. The authors are listed in prov/CZ84MC.jsonl.
"""A simplified, worst-case efficient priority queue in the spirit of Brodal.

This is NOT the full Brodal queue of 1996. It is the skew binomial queue
with a pointer to the minimum root, the structure that Brodal and Okasaki
use as the base of their worst-case queues. It gives, in the worst case:
find_min and insert in O(1); delete_min, delete, decrease_key and meld in
O(log n). The full Brodal queue also has meld and decrease_key in O(1).
"""

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")


class Item(Generic[K, V]):
    __slots__ = ("value", "node")

    def __init__(self, value: V) -> None:
        self.value = value
        self.node: Optional["Node[K, V]"] = None


class Node(Generic[K, V]):
    __slots__ = ("item", "key", "rank", "children", "parent")

    def __init__(self, item: Item[K, V], key: K) -> None:
        self.item = item
        self.key = key
        self.rank = 0
        self.children: list[Node[K, V]] = []
        self.parent: Optional[Node[K, V]] = None
        item.node = self


def _swap(x: Node[K, V], y: Node[K, V]) -> None:
    """Exchange the items and keys of two nodes and fix the handles."""
    x.item, y.item = y.item, x.item
    x.key, y.key = y.key, x.key
    x.item.node = x
    y.item.node = y


def _link(s: Node[K, V], t: Node[K, V]) -> Node[K, V]:
    """Link two roots of the same rank r into one root of rank r + 1."""
    if t.key < s.key:  # @line L1
        s, t = t, s
    s.children.append(t)  # @line L2
    t.parent = s
    s.rank += 1
    return s


class BrodalQueue(Generic[K, V]):
    def __init__(self) -> None:
        self.roots: list[Node[K, V]] = []  # by rank; only roots[0], roots[1] may tie
        self.min: Optional[Node[K, V]] = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def find_min(self) -> tuple[V, K]:
        if self.min is None:
            raise IndexError("find_min from an empty queue")
        return self.min.item.value, self.min.key

    def insert(self, value: V, key: K) -> Item[K, V]:
        e: Item[K, V] = Item(value)
        x = Node(e, key)  # @line L3
        r = self.roots
        if len(r) >= 2 and r[0].rank == r[1].rank:  # @line L4
            was_min = self.min is r[0] or self.min is r[1]
            u = _link(r[0], r[1])  # @line L5
            if was_min:
                self.min = u
            u.children.append(x)  # @line L6
            x.parent = u
            if x.key < u.key:  # @line L7
                _swap(x, u)
            r[0:2] = [u]
            x = u
        else:
            r.insert(0, x)  # @line L8
        if self.min is None or x.key < self.min.key:  # @line L9
            self.min = x
        self.size += 1
        return e

    def _remove_root(self, m: Node[K, V]) -> None:
        self.roots.remove(m)  # @line L11
        trees = self.roots + m.children  # @line L12
        for c in m.children:
            c.parent = None
        m.children = []
        buckets: dict[int, Node[K, V]] = {}
        for t in trees:  # @line L13
            while t.rank in buckets:
                t = _link(t, buckets.pop(t.rank))
            buckets[t.rank] = t
        self.roots = [buckets[k] for k in sorted(buckets)]  # @line L14
        self.min = None
        for t in self.roots:
            if self.min is None or t.key < self.min.key:
                self.min = t
        self.size -= 1

    def delete_min(self) -> tuple[V, K]:
        m = self.min
        if m is None:  # @line L10
            raise IndexError("delete_min from an empty queue")
        e, key = m.item, m.key
        self._remove_root(m)
        e.node = None
        return e.value, key

    def decrease_key(self, e: Item[K, V], k: K) -> None:
        x = e.node
        if x is None:
            raise KeyError("item not in the queue")
        if x.key < k:  # @line L15
            raise ValueError("new key is larger than the current key")
        x.key = k
        while x.parent is not None and x.key < x.parent.key:  # @line L16
            _swap(x, x.parent)
            x = x.parent
        assert self.min is not None
        if x.parent is None and x.key < self.min.key:  # @line L17
            self.min = x

    def delete(self, e: Item[K, V]) -> None:
        x = e.node
        if x is None:
            raise KeyError("item not in the queue")
        while x.parent is not None:  # @line L18
            _swap(x, x.parent)
            x = x.parent
        self._remove_root(x)  # @line L19
        e.node = None

    def meld(self, other: "BrodalQueue[K, V]") -> None:
        trees = self.roots + other.roots  # @line L20
        buckets: dict[int, Node[K, V]] = {}
        for t in trees:
            while t.rank in buckets:
                t = _link(t, buckets.pop(t.rank))
            buckets[t.rank] = t
        self.roots = [buckets[k] for k in sorted(buckets)]
        if other.min is not None and (self.min is None or other.min.key < self.min.key):
            self.min = other.min
        self.size += other.size
        other.roots, other.min, other.size = [], None, 0

    def check_invariant(self) -> None:
        r = self.roots
        assert all(r[i].rank <= r[i + 1].rank for i in range(len(r) - 1))
        assert all(r[i].rank < r[i + 1].rank for i in range(1, len(r) - 1))
        count = 0

        def walk(x: Node[K, V]) -> int:
            assert x.item.node is x
            size = 1
            for c in x.children:
                assert c.parent is x
                assert not c.key < x.key
                assert c.rank < x.rank
                size += walk(c)
            assert size >= 1 << x.rank
            return size

        for t in r:
            assert t.parent is None
            count += walk(t)
        assert count == self.size
        if self.size == 0:
            assert self.min is None
        else:
            assert self.min in r
            assert all(not t.key < self.min.key for t in r)
