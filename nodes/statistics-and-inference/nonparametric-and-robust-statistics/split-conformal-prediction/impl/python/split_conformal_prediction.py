# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-conformal-prediction/. The authors are listed in prov/6A6QRB.jsonl.

import math
import random
from fractions import Fraction
from typing import Callable, List, NamedTuple, Optional, Sequence, Tuple

Point = Tuple[float, float]  # (x, y)
INF = float("inf")


def level(alpha) -> Fraction:
    """alpha as an exact fraction; a float is read as the decimal it prints as (0.1 is 1/10)."""
    a = Fraction(str(alpha)) if isinstance(alpha, float) else Fraction(alpha)
    if not 0 < a < 1:
        raise ValueError("alpha must be in (0, 1)")
    return a


def calibration_rank(n2: int, alpha) -> int:
    """k = ceil((n2 + 1)(1 - alpha)), the rank of the calibration score used as q."""
    return math.ceil((n2 + 1) * (1 - level(alpha)))


def conformal_quantile(scores: Sequence, alpha):
    """The k-th smallest score with k = ceil((n2 + 1)(1 - alpha)), or infinity if k > n2."""
    k = calibration_rank(len(scores), alpha)
    if k > len(scores):
        return INF
    return sorted(scores)[k - 1]


class SplitConformal(NamedTuple):
    mu: Callable  # the fitted predictor
    q: object  # the half width
    k: int  # the rank of q among the calibration scores
    n2: int  # the number of calibration points

    def interval(self, x) -> Tuple[object, object]:
        m = self.mu(x)
        return m - self.q, m + self.q


def split_conformal(
    points: Sequence[Point],
    n1: int,
    fit: Callable[[List[Point]], Callable],
    alpha,
    rng: Optional[random.Random] = None,
) -> SplitConformal:
    """Fit on n1 points, calibrate on the other n2 = n - n1. With rng None the split is the
    given order: the first n1 points train and the rest calibrate."""
    n = len(points)
    if not 1 <= n1 < n:
        raise ValueError("need 1 <= n1 < n")
    order = list(range(n))
    if rng is not None:
        rng.shuffle(order)
    train = [points[i] for i in order[:n1]]  # @line L1
    calib = [points[i] for i in order[n1:]]
    mu = fit(train)  # @line L2
    scores = [abs(y - mu(x)) for x, y in calib]  # @line L3
    n2 = len(calib)
    k = calibration_rank(n2, alpha)  # @line L4
    if k > n2:  # @line L5
        q = INF
    else:  # @line L6
        q = sorted(scores)[k - 1]
    return SplitConformal(mu, q, k, n2)  # @line L7


def fit_line(points: Sequence[Point]) -> Callable:
    """The least squares line through the points, as a function."""
    n = len(points)
    mx = sum(x for x, _ in points) / n
    my = sum(y for _, y in points) / n
    sxx = sum((x - mx) ** 2 for x, _ in points)
    slope = sum((x - mx) * (y - my) for x, y in points) / sxx if sxx else 0
    intercept = my - slope * mx
    return lambda x: intercept + slope * x


# Conformalized quantile regression (Romano, Patterson and Candes 2019): the same split,
# with lower and upper quantile fits and the score max(lo(x) - y, y - hi(x)).


def conformalized_quantile_regression(
    points: Sequence[Point],
    n1: int,
    fit_quantile: Callable[[List[Point], float], Callable],
    alpha,
    rng: Optional[random.Random] = None,
) -> Callable:
    n = len(points)
    if not 1 <= n1 < n:
        raise ValueError("need 1 <= n1 < n")
    order = list(range(n))
    if rng is not None:
        rng.shuffle(order)
    train = [points[i] for i in order[:n1]]
    calib = [points[i] for i in order[n1:]]
    a = float(level(alpha))
    lo = fit_quantile(train, a / 2)
    hi = fit_quantile(train, 1 - a / 2)
    scores = [max(lo(x) - y, y - hi(x)) for x, y in calib]
    q = conformal_quantile(scores, alpha)
    return lambda x: (lo(x) - q, hi(x) + q)


def fit_binned_quantile(points: Sequence[Point], tau: float, bins: int = 8) -> Callable:
    """A simple quantile regression: the empirical tau-quantile of y in equal-width bins of x."""
    xs = [x for x, _ in points]
    lo, hi = min(xs), max(xs)
    width = (hi - lo) / bins or 1.0

    def which(x):
        return min(max(int((x - lo) / width), 0), bins - 1)

    groups = [[] for _ in range(bins)]
    for x, y in points:
        groups[which(x)].append(y)
    every = sorted(y for _, y in points)

    def quantile(ys):
        ys = sorted(ys) if ys else every
        return ys[min(len(ys) - 1, max(0, math.ceil(tau * len(ys)) - 1))]

    values = [quantile(g) for g in groups]
    return lambda x: values[which(x)]
