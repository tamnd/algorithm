# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-counting/. The authors are listed in prov/738TN4.jsonl.
"""Linear counting (Whang, Vander-Zanden and Taylor 1990)."""

import math
from typing import Callable, Hashable, Iterable


def linear_count(stream: Iterable[Hashable], m: int, h: Callable[[Hashable], int]) -> float:
    """One pass over the stream with an m-bit bitmap; return m ln(m / U).

    h maps an item to a position in [0, m). U is the number of 0 bits at the
    end. If U == 0 the bitmap is full and the estimate is infinite.
    """
    bitmap = bytearray(m)  # @line L1
    for x in stream:  # @line L2
        j = h(x)  # @line L3
        bitmap[j] = 1  # @line L4
    u = m - sum(bitmap)  # @line L5
    return estimate_from_empty(m, u)  # @line L6


def estimate_from_empty(m: int, u: int) -> float:
    """The linear counting estimate m ln(m / u) for u empty positions out of m."""
    if not 0 <= u <= m:
        raise ValueError("u must be in 0 .. m")
    if u == 0:
        return math.inf
    return m * math.log(m / u)


class LinearCounter:
    """The bitmap as an object: add items, merge by OR, and query.

    The state is m bits plus the hash seed. An update costs one hash and
    O(1) work; a query costs O(m) (or O(1) with a running count of 1 bits).
    """

    def __init__(self, m: int, h: Callable[[Hashable], int]) -> None:
        if m < 1:
            raise ValueError("m must be positive")
        self.m = m
        self.h = h
        self.bitmap = bytearray(m)
        self.ones = 0

    def add(self, x: Hashable) -> None:
        j = self.h(x)
        if not self.bitmap[j]:
            self.bitmap[j] = 1
            self.ones += 1

    def add_all(self, stream: Iterable[Hashable]) -> None:
        for x in stream:
            self.add(x)

    def empty(self) -> int:
        return self.m - self.ones

    def estimate(self) -> float:
        return estimate_from_empty(self.m, self.empty())

    def merge(self, other: "LinearCounter") -> "LinearCounter":
        """The sketch of the union: the bitwise OR (same m and the same hash)."""
        if other.m != self.m or other.h is not self.h:
            raise ValueError("sketches are not compatible")
        out = LinearCounter(self.m, self.h)
        out.bitmap = bytearray(a | b for a, b in zip(self.bitmap, other.bitmap))
        out.ones = sum(out.bitmap)
        return out


def empty_moments(m: int, n: int) -> tuple[float, float]:
    """Exact E[U] and Var(U) for n distinct items hashed uniformly into m positions."""
    q1 = (1 - 1 / m) ** n
    q2 = (1 - 2 / m) ** n
    mean = m * q1
    var = m * (m - 1) * q2 + m * q1 - m * m * q1 * q1
    return mean, var


def asymptotic_bias(m: int, n: int) -> float:
    """Whang et al.: E[estimate] - n is about (e^t - t - 1) / 2 with load t = n / m."""
    t = n / m
    return (math.exp(t) - t - 1) / 2


def asymptotic_standard_error(m: int, n: int) -> float:
    """Whang et al.: the standard error of estimate / n is about sqrt(m (e^t - t - 1)) / n."""
    t = n / m
    return math.sqrt(m * (math.exp(t) - t - 1)) / n
