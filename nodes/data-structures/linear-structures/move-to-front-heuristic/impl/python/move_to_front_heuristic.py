# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front-heuristic/. The authors are listed in prov/ADRSG4.jsonl.

from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)


class _Node(Generic[K]):
    __slots__ = ("key", "next")

    def __init__(self, key: K, nxt: "_Node[K] | None") -> None:
        self.key = key
        self.next = nxt


class MoveToFrontList(Generic[K]):
    """A singly linked list of distinct keys that moves each accessed key to the front.

    access(x) costs Theta(i) time, where i is the 1-based position of x, and
    uses O(1) extra space. Its return value is i, the cost of the request in
    the list update model of Sleator and Tarjan.
    """

    def __init__(self, keys: Iterable[K] = ()) -> None:
        items = list(keys)
        if len(set(items)) != len(items):
            raise ValueError("the keys must be distinct")
        self.head: _Node[K] | None = None
        for key in reversed(items):
            self.head = _Node(key, self.head)

    def access(self, x: K) -> int:
        """Return the 1-based position of x and move x to the front.

        Precondition: x is in the list (else KeyError, and the list is unchanged).
        """
        prev: _Node[K] | None = None
        cur, i = self.head, 1  # @line L1
        while cur is not None and cur.key != x:  # @line L2
            prev, cur, i = cur, cur.next, i + 1  # @line L3
        if cur is None:
            raise KeyError(x)
        if prev is not None:  # @line L4
            prev.next = cur.next  # @line L5
            cur.next = self.head  # @line L6
            self.head = cur  # @line L7
        return i  # @line L8

    def to_list(self) -> list[K]:
        """Return the keys from front to back. Cost Theta(n)."""
        out: list[K] = []
        cur = self.head
        while cur is not None:
            out.append(cur.key)
            cur = cur.next
        return out


def mtf_total_cost(start: Iterable[K], requests: Iterable[K]) -> int:
    """Return the total cost of MTF on the requests from the start list. Cost O(n m)."""
    lst = MoveToFrontList(start)
    return sum(lst.access(x) for x in requests)
