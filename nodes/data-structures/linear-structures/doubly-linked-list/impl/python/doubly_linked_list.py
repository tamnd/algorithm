# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doubly-linked-list/. The authors are listed in prov/B9V487.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """One cell: an item and pointers to the next and previous nodes."""

    __slots__ = ("key", "next", "prev")

    def __init__(self, key: T) -> None:
        self.key = key
        self.next: "Node[T]" = self
        self.prev: "Node[T]" = self


class DoublyLinkedList(Generic[T]):
    """A doubly linked list closed into a ring by one sentinel node.

    insert_after, insert_before, delete and the four end operations cost
    O(1) worst case. search costs O(n). Space: n + 1 nodes.
    Precondition: a node passed as a handle belongs to this list.
    """

    def __init__(self) -> None:
        self.nil: Node[T] = Node(None)  # type: ignore[arg-type]
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[T]:
        x = self.nil.next
        while x is not self.nil:
            yield x.key
            x = x.next

    def insert_after(self, p: Node[T], x: T) -> Node[T]:
        """Insert x after node p (p may be the sentinel). Cost O(1)."""
        v = Node(x)  # @line L1
        v.next, v.prev = p.next, p  # @line L2
        p.next.prev = v  # @line L3
        p.next = v  # @line L4
        self.n += 1
        return v

    def delete(self, v: Node[T]) -> T:
        """Unlink node v, which is not the sentinel, and return its key. Cost O(1)."""
        if v is self.nil:
            raise IndexError("cannot delete the sentinel")
        v.prev.next = v.next  # @line L5
        v.next.prev = v.prev  # @line L6
        self.n -= 1
        return v.key  # @line L7

    def search(self, k: T) -> Node[T] | None:
        """Return the first node with key k, or None. Cost O(n)."""
        x = self.nil.next
        while x is not self.nil and x.key != k:
            x = x.next
        return None if x is self.nil else x

    def insert_before(self, p: Node[T], x: T) -> Node[T]:
        return self.insert_after(p.prev, x)

    def push_front(self, x: T) -> Node[T]:
        return self.insert_after(self.nil, x)

    def push_back(self, x: T) -> Node[T]:
        return self.insert_after(self.nil.prev, x)

    def pop_front(self) -> T:
        if self.n == 0:
            raise IndexError("pop from empty list")
        return self.delete(self.nil.next)

    def pop_back(self) -> T:
        if self.n == 0:
            raise IndexError("pop from empty list")
        return self.delete(self.nil.prev)

    def check_invariant(self) -> None:
        """Check that next and prev form the same ring of n + 1 distinct nodes."""
        seen = {id(self.nil)}
        x = self.nil
        for _ in range(self.n):
            y = x.next
            assert y.prev is x, "prev does not match next"
            assert id(y) not in seen, "node repeated"
            seen.add(id(y))
            x = y
        assert x.next is self.nil and self.nil.prev is x, "ring not closed"
