# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turnbull-estimator/. The authors are listed in prov/0DBRMH.jsonl.

import math
from collections.abc import Sequence
from typing import NamedTuple


class Region(NamedTuple):
    """An innermost interval: (left, right] if left_open, else the single point [left, left]."""

    left: float
    right: float
    left_open: bool


class TurnbullFit(NamedTuple):
    regions: list[Region]  # Q_1 < ... < Q_m, the innermost intervals
    mass: list[float]  # s_j, the probability of Q_j; sums to 1
    loglik: float  # sum over i of log P(T_i in I_i)
    kkt_gap: float  # max_j g_j - 1 >= 0; the log-likelihood is within n * kkt_gap of the maximum
    iterations: int


def _check(left, right):
    if len(left) == 0 or len(left) != len(right):
        raise ValueError("left and right must have the same positive length")
    for a, b in zip(left, right):
        if math.isnan(a) or math.isnan(b) or a > b or a == math.inf:
            raise ValueError("each observation needs left <= right and a finite left end")


def contains(region: Region, a: float, b: float) -> bool:
    """Whether the region lies inside the observation set: (a, b] if a < b, the point {a} if a == b."""
    if a == b:
        return not region.left_open and region.left == a
    if region.left_open:
        return a <= region.left and region.right <= b
    return a < region.left <= b


def innermost_intervals(left: Sequence[float], right: Sequence[float]) -> list[Region]:
    """Turnbull's innermost intervals of the sets (left_i, right_i], with exact times left_i == right_i."""
    _check(left, right)
    ends = []
    for a, b in zip(left, right):
        # At equal values: a closed left end (an exact time) first, then right ends, then open left ends.
        ends.append((a, 0 if a == b else 2, "L"))
        ends.append((b, 1, "R"))
    ends.sort()  # @line L1
    regions = []
    for (x, kx, sx), (y, _, sy) in zip(ends, ends[1:]):  # @line L2
        if sx == "L" and sy == "R":
            regions.append(Region(x, y, kx == 2))
    return regions


def turnbull(
    left: Sequence[float],
    right: Sequence[float],
    tol: float = 1e-9,
    max_iter: int = 1_000_000,
) -> TurnbullFit:
    """The NPMLE of the distribution of T from the sets T_i in (left_i, right_i].

    left_i == right_i is an exact time, right_i = inf a right censoring at left_i,
    left_i = 0 with T > 0 a left censoring at right_i. Self-consistency (EM)
    iterations run until max_j g_j <= 1 + tol, where g_j is (1/n) times the
    derivative of the log-likelihood in s_j; then the log-likelihood is within
    n * tol of its maximum. Cost per iteration: O(sum_i #{j : Q_j in I_i}).
    """
    regions = innermost_intervals(left, right)
    n, m = len(left), len(regions)
    cover = [[j for j in range(m) if contains(regions[j], a, b)] for a, b in zip(left, right)]  # @line L3
    s = [1.0 / m] * m  # @line L4
    it = 0
    while True:  # @line L5
        dens = [sum(s[j] for j in cover[i]) for i in range(n)]  # @line L6
        g = [0.0] * m  # @line L7
        for i in range(n):
            for j in cover[i]:
                g[j] += 1.0 / dens[i]
        g = [x / n for x in g]
        gap = max(g) - 1.0
        if gap <= tol or it >= max_iter:  # @line L8
            break
        s = [s[j] * g[j] for j in range(m)]  # @line L9
        total = math.fsum(s)  # equal to 1 up to rounding, since sum_j s_j g_j = 1
        s = [x / total for x in s]
        it += 1
    loglik = math.fsum(math.log(d) for d in dens)
    return TurnbullFit(regions, s, loglik, max(gap, 0.0), it)  # @line L10


def survival(fit: TurnbullFit, t: float) -> tuple[float, float]:
    """Bounds (lower, upper) of S(t) = P(T > t) over all NPMLEs with the fitted region masses.

    The two agree unless t falls inside a region of positive width, where the
    NPMLE does not say how the mass of the region is spread.
    """
    lo = hi = 0.0
    for q, w in zip(fit.regions, fit.mass):
        if q.left_open:
            if q.left >= t:
                lo += w
            if q.right > t:
                hi += w
        elif q.left > t:
            lo += w
            hi += w
    return lo, hi
