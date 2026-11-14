# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-percentile-interval/. The authors are listed in prov/3JWEPT.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Callable, Sequence


def empirical_quantile(sorted_values: Sequence, p) -> object:
    """G^{-1}(p) = inf{t : G(t) >= p} for the empirical law of the sorted values.

    This is the ceil(b p)-th smallest value (1-based) for 0 < p <= 1, and the
    smallest value for p = 0. p may be a float or a Fraction.
    """
    b = len(sorted_values)
    if b == 0:
        raise ValueError("no values")
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0, 1]")
    k = max(1, math.ceil(Fraction(p) * b))
    return sorted_values[k - 1]


def percentile_interval(
    x: Sequence[float],
    statistic: Callable[[Sequence[float]], float],
    alpha: float,
    b: int,
    rng: random.Random,
) -> tuple:
    """The 1 - alpha bootstrap percentile interval [G^{-1}(alpha/2), G^{-1}(1 - alpha/2)].

    G is the empirical distribution of b bootstrap replicates of the statistic.
    """
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    n = len(x)
    if n == 0 or b < 1:
        raise ValueError("need data and b >= 1")
    reps = []
    for _ in range(b):  # @line L1
        xs = [x[rng.randrange(n)] for _ in range(n)]  # @line L2
        reps.append(statistic(xs))  # @line L3
    reps.sort()  # @line L4
    lo = empirical_quantile(reps, alpha / 2)  # @line L5
    hi = empirical_quantile(reps, 1 - alpha / 2)  # @line L6
    return lo, hi  # @line L7


def ideal_bootstrap_cdf(x: Sequence, statistic: Callable) -> list:
    """The ideal bootstrap law of the statistic as a sorted list of (value, probability).

    It lists the C(2n - 1, n) multisets of indices with multinomial weights.
    """
    n = len(x)
    fact_n = math.factorial(n)
    dist: dict = {}
    for idx in itertools.combinations_with_replacement(range(n), n):
        w = fact_n
        for _, g in itertools.groupby(idx):
            w //= math.factorial(len(list(g)))
        v = statistic([x[i] for i in idx])
        dist[v] = dist.get(v, 0) + w
    return sorted((v, Fraction(w, n**n)) for v, w in dist.items())


def ideal_percentile_interval(x: Sequence, statistic: Callable, alpha) -> tuple:
    """The percentile interval of the ideal bootstrap (b = infinity), for small n."""
    law = ideal_bootstrap_cdf(x, statistic)

    def quantile(p):
        acc = Fraction(0)
        for v, w in law:
            acc += w
            if acc >= p:
                return v
        return law[-1][0]

    a = Fraction(alpha)
    return quantile(a / 2), quantile(1 - a / 2)
