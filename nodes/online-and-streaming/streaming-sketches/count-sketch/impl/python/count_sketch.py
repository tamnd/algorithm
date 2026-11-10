# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/count-sketch/. The authors are listed in prov/2S6HW2.jsonl.

import math
import random

MERSENNE_61 = (1 << 61) - 1


def parity_sign(a: int, b: int, x: int) -> int:
    """s(x) = (-1)^(<a, x> xor b) over the bits of x: a pairwise independent sign."""
    return -1 if ((a & x).bit_count() + b) & 1 else 1


class CountSketch:
    """The count sketch of Charikar, Chen and Farach-Colton over items 0 .. P-1.

    d rows of w counters. Row j has a bucket hash h_j(x) = ((a x + b) mod P) mod w
    from a universal family and a sign s_j(x) from a pairwise independent family.
    Each row gives the unbiased estimate s_j(x) C[j][h_j(x)] with variance at most
    (||f||_2^2 - f_x^2) / w, and the query is the median of the rows. With
    w = ceil(3/eps^2) and d = ceil(18 ln(1/delta)) the error is at most
    eps * ||f||_2 with probability at least 1 - delta, in the general turnstile model.
    """

    def __init__(self, w: int, d: int, rng: random.Random, prime: int = MERSENNE_61) -> None:
        if w < 1 or d < 1:
            raise ValueError("w and d must be at least 1")
        self.w, self.d, self.prime = w, d, prime
        self.buckets = [(rng.randrange(1, prime), rng.randrange(prime)) for _ in range(d)]
        bits = prime.bit_length()
        self.signs = [(rng.getrandbits(bits), rng.getrandbits(1)) for _ in range(d)]
        self.table = [[0] * w for _ in range(d)]

    @classmethod
    def from_error(cls, eps: float, delta: float, rng: random.Random, prime: int = MERSENNE_61):
        """w = ceil(3/eps^2) and d = ceil(18 ln(1/delta))."""
        if not (0 < eps and 0 < delta < 1):
            raise ValueError("need eps > 0 and 0 < delta < 1")
        return cls(math.ceil(3 / eps**2), math.ceil(18 * math.log(1 / delta)), rng, prime)

    def _check(self, x: int) -> None:
        if not 0 <= x < self.prime:
            raise ValueError("items must be integers in [0, prime)")

    def h(self, j: int, x: int) -> int:
        a, b = self.buckets[j]
        return ((a * x + b) % self.prime) % self.w

    def s(self, j: int, x: int) -> int:
        a, b = self.signs[j]
        return parity_sign(a, b, x)

    def empty_like(self) -> "CountSketch":
        """A zero sketch with the same hash functions."""
        out = CountSketch.__new__(CountSketch)
        out.w, out.d, out.prime = self.w, self.d, self.prime
        out.buckets, out.signs = self.buckets, self.signs
        out.table = [[0] * self.w for _ in range(self.d)]
        return out

    def update(self, x: int, c: int = 1) -> None:
        """Add c to f_x; c may be negative."""
        self._check(x)
        for j in range(self.d):  # @line L1
            self.table[j][self.h(j, x)] += self.s(j, x) * c  # @line L2

    def row_estimates(self, x: int) -> list[int]:
        self._check(x)
        return [self.s(j, x) * self.table[j][self.h(j, x)] for j in range(self.d)]  # @line L3

    def estimate(self, x: int) -> int:
        """The lower median of the row estimates (the median when d is odd)."""
        e = sorted(self.row_estimates(x))
        return e[(self.d + 1) // 2 - 1]  # @line L4

    def _same_hashes(self, other: "CountSketch") -> None:
        if (self.w, self.d, self.prime, self.buckets, self.signs) != (
            other.w, other.d, other.prime, other.buckets, other.signs
        ):
            raise ValueError("the sketches must share w, d and the hash functions")

    def merge(self, other: "CountSketch") -> "CountSketch":
        """The sketch of f + g."""
        self._same_hashes(other)
        out = self.empty_like()
        for j in range(self.d):  # @line L5
            out.table[j] = [u + v for u, v in zip(self.table[j], other.table[j])]  # @line L5
        return out

    def subtract(self, other: "CountSketch") -> "CountSketch":
        """The sketch of f - g."""
        self._same_hashes(other)
        out = self.empty_like()
        for j in range(self.d):
            out.table[j] = [u - v for u, v in zip(self.table[j], other.table[j])]
        return out
