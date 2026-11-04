# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-heap/. The authors are listed in prov/1EX9SR.jsonl.

from collections.abc import Iterator
from typing import Any, Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)
V = TypeVar("V")


class Node(Generic[K, V]):
    """A node of a Fibonacci heap. The caller keeps it as the handle of its item."""

    __slots__ = ("key", "item", "p", "child", "left", "right", "degree", "mark", "in_heap")

    def __init__(self, key: K, item: V) -> None:
        self.key = key
        self.item = item
        self.p: "Node[K, V] | None" = None
        self.child: "Node[K, V] | None" = None
        self.left: "Node[K, V]" = self
        self.right: "Node[K, V]" = self
        self.degree = 0
        self.mark = False
        self.in_heap = False


def _siblings(x: "Node[K, V]") -> "list[Node[K, V]]":
    """The nodes of the circular list of x, starting at x."""
    out = [x]
    y = x.right
    while y is not x:
        out.append(y)
        y = y.right
    return out


def _splice_before(a: "Node[K, V]", x: "Node[K, V]") -> None:
    """Put the single node x just before a in the circular list of a."""
    x.right = a
    x.left = a.left
    a.left.right = x
    a.left = x


def _unlink(x: "Node[K, V]") -> None:
    """Take x out of its circular list and make it a list of one node."""
    x.left.right = x.right
    x.right.left = x.left
    x.left = x.right = x


class FibonacciHeap(Generic[K, V]):
    """A Fibonacci min-heap (Fredman and Tarjan, 1987).

    insert, find_min, union and decrease_key take O(1) amortized time;
    extract_min and delete take O(log n) amortized time. Node objects are the
    handles for decrease_key and delete. Keys need only "<". All loops are
    iterative, so a long chain of cascading cuts does not use the Python stack.
    """

    def __init__(self) -> None:
        self.min: Node[K, V] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def _add_root(self, x: Node[K, V]) -> None:
        x.p = None
        if self.min is None:
            x.left = x.right = x
            self.min = x
        else:
            _splice_before(self.min, x)

    def insert(self, key: K, item: V = None) -> Node[K, V]:  # type: ignore[assignment]
        """Add an item with the given key and return its node. O(1) time."""
        x: Node[K, V] = Node(key, item)
        x.in_heap = True  # @line L1
        self._add_root(x)  # @line L2
        assert self.min is not None
        if x.key < self.min.key:  # @line L3
            self.min = x
        self.n += 1  # @line L4
        return x

    def find_min(self) -> Node[K, V]:
        """Return the node of a minimum key. Raise IndexError on an empty heap."""
        if self.min is None:
            raise IndexError("heap underflow")
        return self.min

    def union(self, other: "FibonacciHeap[K, V]") -> None:
        """Move all items of other into this heap and empty other. O(1) time."""
        if other.min is not None:  # @line L5
            if self.min is None:
                self.min = other.min
            else:
                a, b = self.min, other.min
                a_last, b_last = a.left, b.left
                a_last.right, b.left = b, a_last
                b_last.right, a.left = a, b_last
                if b.key < a.key:  # @line L6
                    self.min = b
        self.n += other.n  # @line L7
        other.min, other.n = None, 0  # @line L8

    def extract_min(self) -> Node[K, V]:
        """Remove and return the node of a minimum key. O(log n) amortized time."""
        z = self.min  # @line L9
        if z is None:  # @line L10
            raise IndexError("heap underflow")
        if z.child is not None:
            for x in _siblings(z.child):  # @line L11
                _unlink(x)
                self._add_root(x)
            z.child = None
        if z.right is z:  # @line L12
            self.min = None
        else:
            self.min = z.right
            _unlink(z)
        if self.n == 1:  # @line L13
            self.min = None
        else:
            self._consolidate()  # @line L14
        self.n -= 1  # @line L15
        z.in_heap = False
        z.degree, z.mark = 0, False
        return z  # @line L16

    def _consolidate(self) -> None:
        assert self.min is not None
        table: dict[int, Node[K, V]] = {}  # @line L17
        for w in _siblings(self.min):  # @line L18
            x, d = w, w.degree  # @line L19
            while d in table:  # @line L20
                y = table[d]  # @line L21
                if y.key < x.key:  # @line L22
                    x, y = y, x
                self._link(y, x)  # @line L23
                del table[d]  # @line L24
                d += 1
            table[d] = x  # @line L25
        self.min = None  # @line L26
        for d in sorted(table):  # @line L27
            x = table[d]  # @line L28
            _unlink(x)
            self._add_root(x)  # @line L29
            assert self.min is not None
            if x.key < self.min.key:  # @line L30
                self.min = x

    def _link(self, y: Node[K, V], x: Node[K, V]) -> None:
        _unlink(y)  # @line L31
        y.p = x  # @line L32
        if x.child is None:
            x.child = y
        else:
            _splice_before(x.child, y)
        x.degree += 1
        y.mark = False  # @line L33

    def decrease_key(self, x: Node[K, V], key: K) -> None:
        """Lower the key of node x to key. O(1) amortized time."""
        if not x.in_heap:
            raise ValueError("the node is not in the heap")
        if x.key < key:  # @line L34
            raise ValueError("new key is larger than the current key")
        x.key = key  # @line L35
        y = x.p
        if y is not None and x.key < y.key:  # @line L36
            self._cut(x, y)  # @line L37
            self._cascading_cut(y)  # @line L38
        assert self.min is not None
        if x.key < self.min.key:  # @line L39
            self.min = x

    def _cut(self, x: Node[K, V], y: Node[K, V]) -> None:
        if y.child is x:  # @line L40
            y.child = None if x.right is x else x.right
        _unlink(x)
        y.degree -= 1
        self._add_root(x)  # @line L41
        x.mark = False

    def _cascading_cut(self, y: Node[K, V]) -> None:
        while True:
            z = y.p  # @line L42
            if z is None:  # @line L43
                return
            if not y.mark:  # @line L44
                y.mark = True
                return
            self._cut(y, z)  # @line L45
            y = z

    def delete(self, x: Node[K, V]) -> None:
        """Remove node x from the heap. O(log n) amortized time."""
        if not x.in_heap:
            raise ValueError("the node is not in the heap")
        y = x.p  # @line L46: decrease the key of x to minus infinity
        if y is not None:
            self._cut(x, y)
            self._cascading_cut(y)
        self.min = x
        self.extract_min()  # @line L47

    def roots(self) -> list[Node[K, V]]:
        """The roots, in the order of the root list from the minimum."""
        return [] if self.min is None else _siblings(self.min)

    def __iter__(self) -> Iterator[Node[K, V]]:
        stack = self.roots()
        while stack:
            x = stack.pop()
            yield x
            if x.child is not None:
                stack.extend(_siblings(x.child))

    def check_invariant(self) -> None:
        """Check the heap order, the links, the degrees, the count, the minimum and the size bound."""
        count = 0
        fib = [1, 2]
        while len(fib) < 100:
            fib.append(fib[-1] + fib[-2])
        roots = self.roots()
        for r in roots:
            assert r.p is None and r.in_heap and r.right.left is r
            assert self.min is not None and not r.key < self.min.key
        sizes: dict[int, int] = {}
        order: list[Node[K, V]] = []
        stack = list(roots)
        while stack:
            x = stack.pop()
            order.append(x)
            count += 1
            kids = [] if x.child is None else _siblings(x.child)
            assert len(kids) == x.degree
            for c in kids:
                assert c.p is x and c.right.left is c and c.in_heap
                assert not c.key < x.key
            stack.extend(kids)
        for x in reversed(order):
            kids = [] if x.child is None else _siblings(x.child)
            sizes[id(x)] = 1 + sum(sizes[id(c)] for c in kids)
            assert sizes[id(x)] >= fib[x.degree]  # size >= F(degree + 2)
        assert count == self.n
        assert (self.min is None) == (self.n == 0)
