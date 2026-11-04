# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-linked-list/. The authors are listed in prov/N4ZP5Y.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """One cell of the ring: an item and a pointer to the next node."""

    __slots__ = ("key", "next")

    def __init__(self, key: T) -> None:
        self.key = key
        self.next: "Node[T]" = self


class CircularLinkedList(Generic[T]):
    """A singly linked ring with one pointer to the last node.

    push_front, push_back, pop_front and rotate cost O(1) worst case.
    Space: n nodes. pop_front and rotate need a non-empty list.
    """

    def __init__(self) -> None:
        self.last: Node[T] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[T]:
        if self.last is None:
            return
        x = self.last.next
        for _ in range(self.n):
            yield x.key
            x = x.next

    def push_front(self, x: T) -> None:
        """Add x at the front. Cost O(1)."""
        v = Node(x)  # @line L1
        if self.last is None:  # @line L2
            v.next = v
            self.last = v
        else:
            v.next, self.last.next = self.last.next, v  # @line L3
        self.n += 1

    def push_back(self, x: T) -> None:
        """Add x at the back. Cost O(1)."""
        self.push_front(x)  # @line L4
        assert self.last is not None
        self.last = self.last.next  # @line L5

    def pop_front(self) -> T:
        """Remove and return the front item. Cost O(1)."""
        if self.last is None:
            raise IndexError("pop from empty list")
        v = self.last.next  # @line L6
        if v is self.last:  # @line L7
            self.last = None
        else:
            self.last.next = v.next
        self.n -= 1
        return v.key  # @line L8

    def rotate(self) -> None:
        """Move the front item to the back. Cost O(1)."""
        if self.last is None:
            raise IndexError("rotate of empty list")
        self.last = self.last.next  # @line L9

    def front(self) -> T:
        if self.last is None:
            raise IndexError("front of empty list")
        return self.last.next.key

    def check_invariant(self) -> None:
        """Check that the nodes form one ring of n distinct nodes."""
        if self.n == 0:
            assert self.last is None
            return
        assert self.last is not None
        seen = set()
        x = self.last
        for _ in range(self.n):
            x = x.next
            assert id(x) not in seen, "ring shorter than n"
            seen.add(id(x))
        assert x is self.last, "ring longer than n or broken"


def josephus(n: int, k: int) -> list[int]:
    """Return the order in which people 1..n leave when every kth leaves. Cost O(nk)."""
    ring: CircularLinkedList[int] = CircularLinkedList()
    for i in range(1, n + 1):
        ring.push_back(i)
    order = []
    while len(ring) > 0:
        for _ in range(k - 1):
            ring.rotate()
        order.append(ring.pop_front())
    return order
