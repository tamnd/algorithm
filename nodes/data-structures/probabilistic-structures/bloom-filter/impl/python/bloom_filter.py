# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloom-filter/. The authors are listed in prov/3RBEYS.jsonl.

"""Bloom filter (Bloom 1970): an approximate set with no false negatives."""

import hashlib

Key = str | bytes | int


class BloomFilter:
    """A bit array of m bits with k hash functions.

    insert and query take O(k) time. A query for an inserted key always
    returns True. A query for another key returns True with probability
    about (1 - exp(-k n / m))^k after n inserts. Keys are str, bytes or int;
    the hash functions are derived from BLAKE2b with the given seed, so the
    filter is the same in each run.
    """

    def __init__(self, m: int, k: int, seed: int = 0) -> None:
        if m < 1 or k < 1:
            raise ValueError("m and k must be positive")
        self.m = m
        self.k = k
        self.seed = seed
        self.bits = bytearray((m + 7) // 8)  # @line L1: m bits, all 0
        self.count = 0  # number of insert calls, for the user

    def _positions(self, key: Key) -> list[int]:
        """The k positions h_1(key), ..., h_k(key) in [0, m).

        Double hashing (Kirsch and Mitzenmacher): g_i = h1 + i * h2 mod m.
        """
        d = hashlib.blake2b(
            repr(key).encode(), digest_size=16, key=self.seed.to_bytes(8, "little")
        ).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:], "little") | 1  # odd, so it is not 0
        return [(h1 + i * h2) % self.m for i in range(self.k)]  # @line L2

    def _get(self, i: int) -> bool:
        return (self.bits[i >> 3] >> (i & 7)) & 1 == 1

    def insert(self, key: Key) -> None:
        """Add key to the set. Bits only change from 0 to 1."""
        for p in self._positions(key):  # @line L3
            self.bits[p >> 3] |= 1 << (p & 7)  # @line L4
        self.count += 1

    def query(self, key: Key) -> bool:
        """False if key was surely never inserted; True if it may have been."""
        for p in self._positions(key):  # @line L5
            if not self._get(p):  # @line L6
                return False
        return True  # @line L7

    def ones(self) -> int:
        """The number of bits that are 1."""
        return sum(bin(b).count("1") for b in self.bits)

    def union(self, other: "BloomFilter") -> "BloomFilter":
        """The filter of the union of the two sets. Same m, k and seed needed."""
        if (self.m, self.k, self.seed) != (other.m, other.k, other.seed):
            raise ValueError("the filters must have the same m, k and seed")
        out = BloomFilter(self.m, self.k, self.seed)
        out.bits = bytearray(a | b for a, b in zip(self.bits, other.bits))
        out.count = self.count + other.count
        return out
