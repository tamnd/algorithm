# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-heap/. The authors are listed in prov/E1PH4P.jsonl.

import random
from typing import Any, Generic, Iterator, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


class Coin(Protocol):
    def random(self) -> float: ...


K = TypeVar("K", bound=Ordered)


class Node(Generic[K]):
    """A node: a key and two subtrees. There is no balance field."""

    __slots__ = ("key", "left", "right")

    def __init__(self, key: K) -> None:
        self.key = key
        self.left: Node[K] | None = None
        self.right: Node[K] | None = None


def meld(a: "Node[K] | None", b: "Node[K] | None", coin: Coin) -> "Node[K] | None":
    """Randomized meld of two heap-ordered trees; return the new root.

    This is the recursive MELD of the page as a loop: at each node of the
    path, a fair coin chooses the child that the rest is melded into.
    """
    if a is None:  # @line L1
        return b
    if b is None:
        return a
    if b.key < a.key:  # @line L2
        a, b = b, a
    root = a
    while True:
        go_left = coin.random() < 0.5  # @line L3
        sub = a.left if go_left else a.right
        if sub is not None and b.key < sub.key:
            sub, b = b, sub  # the smaller root continues the path
        if go_left:  # @line L4
            a.left = sub if sub is not None else b
        else:
            a.right = sub if sub is not None else b
        if sub is None:  # MELD(NIL, b) = b
            break
        a = sub
    return root  # @line L5


class RandomizedHeap(Generic[K]):
    """A min-heap with randomized meld (Gambin and Malinowski, 1998)."""

    def __init__(self, coin: Coin | None = None) -> None:
        self.coin: Coin = coin if coin is not None else random.Random()
        self.root: Node[K] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def is_empty(self) -> bool:
        """Return True if the heap holds no item."""
        return self.root is None

    def insert(self, key: K) -> None:
        """Add key to the heap in O(log n) expected time."""
        self.root = meld(self.root, Node(key), self.coin)  # @line L6
        self.n += 1

    def find_min(self) -> K:
        """Return a smallest key; the heap must not be empty."""
        if self.root is None:
            raise IndexError("find_min on an empty heap")
        return self.root.key

    def delete_min(self) -> K:
        """Remove and return a smallest key in O(log n) expected time."""
        r = self.root
        if r is None:
            raise IndexError("delete_min on an empty heap")
        self.root = meld(r.left, r.right, self.coin)  # @line L7
        self.n -= 1
        return r.key  # @line L8

    def meld(self, other: "RandomizedHeap[K]") -> None:
        """Move all items of other into this heap; other becomes empty."""
        self.root = meld(self.root, other.root, self.coin)
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
