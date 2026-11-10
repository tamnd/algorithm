# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-counter/. The authors are listed in prov/V4GE3S.jsonl.
"""The Morris approximate counter, its exact distribution, Morris+ and Morris++."""

import math
import random
from fractions import Fraction
from typing import Iterable


def morris_counter(stream: Iterable[object], rng: random.Random) -> int:
    """Run the Morris counter of the page on a stream and return the estimate 2^X - 1.

    The items of the stream are ignored: only their number counts. Each event
    costs O(1) expected time and X random bits; the state is the integer X.
    """
    x = 0  # @line L1
    for _ in stream:  # @line L2
        bits = rng.getrandbits(x)  # @line L3
        if bits == 0:  # @line L4
            x += 1
    return 2**x - 1  # @line L5


class MorrisCounter:
    """Morris counter with base 1 + a (a = 1 is the original counter).

    increment() raises X by one with probability (1 + a)^(-X).
    estimate() returns ((1 + a)^X - 1) / a, which is unbiased with variance
    a n (n - 1) / 2 after n increments.
    """

    def __init__(self, rng: random.Random, a: float = 1.0) -> None:
        if a <= 0:
            raise ValueError("a must be positive")
        self.rng = rng
        self.a = a
        self.x = 0

    def _p(self) -> float:
        return (1.0 + self.a) ** (-self.x)

    def increment(self) -> None:
        if self.a == 1.0:
            if self.rng.getrandbits(self.x) == 0:
                self.x += 1
        elif self.rng.random() < self._p():
            self.x += 1

    def increment_by(self, k: int) -> None:
        """Apply k increments. Same distribution as k calls of increment().

        The gap to the next raise of X is geometric with parameter
        p = (1 + a)^(-X), so the method draws the gap directly.
        Expected time O(X + 1) instead of O(k).
        """
        while k > 0:
            p = self._p()
            if p >= 1.0:
                self.x += 1
                k -= 1
                continue
            u = self.rng.random()
            gap = int(math.log1p(-u) / math.log1p(-p)) + 1
            if gap > k:
                return
            self.x += 1
            k -= gap

    def estimate(self) -> float:
        return ((1.0 + self.a) ** self.x - 1.0) / self.a


def exact_distribution(n: int, a: Fraction = Fraction(1)) -> list[Fraction]:
    """Return P[X = x] for x = 0 .. n after n increments, as exact fractions."""
    dist = [Fraction(1)] + [Fraction(0)] * n
    for t in range(n):
        new = [Fraction(0)] * (n + 1)
        for x in range(t + 1):
            px = dist[x]
            if px == 0:
                continue
            q = (1 + a) ** (-x)
            new[x] += px * (1 - q)
            new[x + 1] += px * q
        dist = new
    return dist


def morris_plus(n: int, s: int, rng: random.Random, a: float = 1.0) -> float:
    """Morris+: the mean of s independent counters, each incremented n times."""
    total = 0.0
    for _ in range(s):
        c = MorrisCounter(rng, a)
        c.increment_by(n)
        total += c.estimate()
    return total / s


def morris_plus_plus(n: int, s: int, t: int, rng: random.Random) -> float:
    """Morris++: the median of t independent Morris+ estimates (t odd)."""
    if t % 2 == 0:
        raise ValueError("t must be odd")
    values = sorted(morris_plus(n, s, rng) for _ in range(t))
    return values[t // 2]


def copies_for(eps: float, delta: float) -> tuple[int, int]:
    """Return (s, t) so that Morris++ is an (eps, delta) approximation.

    s = ceil(3 / (2 eps^2)) makes one Morris+ fail with probability below 1/3
    (Chebyshev). t is the smallest odd integer with (8/9)^(t/2) <= delta
    (the Chernoff bound of the median trick).
    """
    s = math.ceil(3.0 / (2.0 * eps * eps))
    t = math.ceil(2.0 * math.log(1.0 / delta) / math.log(9.0 / 8.0))
    if t % 2 == 0:
        t += 1
    return s, t
