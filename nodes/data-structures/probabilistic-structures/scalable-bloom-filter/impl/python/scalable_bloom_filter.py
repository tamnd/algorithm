# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalable-bloom-filter/. The authors are listed in prov/Q55J7F.jsonl.

"""Scalable Bloom filter (Almeida, Baquero, Preguica and Hutchison 2007)."""

import hashlib
import math

Key = str | bytes | int


class Slice:
    """A partitioned Bloom filter: k parts of b bits, one hash function per part."""

    def __init__(self, k: int, b: int) -> None:
        self.k = k
        self.b = b
        self.bits = [bytearray(b) for _ in range(k)]
        self.count = 0
        # the expected fill of each part stays at most 1/2 up to this count
        self.capacity = max(1, math.floor((b - 1) * math.log(2)))


class ScalableBloomFilter:
    """A list of partitioned Bloom filters with growing size and tightening rate.

    Slice i has b0 * s^i bits in each of its k_i = ceil(log2(1 / (eps0 * r^i)))
    parts. Only the last slice takes new keys; a new slice is added when the
    last one is at capacity. The false positive rate is at most eps0 / (1 - r)
    at every size, under ideal hashing.
    """

    def __init__(
        self, b0: int = 64, eps0: float = 0.005, r: float = 0.9, s: int = 2, seed: int = 0
    ) -> None:
        if b0 < 2 or not 0 < eps0 < 1 or not 0 < r < 1 or s < 1:
            raise ValueError("need b0 >= 2, 0 < eps0 < 1, 0 < r < 1 and s >= 1")
        self.b0 = b0
        self.eps0 = eps0
        self.r = r
        self.s = s
        self.seed = seed
        self.slices: list[Slice] = []  # @line L1

    def _positions(self, key: Key, i: int) -> list[int]:
        """The k_i positions of key in slice i, one in each part."""
        sl = self.slices[i]
        out: list[int] = []
        t = 0
        while len(out) < sl.k:  # independent 64-bit words, eight per digest
            d = hashlib.blake2b(
                repr(key).encode(),
                key=self.seed.to_bytes(8, "little"),
                salt=(i << 32 | t).to_bytes(16, "little"),
            ).digest()
            out.extend(int.from_bytes(d[w : w + 8], "little") % sl.b for w in range(0, 64, 8))
            t += 1
        return out[: sl.k]

    def _add_slice(self) -> None:
        i = len(self.slices)
        k = max(1, math.ceil(math.log2(1 / (self.eps0 * self.r**i)) - 1e-9))  # @line L2
        self.slices.append(Slice(k, self.b0 * self.s**i))  # @line L3

    def insert(self, key: Key) -> None:
        """Add key to the last slice, after adding a slice if the last one is full."""
        if not self.slices or self.slices[-1].count >= self.slices[-1].capacity:  # @line L4
            self._add_slice()
        last = len(self.slices) - 1
        sl = self.slices[last]
        for j, p in enumerate(self._positions(key, last)):  # @line L5
            sl.bits[j][p] = 1
        sl.count += 1  # @line L6

    def query(self, key: Key) -> bool:
        """False if key is surely absent; True if it may be present."""
        for i, sl in enumerate(self.slices):  # @line L7
            if all(sl.bits[j][p] for j, p in enumerate(self._positions(key, i))):  # @line L8
                return True
        return False  # @line L9

    def rate_bound(self) -> float:
        """The bound eps0 * (1 + r + ... + r^(l-1)) for the current l slices."""
        return sum(self.eps0 * self.r**i for i in range(len(self.slices)))

    def bits(self) -> int:
        """The total number of bits of all slices."""
        return sum(sl.k * sl.b for sl in self.slices)
