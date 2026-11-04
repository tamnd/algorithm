# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-buffer/. The authors are listed in prov/DCWD8D.jsonl.

from typing import Any, Generic, Iterator, TypeVar

T = TypeVar("T")


class GapBuffer(Generic[T]):
    """A sequence in one array with a gap of free cells at the cursor.

    The text is a[0:g] followed by a[e:cap]; the cursor is at position g.
    insert and delete at the cursor cost O(1) amortized; move_to(p) costs
    O(|p - g| + 1); get(i) costs O(1). Space: cap cells. The buffer never
    shrinks, so cap <= max(initial capacity, 2 * largest n so far).
    """

    def __init__(self, capacity: int = 1) -> None:
        cap = max(1, capacity)
        self.a: list[Any] = [None] * cap
        self.g = 0
        self.e = cap

    def __len__(self) -> int:
        return len(self.a) - (self.e - self.g)

    def __iter__(self) -> Iterator[T]:
        for i in range(len(self)):
            yield self.get(i)

    def cursor(self) -> int:
        return self.g

    def move_to(self, p: int) -> int:
        """Move the cursor to position p, 0 <= p <= n. Return the cells moved."""
        if not 0 <= p <= len(self):
            raise IndexError("position out of range")
        moved = 0
        while self.g > p:  # @line L1
            self.e -= 1
            self.g -= 1
            self.a[self.e] = self.a[self.g]
            moved += 1
        while self.g < p:  # @line L2
            self.a[self.g] = self.a[self.e]
            self.g += 1
            self.e += 1
            moved += 1
        return moved

    def insert(self, x: T) -> None:
        """Insert x before the cursor and move the cursor past it. O(1) amortized."""
        if self.g == self.e:  # @line L3
            self._grow()
        self.a[self.g] = x  # @line L4
        self.g += 1

    def delete_before(self) -> T:
        """Delete the item before the cursor (backspace). Cost O(1)."""
        if self.g == 0:  # @line L5
            raise IndexError("no item before the cursor")
        self.g -= 1
        return self.a[self.g]

    def delete_after(self) -> T:
        """Delete the item after the cursor. Cost O(1)."""
        if self.e == len(self.a):  # @line L6
            raise IndexError("no item after the cursor")
        x = self.a[self.e]
        self.e += 1
        return x

    def get(self, i: int) -> T:
        """Return the item at position i. Cost O(1)."""
        if not 0 <= i < len(self):
            raise IndexError("position out of range")
        return self.a[i] if i < self.g else self.a[i + self.e - self.g]  # @line L7

    def _grow(self) -> None:
        cap = len(self.a)
        new_cap = 2 * cap  # @line L8
        b: list[Any] = [None] * new_cap
        b[: self.g] = self.a[: self.g]
        tail = cap - self.e
        b[new_cap - tail :] = self.a[self.e :]
        self.a = b
        self.e = new_cap - tail

    def check_invariant(self) -> None:
        assert 0 <= self.g <= self.e <= len(self.a)
        assert len(self.a) >= 1
