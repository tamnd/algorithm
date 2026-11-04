# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-table/. The authors are listed in prov/42GYZ4.jsonl.

from collections.abc import Callable, Hashable, Iterator
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class HashTable(Generic[K, V]):
    """A hash table with separate chaining and doubling.

    Each bucket is a list of [key, value] pairs. The table doubles its number
    of buckets when it has more keys than buckets, so the load factor stays at
    most 1. With a hash function that spreads the keys well, each operation
    takes O(1) expected amortized time; in the worst case it takes O(n).
    """

    def __init__(self, m: int = 4, h: Callable[[K], int] = hash) -> None:
        if m < 1:
            raise ValueError("the number of buckets must be at least 1")
        self.h = h
        self.m = m
        self.n = 0
        self.buckets: list[list[list]] = [[] for _ in range(m)]

    def _bucket(self, k: K, m: int) -> int:
        return self.h(k) % m

    def insert(self, k: K, v: V) -> None:
        """Set the value of k to v. Replace the old value if k is a key."""
        i = self._bucket(k, self.m)  # @line L1
        for pair in self.buckets[i]:  # @line L2
            if pair[0] == k:  # @line L3
                pair[1] = v
                return
        self.buckets[i].append([k, v])  # @line L4
        self.n += 1  # @line L5
        if self.n > self.m:  # @line L6
            self.resize(2 * self.m)

    def search(self, k: K) -> V | None:
        """Return the value of k, or None if k is not a key."""
        i = self._bucket(k, self.m)  # @line L7
        for pair in self.buckets[i]:  # @line L8
            if pair[0] == k:  # @line L9
                return pair[1]
        return None  # @line L10

    def contains(self, k: K) -> bool:
        """Return True if k is a key (also when its value is None)."""
        i = self._bucket(k, self.m)
        return any(pair[0] == k for pair in self.buckets[i])

    def delete(self, k: K) -> bool:
        """Remove k and its value. Return True if k was a key."""
        i = self._bucket(k, self.m)  # @line L11
        bucket = self.buckets[i]
        for p in range(len(bucket)):  # @line L12
            if bucket[p][0] == k:  # @line L13
                bucket[p] = bucket[-1]
                bucket.pop()
                self.n -= 1
                return True
        return False

    def resize(self, m2: int) -> None:
        """Move every pair to a new array of m2 buckets. Cost O(n + m + m2)."""
        new: list[list[list]] = [[] for _ in range(m2)]  # @line L14
        for bucket in self.buckets:  # @line L15
            for pair in bucket:
                new[self._bucket(pair[0], m2)].append(pair)  # @line L16
        self.buckets, self.m = new, m2  # @line L17

    def __len__(self) -> int:
        return self.n

    def items(self) -> Iterator[tuple[K, V]]:
        """Yield the pairs in bucket order."""
        for bucket in self.buckets:
            for k, v in bucket:
                yield k, v

    def check_invariant(self) -> None:
        """Assert (H1) to (H4) of the page."""
        assert len(self.buckets) == self.m
        keys = []
        for i, bucket in enumerate(self.buckets):
            for k, _ in bucket:
                assert self._bucket(k, self.m) == i  # (H1)
                keys.append(k)
        assert len(keys) == len(set(keys))  # (H2)
        assert self.n == len(keys)  # (H3)
        assert self.n <= self.m  # (H4)
