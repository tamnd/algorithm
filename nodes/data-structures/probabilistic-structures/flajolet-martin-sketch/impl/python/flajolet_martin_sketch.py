# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flajolet-martin-sketch/. The authors are listed in prov/86TWSR.jsonl.

"""Flajolet-Martin probabilistic counting with stochastic averaging (PCSA, 1985)."""

import hashlib

Key = str | bytes | int

PHI = 0.77351  # the correction constant of Flajolet and Martin


def rho(q: int) -> int:
    """The number of trailing zero bits of q > 0."""
    return (q & -q).bit_length() - 1


class FMSketch:
    """m bitmaps of L bits. add is O(1); estimate is O(m L).

    The state depends only on the set of distinct keys added, so duplicates
    and the order of the stream do not matter.
    """

    def __init__(self, m: int = 64, L: int = 32, seed: int = 0) -> None:
        if m < 1 or L < 1:
            raise ValueError("m and L must be positive")
        self.m, self.L, self.seed = m, L, seed
        self.bitmaps = [0] * m  # @line L1: bit r of bitmaps[j] is B_j[r]

    def _hash(self, key: Key) -> int:
        d = hashlib.blake2b(repr(key).encode(), digest_size=8, key=self.seed.to_bytes(8, "little"))  # @line L2
        return int.from_bytes(d.digest(), "little")

    def add(self, key: Key) -> None:
        """Record one occurrence of key."""
        y = self._hash(key)
        j, q = y % self.m, y // self.m  # @line L3
        if q:
            r = rho(q)
            if r < self.L:
                self.bitmaps[j] |= 1 << r  # @line L4

    def rank(self, j: int) -> int:
        """R_j: the index of the lowest 0 bit of bitmap j."""
        b, r = self.bitmaps[j], 0
        while r < self.L and b >> r & 1:
            r += 1
        return r

    def estimate(self) -> float:
        """The PCSA estimate (m / PHI) * 2^(mean of the R_j)."""
        s = 0  # @line L5
        for j in range(self.m):
            s += self.rank(j)  # @line L6
        return self.m / PHI * 2 ** (s / self.m)  # @line L7

    def merge(self, other: "FMSketch") -> "FMSketch":
        """The sketch of the union of the two key sets."""
        if (self.m, self.L, self.seed) != (other.m, other.L, other.seed):
            raise ValueError("sketches must have the same m, L and seed")
        out = FMSketch(self.m, self.L, self.seed)
        out.bitmaps = [a | b for a, b in zip(self.bitmaps, other.bitmaps)]
        return out
