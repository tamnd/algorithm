# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bootstrap-t-interval/. The authors are listed in prov/48PN4N.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Callable, Sequence

Estimate = Callable[[Sequence[float]], tuple]


def mean_and_se(xs: Sequence[float]) -> tuple:
    """The sample mean and its standard error s / sqrt(n), s with divisor n - 1."""
    n = len(xs)
    if n < 2:
        raise ValueError("need at least two values")
    m = math.fsum(xs) / n
    ss = math.fsum((v - m) ** 2 for v in xs)  # fsum is exactly rounded, so the order of xs does not matter
    return m, math.sqrt(ss / (n - 1)) / math.sqrt(n)


def empirical_quantile(sorted_values: Sequence[float], p: float) -> float:
    """inf{t : G(t) >= p}: the ceil(b p)-th smallest value, or the smallest for p = 0."""
    k = max(1, math.ceil(Fraction(p) * len(sorted_values)))
    return sorted_values[k - 1]


def studentized(theta_star: float, se_star: float, theta_hat: float) -> float:
    """t* = (theta* - theta_hat) / se*. A resample with se* = 0 gives 0 if theta* = theta_hat,
    and plus or minus infinity otherwise, so that it stays in the right tail."""
    diff = theta_star - theta_hat
    if se_star == 0:
        if diff == 0:
            return 0.0
        return math.copysign(math.inf, diff)
    return diff / se_star


def bootstrap_t_interval(
    x: Sequence[float],
    alpha: float,
    b: int,
    rng: random.Random,
    estimate: Estimate = mean_and_se,
) -> tuple:
    """The 1 - alpha studentized bootstrap interval
    [theta_hat - t*_(1 - alpha/2) se, theta_hat - t*_(alpha/2) se]."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    if b < 1:
        raise ValueError("b must be at least 1")
    n = len(x)
    theta_hat, se = estimate(x)  # @line L1
    if se == 0:
        raise ValueError("the standard error of the sample is 0")
    ts = []
    for _ in range(b):  # @line L2
        xs = [x[rng.randrange(n)] for _ in range(n)]  # @line L3
        theta_star, se_star = estimate(xs)  # @line L4
        ts.append(studentized(theta_star, se_star, theta_hat))  # @line L5
    ts.sort()  # @line L6
    t_lo = empirical_quantile(ts, alpha / 2)  # @line L7
    t_hi = empirical_quantile(ts, 1 - alpha / 2)
    return theta_hat - t_hi * se, theta_hat - t_lo * se  # @line L8


def ideal_t_law(x: Sequence[float], estimate: Estimate = mean_and_se) -> list:
    """The ideal bootstrap law of t* (b = infinity) as a sorted list of (t, probability).

    It lists the C(2n - 1, n) multisets of indices with multinomial weights; small n only.
    """
    n = len(x)
    theta_hat, _ = estimate(x)
    fact_n = math.factorial(n)
    law: dict = {}
    for idx in itertools.combinations_with_replacement(range(n), n):
        w = fact_n
        for _, g in itertools.groupby(idx):
            w //= math.factorial(len(list(g)))
        theta_star, se_star = estimate([x[i] for i in idx])
        t = studentized(theta_star, se_star, theta_hat)
        law[t] = law.get(t, 0) + w
    return sorted((t, Fraction(w, n**n)) for t, w in law.items())
