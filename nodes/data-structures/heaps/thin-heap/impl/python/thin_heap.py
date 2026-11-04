# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thin-heap/. The authors are listed in prov/DBACA1.jsonl.

from typing import Any, Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node of a thin tree.

    child is the first child (the one of highest rank). right is the next
    sibling, or the next root in the root list. left is the previous sibling,
    or the parent if the node is a first child, or None for a root.
    """

    __slots__ = ("key", "rank", "child", "left", "right", "is_root")

    def __init__(self, key: K) -> None:
        self.key = key
        self.rank = 0
        self.child: Optional[Node[K]] = None
        self.left: Optional[Node[K]] = None
        self.right: Optional[Node[K]] = None
        self.is_root = True


def _rank(x: "Optional[Node[Any]]") -> int:
    return -1 if x is None else x.rank


def is_thin(x: "Node[Any]") -> bool:
    """A node is thin if its rank is 2 more than the rank of its first child."""
    return x.rank == _rank(x.child) + 2


class ThinHeap(Generic[K]):
    """Kaplan and Tarjan's thin heap: a min-heap with O(1) amortized decrease-key."""

    def __init__(self) -> None:
        self.head: Optional[Node[K]] = None  # singly linked root list
        self.tail: Optional[Node[K]] = None
        self.min: Optional[Node[K]] = None
        self.n = 0
        self.links = 0

    def __len__(self) -> int:
        return self.n

    def _add_root(self, x: Node[K]) -> None:
        x.is_root, x.left, x.right = True, None, None
        if x.rank != _rank(x.child) + 1:
            x.rank = _rank(x.child) + 1  # a root is never thin
        if self.tail is None:
            self.head = self.tail = x
        else:
            self.tail.right = x
            self.tail = x
        if self.min is None or x.key < self.min.key:
            self.min = x

    def _link(self, x: Node[K], y: Node[K]) -> Node[K]:
        """Link two roots of equal rank; the larger key becomes the first child."""
        self.links += 1
        if y.key < x.key:  # @line L1
            x, y = y, x
        y.is_root, y.left, y.right = False, x, x.child  # @line L2
        if x.child is not None:
            x.child.left = y
        x.child = y
        x.rank += 1
        return x

    def insert(self, key: K) -> Node[K]:
        """Add key and return its node, for decrease_key."""
        x = Node(key)
        self._add_root(x)  # @line L3
        self.n += 1
        return x

    def meld(self, other: "ThinHeap[K]") -> None:
        """Move all items of other into this heap, in O(1) time."""
        if other.head is None:
            return
        if self.tail is None:
            self.head, self.tail, self.min = other.head, other.tail, other.min
        else:
            self.tail.right = other.head
            self.tail = other.tail
            assert other.min is not None and self.min is not None
            if other.min.key < self.min.key:
                self.min = other.min
        self.n += other.n
        other.head = other.tail = other.min = None
        other.n = 0

    def find_min(self) -> K:
        if self.min is None:
            raise IndexError("find_min on an empty heap")
        return self.min.key

    def delete_min(self) -> K:
        """Remove and return a smallest key."""
        z = self.min
        if z is None:
            raise IndexError("delete_min on an empty heap")
        roots: list[Node[K]] = []
        x = self.head
        while x is not None:
            nxt = x.right
            if x is not z:
                roots.append(x)
            x = nxt
        c = z.child  # @line L4
        while c is not None:
            nxt = c.right
            roots.append(c)
            c = nxt
        buckets: dict[int, Node[K]] = {}
        for x in roots:
            x.is_root, x.left, x.right = True, None, None
            x.rank = _rank(x.child) + 1  # a thin child becomes normal
            while x.rank in buckets:  # @line L5
                x = self._link(x, buckets.pop(x.rank))
            buckets[x.rank] = x  # @line L6
        self.head = self.tail = self.min = None
        for r in sorted(buckets):  # @line L7
            self._add_root(buckets[r])
        self.n -= 1
        return z.key

    def decrease_key(self, x: Node[K], key: K) -> None:
        """Lower the key of node x to key, which must not be larger."""
        if x.key < key:
            raise ValueError("new key is larger")
        x.key = key  # @line L8
        if x.is_root:
            if self.min is not None and key < self.min.key:
                self.min = x
            return
        y, parent_case = self._cut(x)  # @line L9
        while True:  # @line L10
            if parent_case:  # @line L11
                if y.is_root:  # @line L12
                    y.rank = _rank(y.child) + 1
                    return
                if y.rank == _rank(y.child) + 2:  # @line L13
                    return  # y was normal and is now thin
                y, parent_case = self._cut(y)  # @line L14
            else:
                if not is_thin(y):  # @line L15
                    w = y.child
                    assert w is not None
                    y.child = w.right
                    if w.right is not None:
                        w.right.left = y
                    w.left, w.right = y, y.right
                    if y.right is not None:
                        y.right.left = w
                    y.right = w
                    return
                y.rank -= 1  # @line L16
                x, y = y, y.left
                assert y is not None
                parent_case = y.child is x

    def _cut(self, x: Node[K]) -> tuple[Node[K], bool]:
        """Cut the subtree of x and make x a root; return the old left neighbor and whether it is the parent."""
        y = x.left
        assert y is not None
        parent_case = y.child is x
        if parent_case:
            y.child = x.right
        else:
            y.right = x.right
        if x.right is not None:
            x.right.left = y
        self._add_root(x)
        return y, parent_case

    def check_invariant(self) -> None:
        """Check heap order, the thin-tree rank rules, the pointers and the rank bound."""
        fib = [1, 1]
        while len(fib) < 100:
            fib.append(fib[-1] + fib[-2])
        count = 0
        best: Optional[Node[K]] = None
        r = self.head
        last = None
        while r is not None:
            assert r.is_root and r.left is None
            assert r.rank == _rank(r.child) + 1, "a root must be normal"
            if best is None or r.key < best.key:
                best = r
            stack = [r]
            while stack:
                v = stack.pop()
                count += 1
                size_of = 0
                assert v.rank in (_rank(v.child) + 1, _rank(v.child) + 2)
                prev, c = v, v.child
                expect = _rank(v.child)
                while c is not None:
                    assert not c.is_root and c.left is prev
                    assert c.rank == expect, "child ranks must be consecutive"
                    assert not (c.key < v.key), "heap order"
                    stack.append(c)
                    expect -= 1
                    prev, c = c, c.right
                    size_of += 1
                assert expect == -1, "the last child must have rank 0"
            last = r
            r = r.right
        assert last is self.tail
        assert count == self.n
        if best is not None:
            assert self.min is not None and not (best.key < self.min.key)
        else:
            assert self.min is None
        for root in self._roots():
            self._check_size(root, fib)

    def _roots(self) -> list[Node[K]]:
        out = []
        r = self.head
        while r is not None:
            out.append(r)
            r = r.right
        return out

    def _check_size(self, root: Node[K], fib: list[int]) -> None:
        """A node of rank k has at least F(k+1) nodes in its subtree."""
        order: list[Node[K]] = []
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            c = v.child
            while c is not None:
                stack.append(c)
                c = c.right
        size: dict[int, int] = {}
        for v in reversed(order):
            s, c = 1, v.child
            while c is not None:
                s += size[id(c)]
                c = c.right
            size[id(v)] = s
            assert s >= fib[v.rank], "rank bound"
