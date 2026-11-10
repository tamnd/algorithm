# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flajolet-martin-algorithm/. The authors are listed in prov/YQ5W45.jsonl.
"""The Flajolet-Martin bitmap counter and the AMS variant with pairwise independent hashing."""

import random
from typing import Callable, Hashable, Iterable

PHI = 0.77351  # the bias correction constant of Flajolet and Martin (1985)


def rho(y: int, width: int) -> int:
    """Return the number of trailing zeros of the width-bit integer y (width if y == 0)."""
    if y == 0:
        return width
    return (y & -y).bit_length() - 1


def lowest_zero(bitmap: int) -> int:
    """Return the smallest index r with bit r of bitmap equal to 0."""
    return (~bitmap & (bitmap + 1)).bit_length() - 1


def fm_count(stream: Iterable[Hashable], h: Callable[[Hashable], int], width: int) -> float:
    """One pass of the Flajolet-Martin counter; return the estimate 2^R / PHI.

    h maps an item to a width-bit integer. The state is a bitmap of width + 1
    bits. Each item costs one hash and O(1) word operations.
    """
    bitmap = 0  # @line L1
    for x in stream:  # @line L2
        r = rho(h(x), width)  # @line L3
        bitmap |= 1 << r  # @line L4
    big_r = lowest_zero(bitmap)  # @line L5
    return 2**big_r / PHI  # @line L6


class FMSketch:
    """The Flajolet-Martin bitmap as an object that can add items and merge."""

    def __init__(self, h: Callable[[Hashable], int], width: int) -> None:
        self.h = h
        self.width = width
        self.bitmap = 0

    def add(self, x: Hashable) -> None:
        self.bitmap |= 1 << rho(self.h(x), self.width)

    def big_r(self) -> int:
        return lowest_zero(self.bitmap)

    def estimate(self) -> float:
        return 2 ** self.big_r() / PHI

    def merge(self, other: "FMSketch") -> "FMSketch":
        """Sketch of the union of both streams. Both sketches must use the same h."""
        if other.h is not self.h or other.width != self.width:
            raise ValueError("sketches use different hash functions")
        out = FMSketch(self.h, self.width)
        out.bitmap = self.bitmap | other.bitmap
        return out


class GF2AffineHash:
    """h(x) = A x + b over GF(2), with A a random L x L bit matrix and b a random vector.

    For each pair x != y of L-bit inputs, (h(x), h(y)) is uniform over all
    pairs of L-bit outputs, so the family is pairwise independent. The seed
    is L^2 + L random bits.
    """

    def __init__(self, bits: int, rng: random.Random) -> None:
        self.bits = bits
        self.columns = [rng.getrandbits(bits) for _ in range(bits)]
        self.offset = rng.getrandbits(bits)

    def __call__(self, x: int) -> int:
        if not 0 <= x < 1 << self.bits:
            raise ValueError("input out of range")
        y = self.offset
        j = 0
        while x:
            if x & 1:
                y ^= self.columns[j]
            x >>= 1
            j += 1
        return y


def ams_f0(stream: Iterable[int], h: GF2AffineHash) -> float:
    """The AMS estimate 2^(Z + 1/2), with Z the largest number of trailing zeros of h(x).

    With h pairwise independent and d >= 1 distinct items:
    P[estimate >= 3d] <= sqrt(2)/3 and P[estimate <= d/3] <= sqrt(2)/3.
    The state is Z (O(log log n) bits) and the seed of h (O(log^2 n) bits here).
    """
    z = -1
    for x in stream:
        z = max(z, rho(h(x), h.bits))
    if z < 0:
        return 0.0
    return 2 ** (z + 0.5)


def ams_median(stream: Iterable[int], hashes: list[GF2AffineHash]) -> float:
    """The median of the AMS estimates for an odd number of independent hash functions."""
    if len(hashes) % 2 == 0:
        raise ValueError("use an odd number of hash functions")
    items = list(stream)
    values = sorted(ams_f0(items, h) for h in hashes)
    return values[len(values) // 2]
