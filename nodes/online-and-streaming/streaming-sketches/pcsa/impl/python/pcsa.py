# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pcsa/. The authors are listed in prov/1T1SSZ.jsonl.
"""Probabilistic counting with stochastic averaging (Flajolet and Martin 1985)."""

from typing import Callable, Hashable, Iterable

PHI = 0.77351  # the bias correction constant of Flajolet and Martin


def rho(y: int, width: int) -> int:
    """Number of trailing zeros of the width-bit integer y (width if y == 0)."""
    if y == 0:
        return width
    return (y & -y).bit_length() - 1


def lowest_zero(bitmap: int) -> int:
    """Smallest index r with bit r of bitmap equal to 0."""
    return (~bitmap & (bitmap + 1)).bit_length() - 1


class PCSA:
    """m Flajolet-Martin bitmaps; each item updates only the bitmap that its hash selects.

    h maps an item to an integer of hash_bits bits. The state is m bitmaps of
    about hash_bits - log2(m) bits each. An update costs one hash and O(1)
    word operations; a query costs O(m).
    """

    def __init__(self, m: int, h: Callable[[Hashable], int], hash_bits: int = 64) -> None:
        if m < 1:
            raise ValueError("m must be positive")
        self.m = m
        self.h = h
        self.hash_bits = hash_bits
        self.width = hash_bits - (m - 1).bit_length()
        self.bitmaps = [0] * m  # @line L1

    def add(self, x: Hashable) -> None:
        y = self.h(x)  # @line L3
        j, w = y % self.m, y // self.m  # @line L4
        self.bitmaps[j] |= 1 << rho(w, self.width)  # @line L5

    def add_all(self, stream: Iterable[Hashable]) -> None:
        for x in stream:  # @line L2
            self.add(x)

    def estimate(self) -> float:
        s = sum(lowest_zero(b) for b in self.bitmaps)  # @line L6
        return self.m / PHI * 2 ** (s / self.m)  # @line L7

    def merge(self, other: "PCSA") -> "PCSA":
        """The sketch of the union of both streams (same m and the same hash function)."""
        if other.m != self.m or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = PCSA(self.m, self.h, self.hash_bits)
        out.bitmaps = [a | b for a, b in zip(self.bitmaps, other.bitmaps)]
        return out
