# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loglog-counting/. The authors are listed in prov/919CZB.jsonl.
"""LogLog counting (Durand and Flajolet 2003)."""

import math
from typing import Callable, Hashable, Iterable

ALPHA_INF = 0.39701  # e^(-gamma) sqrt(2) / 2


def alpha(m: int) -> float:
    """The bias constant alpha_m = (Gamma(-1/m) (1 - 2^(1/m)) / ln 2)^(-m)."""
    return (math.gamma(-1.0 / m) * (1.0 - 2.0 ** (1.0 / m)) / math.log(2.0)) ** (-m)


def rho_left(w: int, width: int) -> int:
    """Position of the leftmost 1 in the width-bit string w, counted from 1 (width + 1 if w == 0)."""
    return width - w.bit_length() + 1


class LogLog:
    """m = 2^b registers; each keeps the largest rho of the hashes routed to it.

    h maps an item to a 32-bit integer. Each register needs about
    log2 log2 n bits (5 bits for a 32-bit hash). An update costs one hash and
    O(1) word operations; a query costs O(m).
    """

    HASH_BITS = 32

    def __init__(self, b: int, h: Callable[[Hashable], int]) -> None:
        if not 1 <= b <= 16:
            raise ValueError("b must be in 1 .. 16")
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

    def estimate(self) -> float:
        mean = sum(self.registers) / self.m
        return alpha(self.m) * self.m * 2.0**mean  # @line L6

    def merge(self, other: "LogLog") -> "LogLog":
        """The sketch of the union: the register-wise maximum (same b and the same hash)."""
        if other.b != self.b or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = LogLog(self.b, self.h)
        out.registers = [max(p, q) for p, q in zip(self.registers, other.registers)]
        return out
