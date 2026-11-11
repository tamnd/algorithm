# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rainbow-table/. The authors are listed in prov/W2QHWJ.jsonl.
"""Rainbow tables (Oechslin 2003), with Hellman tables for comparison.

For study only. The code is not constant time, and it runs only on a toy
function on 16 to 24 bits. Do not use the toy function to protect real data;
store passwords with a salted memory-hard function such as Argon2 or scrypt
(for example from libsodium or the hashlib module).

A rainbow table holds m chains x_0 -> x_1 -> ... -> x_t with
x_{j+1} = R_j(f(x_j)), and stores only the pairs (x_t, x_0), keyed by x_t.
Build: m t calls of f. Lookup: at most t(t-1)/2 calls of f and t table
lookups, plus false alarms.
"""

import random
from typing import Callable

M64 = (1 << 64) - 1


def toy_oneway(x: int, n: int, key: int = 0x5EED) -> int:
    """A toy one-way function on n-bit values (a 64-bit mixer, top n bits kept)."""
    z = ((key << 32) ^ x) & M64
    z = (z + 0x9E3779B97F4A7C15) & M64
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    z ^= z >> 31
    return z >> (64 - n)


class RainbowTable:
    """A rainbow table for f on {0, ..., 2^n - 1} with chains of length t."""

    def __init__(self, f: Callable[[int], int], n: int, t: int) -> None:
        self.f, self.n, self.t = f, n, t
        self.mask = (1 << n) - 1
        self.ends: dict[int, int] = {}  # end point -> start point
        self.f_calls = 0
        self.lookups = 0
        self.false_alarms = 0
        self.merged = 0  # chains dropped because their end point was already present

    def reduce(self, j: int, y: int) -> int:
        """R_j: the reduction of column j (XOR with a constant of the column)."""
        return (y ^ (j * 0x9E3779B1)) & self.mask

    def add_chain(self, start: int) -> bool:
        """Compute the chain from start and store (end, start). Return False if the end was present."""
        x = start
        for j in range(self.t):  # @line L1
            x = self.reduce(j, self.f(x))  # @line L2
        self.f_calls += self.t
        if x in self.ends:  # @line L3
            self.merged += 1
            return False
        self.ends[x] = start  # @line L4
        return True

    def lookup(self, y: int) -> int | None:
        """Return x with f(x) == y, or None. Tries the last column first."""
        f, t = self.f, self.t
        for j in range(t - 1, -1, -1):  # @line L5
            z = self.reduce(j, y)  # @line L6
            for c in range(j + 1, t):  # @line L7
                z = self.reduce(c, f(z))  # @line L7
            self.f_calls += t - 1 - j
            self.lookups += 1
            if z in self.ends:  # @line L8
                x = self.ends[z]  # @line L9
                for c in range(j):  # @line L9
                    x = self.reduce(c, f(x))  # @line L9
                self.f_calls += j + 1
                if f(x) == y:  # @line L10
                    return x  # @line L10
                self.false_alarms += 1
        return None  # @line L11

    def check_invariant(self) -> bool:
        """Each stored start point leads to its end point."""
        for end, start in self.ends.items():
            x = start
            for j in range(self.t):
                x = self.reduce(j, self.f(x))
            if x != end:
                return False
        return True


def build_rainbow(f: Callable[[int], int], n: int, m: int, t: int, rng: random.Random) -> RainbowTable:
    """A rainbow table with m random start points."""
    rt = RainbowTable(f, n, t)
    for _ in range(m):
        rt.add_chain(rng.randrange(1 << n))
    return rt


def rainbow_success(n: int, m: int, t: int) -> float:
    """Oechslin's success probability 1 - prod_{i=1}^{t} (1 - m_i / N), m_1 = m, m_{i+1} = N (1 - exp(-m_i / N))."""
    import math

    big_n = float(1 << n)
    mi = float(m)
    miss = 1.0
    for _ in range(t):
        miss *= 1.0 - mi / big_n
        mi = big_n * (1.0 - math.exp(-mi / big_n))
    return 1.0 - miss


class HellmanTables:
    """ell classic Hellman tables of m chains of length t, one reduction per table, for comparison."""

    def __init__(self, f: Callable[[int], int], n: int, m: int, t: int, ell: int, rng: random.Random) -> None:
        self.f, self.t = f, t
        self.mask = (1 << n) - 1
        self.tables: list[dict[int, int]] = []
        self.f_calls = 0
        self.lookups = 0
        self.false_alarms = 0
        for i in range(ell):
            table: dict[int, int] = {}
            for _ in range(m):
                start = x = rng.randrange(1 << n)
                for _ in range(t):
                    x = self.reduce(i, f(x))
                self.f_calls += t
                table.setdefault(x, start)
            self.tables.append(table)

    def reduce(self, i: int, y: int) -> int:
        return (y ^ (i * 0x9E3779B1)) & self.mask

    def lookup(self, y: int) -> int | None:
        f, t = self.f, self.t
        for i, table in enumerate(self.tables):
            z = self.reduce(i, y)
            for s in range(t):
                self.lookups += 1
                if z in table:
                    x = table[z]
                    for _ in range(t - 1 - s):
                        x = self.reduce(i, f(x))
                    self.f_calls += t - s
                    if f(x) == y:
                        return x
                    self.false_alarms += 1
                if s < t - 1:
                    z = self.reduce(i, f(z))
                    self.f_calls += 1
        return None
