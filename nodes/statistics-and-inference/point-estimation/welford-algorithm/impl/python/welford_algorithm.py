# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/welford-algorithm/. The authors are listed in prov/3F3F57.jsonl.

from collections.abc import Iterable, Sequence


def welford_algorithm(xs: Sequence[float]) -> tuple[float, float, float]:
    """Return (M, V, S) for the data xs in one pass.

    M is the mean, S the sum of squared deviations from M, and V = S / (n - 1)
    the sample variance. Precondition: len(xs) >= 2. Cost: 6 n + 1 arithmetic
    operations and O(1) extra memory. Exact for Fraction inputs.
    """
    n = len(xs)
    if n < 2:
        raise ValueError("need at least two values")
    m, s = 0 * xs[0], 0 * xs[0]  # @line L1
    for k in range(1, n + 1):  # @line L2
        x = xs[k - 1]
        d = x - m  # @line L3
        m = m + d / k  # @line L4
        s = s + d * (x - m)  # @line L5
    v = s / (n - 1)  # @line L6
    return m, v, s  # @line L7


class RunningVariance:
    """Welford's update as an online accumulator.

    push costs O(1) time; the object holds three numbers. After k pushes,
    mean is the mean of the k values and ss their sum of squared deviations.
    """

    def __init__(self) -> None:
        self.count = 0
        self.mean: float = 0  # an int 0 keeps Fraction inputs exact
        self.ss: float = 0

    def push(self, x: float) -> None:
        """Add one value."""
        self.count += 1
        d = x - self.mean
        self.mean = self.mean + d / self.count
        self.ss = self.ss + d * (x - self.mean)

    def extend(self, xs: Iterable[float]) -> None:
        """Add every value of xs, in order."""
        for x in xs:
            self.push(x)

    def variance(self, ddof: int = 1) -> float:
        """Return ss / (count - ddof): ddof = 1 gives S^2, ddof = 0 the divisor-n variance."""
        if self.count - ddof <= 0:
            raise ValueError("too few values for this divisor")
        return self.ss / (self.count - ddof)
