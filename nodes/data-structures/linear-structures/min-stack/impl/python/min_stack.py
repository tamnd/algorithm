# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-stack/. The authors are listed in prov/PR4H8X.jsonl.

from typing import Generic, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


class MinStack(Generic[T]):
    """A stack that also returns the least item it holds.

    Each entry is a pair (x, m), where m is the least item at or below that
    entry. push, pop, top and min cost O(1) amortized on a Python list
    (O(1) worst case on a fixed array or a linked list). Space: 2n cells.
    """

    def __init__(self) -> None:
        self.s: list[tuple[T, T]] = []

    def __len__(self) -> int:
        return len(self.s)

    def is_empty(self) -> bool:
        return not self.s

    def push(self, x: T) -> None:
        """Push x. Cost O(1)."""
        if not self.s:  # @line L1
            m = x
        else:
            m = self.s[-1][1]
            if x < m:
                m = x
        self.s.append((x, m))  # @line L2

    def pop(self) -> T:
        """Remove and return the top item. Precondition: not empty. Cost O(1)."""
        if not self.s:
            raise IndexError("pop from an empty stack")
        x, _ = self.s.pop()  # @line L3
        return x  # @line L4

    def top(self) -> T:
        """Return the top item. Precondition: not empty. Cost O(1)."""
        if not self.s:
            raise IndexError("top of an empty stack")
        return self.s[-1][0]  # @line L5

    def min(self) -> T:
        """Return the least item. Precondition: not empty. Cost O(1)."""
        if not self.s:
            raise IndexError("min of an empty stack")
        return self.s[-1][1]  # @line L6

    def check_invariant(self) -> None:
        for k, (x, m) in enumerate(self.s):
            below = self.s[k - 1][1] if k else x
            assert not x < m and not below < m and (m == x or m == below)


class LeanMinStack(Generic[T]):
    """The variant with a second stack that holds only the new minima (pushed when x <= min)."""

    def __init__(self) -> None:
        self.items: list[T] = []
        self.mins: list[T] = []

    def push(self, x: T) -> None:
        self.items.append(x)
        if not self.mins or not self.mins[-1] < x:  # x <= current min
            self.mins.append(x)

    def pop(self) -> T:
        x = self.items.pop()
        if not self.mins[-1] < x and not x < self.mins[-1]:  # x == current min
            self.mins.pop()
        return x

    def min(self) -> T:
        return self.mins[-1]
