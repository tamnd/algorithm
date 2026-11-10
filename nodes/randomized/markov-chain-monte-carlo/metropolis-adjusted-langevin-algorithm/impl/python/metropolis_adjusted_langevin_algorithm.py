# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-adjusted-langevin-algorithm/. The authors are listed in prov/CGM810.jsonl.

import math
import random
from typing import Callable, Sequence

Point = tuple[float, ...]


def log_proposal(grad_log_target, x: Sequence[float], y: Sequence[float], h: float) -> float:
    """log q(y | x) up to a constant, for q(. | x) = N(x + (h/2) grad log pi(x), h I)."""
    g = grad_log_target(x)
    return -sum((b - a - h / 2 * c) ** 2 for a, b, c in zip(x, y, g)) / (2 * h)


def metropolis_adjusted_langevin_algorithm(
    log_target: Callable[[Sequence[float]], float],
    grad_log_target: Callable[[Sequence[float]], Sequence[float]],
    x0: Sequence[float],
    h: float,
    n_steps: int,
    rng: random.Random,
) -> tuple[list[Point], int]:
    """Run MALA with step size h: propose y = x + (h/2) grad log pi(x) + sqrt(h) Z.

    Returns (chain X_1..X_T, number of accepted proposals).
    Cost: T target calls and T gradient calls (the gradient at x is kept).
    """
    if h <= 0:
        raise ValueError("h must be positive")
    x: Point = tuple(float(v) for v in x0)  # @line L1
    lx = log_target(x)
    if lx == -math.inf:
        raise ValueError("x0 must be in the support of the target")
    gx = grad_log_target(x)
    sq = math.sqrt(h)
    chain: list[Point] = []
    accepted = 0
    for _ in range(n_steps):  # @line L2
        z = [rng.gauss(0.0, 1.0) for _ in x]  # @line L3
        y = tuple(a + h / 2 * c + sq * b for a, b, c in zip(x, z, gx))  # @line L4
        ly = log_target(y)
        if ly > -math.inf:
            gy = grad_log_target(y)
            fwd = -sum((b - a - h / 2 * c) ** 2 for a, b, c in zip(x, y, gx)) / (2 * h)
            bwd = -sum((a - b - h / 2 * c) ** 2 for a, b, c in zip(x, y, gy)) / (2 * h)
            log_r = ly + bwd - lx - fwd  # @line L5
        else:
            log_r = -math.inf
        u = rng.random()  # @line L6
        if log_r >= 0 or u < math.exp(log_r):  # @line L7
            x, lx, gx = y, ly, gy
            accepted += 1
        chain.append(x)  # @line L8
    return chain, accepted  # @line L9


def unadjusted_langevin(
    grad_log_target: Callable[[Sequence[float]], Sequence[float]],
    x0: Sequence[float],
    h: float,
    n_steps: int,
    rng: random.Random,
) -> list[Point]:
    """The Langevin step without the Metropolis test. Its stationary law is not pi in general."""
    x = tuple(float(v) for v in x0)
    sq = math.sqrt(h)
    chain = []
    for _ in range(n_steps):
        g = grad_log_target(x)
        x = tuple(a + h / 2 * c + sq * rng.gauss(0.0, 1.0) for a, c in zip(x, g))
        chain.append(x)
    return chain
