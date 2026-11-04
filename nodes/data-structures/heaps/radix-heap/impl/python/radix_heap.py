# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-heap/. The authors are listed in prov/FZSDPB.jsonl.

from typing import Generic, TypeVar

V = TypeVar("V")


class RadixHeap(Generic[V]):
    """A monotone min-priority queue on nonnegative integer keys.

    Bucket 0 holds the items whose key equals last, the last extracted key.
    Bucket i >= 1 holds the items whose key differs from last first in bit
    i - 1, counting from bit 0. Every key inserted must be at least last.
    """

    def __init__(self) -> None:
        self.last = 0
        self.buckets: list[list[tuple[int, V | None]]] = [[]]
        self.n = 0
        self.moves = 0

    def __len__(self) -> int:
        return self.n

    def is_empty(self) -> bool:
        """Return True if the heap holds no item."""
        return self.n == 0

    def _bucket(self, key: int) -> int:
        return (key ^ self.last).bit_length()

    def _put(self, key: int, value: V | None) -> None:
        i = self._bucket(key)
        while len(self.buckets) <= i:
            self.buckets.append([])
        self.buckets[i].append((key, value))  # @line L2

    def insert(self, key: int, value: V | None = None) -> None:
        """Add an item; key must be an integer at least the last extracted key."""
        if key < self.last:  # @line L1
            raise ValueError("radix heap is monotone: key below the last extracted key")
        self._put(key, value)
        self.n += 1

    def find_min(self) -> int:
        """Return a smallest key without removing it."""
        if self.n == 0:
            raise IndexError("find_min on an empty heap")
        self._refill()
        return self.last

    def _refill(self) -> None:
        if self.buckets[0]:  # @line L3
            return
        i = 1  # @line L4
        while not self.buckets[i]:
            i += 1
        items = self.buckets[i]
        self.last = min(k for k, _ in items)  # @line L5
        self.buckets[i] = []  # @line L6
        for k, v in items:  # @line L7
            self._put(k, v)
            self.moves += 1

    def extract_min(self) -> tuple[int, V | None]:
        """Remove and return an item (key, value) with the smallest key."""
        if self.n == 0:
            raise IndexError("extract_min on an empty heap")
        self._refill()
        self.n -= 1
        return self.buckets[0].pop()  # @line L8

    def check_invariant(self) -> None:
        """Check that every item is in the bucket given by its key and last."""
        count = 0
        for i, b in enumerate(self.buckets):
            for k, _ in b:
                assert k >= self.last, "monotone"
                assert self._bucket(k) == i, "bucket"
                count += 1
        assert count == self.n, "count"
