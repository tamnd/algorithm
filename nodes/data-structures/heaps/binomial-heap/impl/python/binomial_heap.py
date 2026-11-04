# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binomial-heap/. The authors are listed in prov/A5XZ80.jsonl.

from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")


class Entry(Generic[K, V]):
    """The handle of one item. It stays valid while the item moves between nodes."""

    __slots__ = ("key", "item", "node")

    def __init__(self, key: K, item: V) -> None:
        self.key = key
        self.item = item
        self.node: "BNode[K, V] | None" = None


class BNode(Generic[K, V]):
    __slots__ = ("entry", "p", "children")

    def __init__(self, entry: Entry[K, V]) -> None:
        self.entry = entry
        entry.node = self
        self.p: "BNode[K, V] | None" = None
        # The children in increasing order of degree: the i-th child has degree i.
        self.children: "list[BNode[K, V]]" = []

    @property
    def degree(self) -> int:
        return len(self.children)


def _link(y: BNode[K, V], x: BNode[K, V]) -> None:
    """Make the root y the last child of the root x. Both have the same degree."""
    y.p = x  # @line L1
    x.children.append(y)  # @line L2 @line L3


class BinomialHeap(Generic[K, V]):
    """A binomial min-heap (Vuillemin, 1978).

    The roots are kept in decreasing order of degree, so the root of least
    degree is at the end of the list. insert takes O(1) amortized and
    O(log n) worst-case time; find_min, extract_min, union, decrease_key and
    delete take O(log n) worst-case time. insert returns an Entry, the handle
    for decrease_key and delete. Keys need only "<".
    """

    def __init__(self) -> None:
        self.roots: list[BNode[K, V]] = []
        self.n = 0

    def __len__(self) -> int:
        return self.n

    @staticmethod
    def _union_roots(a: list[BNode[K, V]], b: list[BNode[K, V]]) -> list[BNode[K, V]]:
        table: dict[int, BNode[K, V]] = {}  # @line L4
        for x in a + b:  # @line L5
            d = x.degree  # @line L6
            while d in table:  # @line L7
                y = table.pop(d)  # @line L8
                if y.entry.key < x.entry.key:  # @line L9
                    x, y = y, x
                _link(y, x)  # @line L10
                d += 1
            table[d] = x  # @line L11
        return [table[d] for d in sorted(table, reverse=True)]  # @line L12 @line L13

    def union(self, other: "BinomialHeap[K, V]") -> None:
        """Move all items of other into this heap and empty other. O(log n) time."""
        self.roots = self._union_roots(self.roots, other.roots)
        self.n += other.n
        other.roots, other.n = [], 0

    def insert(self, key: K, item: V = None) -> Entry[K, V]:  # type: ignore[assignment]
        """Add an item and return its handle. O(1) amortized, O(log n) worst case."""
        e: Entry[K, V] = Entry(key, item)
        x = BNode(e)  # @line L14
        while self.roots and self.roots[-1].degree == x.degree:  # @line L15
            y = self.roots.pop()  # @line L16
            if y.entry.key < x.entry.key:  # @line L17
                x, y = y, x
            _link(y, x)  # @line L18
        self.roots.append(x)  # @line L19
        self.n += 1
        return e

    def _min_index(self) -> int:
        if not self.roots:  # @line L20
            raise IndexError("heap underflow")
        best = 0
        for i in range(1, len(self.roots)):  # @line L21
            if self.roots[i].entry.key < self.roots[best].entry.key:
                best = i
        return best

    def find_min(self) -> Entry[K, V]:
        """Return the handle of a minimum item. O(log n) time."""
        return self.roots[self._min_index()].entry

    def extract_min(self) -> Entry[K, V]:
        """Remove and return the handle of a minimum item. O(log n) time."""
        i = self._min_index()  # @line L22
        x = self.roots.pop(i)  # @line L23
        kids = x.children[::-1]  # @line L24: decreasing order of degree
        for c in kids:
            c.p = None
        x.children = []
        self.roots = self._union_roots(self.roots, kids)  # @line L25
        self.n -= 1
        x.entry.node = None
        return x.entry  # @line L26

    def _bubble_up(self, x: BNode[K, V], to_root: bool) -> None:
        while x.p is not None and (to_root or x.entry.key < x.p.entry.key):  # @line L29
            p = x.p
            x.entry, p.entry = p.entry, x.entry  # @line L30
            x.entry.node, p.entry.node = x, p
            x = p  # @line L31

    def decrease_key(self, e: Entry[K, V], key: K) -> None:
        """Lower the key of the item e to key. O(log n) time."""
        if e.node is None:
            raise ValueError("the item is not in the heap")
        if e.key < key:  # @line L27
            raise ValueError("new key is larger than the current key")
        e.key = key  # @line L28
        self._bubble_up(e.node, False)

    def delete(self, e: Entry[K, V]) -> None:
        """Remove the item e. O(log n) time."""
        if e.node is None:
            raise ValueError("the item is not in the heap")
        self._bubble_up(e.node, True)  # @line L32: as a decrease to minus infinity
        x = e.node
        assert x is not None and x.p is None
        i = self.roots.index(x)
        self.roots.pop(i)  # @line L33: extract the root x
        kids = x.children[::-1]
        for c in kids:
            c.p = None
        x.children = []
        self.roots = self._union_roots(self.roots, kids)
        self.n -= 1
        e.node = None

    def check_invariant(self) -> None:
        """Check the binomial shape, the heap order, the handles and the count."""
        count = 0
        degs = [r.degree for r in self.roots]
        assert all(degs[i] > degs[i + 1] for i in range(len(degs) - 1))
        assert sum(1 << d for d in degs) == self.n
        for r in self.roots:
            assert r.p is None
            stack = [r]
            while stack:
                x = stack.pop()
                count += 1
                assert x.entry.node is x
                for i, c in enumerate(x.children):
                    assert c.p is x and c.degree == i
                    assert not c.entry.key < x.entry.key
                    stack.append(c)
        assert count == self.n
