# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parametric-bootstrap/. The authors are listed in prov/EDDGAQ.jsonl.

import math
import random
import statistics
from fractions import Fraction
from statistics import NormalDist
from typing import Callable, Sequence


def parametric_bootstrap(
    x: Sequence[float],
    fit: Callable[[Sequence[float]], object],
    sample: Callable[[object, int, random.Random], list],
    statistic: Callable[[Sequence[float]], float],
    b: int,
    rng: random.Random,
) -> list:
    """Replicates statistic(x*) for b samples x* of size n drawn from the fitted model."""
    if b < 1:
        raise ValueError("b must be at least 1")
    n = len(x)
    theta_hat = fit(x)  # @line L1
    reps = []
    for _ in range(b):  # @line L2
        xs = sample(theta_hat, n, rng)  # @line L3
        reps.append(statistic(xs))  # @line L4
    return reps  # @line L5


# The exponential model with mean mu.
def fit_exponential(x: Sequence[float]) -> float:
    return statistics.fmean(x)


def sample_exponential(mu: float, n: int, rng: random.Random) -> list:
    return [rng.expovariate(1.0 / mu) for _ in range(n)]


# The normal model with mean mu and standard deviation sigma (maximum likelihood fit).
def fit_normal(x: Sequence[float]) -> tuple:
    return statistics.fmean(x), statistics.pstdev(x)


def sample_normal(theta: tuple, n: int, rng: random.Random) -> list:
    mu, sigma = theta
    return [rng.gauss(mu, sigma) for _ in range(n)]


def ks_normal_statistic(x: Sequence[float]) -> float:
    """Kolmogorov-Smirnov distance between the sample and N(xbar, s^2), s with divisor n - 1.

    The statistic is the same for x and a + c x with c > 0, so its null law does not
    depend on the normal parameters.
    """
    n = len(x)
    if n < 2:
        raise ValueError("need at least two values")
    mu, s = statistics.fmean(x), statistics.stdev(x)
    if s == 0:
        raise ValueError("all values are equal")
    phi = NormalDist().cdf
    d = 0.0
    for i, v in enumerate(sorted(x), start=1):
        u = phi((v - mu) / s)
        d = max(d, i / n - u, u - (i - 1) / n)
    return d


def lilliefors_test(x: Sequence[float], b: int, rng: random.Random) -> tuple:
    """Monte Carlo test of normality with estimated mean and variance.

    Returns (d, p) with p = (1 + c)/(1 + b), where c counts the simulated statistics
    at least as large as d. Because the statistic is invariant under a + c x, the
    simulation can use N(0, 1), and the test has exact level for every n.
    """
    d = ks_normal_statistic(x)
    n = len(x)
    reps = parametric_bootstrap(x, lambda _: (0.0, 1.0), sample_normal, ks_normal_statistic, b, rng)
    c = sum(1 for t in reps if t >= d)
    return d, Fraction(1 + c, 1 + b)


def t_pivot(xs: Sequence[float], mu: float) -> float:
    """(xbar - mu) / (s / sqrt(n)), the studentized mean."""
    return (statistics.fmean(xs) - mu) / (statistics.stdev(xs) / math.sqrt(len(xs)))
