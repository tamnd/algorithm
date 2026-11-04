# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bloomier-filter/. The authors are listed in prov/8T9R6F.jsonl.

"""Bloomier filter (Chazelle, Kilian, Rubinfeld and Tal 2004) with three hash functions."""

import hashlib
from collections import deque
from collections.abc import Mapping

Key = str | bytes | int


class BloomierFilter:
    """A static function table: lookup(x) gives f(x) for x in S, and usually None otherwise.

    T has M cells of q bits that encode, for each key, which of its three cells
    holds its value; R has M cells of r bits that hold the values. A key not in
    S gets a value with probability 3 / 2^q. Values of keys in S can be changed
    with set(); the set S itself is fixed.
    """

    def __init__(self, f: Mapping[Key, int], r: int, q: int = 8, seed: int = 0, seg: int | None = None) -> None:
        if r < 1 or q < 2:
            raise ValueError("r must be positive and q at least 2")
        if any(not 0 <= v < 1 << r for v in f.values()):
            raise ValueError("values must fit in r bits")
        self.r, self.q = r, q
        keys = list(f)
        self.seg = seg if seg else (123 * len(keys) + 299) // 300 + 1  # cells per third
        self.seed, tries = seed, 0
        while True:  # @line L1: choose hash functions until peeling succeeds
            order = self._peel(keys)  # @line L2
            if order is not None:
                break
            self.seed, tries = self.seed + 1, tries + 1
            if tries % 10 == 0:
                self.seg += self.seg // 10 + 1
        size = 3 * self.seg
        self.T = [0] * size  # @line L3
        self.R = [0] * size
        for x, c in reversed(order):  # @line L4
            cells, mask = self._cells(x)
            tau = cells.index(c)  # @line L5
            acc = tau ^ mask
            for h in cells:
                if h != c:
                    acc ^= self.T[h]
            self.T[c] = acc  # @line L6
            self.R[c] = f[x]  # @line L7

    def _cells(self, key: Key) -> tuple[tuple[int, int, int], int]:
        """Three cells, one in each third of the table, and a q-bit mask."""
        d = hashlib.blake2b(repr(key).encode(), digest_size=32, key=self.seed.to_bytes(8, "little")).digest()
        a, b, c, m = (int.from_bytes(d[i : i + 8], "little") for i in range(0, 32, 8))
        s = self.seg
        return (a % s, s + b % s, 2 * s + c % s), m % (1 << self.q)

    def _peel(self, keys: list[Key]) -> list[tuple[Key, int]] | None:
        """A peeling order: pairs (x, c) where c is a cell of x and of no later key."""
        size = 3 * self.seg
        count, xor = [0] * size, [0] * size
        cells = [self._cells(x)[0] for x in keys]
        for i, cs in enumerate(cells):  # @line L12
            for c in cs:
                count[c] += 1
                xor[c] ^= i
        queue = deque(c for c in range(size) if count[c] == 1)
        order: list[tuple[Key, int]] = []
        while queue:  # @line L13
            c = queue.popleft()
            if count[c] != 1:
                continue
            i = xor[c]  # the only key left at cell c
            order.append((keys[i], c))
            for h in cells[i]:
                count[h] -= 1
                xor[h] ^= i
                if count[h] == 1:
                    queue.append(h)
        return order if len(order) == len(keys) else None  # @line L14

    def _tau(self, key: Key) -> tuple[tuple[int, int, int], int]:
        cells, mask = self._cells(key)
        return cells, mask ^ self.T[cells[0]] ^ self.T[cells[1]] ^ self.T[cells[2]]  # @line L8

    def lookup(self, key: Key) -> int | None:
        """f(key) for key in S; None, or with probability 3 / 2^q a wrong value, otherwise."""
        cells, tau = self._tau(key)
        if tau < 3:  # @line L9
            return self.R[cells[tau]]
        return None  # @line L10

    def set(self, key: Key, value: int) -> None:
        """Change f(key) for a key in S. Precondition: key is in S."""
        if not 0 <= value < 1 << self.r:
            raise ValueError("value must fit in r bits")
        cells, tau = self._tau(key)  # @line L11
        if tau >= 3:
            raise KeyError(key)
        self.R[cells[tau]] = value
