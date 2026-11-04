# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pairing-heap/. The authors are listed in prov/G7BE09.jsonl.

from typing import Any, Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node of the tree: key, first child, next sibling, and prev.

    prev is the parent when the node is a first child, else the left sibling.
    """

    __slots__ = ("key", "child", "sibling", "prev")

    def __init__(self, key: K) -> None:
        self.key = key
        self.child: Node[K] | None = None
        self.sibling: Node[K] | None = None
        self.prev: Node[K] | None = None


def link(a: "Node[K] | None", b: "Node[K] | None") -> "Node[K] | None":
    """Link two heap-ordered trees whose roots have no siblings; return the new root."""
    if a is None:
        return b
    if b is None:
        return a
    if b.key < a.key:  # @line L2
        a, b = b, a
    b.sibling = a.child  # @line L3
    if a.child is not None:
        a.child.prev = b
    b.prev = a
    a.child = b
    a.sibling = None
    a.prev = None
    return a  # @line L4


class PairingHeap(Generic[K]):
    """A min-oriented pairing heap with handles.

    find_min is O(1). insert and meld do one link, O(1) actual time.
    delete_min does two-pass pairing. All operations take O(log n) amortized
    time; decrease_key takes O(1) actual time.
    """

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def is_empty(self) -> bool:
        return self.root is None

    def find_min(self) -> K:
        if self.root is None:
            raise IndexError("find_min on an empty heap")
        return self.root.key

    def insert(self, key: K) -> Node[K]:
        """Insert key and return its handle."""
        x: Node[K] = Node(key)
        self.root = link(self.root, x)  # @line L5
        self.n += 1
        return x

    def meld(self, other: "PairingHeap[K]") -> None:
        """Move all items of other into self; other becomes empty."""
        if other is self:
            return
        self.root = link(self.root, other.root)  # @line L1
        self.n += other.n
        other.root, other.n = None, 0

    def delete_min(self) -> K:
        """Remove and return a smallest key. O(log n) amortized."""
        r = self.root
        if r is None:
            raise IndexError("delete_min on an empty heap")
        self.root = merge_pairs(r.child)  # @line L6
        if self.root is not None:
            self.root.prev = None
        self.n -= 1
        r.child = None
        return r.key  # @line L7

    def decrease_key(self, x: Node[K], key: K) -> None:
        """Lower the key of the handle x to key. O(1) actual time."""
        if x.key < key:
            raise ValueError("the new key is larger than the old key")
        x.key = key
        if x is self.root:
            return
        cut(x)
        self.root = link(self.root, x)

    def delete(self, x: Node[K]) -> K:
        """Remove the item of the handle x and return its key."""
        if x is self.root:
            return self.delete_min()
        cut(x)
        rest = merge_pairs(x.child)
        x.child = None
        if rest is not None:
            rest.prev = None
        self.root = link(self.root, rest)
        self.n -= 1
        return x.key

    def check_invariant(self) -> None:
        """Check heap order, the prev pointers and the size."""
        count = 0
        if self.root is not None:
            assert self.root.prev is None and self.root.sibling is None
            stack = [self.root]
            while stack:
                v = stack.pop()
                count += 1
                prev = v
                c = v.child
                while c is not None:
                    assert c.prev is prev
                    assert not c.key < v.key
                    stack.append(c)
                    prev = c
                    c = c.sibling
        assert count == self.n

    def keys(self) -> Iterator[K]:
        if self.root is None:
            return
        stack = [self.root]
        while stack:
            v = stack.pop()
            yield v.key
            c = v.child
            while c is not None:
                stack.append(c)
                c = c.sibling


def cut(x: "Node[K]") -> None:
    """Detach the subtree of x (x is not a root) from its parent's child list."""
    p = x.prev
    assert p is not None
    if p.child is x:
        p.child = x.sibling
    else:
        p.sibling = x.sibling
    if x.sibling is not None:
        x.sibling.prev = p
    x.sibling = None
    x.prev = None


def merge_pairs(first: "Node[K] | None") -> "Node[K] | None":
    """Two-pass pairing of the list of trees that starts at first."""
    pairs: list[Node[K]] = []
    x = first
    while x is not None:  # @line L8: first pass, left to right
        a = x
        b = a.sibling
        if b is None:
            a.prev = None
            pairs.append(a)
            break
        x = b.sibling
        a.sibling = b.sibling = None
        a.prev = b.prev = None
        t = link(a, b)  # @line L9
        assert t is not None
        pairs.append(t)
    root: Node[K] | None = None
    for t in reversed(pairs):  # @line L10: second pass, right to left
        root = link(t, root)  # @line L11
    return root  # @line L12
