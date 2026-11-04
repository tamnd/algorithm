# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-stack/. The authors are listed in prov/WF0RT5.jsonl.

from __future__ import annotations

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    """One cell of the list. Its fields never change after it is made."""

    __slots__ = ("item", "next", "size")

    def __init__(self, item: T, nxt: _Node[T] | None) -> None:
        self.item = item
        self.next = nxt
        self.size = 1 + (nxt.size if nxt is not None else 0)


class PersistentStack(Generic[T]):
    """An immutable stack. Each update returns a new stack and keeps the old one.

    push, pop, top, is_empty and size take O(1) worst-case time. A push adds one
    node; the new stack shares all nodes of the old one.
    """

    __slots__ = ("_head",)

    def __init__(self, _head: _Node[T] | None = None) -> None:
        self._head = _head

    def push(self, x: T) -> PersistentStack[T]:
        """Return the stack with x on top of self. O(1)."""
        return PersistentStack(_Node(x, self._head))  # @line L1

    def pop(self) -> tuple[T, PersistentStack[T]]:
        """Return (top item, the stack below it). Raise IndexError on the empty stack. O(1)."""
        s = self._head
        if s is None:  # @line L2
            raise IndexError("pop from an empty stack")
        return s.item, PersistentStack(s.next)  # @line L3

    def top(self) -> T:
        """Return the top item. Raise IndexError on the empty stack. O(1)."""
        s = self._head
        if s is None:  # @line L4
            raise IndexError("top of an empty stack")
        return s.item  # @line L5

    def is_empty(self) -> bool:
        """True when the stack has no item. O(1)."""
        return self._head is None

    def size(self) -> int:
        """The number of items. O(1), because each node stores the size of its list."""
        return self._head.size if self._head is not None else 0

    def __iter__(self) -> Iterator[T]:
        """The items from the top down, with a loop (no recursion)."""
        s = self._head
        while s is not None:
            yield s.item
            s = s.next

    def check_invariant(self) -> None:
        """Check that each stored size is 1 plus the size of the next node."""
        s = self._head
        while s is not None:
            assert s.size == 1 + (s.next.size if s.next is not None else 0)
            s = s.next
