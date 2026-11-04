# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list/. The authors are listed in prov/8R26VK.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """One cell of the list: an item and a pointer to the next node."""

    __slots__ = ("key", "next")

    def __init__(self, key: T, next: "Node[T] | None" = None) -> None:
        self.key = key
        self.next = next


class LinkedList(Generic[T]):
    """A singly linked list with a head pointer and a count.

    push_front, insert_after, delete_front and delete_after cost O(1).
    search costs O(n) and node_at(i) costs O(i + 1). Space: n nodes.
    """

    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def push_front(self, x: T) -> Node[T]:
        """Insert x before the first item and return its node. Cost O(1)."""
        v = Node(x)  # @line L1
        v.next = self.head  # @line L2
        self.head = v  # @line L3
        self.n += 1
        return v

    def insert_after(self, p: Node[T], x: T) -> Node[T]:
        """Insert x just after node p and return its node. Precondition: p is in the list. Cost O(1)."""
        v = Node(x)  # @line L4
        v.next = p.next  # @line L5
        p.next = v  # @line L6
        self.n += 1
        return v

    def delete_front(self) -> T:
        """Remove and return the first item. Precondition: the list is not empty. Cost O(1)."""
        v = self.head  # @line L7
        if v is None:
            raise IndexError("delete from an empty list")
        self.head = v.next  # @line L8
        self.n -= 1
        return v.key  # @line L9

    def delete_after(self, p: Node[T]) -> T:
        """Remove and return the item after node p. Precondition: p.next is a node. Cost O(1)."""
        v = p.next  # @line L10
        if v is None:
            raise IndexError("no node after p")
        p.next = v.next  # @line L11
        self.n -= 1
        return v.key  # @line L12

    def search(self, x: T) -> Node[T] | None:
        """Return the first node with key x, or None. Cost O(n)."""
        p = self.head  # @line S1
        while p is not None and p.key != x:  # @line S2
            p = p.next  # @line S3
        return p  # @line S4

    def node_at(self, i: int) -> Node[T]:
        """Return the node at position i. Precondition: 0 <= i < n. Cost O(i + 1)."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        p = self.head  # @line S5
        for _ in range(i):  # @line S6
            p = p.next  # type: ignore[union-attr]
        return p  # type: ignore[return-value]  # @line S7

    def __iter__(self) -> Iterator[T]:
        p = self.head
        while p is not None:
            yield p.key
            p = p.next

    def check_invariant(self) -> None:
        seen: set[int] = set()
        p = self.head
        while p is not None:
            assert id(p) not in seen, "the chain has a cycle"
            seen.add(id(p))
            p = p.next
        assert len(seen) == self.n
