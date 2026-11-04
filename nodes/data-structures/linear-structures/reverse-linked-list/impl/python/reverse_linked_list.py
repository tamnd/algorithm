# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reverse-linked-list/. The authors are listed in prov/X89XHB.jsonl.

from typing import Generic, Iterable, TypeVar

T = TypeVar("T")


class Node(Generic[T]):
    """A node of a singly linked list: a value and a pointer to the next node."""

    __slots__ = ("value", "next")

    def __init__(self, value: T, next: "Node[T] | None" = None) -> None:
        self.value = value
        self.next = next


def from_iterable(items: Iterable[T]) -> Node[T] | None:
    """Build a list with the items in order and return its first node, or None."""
    head: Node[T] | None = None
    tail: Node[T] | None = None
    for x in items:
        node = Node(x)
        if tail is None:
            head = node
        else:
            tail.next = node
        tail = node
    return head


def to_list(head: Node[T] | None) -> list[T]:
    """Return the values of the list that starts at head, in order."""
    out: list[T] = []
    while head is not None:
        out.append(head.value)
        head = head.next
    return out


def reverse(head: Node[T] | None) -> Node[T] | None:
    """Reverse the list that starts at head in place and return the new first node.

    Precondition: the list has no cycle. The nodes are reused and the old
    list is destroyed. Cost: Theta(n) time, Theta(1) extra space, n writes.
    """
    prev: Node[T] | None = None  # @line L1
    curr = head  # @line L2
    while curr is not None:  # @line L3
        nxt = curr.next  # @line L4
        curr.next = prev  # @line L5
        prev = curr  # @line L6
        curr = nxt  # @line L7
    return prev  # @line L8
