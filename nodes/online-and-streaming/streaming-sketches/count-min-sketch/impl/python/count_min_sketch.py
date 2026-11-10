# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/count-min-sketch/. The authors are listed in prov/4BWT77.jsonl.

import math
import random

MERSENNE_61 = (1 << 61) - 1


class CountMinSketch:
    """The count-min sketch of Cormode and Muthukrishnan over items 0 .. P-1.

    d rows of w counters, with h_j(x) = ((a_j x + b_j) mod P) mod w drawn from
    a universal family. In the strict turnstile model (all counts >= 0) the
    estimate satisfies f_x <= estimate(x), and with w = ceil(e/eps) and
    d = ceil(ln(1/delta)) also estimate(x) <= f_x + eps * ||f||_1 with
    probability at least 1 - delta. The sketch is linear: sketches with the
    same hash functions can be added and subtracted.
    """

    def __init__(self, w: int, d: int, rng: random.Random, prime: int = MERSENNE_61) -> None:
        if w < 1 or d < 1:
            raise ValueError("w and d must be at least 1")
        self.w, self.d, self.prime = w, d, prime
        self.hashes = [(rng.randrange(1, prime), rng.randrange(prime)) for _ in range(d)]
        self.table = [[0] * w for _ in range(d)]
        self.total = 0  # ||f||_1 in the strict turnstile model

    @classmethod
    def from_error(cls, eps: float, delta: float, rng: random.Random, prime: int = MERSENNE_61):
        """w = ceil(e/eps) and d = ceil(ln(1/delta))."""
        if not (0 < eps and 0 < delta < 1):
            raise ValueError("need eps > 0 and 0 < delta < 1")
        return cls(math.ceil(math.e / eps), math.ceil(math.log(1 / delta)), rng, prime)

    def _h(self, j: int, x: int) -> int:
        a, b = self.hashes[j]
        return ((a * x + b) % self.prime) % self.w

    def _check(self, x: int) -> None:
        if not 0 <= x < self.prime:
            raise ValueError("items must be integers in [0, prime)")

    def empty_like(self) -> "CountMinSketch":
        """A zero sketch with the same hash functions."""
        out = CountMinSketch.__new__(CountMinSketch)
        out.w, out.d, out.prime = self.w, self.d, self.prime
        out.hashes = self.hashes
        out.table = [[0] * self.w for _ in range(self.d)]
        out.total = 0
        return out

    def update(self, x: int, c: int = 1) -> None:
        """Add c to f_x (c may be negative in the turnstile model)."""
        self._check(x)
        self.total += c
        for j in range(self.d):  # @line L1
            self.table[j][self._h(j, x)] += c  # @line L2

    def estimate(self, x: int) -> int:
        """min over the rows: never below f_x when all counts are >= 0."""
        self._check(x)
        return min(self.table[j][self._h(j, x)] for j in range(self.d))  # @line L3

    def update_conservative(self, x: int, c: int = 1) -> None:
        """Conservative update: raise each counter of x only as far as needed.

        Only for c > 0 (the cash register model). Each counter stays at most
        the counter of plain updates, and estimate(x) stays >= f_x.
        """
        if c <= 0:
            raise ValueError("conservative update needs c > 0")
        self._check(x)
        self.total += c
        v = self.estimate(x) + c  # @line L4
        for j in range(self.d):  # @line L5
            b = self._h(j, x)
            self.table[j][b] = max(self.table[j][b], v)  # @line L6

    def _same_hashes(self, other: "CountMinSketch") -> None:
        if (self.w, self.d, self.prime, self.hashes) != (other.w, other.d, other.prime, other.hashes):
            raise ValueError("the sketches must share w, d and the hash functions")

    def merge(self, other: "CountMinSketch") -> "CountMinSketch":
        """The sketch of the sum of the two frequency vectors."""
        self._same_hashes(other)
        out = self.empty_like()
        for j in range(self.d):  # @line L7
            out.table[j] = [u + v for u, v in zip(self.table[j], other.table[j])]  # @line L7
        out.total = self.total + other.total
        return out

    def subtract(self, other: "CountMinSketch") -> "CountMinSketch":
        """The sketch of the difference of the two frequency vectors."""
        self._same_hashes(other)
        out = self.empty_like()
        for j in range(self.d):
            out.table[j] = [u - v for u, v in zip(self.table[j], other.table[j])]
        out.total = self.total - other.total
        return out


class DyadicCountMin:
    """Range queries over items 0 .. 2^levels - 1 with one sketch per level.

    Level l counts the dyadic interval x >> l. A range [lo, hi] splits into at
    most 2 * levels dyadic intervals, and the sum of their estimates is at
    least the true range sum and at most it plus 2 * levels * eps * ||f||_1,
    with probability at least 1 - 2 * levels * delta.
    """

    def __init__(self, levels: int, w: int, d: int, rng: random.Random) -> None:
        self.levels = levels
        self.sketches = [CountMinSketch(w, d, rng) for _ in range(levels + 1)]

    def update(self, x: int, c: int = 1) -> None:
        if not 0 <= x < (1 << self.levels):
            raise ValueError("item out of range")
        for lev, sk in enumerate(self.sketches):
            sk.update(x >> lev, c)

    @staticmethod
    def dyadic_cover(lo: int, hi: int) -> list[tuple[int, int]]:
        """The canonical cover of [lo, hi] by dyadic intervals, as (level, index)."""
        out = []
        while lo <= hi:
            lev = 0
            while lo % (1 << (lev + 1)) == 0 and lo + (1 << (lev + 1)) - 1 <= hi:
                lev += 1
            out.append((lev, lo >> lev))
            lo += 1 << lev
        return out

    def range_query(self, lo: int, hi: int) -> int:
        return sum(self.sketches[lev].estimate(i) for lev, i in self.dyadic_cover(lo, hi))
