# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chan-parallel-variance/. The authors are listed in prov/EJXH8E.jsonl.

from collections.abc import Sequence
from typing import NamedTuple


class Summary(NamedTuple):
    """Count n, mean and sum of squared deviations m2 of a nonempty part."""

    n: int
    mean: float
    m2: float


def combine(a: Summary, b: Summary) -> Summary:
    """Return the summary of the union of the parts summarized by a and b.

    Precondition: a.n >= 0, b.n >= 0; a part with n = 0 is the identity.
    Cost: 10 arithmetic operations. Exact for Fraction means and sums.
    """
    if a.n == 0:
        return b
    if b.n == 0:
        return a
    n = a.n + b.n  # @line L1
    delta = b.mean - a.mean  # @line L2
    mean = a.mean + delta * b.n / n  # @line L3
    m2 = a.m2 + b.m2 + delta * delta * a.n * b.n / n  # @line L4
    return Summary(n, mean, m2)  # @line L5


def summarize(xs: Sequence[float], lo: int = 0, hi: int | None = None) -> Summary:
    """Summary of xs[lo:hi] by pairwise merging. Precondition: hi - lo >= 1.

    Cost: Theta(hi - lo) operations and Theta(log(hi - lo)) recursion depth.
    """
    if hi is None:
        hi = len(xs)
    if hi - lo == 1:  # @line L6
        return Summary(1, xs[lo], 0 * xs[lo])
    mid = lo + (hi - lo) // 2  # @line L7
    a = summarize(xs, lo, mid)  # @line L8
    b = summarize(xs, mid, hi)  # @line L9
    return combine(a, b)  # @line L10


def chan_parallel_variance(xs: Sequence[float]) -> tuple[float, float, float]:
    """Return (mean, sample variance with divisor n - 1, sum of squared deviations).

    Precondition: len(xs) >= 2. Cost: 10 n - 9 arithmetic operations.
    """
    if len(xs) < 2:
        raise ValueError("need at least two values")
    n, mean, m2 = summarize(xs, 0, len(xs))  # @line L11
    return mean, m2 / (n - 1), m2  # @line L12
