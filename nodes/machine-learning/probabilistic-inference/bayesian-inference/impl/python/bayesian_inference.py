# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-inference/. The authors are listed in prov/CSGT71.jsonl.

"""Bayesian inference for a Bernoulli parameter with a beta prior.

The prior is Beta(a, b) and the data are 0/1 outcomes that are i.i.d.
given theta. The posterior is Beta(a + s, b + f) with s successes and f
failures. The module gives the batch update, the sequential update, the
posterior predictive, and the exact evidence for integer a and b, all in
exact arithmetic, plus a grid posterior for any prior density.
"""

from fractions import Fraction
from math import factorial
from typing import Callable, Iterable, List, Sequence, Tuple


def batch_update(a: Fraction, b: Fraction, data: Sequence[int]) -> Tuple[Fraction, Fraction]:
    s = sum(data)
    return a + s, b + (len(data) - s)


def sequential_update(a: Fraction, b: Fraction, data: Iterable[int]) -> List[Tuple[Fraction, Fraction]]:
    """Return the posterior parameters after each observation."""
    path = []
    for x in data:
        if x not in (0, 1):
            raise ValueError("outcomes must be 0 or 1")
        a, b = (a + 1, b) if x == 1 else (a, b + 1)
        path.append((a, b))
    return path


def predictive_one(a: Fraction, b: Fraction) -> Fraction:
    """Posterior predictive Pr(next = 1) under Beta(a, b): the mean a / (a + b)."""
    return Fraction(a) / (a + b)


def beta_function_int(a: int, b: int) -> Fraction:
    """B(a, b) = (a-1)! (b-1)! / (a+b-1)! for positive integers."""
    return Fraction(factorial(a - 1) * factorial(b - 1), factorial(a + b - 1))


def evidence_sequence(a: int, b: int, data: Sequence[int]) -> Fraction:
    """p(x_1..x_n) for one ordered sequence: B(a+s, b+f) / B(a, b)."""
    s = sum(data)
    return beta_function_int(a + s, b + len(data) - s) / beta_function_int(a, b)


def grid_posterior(prior: Callable[[float], float], data: Sequence[int], m: int = 4000) -> Tuple[List[float], List[float]]:
    """Posterior weights on the midpoints of m equal cells of (0, 1)."""
    s = sum(data)
    f = len(data) - s
    grid = [(i + 0.5) / m for i in range(m)]
    w = [prior(t) * t ** s * (1 - t) ** f for t in grid]
    z = sum(w)
    return grid, [x / z for x in w]


def grid_mean(grid: Sequence[float], w: Sequence[float]) -> float:
    return sum(t * x for t, x in zip(grid, w))
