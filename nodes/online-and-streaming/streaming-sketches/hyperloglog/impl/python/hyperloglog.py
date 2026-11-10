# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperloglog/. The authors are listed in prov/ZE356T.jsonl.
"""HyperLogLog (Flajolet, Fusy, Gandouet and Meunier 2007), the 32-bit program of their Figure 3."""

import math
from typing import Callable, Hashable, Iterable

TWO_32 = float(1 << 32)


def alpha(m: int) -> float:
    """The constant alpha_m of the 32-bit program (m = 16, 32, 64, or m >= 128)."""
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    if m >= 128:
        return 0.7213 / (1.0 + 1.079 / m)
    raise ValueError("m must be 16, 32, 64 or at least 128")


def rho_left(w: int, width: int) -> int:
    """Position of the leftmost 1 in the width-bit string w, counted from 1 (width + 1 if w == 0)."""
    return width - w.bit_length() + 1


def raw_estimate(registers: list[int]) -> float:
    """The harmonic mean estimate alpha_m m^2 / sum 2^(-M[j])."""
    m = len(registers)
    z = sum(2.0 ** (-r) for r in registers)
    return alpha(m) * m * m / z


def corrected_estimate(registers: list[int]) -> float:
    """The raw estimate with the small range and the large range corrections."""
    m = len(registers)
    e = raw_estimate(registers)
    if e <= 2.5 * m:
        v = registers.count(0)
        if v != 0:
            return m * math.log(m / v)
        return e
    if e <= TWO_32 / 30.0:
        return e
    return -TWO_32 * math.log(1.0 - e / TWO_32)


class HyperLogLog:
    """m = 2^b registers of 5 bits; the query is a harmonic mean of 2^M[j].

    h maps an item to a 32-bit integer and is assumed to behave as a fully
    random function. An update costs one hash and O(1) word operations; a
    query costs O(m). The space is 5m bits plus the hash seed.
    """

    HASH_BITS = 32

    def __init__(self, b: int, h: Callable[[Hashable], int]) -> None:
        if not 4 <= b <= 16:
            raise ValueError("b must be in 4 .. 16")
        self.b = b
        self.m = 1 << b
        self.h = h
        self.width = self.HASH_BITS - b
        self.registers = [0] * self.m  # @line L1

    def add(self, x: Hashable) -> None:
        y = self.h(x)  # @line L3
        j, w = y >> self.width, y & ((1 << self.width) - 1)  # @line L4
        r = rho_left(w, self.width)
        if r > self.registers[j]:  # @line L5
            self.registers[j] = r

    def add_all(self, stream: Iterable[Hashable]) -> None:
        for x in stream:  # @line L2
            self.add(x)

    def raw(self) -> float:
        return raw_estimate(self.registers)  # @line L6

    def estimate(self) -> float:
        return corrected_estimate(self.registers)  # @line L7

    def merge(self, other: "HyperLogLog") -> "HyperLogLog":
        """The sketch of the union: the register-wise maximum (same b and the same hash)."""
        if other.b != self.b or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = HyperLogLog(self.b, self.h)
        out.registers = [max(p, q) for p, q in zip(self.registers, other.registers)]
        return out
