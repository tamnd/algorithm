# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-fuse-filter/. The authors are listed in prov/WV9S0Z.jsonl.

"""Binary fuse filter with three hash functions (Graf and Lemire 2022)."""

import hashlib
import math
from collections import deque
from collections.abc import Iterable

Key = str | bytes | int


def fuse_size(n: int) -> tuple[int, int]:
    """The segment length L (a power of 2) and the number of start segments for n keys."""
    n = max(n, 2)
    seg_len = min(1 << math.floor(math.log(n) / math.log(3.33) + 2.25), 1 << 18)
    factor = max(1.125, 0.875 + 0.25 * math.log(1e6) / math.log(n))
    capacity = round(n * factor)
    count = max(1, -(-capacity // seg_len) - 2)
    return seg_len, count


class BinaryFuseFilter:
    """A static filter whose table has (count + 2) segments of L cells of r bits.

    Key x picks a start segment s < count and one cell in each of the segments
    s, s + 1 and s + 2; the table satisfies B[c0] ^ B[c1] ^ B[c2] = fp(x) for
    each x in S. A key not in S is accepted with probability 2^-r.
    """

    def __init__(
        self,
        keys: Iterable[Key],
        r: int = 8,
        seed: int = 0,
        seg_len: int | None = None,
        seg_count: int | None = None,
    ) -> None:
        if r < 1:
            raise ValueError("r must be positive")
        self.r = r
        ks = list(dict.fromkeys(keys))  # distinct keys
        self.n = len(ks)
        L, c = fuse_size(self.n)  # @line L1
        self.L = seg_len or L
        self.count = seg_count or c
        self.seed = seed
        while True:  # @line L2: new hash functions until peeling succeeds
            order = self._peel(ks)
            if order is not None:
                break
            self.seed += 1
        self.B = [0] * ((self.count + 2) * self.L)  # @line L3
        for x, cell in reversed(order):  # @line L4
            cells, fp = self._hash(x)
            acc = fp
            for h in cells:
                if h != cell:
                    acc ^= self.B[h]
            self.B[cell] = acc  # @line L5

    def _hash(self, key: Key) -> tuple[tuple[int, int, int], int]:
        """Cells in three consecutive segments, and an r-bit fingerprint."""
        d = hashlib.blake2b(repr(key).encode(), digest_size=40, key=self.seed.to_bytes(8, "little")).digest()
        s, a, b, c, f = (int.from_bytes(d[i : i + 8], "little") for i in range(0, 40, 8))
        L = self.L
        base = (s % self.count) * L
        return (base + a % L, base + L + b % L, base + 2 * L + c % L), f % (1 << self.r)  # @line L6

    def _peel(self, keys: list[Key]) -> list[tuple[Key, int]] | None:
        """Pairs (x, c) in peeling order: c is a cell of x and of no later key."""
        size = (self.count + 2) * self.L
        cnt, xor = [0] * size, [0] * size
        cells = [self._hash(x)[0] for x in keys]
        for i, cs in enumerate(cells):  # @line L7
            for c in cs:
                cnt[c] += 1
                xor[c] ^= i
        queue = deque(c for c in range(size) if cnt[c] == 1)  # @line L8
        order: list[tuple[Key, int]] = []
        while queue:  # @line L9
            c = queue.popleft()
            if cnt[c] != 1:
                continue
            i = xor[c]
            order.append((keys[i], c))
            for h in cells[i]:  # @line L10
                cnt[h] -= 1
                xor[h] ^= i
                if cnt[h] == 1:
                    queue.append(h)
        return order if len(order) == len(keys) else None  # @line L11

    def query(self, key: Key) -> bool:
        """False if key is surely not in S; True if it may be."""
        (a, b, c), fp = self._hash(key)
        return fp == self.B[a] ^ self.B[b] ^ self.B[c]  # @line L12

    def bits(self) -> int:
        """The size of the table in bits."""
        return len(self.B) * self.r
