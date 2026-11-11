# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hellman-time-memory-tradeoff/. The authors are listed in prov/EQFZ4J.jsonl.
"""Hellman's time-memory trade-off: invert a one-way function with precomputed chain tables.

For study only. The code is not constant time, and it runs only on a toy
function on 20 to 24 bits. Do not use the toy function to protect real data;
store passwords with a salted memory-hard function such as Argon2 or scrypt
(for example from libsodium or the hashlib module).

N = 2^n points. ell tables of m chains of length t. Precomputation: m t ell
calls of f. Memory: m ell (start, end) pairs. Online: at most t ell calls of f,
plus the work of the false alarms.
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


class HellmanTables:
    """ell Hellman tables for f on {0, ..., 2^n - 1}; table i uses the reduction R_i."""

    def __init__(self, f: Callable[[int], int], n: int, m: int, t: int, ell: int, rng: random.Random) -> None:
        self.f, self.n, self.t = f, n, t
        self.mask = (1 << n) - 1
        self.tables: list[dict[int, int]] = []
        self.merges = 0  # chains lost because another chain had the same end point
        self.precomputation = 0
        for i in range(ell):  # @line L1
            table: dict[int, int] = {}  # @line L2
            for _ in range(m):  # @line L3
                start = rng.randrange(1 << n)  # @line L3
                x = start
                for _ in range(t):  # @line L4
                    x = self.reduce(i, f(x))  # @line L4
                self.precomputation += t
                if x in table:
                    self.merges += 1
                else:
                    table[x] = start  # @line L5
            self.tables.append(table)
        self.online_calls = 0
        self.false_alarms = 0
        self.lookups = 0

    def reduce(self, i: int, y: int) -> int:
        """R_i: XOR with a constant of table i, a different bijection for each table."""
        return (y ^ (i * 0x9E3779B1)) & self.mask

    def invert(self, y: int) -> int | None:
        """Return x with f(x) == y, or None."""
        f, t = self.f, self.t
        for i, table in enumerate(self.tables):  # @line L6
            z = self.reduce(i, y)  # @line L7
            for s in range(t):  # @line L8
                self.lookups += 1
                if z in table:  # @line L9
                    x = table[z]  # @line L9
                    for _ in range(t - 1 - s):  # @line L9
                        x = self.reduce(i, f(x))  # @line L9
                    self.online_calls += t - s
                    if f(x) == y:  # @line L9
                        return x  # @line L9
                    self.false_alarms += 1
                if s < t - 1:
                    z = self.reduce(i, f(z))  # @line L10
                    self.online_calls += 1
        return None  # @line L11


def hellman_coverage_bound(n: int, m: int, t: int) -> float:
    """Hellman's lower bound on the success of one table for a random point:
    (1/N) sum_{i=1}^{m} sum_{j=0}^{t-1} (1 - i t / N)^(j+1)."""
    big_n = float(1 << n)
    total = 0.0
    for i in range(1, m + 1):
        r = 1.0 - i * t / big_n
        if r <= 0:
            break
        # geometric sum r + r^2 + ... + r^t
        total += r * (1 - r**t) / (1 - r) if r < 1 else t
    return total / big_n
