# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/violation-heap/. The authors are listed in prov/HWWSW6.jsonl.

from typing import Any, Dict, Generic, Iterator, List, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node of a violation heap.

    The children of a node are in a doubly linked list, oldest first. last
    points to the last (newest) child. left points to the previous sibling,
    or is None for the first child and for a root. right points to the next
    sibling; for the last child it points to the parent, and for a root it is
    None. There is no parent pointer.
    """

    __slots__ = ("key", "rank", "last", "left", "right")

    def __init__(self, key: K) -> None:
        self.key = key
        self.rank = 0
        self.last: Optional[Node[K]] = None
        self.left: Optional[Node[K]] = None
        self.right: Optional[Node[K]] = None


def _rank(x: "Optional[Node[Any]]") -> int:
    return -1 if x is None else x.rank


def is_root(x: "Node[Any]") -> bool:
    return x.right is None


def parent_if_active(x: "Node[Any]") -> "Optional[Node[Any]]":
    """The parent of x if x is one of the last two children, else None."""
    y = x.right
    if y is None:
        return None
    if y.last is x:
        return y
    if y.right is not None and y.right.last is y:
        return y.right
    return None


def active_children(z: "Node[Any]") -> "tuple[Optional[Node[Any]], Optional[Node[Any]]]":
    a = z.last
    return a, (None if a is None else a.left)


def formula_rank(z: "Node[Any]") -> int:
    """Formula (1) of Elmasry: ceil((r1 + r2) / 2) + 1 over the active children."""
    a, b = active_children(z)
    s = _rank(a) + _rank(b)
    return -((-s) // 2) + 1


class ViolationHeap(Generic[K]):
    """Violation heap of Elmasry (2010): a min-heap with Fibonacci-heap bounds."""

    def __init__(self) -> None:
        self.roots: List[Node[K]] = []
        self.min: Optional[Node[K]] = None
        self.n = 0
        self.joins = 0
        self.rank_steps = 0

    def __len__(self) -> int:
        return self.n

    def _add_root(self, x: Node[K]) -> None:
        x.left = x.right = None
        self.roots.append(x)
        if self.min is None or x.key < self.min.key:
            self.min = x

    def _append_child(self, z: Node[K], c: Node[K]) -> None:
        c.left, c.right = z.last, z
        if z.last is not None:
            z.last.right = c
        z.last = c

    def join3(self, z: Node[K], z1: Node[K], z2: Node[K]) -> Node[K]:
        """3-way join of three roots of equal rank."""
        self.joins += 1
        if z1.key < z.key and not z2.key < z1.key:  # @line L1
            z, z1 = z1, z
        elif z2.key < z.key:
            z, z2 = z2, z
        a, b = active_children(z)  # @line L2
        if a is not None and b is not None and a.rank < b.rank:
            self._swap_last_two(z)
        self._append_child(z, z1)  # @line L3
        self._append_child(z, z2)
        z.rank += 1
        return z

    def _swap_last_two(self, z: Node[K]) -> None:
        a = z.last
        assert a is not None and a.left is not None
        b = a.left
        c = b.left
        a.left, a.right = c, b
        b.left, b.right = a, z
        if c is not None:
            c.right = a
        z.last = b

    def insert(self, key: K) -> Node[K]:
        """Insert key and return its node, the handle for decrease_key."""
        x = Node(key)  # @line L4
        self._add_root(x)
        self.n += 1
        return x

    def meld(self, other: "ViolationHeap[K]") -> None:
        """Move all items of other into this heap."""
        self.roots.extend(other.roots)  # @line L5
        if other.min is not None and (self.min is None or other.min.key < self.min.key):
            self.min = other.min
        self.n += other.n
        self.joins += other.joins
        other.roots, other.min, other.n = [], None, 0

    def find_min(self) -> K:
        if self.min is None:
            raise IndexError("find_min from an empty heap")
        return self.min.key

    def delete_min(self) -> K:
        """Remove and return a smallest key."""
        if self.min is None:
            raise IndexError("delete_min from an empty heap")
        z = self.min  # @line L6
        trees = [r for r in self.roots if r is not z]
        c = z.last
        while c is not None:
            nxt = c.left
            c.left = c.right = None
            trees.append(c)
            c = nxt
        bucket: Dict[int, List[Node[K]]] = {}
        for x in trees:  # @line L7
            while len(bucket.get(x.rank, [])) == 2:
                y1, y2 = bucket.pop(x.rank)
                x = self.join3(x, y1, y2)
            bucket.setdefault(x.rank, []).append(x)  # @line L8
        self.roots, self.min = [], None  # @line L9
        for group in bucket.values():
            for x in group:
                self._add_root(x)
        self.n -= 1
        return z.key

    def _replace(self, x: Node[K], y: Optional[Node[K]]) -> None:
        """Put y in the place of x in its sibling list, or remove x if y is None."""
        l, r = x.left, x.right
        assert r is not None
        if y is None:
            if r.last is x:
                r.last = l
                if l is not None:
                    l.right = r
            else:
                r.left = l
                if l is not None:
                    l.right = r
        else:
            y.left, y.right = l, r
            if l is not None:
                l.right = y
            if r.last is x:
                r.last = y
            else:
                r.left = y
        x.left = x.right = None

    def _detach_child(self, x: Node[K], c: Node[K]) -> None:
        """Remove the child c from the list of x."""
        self._replace(c, None)

    def decrease_key(self, x: Node[K], key: K) -> None:
        """Lower the key of node x to key, which must not be larger."""
        if x.key < key:
            raise ValueError("new key is larger than the current key")
        x.key = key  # @line L10
        if is_root(x):
            if self.min is None or key < self.min.key:
                self.min = x
            return
        p = parent_if_active(x)  # @line L11
        if p is not None and not key < p.key:
            return
        a, b = active_children(x)  # @line L12
        z1 = a if b is None or not a.rank < b.rank else b  # type: ignore[union-attr]
        if z1 is not None:  # @line L13
            self._detach_child(x, z1)
        self._replace(x, z1)
        x.rank = formula_rank(x)  # @line L14
        self._add_root(x)
        while p is not None:  # @line L15
            k = formula_rank(p)
            if k >= p.rank:
                return
            self.rank_steps += 1  # @line L16
            p.rank = k
            p = parent_if_active(p)

    def tree_nodes(self, r: Node[K]) -> Iterator[Node[K]]:
        """All nodes of the tree rooted at r, without recursion."""
        stack = [r]
        while stack:
            v = stack.pop()
            yield v
            c = v.last
            while c is not None:
                stack.append(c)
                c = c.left

    def check_invariant(self) -> None:
        """Check the links, heap order, the rank rule and the size bound."""
        fib = [0, 1]
        while len(fib) < 200:
            fib.append(fib[-1] + fib[-2])
        count = 0
        for r in self.roots:
            assert r.right is None and r.left is None
            assert self.min is not None and not r.key < self.min.key
            order: List[Node[K]] = []
            for v in self.tree_nodes(r):
                order.append(v)
                c, prev = v.last, None
                while c is not None:
                    assert c.right is (v if prev is None else prev)
                    assert not c.key < v.key
                    prev, c = c, c.left
                assert 0 <= v.rank <= formula_rank(v)
            size: Dict[int, int] = {}
            for v in reversed(order):
                s, c = 1, v.last
                while c is not None:
                    s += size[id(c)]
                    c = c.left
                size[id(v)] = s
                assert s >= fib[v.rank + 2]
            count += len(order)
        assert count == self.n
        assert (self.min is None) == (self.n == 0)
