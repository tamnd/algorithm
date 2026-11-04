# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-filter/. The authors are listed in prov/131BXM.jsonl.

"""Cuckoo filter (Fan, Andersen, Kaminsky and Mitzenmacher 2014)."""

import hashlib
import random

Key = str | bytes | int


class CuckooFilter:
    """m buckets of b slots that hold f-bit fingerprints, with partial-key cuckoo hashing.

    The value 0 marks an empty slot, so fingerprints are in 1 .. 2^f - 1.
    m must be a power of two, so that i XOR (h(fp) mod m) is a bucket index.
    delete(x) is allowed only for a key x that is present.
    """

    def __init__(self, m: int, b: int = 4, f: int = 8, max_kicks: int = 500, seed: int = 0) -> None:
        if m < 1 or m & (m - 1):
            raise ValueError("m must be a power of two")
        if b < 1 or f < 1:
            raise ValueError("b and f must be positive")
        self.m, self.b, self.f, self.max_kicks, self.seed = m, b, f, max_kicks, seed
        self.table: list[list[int]] = [[] for _ in range(m)]  # @line L1
        self.victim: tuple[int, int] | None = None
        self.rng = random.Random(seed)

    def _h(self, data: bytes) -> int:
        d = hashlib.blake2b(data, digest_size=8, key=self.seed.to_bytes(8, "little")).digest()
        return int.from_bytes(d, "little")

    def _fp_index(self, key: Key) -> tuple[int, int]:
        """The fingerprint of key (never 0) and its first bucket."""
        v = self._h(repr(key).encode())
        fp = (v >> 32) % ((1 << self.f) - 1) + 1 if self.f > 1 else 1
        return fp, (v & 0xFFFFFFFF) % self.m

    def _alt(self, i: int, fp: int) -> int:
        """The other bucket of fingerprint fp in bucket i. _alt(_alt(i, fp), fp) == i."""
        return i ^ (self._h(b"fp" + fp.to_bytes(8, "little")) % self.m)

    def _choose(self, n: int) -> int:
        return self.rng.randrange(n)

    def _place(self, i: int, fp: int) -> None:
        """Store fp in bucket i or its other bucket, kicking entries if needed."""
        for j in (i, self._alt(i, fp)):
            if len(self.table[j]) < self.b:  # @line L4
                self.table[j].append(fp)
                return
        i = (i, self._alt(i, fp))[self._choose(2)]  # @line L5
        for _ in range(self.max_kicks):  # @line L6
            s = self._choose(self.b)
            fp, self.table[i][s] = self.table[i][s], fp  # @line L7
            i = self._alt(i, fp)  # @line L8
            if len(self.table[i]) < self.b:  # @line L9
                self.table[i].append(fp)
                return
        self.victim = (i, fp)  # @line L10: the table is now full

    def insert(self, key: Key) -> bool:
        """Add key. False, with no change, if the filter is full."""
        if self.victim is not None:  # @line L2
            return False
        fp, i1 = self._fp_index(key)  # @line L3
        self._place(i1, fp)
        return True

    def query(self, key: Key) -> bool:
        """False if key is surely absent; True if it may be present."""
        fp, i1 = self._fp_index(key)  # @line L11
        i2 = self._alt(i1, fp)
        if fp in self.table[i1] or fp in self.table[i2]:  # @line L12
            return True
        return self.victim is not None and self.victim[1] == fp and self.victim[0] in (i1, i2)

    def delete(self, key: Key) -> bool:
        """Remove one copy of key. Precondition: key is present."""
        fp, i1 = self._fp_index(key)  # @line L13
        i2 = self._alt(i1, fp)
        for j in (i1, i2):
            if fp in self.table[j]:  # @line L14
                self.table[j].remove(fp)
                if self.victim is not None:  # @line L15: there is room again
                    vi, vfp = self.victim
                    self.victim = None
                    self._place(vi, vfp)
                return True
        if self.victim is not None and self.victim[1] == fp and self.victim[0] in (i1, i2):  # @line L16
            self.victim = None
            return True
        return False  # @line L17

    def __len__(self) -> int:
        return sum(len(t) for t in self.table) + (self.victim is not None)
