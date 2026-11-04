# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/array/. The authors are listed in prov/43DJ9Z.jsonl.

from typing import Generic, TypeVar

T = TypeVar("T")


class Array(Generic[T]):
    """A partially filled array of fixed capacity.

    The list held is cells[0:n]. get and set cost O(1). insert at index i
    makes n - i moves and delete at index i makes n - 1 - i moves. search
    makes at most n comparisons. Space: capacity cells.
    """

    def __init__(self, capacity: int = 0) -> None:
        if capacity < 0:
            raise ValueError("capacity must be >= 0")
        self.cells: list[T | None] = [None] * capacity
        self.n = 0
        self.moves = 0  # the number of executions of line L4 or L9, for tests

    @property
    def capacity(self) -> int:
        return len(self.cells)

    def __len__(self) -> int:
        return self.n

    def _check(self, i: int, hi: int) -> None:
        if not 0 <= i < hi:
            raise IndexError("index out of range")

    def get(self, i: int) -> T:
        """Return the item at index i. Precondition: 0 <= i < n. Cost O(1)."""
        self._check(i, self.n)
        return self.cells[i]  # type: ignore[return-value]  # @line L1

    def set(self, i: int, x: T) -> None:
        """Replace the item at index i by x. Precondition: 0 <= i < n. Cost O(1)."""
        self._check(i, self.n)
        self.cells[i] = x  # @line L2

    def insert(self, i: int, x: T) -> None:
        """Insert x at index i. Precondition: 0 <= i <= n < capacity. Cost O(n - i + 1)."""
        self._check(i, self.n + 1)
        if self.n >= self.capacity:
            raise OverflowError("array is full")
        for j in range(self.n, i, -1):  # @line L3
            self.cells[j] = self.cells[j - 1]  # @line L4
            self.moves += 1
        self.cells[i] = x  # @line L5
        self.n += 1  # @line L6

    def delete(self, i: int) -> T:
        """Remove and return the item at index i. Precondition: 0 <= i < n. Cost O(n - i)."""
        self._check(i, self.n)
        x = self.cells[i]  # @line L7
        for j in range(i, self.n - 1):  # @line L8
            self.cells[j] = self.cells[j + 1]  # @line L9
            self.moves += 1
        self.n -= 1  # @line L10
        return x  # type: ignore[return-value]  # @line L11

    def search(self, x: T) -> int | None:
        """Return the first index of x, or None. Cost O(n) comparisons."""
        for i in range(self.n):  # @line S1
            if self.cells[i] == x:  # @line S2
                return i
        return None  # @line S3

    def to_list(self) -> list[T]:
        return list(self.cells[: self.n])  # type: ignore[arg-type]

    def check_invariant(self) -> None:
        assert 0 <= self.n <= self.capacity
