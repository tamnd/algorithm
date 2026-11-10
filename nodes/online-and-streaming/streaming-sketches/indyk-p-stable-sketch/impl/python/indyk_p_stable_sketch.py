# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indyk-p-stable-sketch/. The authors are listed in prov/RGY2FY.jsonl.

"""Indyk's p-stable sketch for the l_p norm of a frequency vector, 0 < p <= 2.

The sketch keeps k counters y_j = sum_i X[j][i] f_i, where the X[j][i] are
independent standard p-stable variables. Each y_j has the law of ||f||_p X,
so median_j |y_j| divided by the median of |X| estimates ||f||_p, and its
p-th power estimates F_p = sum_i |f_i|^p.

The column X[.][i] is made again from a seed each time item i arrives, so
the matrix is never stored. Indyk used a pseudorandom generator for this;
here a seeded random.Random stands in for it.
"""

import math
import random
from statistics import NormalDist

# The median of |X| for the standard law with characteristic function exp(-|t|^p).
MEDIAN_ABS = {1.0: 1.0, 2.0: math.sqrt(2) * NormalDist().inv_cdf(0.75)}


def stable_sample(p: float, rng: random.Random) -> float:
    """A standard symmetric p-stable draw by the Chambers-Mallows-Stuck method."""
    theta = math.pi * (rng.random() - 0.5)
    while theta == -math.pi / 2:
        theta = math.pi * (rng.random() - 0.5)
    if p == 1:
        return math.tan(theta)
    w = rng.expovariate(1.0)
    while w == 0.0:
        w = rng.expovariate(1.0)
    return (
        math.sin(p * theta)
        / math.cos(theta) ** (1 / p)
        * (math.cos((1 - p) * theta) / w) ** ((1 - p) / p)
    )


def estimate_median_abs(p: float, rng: random.Random, samples: int = 20001) -> float:
    """A Monte Carlo value of the median of |X|, for p without a closed form."""
    xs = sorted(abs(stable_sample(p, rng)) for _ in range(samples))
    return xs[samples // 2]


def rows_for(eps: float, delta: float) -> int:
    """k for p = 1: ceil(ln(2/delta) * 25 pi^2 / (8 eps^2)), from the proof."""
    return math.ceil(math.log(2 / delta) * 25 * math.pi**2 / (8 * eps * eps))


def lower_median(values: list[float]) -> float:
    s = sorted(values)
    return s[(len(s) + 1) // 2 - 1]


class StableSketch:
    def __init__(self, p: float, k: int, rng: random.Random, median_abs: float | None = None, column=None) -> None:
        if not 0 < p <= 2:
            raise ValueError("p must be in (0, 2]")
        self.p = float(p)
        self.k = k
        # The seed of the random matrix; every column is made from it on demand.
        self.seed = rng.getrandbits(64)
        if median_abs is None:
            if self.p not in MEDIAN_ABS:
                raise ValueError("give median_abs for this p")
            median_abs = MEDIAN_ABS[self.p]
        self.median_abs = median_abs
        # column(i) returns the list X[0][i], ..., X[k-1][i]; a test may pass a fixed matrix.
        self._custom = column
        self._column = column if column is not None else self._seeded_column
        self.y = [0.0] * k

    def _seeded_column(self, item) -> list[float]:
        rng = random.Random(f"{self.seed}:{item}")
        return [stable_sample(self.p, rng) for _ in range(self.k)]

    def empty_like(self) -> "StableSketch":
        """A zero sketch with the same random matrix."""
        out = object.__new__(StableSketch)
        out.__dict__.update(self.__dict__)
        out._column = self._custom if self._custom is not None else out._seeded_column
        out.y = [0.0] * self.k
        return out

    def update(self, item, c: float = 1) -> None:
        col = self._column(item)
        y = self.y
        for j in range(self.k):  # @line L1
            y[j] += c * col[j]  # @line L2

    def norm(self) -> float:
        """The estimate of ||f||_p."""
        return lower_median([abs(v) for v in self.y]) / self.median_abs  # @line L3

    def moment(self) -> float:
        """The estimate of F_p = ||f||_p^p."""
        return self.norm() ** self.p  # @line L4

    def merge(self, other: "StableSketch") -> "StableSketch":
        same = (self.p, self.k, self.seed) == (other.p, other.k, other.seed) and self._custom is other._custom
        if not same:
            raise ValueError("sketches must share p, k and the random matrix")
        out = self.empty_like()
        out.y = [a + b for a, b in zip(self.y, other.y)]  # @line L5
        return out
