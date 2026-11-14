# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subsampling-inference/. The authors are listed in prov/HBQCGG.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Callable, Sequence

Statistic = Callable[[Sequence[float]], float]
Rate = Callable[[int], float]


def empirical_quantile(sorted_values: Sequence[float], p: float) -> float:
    """inf{t : L(t) >= p}: the ceil(b p)-th smallest value, or the smallest for p = 0."""
    k = max(1, math.ceil(Fraction(p) * len(sorted_values)))
    return sorted_values[k - 1]


def subsample_roots(
    x: Sequence[float],
    statistic: Statistic,
    m: int,
    tau: Rate,
    b: int | None = None,
    rng: random.Random | None = None,
) -> list:
    """The sorted roots tau(m) (theta_hat_S - theta_hat) over subsets S of size m drawn without
    replacement. b=None lists all C(n, m) subsets; otherwise b subsets are drawn at random."""
    n = len(x)
    if not 1 <= m < n:
        raise ValueError("need 1 <= m < n")
    theta_hat = statistic(x)  # @line L1
    if b is None:
        subsets = itertools.combinations(range(n), m)
    else:
        subsets = (rng.sample(range(n), m) for _ in range(b))  # @line L3
    roots = []
    for idx in subsets:  # @line L2
        roots.append(tau(m) * (statistic([x[i] for i in idx]) - theta_hat))  # @line L4
    roots.sort()  # @line L5
    return roots


def subsampling_interval(
    x: Sequence[float],
    statistic: Statistic,
    m: int,
    tau: Rate,
    alpha: float,
    b: int | None = None,
    rng: random.Random | None = None,
) -> tuple:
    """The equal-tailed 1 - alpha subsampling interval
    [theta_hat - c_(1 - alpha/2)/tau(n), theta_hat - c_(alpha/2)/tau(n)]."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    roots = subsample_roots(x, statistic, m, tau, b, rng)
    c_lo = empirical_quantile(roots, alpha / 2)  # @line L6
    c_hi = empirical_quantile(roots, 1 - alpha / 2)
    theta_hat, n = statistic(x), len(x)
    return theta_hat - c_hi / tau(n), theta_hat - c_lo / tau(n)  # @line L7


def subsampling_variance(x: Sequence, statistic: Statistic, m: int):
    """The variance of the statistic over all C(n, m) subsets, exactly (small n only)."""
    values = [statistic([x[i] for i in idx]) for idx in itertools.combinations(range(len(x)), m)]
    mean = sum(values[1:], values[0]) / len(values)
    return sum(((v - mean) ** 2 for v in values[1:]), (values[0] - mean) ** 2) / len(values)


def m_out_of_n_roots(
    x: Sequence[float], statistic: Statistic, m: int, tau: Rate, b: int, rng: random.Random
) -> list:
    """The m-out-of-n bootstrap: the same roots, but each subsample is m draws WITH replacement."""
    n = len(x)
    theta_hat = statistic(x)
    roots = [tau(m) * (statistic([x[rng.randrange(n)] for _ in range(m)]) - theta_hat) for _ in range(b)]
    roots.sort()
    return roots


def max_at_rank_probability(n: int, m: int, k: int) -> Fraction:
    """P(the maximum of a uniform random m-subset is the k-th smallest of n distinct values)."""
    return Fraction(math.comb(k - 1, m - 1), math.comb(n, m))


def resample_hits_maximum(n: int, m: int) -> Fraction:
    """P(a with-replacement resample of size m contains the largest of n distinct values)."""
    return 1 - Fraction(n - 1, n) ** m
