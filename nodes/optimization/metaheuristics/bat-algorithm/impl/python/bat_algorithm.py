# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bat-algorithm/. The authors are listed in prov/F7GN0A.jsonl.

import math
import random
from collections.abc import Callable, Sequence

Vector = list[float]


def velocity_step(x: Sequence[float], v: Sequence[float], best: Sequence[float], freq: float) -> tuple[Vector, Vector]:
    """Yang's equations (3) and (4): v' = v + (x - best) freq and x' = x + v'.

    With freq > 0 this pushes x away from best. A negative freq gives the
    pull v' = v + |freq| (best - x) of PSO with inertia 1 and no personal term.
    """
    v2 = [vk + (xk - bk) * freq for xk, vk, bk in zip(x, v, best)]
    return [xk + vk for xk, vk in zip(x, v2)], v2


def bat_algorithm(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    n: int,
    f_min: float,
    f_max: float,
    loudness0: float,
    rate0: float,
    alpha: float,
    gamma: float,
    iterations: int,
    rng: random.Random,
    on_bat: Callable[[int, int, Vector, float, bool, bool, float, float], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """Bat algorithm (Yang 2010) for minimizing f on a box.

    Each bat draws a frequency in [f_min, f_max], updates its velocity and
    makes a proposal x + v. With probability 1 - r_i the proposal is replaced
    by a uniform step of size mean(A) around the best point. The proposal is
    clipped and evaluated. It is accepted if it is better than the bat's
    current point and a uniform draw is below the loudness A_i. Then
    A_i <- alpha A_i and r_i <- rate0 (1 - exp(-gamma t)). The best point
    ever evaluated is kept. Precondition: n >= 1, lower[k] < upper[k],
    0 < alpha <= 1.
    Returns (best point, its value, history of the best value).
    Cost: O(iterations * n * (D + c)) time and O(n D) space.
    """
    d = len(lower)
    x = [[rng.uniform(lower[k], upper[k]) for k in range(d)] for _ in range(n)]  # @line L1
    v = [[0.0] * d for _ in range(n)]
    fx = [f(p) for p in x]
    loud = [loudness0] * n
    rate = [0.0] * n  # r_i = rate0 (1 - exp(0)) = 0 at t = 0
    b = min(range(n), key=lambda i: fx[i])
    best, best_f = list(x[b]), fx[b]
    history = [best_f]
    for t in range(1, iterations + 1):  # @line L2
        for i in range(n):
            freq = f_min + (f_max - f_min) * rng.random()  # @line L3
            y, v[i] = velocity_step(x[i], v[i], best, freq)
            local = rng.random() > rate[i]
            if local:  # @line L4
                mean_loud = sum(loud) / n
                y = [best[k] + rng.uniform(-1.0, 1.0) * mean_loud for k in range(d)]
            y = [min(upper[k], max(lower[k], y[k])) for k in range(d)]  # @line L5
            fy = f(y)
            accept = fy < fx[i] and rng.random() < loud[i]
            if accept:  # @line L6
                x[i], fx[i] = y, fy
                loud[i] *= alpha
                rate[i] = rate0 * (1.0 - math.exp(-gamma * t))
            if fy < best_f:  # @line L7
                best, best_f = list(y), fy
            if on_bat is not None:
                on_bat(t, i, list(y), fy, local, accept, loud[i], rate[i])
        history.append(best_f)
    return best, best_f, history  # @line L8


def sphere(x: Sequence[float]) -> float:
    return sum(v * v for v in x)


def rastrigin(x: Sequence[float]) -> float:
    return 10.0 * len(x) + sum(v * v - 10.0 * math.cos(2 * math.pi * v) for v in x)
