# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list-merge-sort/. The authors are listed in prov/NEN2CA.jsonl.

from typing import Generic, Optional, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Node(Generic[T]):
    """A node of a singly linked list."""

    __slots__ = ("key", "next")

    def __init__(self, key: T, next: "Optional[Node[T]]" = None) -> None:
        self.key = key
        self.next = next


def sort_list(head: Optional[Node[T]]) -> tuple[Optional[Node[T]], int]:
    """Sort a singly linked list by relinking its nodes; return the new head and the comparisons.

    Bottom-up merge sort: pass k merges neighbouring sorted runs of w = 2^k
    nodes. It uses O(1) extra space and is stable.
    Cost: at most n * ceil(lg n) comparisons and ceil(lg n) passes.
    """
    if head is None:
        return None, 0
    comparisons = 0
    dummy: Node[T] = Node(head.key)
    w = 1  # @line L1
    while True:  # @line L2
        tail, p, merges = dummy, head, 0  # @line L3
        while p is not None:  # @line L4
            merges += 1  # @line L5
            q, a = p, 0  # @line L6: q goes w nodes past p, a counts them
            while a < w and q is not None:
                q, a = q.next, a + 1
            b = w  # @line L7
            while a > 0 or (b > 0 and q is not None):  # @line L8
                if a > 0 and b > 0 and q is not None:
                    comparisons += 1
                if a == 0 or (b > 0 and q is not None and q.key < p.key):  # @line L9
                    e, q, b = q, q.next, b - 1
                else:  # @line L10
                    e, p, a = p, p.next, a - 1
                tail.next = e  # @line L11
                tail = e
            p = q  # @line L12
        tail.next = None  # @line L13
        if merges <= 1:  # @line L14
            return dummy.next, comparisons
        head, w = dummy.next, 2 * w  # @line L15


def linked_list_merge_sort(a: list[T]) -> int:
    """Sort the list a in place with the linked-list merge sort; return the comparisons."""
    head: Optional[Node[T]] = None
    for x in reversed(a):
        head = Node(x, head)
    head, comparisons = sort_list(head)
    i = 0
    while head is not None:
        a[i] = head.key
        head, i = head.next, i + 1
    return comparisons
