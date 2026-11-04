# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-buffer/. The authors are listed in prov/9NS9WP.jsonl.

from typing import Any, Generic, Iterator, TypeVar

T = TypeVar("T")


class CircularBuffer(Generic[T]):
    """A bounded queue and deque in an array of fixed capacity.

    enqueue, dequeue, push_front, pop_back and get cost O(1) worst case.
    Space: capacity cells. Precondition: capacity >= 1.
    enqueue and push_front raise OverflowError on a full buffer.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.cap = capacity
        self.a: list[Any] = [None] * capacity
        self.h = 0
        self.n = 0

    def __len__(self) -> int:
        return self.n

    def __iter__(self) -> Iterator[T]:
        for i in range(self.n):
            yield self.get(i)

    def is_full(self) -> bool:
        return self.n == self.cap

    def enqueue(self, x: T) -> None:
        """Add x at the back. Cost O(1)."""
        if self.n == self.cap:  # @line L1
            raise OverflowError("buffer is full")
        self.a[(self.h + self.n) % self.cap] = x  # @line L2
        self.n += 1  # @line L3

    def dequeue(self) -> T:
        """Remove and return the front item. Cost O(1)."""
        if self.n == 0:  # @line L4
            raise IndexError("dequeue from empty buffer")
        x = self.a[self.h]  # @line L5
        self.h = (self.h + 1) % self.cap  # @line L6
        self.n -= 1
        return x  # @line L7

    def push_front(self, x: T) -> None:
        """Add x at the front. Cost O(1)."""
        if self.n == self.cap:
            raise OverflowError("buffer is full")
        self.h = (self.h - 1) % self.cap  # @line L8
        self.a[self.h] = x
        self.n += 1

    def pop_back(self) -> T:
        """Remove and return the back item. Cost O(1)."""
        if self.n == 0:
            raise IndexError("pop from empty buffer")
        self.n -= 1  # @line L9
        return self.a[(self.h + self.n) % self.cap]  # @line L10

    def get(self, i: int) -> T:
        """Return the item at position i from the front. Cost O(1)."""
        if not 0 <= i < self.n:
            raise IndexError("position out of range")
        return self.a[(self.h + i) % self.cap]  # @line L11

    def check_invariant(self) -> None:
        assert len(self.a) == self.cap
        assert 0 <= self.h < self.cap
        assert 0 <= self.n <= self.cap
