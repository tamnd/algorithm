# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independence-sampler/. The authors are listed in prov/AW5Q0G.jsonl.

import math
import random
from fractions import Fraction
from typing import Callable, Sequence, TypeVar

S = TypeVar("S")


def independence_sampler(
    log_target: Callable[[S], float],
    draw_proposal: Callable[[random.Random], S],
    log_proposal: Callable[[S], float],
    x0: S,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[S], int]:
    """Run the independence sampler and return (chain X_1..X_T, number accepted).

    log_target is log of the unnormalized target (-inf outside the support),
    draw_proposal(rng) draws y from q, and log_proposal(y) is log q(y) up to a constant.
    Precondition: log_target(x0) > -inf, and q > 0 on the support. Cost: T draws and T weight calls.
    """
    x = x0  # @line L1
    lx = log_target(x)
    if lx == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    lw_x = lx - log_proposal(x)
    chain: list[S] = []
    accepted = 0
    for _ in range(n_steps):  # @line L2
        y = draw_proposal(rng)  # @line L3
        ly = log_target(y)
        lw_y = ly - log_proposal(y) if ly > -math.inf else -math.inf
        log_r = lw_y - lw_x  # @line L4
        u = rng.random()  # @line L5
        if log_r >= 0 or u < math.exp(log_r):  # @line L6
            x, lw_x = y, lw_y
            accepted += 1
        chain.append(x)  # @line L7
    return chain, accepted  # @line L8


def transition_matrix(
    target: Sequence[Fraction], proposal: Sequence[Fraction]
) -> list[list[Fraction]]:
    """Exact kernel on the states 0..n-1 for unnormalized target[x] > 0 and proposal[y] > 0."""
    n = len(target)
    zt, zq = sum(target), sum(proposal)
    w = [(target[i] / zt) / (proposal[i] / zq) for i in range(n)]
    p = [[Fraction(0)] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if y != x:
                p[x][y] = proposal[y] / zq * min(Fraction(1), w[y] / w[x])
        p[x][x] = 1 - sum(p[x])
    return p
