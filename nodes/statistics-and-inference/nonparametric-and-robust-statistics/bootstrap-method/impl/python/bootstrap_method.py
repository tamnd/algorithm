# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-method/. The authors are listed in prov/V0JBK5.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction
from typing import Callable, Sequence

Statistic = Callable[[Sequence], object]


def resample(x: Sequence, rng: random.Random) -> list:
    """One bootstrap sample: n draws with replacement from x, each index equally likely."""
    n = len(x)
    return [x[rng.randrange(n)] for _ in range(n)]


def bootstrap_replicates(x: Sequence, statistic: Statistic, b: int, rng: random.Random) -> list:
    """The b bootstrap replicates statistic(x*_1), ..., statistic(x*_b)."""
    if len(x) == 0:
        raise ValueError("empty sample")
    if b < 1:
        raise ValueError("b must be at least 1")
    reps = []
    for _ in range(b):  # @line L1
        xs = resample(x, rng)  # @line L2
        reps.append(statistic(xs))  # @line L3
    return reps  # @line L6


def bootstrap_se(reps: Sequence[float]) -> float:
    """The standard deviation of the replicates, with divisor b - 1."""
    return statistics.stdev(reps)  # @line L4


def bootstrap_bias(reps: Sequence[float], theta_hat: float) -> float:
    """The mean of the replicates minus the estimate on the original sample."""
    return statistics.fmean(reps) - theta_hat  # @line L5


def exact_bootstrap_distribution(x: Sequence, statistic: Statistic) -> dict:
    """The ideal bootstrap distribution (b = infinity) as {value: probability}.

    It lists the C(2n - 1, n) multisets of indices instead of the n^n ordered
    resamples. A multiset with counts c_1, ..., c_n has probability
    n! / (c_1! ... c_n!) / n^n. Feasible for n up to about 9.
    """
    n = len(x)
    if n == 0:
        raise ValueError("empty sample")
    total = n**n
    fact_n = math.factorial(n)
    dist: dict = {}
    for idx in itertools.combinations_with_replacement(range(n), n):
        weight = fact_n
        for _, group in itertools.groupby(idx):
            weight //= math.factorial(len(list(group)))
        value = statistic([x[i] for i in idx])
        dist[value] = dist.get(value, 0) + weight
    return {v: Fraction(w, total) for v, w in dist.items()}


def exact_bootstrap_moments(x: Sequence, statistic: Statistic) -> tuple:
    """Mean and variance of the ideal bootstrap distribution. Exact for int or Fraction values."""
    dist = exact_bootstrap_distribution(x, statistic)
    mean = sum(p * v for v, p in dist.items())
    var = sum(p * (v - mean) ** 2 for v, p in dist.items())
    return mean, var


def exact_mean(xs: Sequence) -> Fraction:
    """The sample mean as an exact Fraction, for use as a statistic."""
    return Fraction(sum(Fraction(v) for v in xs), len(xs))
