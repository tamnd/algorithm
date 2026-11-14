# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permutation-test/. The authors are listed in prov/KSN49K.jsonl.

import itertools
import math
import random
from fractions import Fraction
from typing import Callable, Sequence

ALTERNATIVES = ("greater", "less", "two-sided")

Statistic = Callable[[Sequence, Sequence], float]


def mean_difference(x: Sequence, y: Sequence):
    """The mean of x minus the mean of y. Exact when the values are int or Fraction."""
    sx, sy = sum(x), sum(y)
    if all(isinstance(v, (int, Fraction)) for v in (sx, sy)):
        return Fraction(sx) / len(x) - Fraction(sy) / len(y)
    return sx / len(x) - sy / len(y)


def _exact(v) -> bool:
    return isinstance(v, (int, Fraction))


def _at_least_as_extreme(t, t_obs, alternative: str) -> bool:
    """t is at least as extreme as t_obs. Floats get a small relative tolerance,
    because the same split can give a statistic that differs in the last bit."""
    if alternative == "two-sided":
        t, t_obs = abs(t), abs(t_obs)
    elif alternative == "less":
        t, t_obs = -t, -t_obs
    if _exact(t) and _exact(t_obs):
        return t >= t_obs
    return t >= t_obs - 1e-9 * max(1.0, abs(t_obs))


def permutation_test(
    x: Sequence,
    y: Sequence,
    statistic: Statistic = mean_difference,
    alternative: str = "greater",
    b: int | None = None,
    rng: random.Random | None = None,
) -> Fraction:
    """Two-sample permutation test of H0: the pooled values are exchangeable.

    With b = None the test is exact: it lists all C(N, m) ways to choose the
    first group and returns the fraction of splits whose statistic is at least
    as extreme as the observed one. With an integer b it draws b uniform random
    permutations with rng and returns the Monte Carlo p-value (1 + c)/(1 + b).
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    z = list(x) + list(y)
    n_total, m = len(z), len(x)
    if m == 0 or m == n_total:
        raise ValueError("both groups must be non-empty")
    t_obs = statistic(z[:m], z[m:])  # @line L1
    if b is None:
        count = 0  # @line L8
        for chosen in itertools.combinations(range(n_total), m):  # @line L9
            inside = set(chosen)
            first = [z[i] for i in chosen]
            second = [z[i] for i in range(n_total) if i not in inside]
            if _at_least_as_extreme(statistic(first, second), t_obs, alternative):  # @line L10
                count += 1
        return Fraction(count, math.comb(n_total, m))  # @line L11
    if rng is None:
        raise ValueError("pass rng=random.Random(seed) for the Monte Carlo test")
    if b < 1:
        raise ValueError("b must be at least 1")
    count = 0  # @line L2
    for _ in range(b):  # @line L3
        w = z[:]
        rng.shuffle(w)  # @line L4
        t = statistic(w[:m], w[m:])  # @line L5
        if _at_least_as_extreme(t, t_obs, alternative):  # @line L6
            count += 1
    return Fraction(1 + count, 1 + b)  # @line L7


def sign_flip_test(
    d: Sequence,
    alternative: str = "two-sided",
    b: int | None = None,
    rng: random.Random | None = None,
) -> Fraction:
    """Paired permutation test of H0: each difference is symmetric about 0.

    The statistic is the sum of the differences. With b = None all 2^n sign
    vectors are listed; with an integer b, b random sign vectors are drawn and
    the p-value is (1 + c)/(1 + b).
    """
    if alternative not in ALTERNATIVES:
        raise ValueError("unknown alternative")
    d = list(d)
    t_obs = sum(d)
    if b is None:
        count = 0
        for signs in itertools.product((1, -1), repeat=len(d)):
            if _at_least_as_extreme(sum(s * v for s, v in zip(signs, d)), t_obs, alternative):
                count += 1
        return Fraction(count, 2 ** len(d))
    if rng is None:
        raise ValueError("pass rng=random.Random(seed) for the Monte Carlo test")
    count = 0
    for _ in range(b):
        t = sum(v if rng.random() < 0.5 else -v for v in d)
        if _at_least_as_extreme(t, t_obs, alternative):
            count += 1
    return Fraction(1 + count, 1 + b)
