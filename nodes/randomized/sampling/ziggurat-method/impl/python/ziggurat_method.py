# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ziggurat-method/. The authors are listed in prov/0RX5CX.jsonl.

"""The ziggurat method for standard normal variates (Marsaglia and Tsang, 2000).

The half density f(x) = exp(-x^2 / 2) on [0, inf) is covered by N layers of
equal area v: a base layer (a rectangle of width r and height f(r), plus the
tail x > r) and N - 1 rectangles stacked on it. A uniform layer and a uniform
point in it give a uniform point in the cover; the point is kept if it lies
under f. Most of the time the x coordinate alone decides.

The table is built from r. The method is exact (for exact arithmetic) when
the layers have equal area and cover the density. Marsaglia and Tsang publish
r = 3.442619855899 for N = 128; with that value the top layer falls short of
f(0) = 1 by about 4e-11, so here r is taken a little smaller, which makes the
top layer reach just above 1.
"""

import math
import random
from typing import List, Tuple

R_DEFAULT = 3.44261985589


def f(x: float) -> float:
    return math.exp(-0.5 * x * x)


def tail_area(r: float) -> float:
    """The area under f on (r, inf)."""
    return math.sqrt(math.pi / 2.0) * math.erfc(r / math.sqrt(2.0))


def build_table(n: int = 128, r: float = R_DEFAULT) -> Tuple[List[float], List[float], float]:
    """Return (x, y, v) for n layers.

    Layer 0 is the base: x coordinates in [0, x[0]) with x[0] = v / f(r); the
    part beyond x[1] = r stands for the tail. Layer i, 1 <= i <= n - 1, is the
    rectangle [0, x[i]] x [y[i], y[i + 1]] of area v. x[n] = 0 and y[n] >= 1.
    """
    v = r * f(r) + tail_area(r)
    x = [0.0] * (n + 1)
    y = [0.0] * (n + 1)
    x[0] = v / f(r)
    x[1] = r
    y[1] = f(r)
    for i in range(1, n - 1):
        y[i + 1] = y[i] + v / x[i]
        x[i + 1] = math.sqrt(-2.0 * math.log(y[i + 1]))
    y[n] = y[n - 1] + v / x[n - 1]
    x[n] = 0.0
    if y[n] < 1.0:
        raise ValueError("r is too large: the layers do not cover the density")
    return x, y, v


def normal_tail(r: float, rng: random.Random) -> float:
    """Marsaglia's tail method: a variate with density proportional to f on (r, inf)."""
    while True:  # @line T1
        e1 = -math.log(1.0 - rng.random()) / r  # @line T2
        e2 = -math.log(1.0 - rng.random())  # @line T2
        if 2.0 * e2 > e1 * e1:  # @line T3
            return r + e1  # @line T4


class Ziggurat:
    def __init__(self, n: int = 128, r: float = R_DEFAULT) -> None:
        self.n = n
        self.r = r
        self.x, self.y, self.v = build_table(n, r)

    def sample(self, rng: random.Random) -> float:
        """Return one standard normal variate."""
        x, y = self.x, self.y
        while True:  # @line L1
            i = rng.randrange(self.n)  # @line L2
            s = 1.0 if rng.random() < 0.5 else -1.0  # @line L2
            u = rng.random() * x[i]  # @line L3
            if u < x[i + 1]:  # @line L4
                return s * u  # @line L4
            if i == 0:  # @line L5
                return s * normal_tail(self.r, rng)  # @line L5
            h = y[i] + rng.random() * (y[i + 1] - y[i])  # @line L6
            if h < f(u):  # @line L7
                return s * u  # @line L7

    def sample_counted(self, rng: random.Random) -> Tuple[float, int, bool]:
        """Return (z, tries, fast) where fast is True if the first try took the fast path."""
        x, y = self.x, self.y
        tries = 0
        while True:
            tries += 1
            i = rng.randrange(self.n)
            s = 1.0 if rng.random() < 0.5 else -1.0
            u = rng.random() * x[i]
            if u < x[i + 1]:
                return s * u, tries, tries == 1
            if i == 0:
                return s * normal_tail(self.r, rng), tries, False
            h = y[i] + rng.random() * (y[i + 1] - y[i])
            if h < f(u):
                return s * u, tries, False
