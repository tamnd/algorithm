# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walk-metropolis/. The authors are listed in prov/C4EVM2.jsonl.

import math
import random
from fractions import Fraction
from typing import Callable, Sequence

Point = tuple[float, ...]


def random_walk_metropolis(
    log_target: Callable[[Point], float],
    x0: Sequence[float],
    sigma: float,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[Point], int]:
    """Run random-walk Metropolis with Gaussian steps N(0, sigma^2 I).

    log_target(x) is log of the unnormalized density, -inf outside the support.
    Returns (chain X_1..X_T, number of accepted proposals).
    Precondition: log_target(x0) > -inf and sigma > 0. Cost: T target calls, O(T d) other work.
    """
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    x: Point = tuple(float(v) for v in x0)  # @line L1
    lx = log_target(x)
    if lx == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    chain: list[Point] = []
    accepted = 0
    for _ in range(n_steps):  # @line L2
        z = [rng.gauss(0.0, 1.0) for _ in x]  # @line L3
        y = tuple(a + sigma * b for a, b in zip(x, z))  # @line L4
        ly = log_target(y)
        u = rng.random()  # @line L5
        if ly > -math.inf and (ly >= lx or u < math.exp(ly - lx)):  # @line L6
            x, lx = y, ly
            accepted += 1
        chain.append(x)  # @line L7
    return chain, accepted  # @line L8


def cycle_transition_matrix(weights: Sequence[Fraction]) -> list[list[Fraction]]:
    """Exact kernel of random-walk Metropolis on the cycle Z_n with steps +1 and -1.

    Each step is proposed with probability 1/2, so the proposal is symmetric.
    weights[k] > 0 is the unnormalized target at state k. Requires n >= 3.
    """
    n = len(weights)
    if n < 3:
        raise ValueError("the cycle needs at least 3 states")
    p = [[Fraction(0)] * n for _ in range(n)]
    for x in range(n):
        for y in ((x + 1) % n, (x - 1) % n):
            p[x][y] += Fraction(1, 2) * min(Fraction(1), weights[y] / weights[x])
        p[x][x] = 1 - sum(p[x])
    return p
