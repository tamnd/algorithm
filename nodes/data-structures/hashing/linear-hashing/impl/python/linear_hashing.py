# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-hashing/. The authors are listed in prov/EA0KDC.jsonl.

from collections.abc import Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LinearHashing(Generic[K, V]):
    """A map from keys to values by Litwin's linear hashing, with chained buckets.

    The table has N * 2**L + p buckets. A key k lives in bucket h(k) mod N * 2**L,
    or in bucket h(k) mod N * 2**(L+1) when the first value is below the split
    pointer p. Here h is Python's hash. An insertion that makes the load factor
    n / (number of buckets) exceed max_load splits bucket p, then moves p one
    step; a deletion that makes it fall below min_load undoes the last split.
    Each operation costs O(1) expected amortized time when the hash values
    behave like independent uniform values and max_load is a constant.
    """

    def __init__(self, initial_buckets: int = 2, max_load: float = 1.0, min_load: float | None = None) -> None:
        """Make an empty table. Needs initial_buckets >= 1, max_load > 0 and 0 <= min_load <= max_load / 2."""
        if min_load is None:
            min_load = max_load / 4
        if initial_buckets < 1 or max_load <= 0 or not 0 <= min_load <= max_load / 2:
            raise ValueError("need initial_buckets >= 1, max_load > 0, 0 <= min_load <= max_load / 2")
        self.n0 = initial_buckets  # N in the text
        self.max_load = max_load
        self.min_load = min_load
        self.level = 0  # L
        self.p = 0  # the split pointer
        self.n = 0  # the number of pairs
        self.buckets: list[list[tuple[K, V]]] = [[] for _ in range(initial_buckets)]

    def __len__(self) -> int:
        return self.n

    def address(self, key: K) -> int:
        """Return the index of the bucket that holds key, if it is present."""
        hk = hash(key)
        a = hk % (self.n0 << self.level)  # @line L1
        if a < self.p:  # @line L2
            a = hk % (self.n0 << (self.level + 1))
        return a  # @line L3

    def search(self, key: K) -> V | None:
        """Return the value of key, or None when key is absent."""
        for k, v in self.buckets[self.address(key)]:  # @line L4
            if k == key:  # @line L5
                return v
        return None  # @line L6

    def insert(self, key: K, value: V) -> None:
        """Map key to value; replace the old value when key is present."""
        a = self.address(key)  # @line L7
        bucket = self.buckets[a]
        for i, (k, _) in enumerate(bucket):  # @line L8
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))  # @line L9
        self.n += 1
        while self.n > self.max_load * len(self.buckets):  # @line L10
            self.split()

    def split(self) -> None:
        """Split the bucket at the split pointer and move the pointer one step."""
        half = self.n0 << self.level
        self.buckets.append([])  # @line L11: the new bucket gets index p + half
        old = self.buckets[self.p]  # @line L12
        self.buckets[self.p] = []
        wide = half << 1
        for k, v in old:  # @line L13
            self.buckets[hash(k) % wide].append((k, v))  # @line L14
        self.p += 1  # @line L15
        if self.p == half:  # @line L16
            self.level += 1
            self.p = 0

    def delete(self, key: K) -> bool:
        """Remove key. Return True when it was present."""
        bucket = self.buckets[self.address(key)]  # D1
        for i, (k, _) in enumerate(bucket):  # D2
            if k == key:
                bucket[i] = bucket[-1]  # D3: order inside a bucket does not matter
                bucket.pop()
                self.n -= 1
                while len(self.buckets) > self.n0 and self.n < self.min_load * len(self.buckets):  # D4
                    self.merge()
                return True  # D5
        return False

    def merge(self) -> None:
        """Undo the last split: merge the last bucket into its partner."""
        if self.p == 0:  # M1
            self.level -= 1
            self.p = self.n0 << self.level
        self.p -= 1  # M2
        last = self.buckets.pop()  # M3, M4: the last bucket has index p + N * 2**L
        self.buckets[self.p].extend(last)

    def items(self) -> list[tuple[K, V]]:
        """Return all pairs, in no particular order."""
        return [pair for bucket in self.buckets for pair in bucket]

    def check_invariant(self) -> None:
        """Raise AssertionError when an invariant of the page fails."""
        half = self.n0 << self.level
        assert self.level >= 0 and 0 <= self.p < half  # I1
        assert len(self.buckets) == half + self.p >= self.n0  # I1
        keys = []
        for j, bucket in enumerate(self.buckets):
            for k, _ in bucket:
                assert self.address(k) == j  # I2
                keys.append(k)
        assert len(keys) == len(set(keys)) == self.n  # I3
        assert self.n <= self.max_load * len(self.buckets)  # I4
