# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skew-heap/. The authors are listed in prov/PY5NQC.jsonl.

from typing import Any, Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node: a key and two subtrees. There is no balance field."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None


def merge(a: "Node[K] | None", b: "Node[K] | None") -> "Node[K] | None":
    """Top-down skew merge of two heap-ordered trees; return the new root.

    Equal to the recursive MERGE of the page, done with a loop, since the length
    of a merge path is bounded only by n.
    """
    if a is None:  # @line L1
        return b
    if b is None:
        return a
    if b.key < a.key:  # @line L2
        a, b = b, a
    root = a
    while True:
        nxt = a.right  # @line L3
        a.right = a.left  # @line L4
        if nxt is None:  # MERGE(NIL, b) = b
            a.left = b  # @line L5
            break
        if b.key < nxt.key:
            nxt, b = b, nxt
        a.left = nxt  # the smaller root of the rest; the merge goes on below it
        a = nxt
    return root  # @line L6


class SkewHeap(Generic[K]):
    """A min-heap stored as a skew heap (Sleator and Tarjan, 1986)."""

    def __init__(self) -> None:
        self.root: Node[K] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def is_empty(self) -> bool:
        """Return True if the heap holds no item."""
        return self.root is None

    def insert(self, key: K) -> None:
        """Add key to the heap."""
        self.root = merge(self.root, Node(key))  # @line L7
        self.n += 1

    def find_min(self) -> K:
        """Return a smallest key; the heap must not be empty."""
        if self.root is None:
            raise IndexError("find_min on an empty heap")
        return self.root.key

    def delete_min(self) -> K:
        """Remove and return a smallest key; the heap must not be empty."""
        r = self.root
        if r is None:
            raise IndexError("delete_min on an empty heap")
        self.root = merge(r.left, r.right)  # @line L8
        self.n -= 1
        return r.key  # @line L9

    def meld(self, other: "SkewHeap[K]") -> None:
        """Move all items of other into this heap; other becomes empty."""
        self.root = merge(self.root, other.root)
        self.n += other.n
        other.root, other.n = None, 0

    def keys(self) -> Iterator[K]:
        """Yield all keys in preorder."""
        stack = [self.root] if self.root is not None else []
        while stack:
            v = stack.pop()
            yield v.key
            for c in (v.right, v.left):
                if c is not None:
                    stack.append(c)

    def heavy_count(self) -> int:
        """The potential of the analysis: nodes whose right subtree is larger than the left."""
        size: dict[int, int] = {}
        order: list[Node[K]] = []
        stack = [self.root] if self.root is not None else []
        while stack:
            v = stack.pop()
            order.append(v)
            stack.extend(c for c in (v.left, v.right) if c is not None)
        heavy = 0
        for v in reversed(order):
            sl = size[id(v.left)] if v.left is not None else 0
            sr = size[id(v.right)] if v.right is not None else 0
            size[id(v)] = sl + sr + 1
            heavy += sr > sl
        return heavy

    def check_invariant(self) -> None:
        """Check heap order and the count."""
        count = 0
        stack = [self.root] if self.root is not None else []
        while stack:
            v = stack.pop()
            count += 1
            for c in (v.left, v.right):
                if c is not None:
                    assert not (c.key < v.key), "heap order"
                    stack.append(c)
        assert count == self.n, "count"
