# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-hastings/. The authors are listed in prov/F19R05.jsonl.

import math
import random
from fractions import Fraction
from typing import Callable, Sequence, TypeVar

S = TypeVar("S")


def metropolis_hastings(
    log_target: Callable[[S], float],
    propose: Callable[[S, random.Random], S],
    log_proposal: Callable[[S, S], float],
    x0: S,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[S], int]:
    """Run n_steps of Metropolis-Hastings and return (chain, number accepted).

    log_target(x) is log of the unnormalized target, -inf outside the support.
    propose(x, rng) draws y from Q(x, .), and log_proposal(x, y) = log Q(x, y).
    For a symmetric proposal, log_proposal may return 0.
    Precondition: log_target(x0) > -inf. Cost: n_steps target evaluations.
    """
    x = x0  # @line L1
    lx = log_target(x)
    if lx == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    chain: list[S] = []
    accepted = 0
    for _ in range(n_steps):  # @line L2
        y = propose(x, rng)  # @line L3
        ly = log_target(y)
        if ly == -math.inf:
            log_r = -math.inf
        else:
            log_r = ly + log_proposal(y, x) - lx - log_proposal(x, y)  # @line L4
        u = rng.random()  # @line L5
        if log_r >= 0 or u < math.exp(log_r):  # @line L6
            x, lx = y, ly
            accepted += 1
        chain.append(x)  # @line L7
    return chain, accepted  # @line L8


def transition_matrix(
    weights: Sequence[Fraction], proposal: Sequence[Sequence[Fraction]]
) -> list[list[Fraction]]:
    """Exact Metropolis-Hastings kernel on the states 0..n-1.

    weights[x] > 0 is the unnormalized target and proposal[x][y] = Q(x, y).
    Row x is P(x, .): Q(x, y) min(1, r) off the diagonal, the rest on it.
    """
    n = len(weights)
    p = [[Fraction(0)] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if y != x and proposal[x][y] > 0:
                r = (weights[y] * proposal[y][x]) / (weights[x] * proposal[x][y])
                p[x][y] = proposal[x][y] * min(Fraction(1), r)
        p[x][x] = 1 - sum(p[x][y] for y in range(n) if y != x)
    return p
