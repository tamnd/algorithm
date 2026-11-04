# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/counting-bloom-filter/. The authors are listed in prov/EHFR24.jsonl.

"""Counting Bloom filter (Fan, Cao, Almeida and Broder 2000)."""

import hashlib

Key = str | bytes | int


class CountingBloomFilter:
    """m counters of c bits each and k hash functions.

    insert, delete and query take O(k) time. A counter that reaches the
    largest value 2^c - 1 sticks there, so it never causes a false negative.
    delete(x) is allowed only for a key x that is in the multiset of keys
    inserted and not yet deleted; deleting another key can cause false
    negatives, and the code cannot detect it.
    """

    def __init__(self, m: int, k: int, c: int = 4, seed: int = 0) -> None:
        if m < 1 or k < 1 or c < 1:
            raise ValueError("m, k and c must be positive")
        self.m = m
        self.k = k
        self.seed = seed
        self.cmax = (1 << c) - 1
        self.counters = [0] * m  # @line L1

    def _positions(self, key: Key) -> list[int]:
        """h_1(key), ..., h_k(key) by double hashing on BLAKE2b."""
        d = hashlib.blake2b(
            repr(key).encode(), digest_size=16, key=self.seed.to_bytes(8, "little")
        ).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:], "little") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]  # @line L2

    def insert(self, key: Key) -> None:
        """Add one copy of key."""
        for p in self._positions(key):  # @line L3
            if self.counters[p] < self.cmax:  # @line L4: a full counter sticks
                self.counters[p] += 1

    def delete(self, key: Key) -> None:
        """Remove one copy of key. Precondition: a copy of key is present."""
        for p in self._positions(key):  # @line L5
            if self.counters[p] < self.cmax:  # @line L6: a stuck counter stays
                self.counters[p] -= 1

    def query(self, key: Key) -> bool:
        """False if key is surely absent; True if it may be present."""
        for p in self._positions(key):  # @line L7
            if self.counters[p] == 0:  # @line L8
                return False
        return True  # @line L9

    def saturated(self) -> int:
        """The number of counters stuck at the largest value."""
        return sum(1 for v in self.counters if v == self.cmax)
