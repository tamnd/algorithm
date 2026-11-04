# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/singly-linked-list/. The authors are listed in prov/QXYA7A.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """One node of the list: a key and a link to the next node (None is NIL)."""

    __slots__ = ("key", "next")

    def __init__(self, key: T, nxt: "Node[T] | None" = None) -> None:
        self.key = key
        self.next = nxt


class SinglyLinkedList(Generic[T]):
    """A singly linked list with head and tail pointers and a size count.

    push_front, push_back, pop_front and insert_after cost O(1) in the worst
    case; search and delete cost O(n) in the worst case. Space: n nodes.
    """

    def __init__(self) -> None:
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[T]:
        x = self.head
        while x is not None:
            yield x.key
            x = x.next

    def is_empty(self) -> bool:
        return self.n == 0

    def push_front(self, k: T) -> Node[T]:
        """Add k before the first node and return its node. Cost O(1)."""
        x = Node(k)  # @line L1
        x.next = self.head  # @line L2
        self.head = x  # @line L3
        if self.tail is None:  # @line L4
            self.tail = x
        self.n += 1  # @line L5
        return x

    def push_back(self, k: T) -> Node[T]:
        """Add k after the last node and return its node. Cost O(1)."""
        x = Node(k, None)  # @line L6
        if self.tail is None:  # @line L7
            self.head = x
        else:
            self.tail.next = x  # @line L8
        self.tail = x  # @line L9
        self.n += 1  # @line L10
        return x

    def pop_front(self) -> T:
        """Remove the first node and return its key. Precondition: not empty. Cost O(1)."""
        if self.head is None:
            raise IndexError("pop_front from an empty list")
        x = self.head  # @line L11
        self.head = x.next  # @line L12
        if self.head is None:  # @line L13
            self.tail = None
        self.n -= 1  # @line L14
        x.next = None
        return x.key  # @line L15

    def front(self) -> T:
        """Return the first key. Precondition: not empty. Cost O(1)."""
        if self.head is None:
            raise IndexError("front of an empty list")
        return self.head.key

    def search(self, k: T) -> Node[T] | None:
        """Return the first node with key k, or None. Cost O(n) in the worst case."""
        x = self.head  # @line S1
        while x is not None and x.key != k:  # @line S2
            x = x.next  # @line S3
        return x  # @line S4

    def insert_after(self, y: Node[T], k: T) -> Node[T]:
        """Add k right after the node y, which must be in this list. Cost O(1)."""
        x = Node(k)  # @line A1
        x.next = y.next  # @line A2
        y.next = x  # @line A3
        if self.tail is y:  # @line A4
            self.tail = x
        self.n += 1  # @line A5
        return x

    def delete(self, k: T) -> bool:
        """Remove the first node with key k. Return True if one was found. Cost O(n)."""
        prev: Node[T] | None = None  # @line D1
        x = self.head
        while x is not None and x.key != k:  # @line D2
            prev, x = x, x.next  # @line D3
        if x is None:  # @line D4
            return False
        if prev is None:  # @line D5
            self.head = x.next
        else:
            prev.next = x.next
        if self.tail is x:  # @line D6
            self.tail = prev
        self.n -= 1  # @line D7
        x.next = None
        return True  # @line D8

    def check_invariant(self) -> None:
        """Raise AssertionError unless the representation invariant holds."""
        seen: set[int] = set()
        last: Node[T] | None = None
        x = self.head
        while x is not None:
            assert id(x) not in seen, "the list has a cycle"
            seen.add(id(x))
            last = x
            x = x.next
        assert len(seen) == self.n, "n does not match the number of nodes"
        assert self.tail is last, "tail is not the last node"
