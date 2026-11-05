# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eytzinger-layout/. The authors are listed in prov/Q8TG36.jsonl.

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class Eytzinger(Generic[T]):
    """A sorted array stored in breadth-first order of its implicit search tree.

    Slot k (1-based) has children 2k and 2k + 1; slot 0 is unused. The
    in-order traversal of the slots gives the sorted order. The array
    rank[k] holds the sorted index of the item in slot k.
    """

    def __init__(self, items: Sequence[T]) -> None:
        self.n = len(items)
        self.b: list[T | None] = [None] * (self.n + 1)
        self.rank = [0] * (self.n + 1)
        self._fill(items)  # @line L3

    def _fill(self, a: Sequence[T]) -> None:
        """Copy the sorted items into the slots in in-order. O(n)."""
        n = self.n
        i = 0  # @line L1
        stack: list[int] = []
        k = 1  # @line L2
        while stack or k <= n:
            if k <= n:  # @line L4
                stack.append(k)
                k = 2 * k  # @line L5
            else:
                k = stack.pop()
                self.b[k] = a[i]  # @line L6
                self.rank[k] = i
                i += 1
                k = 2 * k + 1  # @line L7

    def __len__(self) -> int:
        return self.n

    def lower_bound_slot(self, x: T) -> int:
        """Return the slot of the first item >= x, or 0 when every item is < x."""
        b, n = self.b, self.n
        k = 1  # @line L8
        while k <= n:  # @line L9
            k = 2 * k + (1 if b[k] < x else 0)  # type: ignore[operator]  # @line L10
        k >>= (k ^ (k + 1)).bit_length()  # @line L11
        return k  # @line L12

    def lower_bound(self, x: T) -> int:
        """Return the number of items less than x (the sorted index of the lower bound)."""
        k = self.lower_bound_slot(x)
        return self.rank[k] if k != 0 else self.n

    def find(self, x: T) -> int:
        """Return the smallest sorted index i with item i == x, or -1."""
        k = self.lower_bound_slot(x)
        if k != 0 and self.b[k] == x:
            return self.rank[k]
        return -1

    def __contains__(self, x: T) -> bool:
        return self.find(x) != -1

    def __iter__(self) -> Iterator[T]:
        """Yield the items in sorted order by an in-order walk of the slots."""
        stack: list[int] = []
        k = 1
        while stack or k <= self.n:
            if k <= self.n:
                stack.append(k)
                k = 2 * k
            else:
                k = stack.pop()
                yield self.b[k]  # type: ignore[misc]
                k = 2 * k + 1

    def check_invariant(self) -> None:
        """Check the in-order sortedness and the rank array."""
        items = list(self)
        assert len(items) == self.n
        for i in range(1, self.n):
            assert not (items[i] < items[i - 1])
        for k in range(1, self.n + 1):
            assert items[self.rank[k]] == self.b[k]
            l, r = 2 * k, 2 * k + 1
            if l <= self.n:
                assert not (self.b[k] < self.b[l])  # type: ignore[operator]
            if r <= self.n:
                assert not (self.b[r] < self.b[k])  # type: ignore[operator]


def eytzinger_layout(items: Sequence[T]) -> list[T]:
    """Return the items in Eytzinger order as a 0-based list (slot k at index k - 1)."""
    return list(Eytzinger(items).b[1:])  # type: ignore[arg-type]
