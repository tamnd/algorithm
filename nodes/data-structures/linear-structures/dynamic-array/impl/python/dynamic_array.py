# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-array/. The authors are listed in prov/9C8NGV.jsonl.

from typing import Generic, Iterator, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """An array that doubles when full and halves when a quarter full.

    get and set cost O(1) in the worst case. append costs O(1) amortized
    (at most 3 units) and pop O(1) amortized (at most 2 units), counting
    one unit per item written, read or copied. The capacity is a power of
    two and is less than 4 * max(n, 1).
    """

    def __init__(self) -> None:
        self.cap = 1
        self.n = 0
        self.a: list[T | None] = [None]
        self.copies = 0  # the number of executions of line L10, for tests

    def __len__(self) -> int:
        return self.n

    def get(self, i: int) -> T:
        """Return the item at index i. Precondition: 0 <= i < n. Cost O(1)."""
        if not 0 <= i < self.n:
            raise IndexError("index out of range")
        return self.a[i]  # type: ignore[return-value]

    def set(self, i: int, x: T) -> None:
        """Replace the item at index i. Precondition: 0 <= i < n. Cost O(1)."""
        if not 0 <= i < self.n:
            raise IndexError("index out of range")
        self.a[i] = x

    def append(self, x: T) -> None:
        """Add x at the end. Cost O(1) amortized, O(n) worst case."""
        if self.n == self.cap:  # @line L1
            self._resize(2 * self.cap)
        self.a[self.n] = x  # @line L2
        self.n += 1  # @line L3

    def pop(self) -> T:
        """Remove and return the last item. Precondition: n > 0. Cost O(1) amortized."""
        if self.n == 0:
            raise IndexError("pop from an empty array")
        self.n -= 1  # @line L4
        x = self.a[self.n]  # @line L5
        self.a[self.n] = None  # drop the reference so that the item can be freed
        if self.n > 0 and 4 * self.n == self.cap:  # @line L6
            self._resize(self.cap // 2)
        return x  # type: ignore[return-value]  # @line L7

    def _resize(self, c: int) -> None:
        b: list[T | None] = [None] * c  # @line L8
        for i in range(self.n):  # @line L9
            b[i] = self.a[i]  # @line L10
            self.copies += 1
        self.a, self.cap = b, c  # @line L11

    def __iter__(self) -> Iterator[T]:
        for i in range(self.n):
            yield self.a[i]  # type: ignore[misc]

    def check_invariant(self) -> None:
        assert 0 <= self.n <= self.cap == len(self.a)
        assert self.cap & (self.cap - 1) == 0
        assert self.cap < 4 * max(self.n, 1)
