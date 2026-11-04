# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stable-bloom-filter/. The authors are listed in prov/XYQ2CR.jsonl.

"""Stable Bloom filter (Deng and Rafiei 2006) for duplicate detection in a stream."""

import hashlib
import random

Key = str | bytes | int


class StableBloomFilter:
    """m cells of d bits, K hash functions, and P random decrements per element.

    process(x) reports whether x looks like a duplicate of a recent element,
    then forgets a little (P random cells lose 1) and records x (its K cells
    are set to Max = 2^d - 1). Both false positives and false negatives occur;
    the fraction of zero cells tends to a constant, so the error rates stay
    stable on an unbounded stream.
    """

    def __init__(self, m: int, K: int, d: int = 3, P: int = 10, seed: int = 0, rng_seed: int = 0) -> None:
        if not 1 <= K <= m or d < 1 or not 0 <= P <= m:
            raise ValueError("need 1 <= K <= m, d >= 1 and 0 <= P <= m")
        self.m, self.K, self.P, self.seed = m, K, P, seed
        self.max = (1 << d) - 1
        self.rng = random.Random(rng_seed)
        self.cells = [0] * m  # @line L1

    def _positions(self, key: Key) -> list[int]:
        """K distinct cells of key, from 64-bit words of BLAKE2b."""
        out: list[int] = []
        t = 0
        while len(out) < self.K:
            d = hashlib.blake2b(
                repr(key).encode(), key=self.seed.to_bytes(8, "little"), salt=t.to_bytes(16, "little")
            ).digest()
            for w in range(0, 64, 8):
                p = int.from_bytes(d[w : w + 8], "little") % self.m
                if p not in out and len(out) < self.K:
                    out.append(p)
            t += 1
        return out

    def _victims(self) -> list[int]:
        """P distinct cells chosen uniformly at random."""
        return self.rng.sample(range(self.m), self.P)

    def query(self, key: Key) -> bool:
        """True if all K cells of key are nonzero."""
        return all(self.cells[p] for p in self._positions(key))

    def process(self, key: Key) -> bool:
        """Report whether key looks like a recent duplicate, then record it."""
        ps = self._positions(key)
        dup = all(self.cells[p] for p in ps)  # @line L2
        for j in self._victims():  # @line L3
            if self.cells[j] > 0:
                self.cells[j] -= 1
        for p in ps:  # @line L4
            self.cells[p] = self.max
        return dup  # @line L5

    def zero_fraction(self) -> float:
        """The fraction of cells that are 0."""
        return self.cells.count(0) / self.m

    def stable_zero_fraction(self) -> float:
        """The limit (1 / (1 + 1 / (P (1/K - 1/m))))^Max of the zero fraction."""
        if self.P == 0:
            return 0.0
        if self.K == self.m:
            return 0.0
        return (1 / (1 + 1 / (self.P * (1 / self.K - 1 / self.m)))) ** self.max
