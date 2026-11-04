# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leftist-heap/. The authors are listed in prov/Z662CN.jsonl.

from collections import deque
from typing import Any, Generic, Iterable, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node: key, left and right subtrees, and rank s (null path length)."""

    __slots__ = ("key", "left", "right", "s")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None
        self.s = 1


def rank(v: "Node[Any] | None") -> int:
    """The rank s(v): 0 for an empty tree, else the length of the right spine."""
    return 0 if v is None else v.s


def merge(a: "Node[K] | None", b: "Node[K] | None") -> "Node[K] | None":
    """Merge two leftist heaps and return the root.

    This is the recursive MERGE of the page, done with an explicit stack: walk
    down the two right spines, then fix the ranks on the way back up.
    """
    if a is None:  # @line L1
        return b
    if b is None:
        return a
    path: list[Node[K]] = []
    while a is not None and b is not None:
        if b.key < a.key:  # @line L2
            a, b = b, a
        path.append(a)
        a = a.right  # MERGE(a.right, b) continues with this pair
    rest = a if a is not None else b
    for v in reversed(path):
        v.right = rest  # @line L3
        if rank(v.left) < rank(v.right):  # @line L4
            v.left, v.right = v.right, v.left
        v.s = rank(v.right) + 1  # @line L5
        rest = v  # @line L6
    return rest


class LeftistHeap(Generic[K]):
    """A min-heap stored as a leftist tree."""

    def __init__(self, items: Iterable[K] = ()) -> None:
        """Build a heap from items in O(n) time by merging in FIFO order."""
        q: deque[Node[K]] = deque(Node(x) for x in items)
        self.n = len(q)
        while len(q) > 1:
            q.append(merge(q.popleft(), q.popleft()))  # type: ignore[arg-type]
        self.root: Node[K] | None = q[0] if q else None

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

    def meld(self, other: "LeftistHeap[K]") -> None:
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

    def check_invariant(self) -> None:
        """Check heap order, the leftist property, the ranks and the count."""
        count = 0
        order: list[Node[K]] = []
        stack = [self.root] if self.root is not None else []
        while stack:
            v = stack.pop()
            order.append(v)
            count += 1
            for c in (v.left, v.right):
                if c is not None:
                    assert not (c.key < v.key), "heap order"
                    stack.append(c)
        for v in reversed(order):  # children before parents
            assert rank(v.left) >= rank(v.right), "leftist property"
            assert v.s == rank(v.right) + 1, "rank"
        assert count == self.n, "count"
        if self.n > 0:
            assert rank(self.root) <= (self.n + 1).bit_length() - 1, "rank bound"
