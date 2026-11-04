# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ribbon-filter/. The authors are listed in prov/K1BXC2.jsonl.

"""Standard ribbon filter (Dillinger and Walzer 2021): banded on-the-fly elimination."""

import hashlib
import math
from collections.abc import Iterable

Key = str | bytes | int


class RibbonFilter:
    """A static filter: a solution Z of one xor equation per key, with r-bit values.

    Key x has a start s(x) in [0, m - w], a w-bit coefficient row c(x) with bit 0
    set, and an r-bit fingerprint fp(x); bit j of c(x) stands for row s(x) + j
    of Z. The filter stores Z with xor of Z[s + j] over the set bits j equal to
    fp(x) for each x in S. A key not in S is accepted with probability 2^-r.
    """

    def __init__(
        self,
        keys: Iterable[Key],
        r: int = 8,
        w: int = 64,
        overhead: float = 0.05,
        seed: int = 0,
        m: int | None = None,
    ) -> None:
        if r < 1 or w < 1 or overhead < 0:
            raise ValueError("need r >= 1, w >= 1 and overhead >= 0")
        self.r, self.w = r, w
        ks = list(keys)
        self.n = len(ks)
        self.m = m if m else max(w, math.ceil((1 + overhead) * self.n) + w)  # @line L1
        self.seed = seed
        while True:  # @line L2: new hash functions until every row fits
            rows = self._band(ks)
            if rows is not None:
                break
            self.seed += 1
        C, B = rows
        self.Z = [0] * self.m
        for i in range(self.m - 1, -1, -1):  # @line L8: back substitution
            if C[i]:
                z, c, j = B[i], C[i] >> 1, 1
                while c:
                    if c & 1:
                        z ^= self.Z[i + j]  # @line L9
                    c >>= 1
                    j += 1
                self.Z[i] = z

    def _hash(self, key: Key) -> tuple[int, int, int]:
        """The start s, the w-bit row c with bit 0 set, and the r-bit fingerprint."""
        d = hashlib.blake2b(repr(key).encode(), digest_size=24, key=self.seed.to_bytes(8, "little")).digest()
        a, b, f = (int.from_bytes(d[i : i + 8], "little") for i in range(0, 24, 8))
        s = a % (self.m - self.w + 1)
        c = (b % (1 << self.w)) | 1
        return s, c, f % (1 << self.r)

    def _band(self, keys: list[Key]) -> tuple[list[int], list[int]] | None:
        """Banded elimination: C[i] is 0 or has bit 0 set (leading column i)."""
        C, B = [0] * self.m, [0] * self.m
        for x in keys:
            s, c, b = self._hash(x)
            while True:  # @line L3
                if C[s] == 0:  # @line L4
                    C[s], B[s] = c, b
                    break
                c ^= C[s]  # @line L5
                b ^= B[s]
                if c == 0:  # @line L6: the row is a sum of stored rows
                    if b != 0:
                        return None
                    break
                j = (c & -c).bit_length() - 1  # @line L7
                s += j
                c >>= j
        return C, B

    def query(self, key: Key) -> bool:
        """False if key is surely not in S; True if it may be."""
        s, c, f = self._hash(key)
        acc, j = 0, 0
        while c:  # @line L10
            if c & 1:
                acc ^= self.Z[s + j]
            c >>= 1
            j += 1
        return acc == f

    def bits(self) -> int:
        """The size of Z in bits."""
        return self.m * self.r
