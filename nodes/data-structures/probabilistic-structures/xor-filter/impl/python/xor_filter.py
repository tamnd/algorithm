# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-filter/. The authors are listed in prov/6QE9XB.jsonl.

"""Xor filter (Graf and Lemire 2020) with three blocks and r-bit fingerprints."""

import hashlib
from collections import deque
from collections.abc import Iterable

Key = str | bytes | int


class XorFilter:
    """A static filter: query(x) is True for each x in S, and for x not in S
    with probability 2^-r.

    The table has 3 * seg cells of r bits, with seg = ceil((floor(1.23 n) + 32) / 3).
    Key x has one cell in each block and the fingerprint fp(x); the table
    satisfies B[h0(x)] ^ B[h1(x)] ^ B[h2(x)] = fp(x) for each x in S.
    """

    def __init__(self, keys: Iterable[Key], r: int = 8, seed: int = 0, seg: int | None = None) -> None:
        if r < 1:
            raise ValueError("r must be positive")
        self.r = r
        ks = list(dict.fromkeys(keys))  # distinct keys, in first-seen order
        self.n = len(ks)
        self.seg = seg if seg else -(-(123 * self.n // 100 + 32) // 3)  # @line L1
        self.seed = seed
        while True:  # @line L2: new hash functions until peeling succeeds
            order = self._peel(ks)
            if order is not None:
                break
            self.seed += 1
        self.B = [0] * (3 * self.seg)  # @line L3
        for x, c in reversed(order):  # @line L4
            cells, fp = self._hash(x)
            acc = fp
            for h in cells:
                if h != c:
                    acc ^= self.B[h]
            self.B[c] = acc  # @line L5

    def _hash(self, key: Key) -> tuple[tuple[int, int, int], int]:
        """One cell in each block, and an r-bit fingerprint."""
        d = hashlib.blake2b(repr(key).encode(), digest_size=32, key=self.seed.to_bytes(8, "little")).digest()
        a, b, c, f = (int.from_bytes(d[i : i + 8], "little") for i in range(0, 32, 8))
        s = self.seg
        return (a % s, s + b % s, 2 * s + c % s), f % (1 << self.r)

    def _peel(self, keys: list[Key]) -> list[tuple[Key, int]] | None:
        """Pairs (x, c) in peeling order: c is a cell of x and of no later key."""
        size = 3 * self.seg
        count, xor = [0] * size, [0] * size
        cells = [self._hash(x)[0] for x in keys]
        for i, cs in enumerate(cells):  # @line L6
            for c in cs:
                count[c] += 1
                xor[c] ^= i
        queue = deque(c for c in range(size) if count[c] == 1)  # @line L7
        order: list[tuple[Key, int]] = []
        while queue:  # @line L8
            c = queue.popleft()
            if count[c] != 1:
                continue
            i = xor[c]  # the only key left at cell c
            order.append((keys[i], c))
            for h in cells[i]:  # @line L9
                count[h] -= 1
                xor[h] ^= i
                if count[h] == 1:
                    queue.append(h)
        return order if len(order) == len(keys) else None  # @line L10

    def query(self, key: Key) -> bool:
        """False if key is surely not in S; True if it may be."""
        (a, b, c), fp = self._hash(key)
        return fp == self.B[a] ^ self.B[b] ^ self.B[c]  # @line L11

    def bits(self) -> int:
        """The size of the table in bits."""
        return len(self.B) * self.r
