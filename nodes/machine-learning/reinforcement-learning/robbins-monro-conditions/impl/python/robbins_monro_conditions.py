# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robbins-monro-conditions/. The authors are listed in prov/W0MVTZ.jsonl.

"""The test problem of the page: the noisy linear field h(x) = theta - x on the real line.

The iteration is x_(n+1) = x_n + a_n (theta - x_n + M_(n+1)) with independent noise of mean 0 and
variance sigma^2. Its mean squared error e_n = E (x_n - theta)^2 obeys the exact recursion
e_(n+1) = (1 - a_n)^2 e_n + a_n^2 sigma^2, which the functions below compute with any number type.
"""

import random
from fractions import Fraction
from typing import Callable

Number = float | Fraction


def power_steps_meet_conditions(p: Fraction) -> tuple[bool, bool]:
    """For a_n = (n + 1)^(-p) with p > 0: (sum a_n diverges, sum a_n^2 converges).

    The p-series sum n^(-q) converges exactly when q > 1, so the first holds for p <= 1
    and the second for 2 p > 1.
    """
    if p <= 0:
        raise ValueError("p must be positive")
    return p <= 1, 2 * p > 1


def noisy_iteration(
    theta: float,
    x0: float,
    step: Callable[[int], float],
    n_iter: int,
    noise: Callable[[random.Random], float],
    rng: random.Random,
) -> list[float]:
    """Run x_(n+1) = x_n + a_n (theta - x_n + M_(n+1)) and return x_0, ..., x_N. Cost O(N)."""
    xs = [x0]
    x = x0
    for n in range(n_iter):
        x = x + step(n) * (theta - x + noise(rng))
        xs.append(x)
    return xs


def exact_mse(step: Callable[[int], Number], n_iter: int, e0: Number, sigma2: Number) -> list[Number]:
    """e_0, ..., e_N for the linear field, from e_(n+1) = (1 - a_n)^2 e_n + a_n^2 sigma^2."""
    out = [e0]
    e = e0
    for n in range(n_iter):
        a = step(n)
        e = (1 - a) ** 2 * e + a * a * sigma2
        out.append(e)
    return out


def noise_floor(a: Number, sigma2: Number) -> Number:
    """Limit of e_n for a constant step a in (0, 2): the fixed point a sigma^2 / (2 - a)."""
    return a * sigma2 / (2 - a)


def reach(step: Callable[[int], Number], n_iter: int, bound: Number) -> Number:
    """If every observation has |h(x) + M| <= bound, then |x_n - x_0| <= bound (a_0 + ... + a_(n-1))."""
    return bound * sum(step(n) for n in range(n_iter))
