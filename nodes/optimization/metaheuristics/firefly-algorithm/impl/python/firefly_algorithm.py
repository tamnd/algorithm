# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/firefly-algorithm/. The authors are listed in prov/BF1W32.jsonl.

import math
import random
from collections.abc import Callable, Sequence

Vector = list[float]


def attractiveness(beta0: float, gamma: float, r2: float) -> float:
    """beta0 * exp(-gamma * r^2), for the squared distance r2."""
    return beta0 * math.exp(-gamma * r2)


def firefly_move(
    xi: Sequence[float], xj: Sequence[float], beta0: float, gamma: float, alpha: float, u: Sequence[float], scale: Sequence[float]
) -> Vector:
    """x_i + beta0 e^(-gamma r^2) (x_j - x_i) + alpha (u - 1/2) * scale, coordinate by coordinate, with r = ||x_i - x_j||."""
    r2 = sum((a - b) ** 2 for a, b in zip(xi, xj))
    beta = attractiveness(beta0, gamma, r2)
    return [a + beta * (b - a) + alpha * (uk - 0.5) * s for a, b, uk, s in zip(xi, xj, u, scale)]


def firefly_algorithm(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    n: int,
    beta0: float,
    gamma: float,
    alpha: float,
    delta: float,
    iterations: int,
    rng: random.Random,
    on_move: Callable[[int, int, Vector, Vector, Vector], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """Firefly algorithm (Yang 2008) for minimizing f on a box.

    For each ordered pair (i, j) with f(x_j) < f(x_i), firefly i moves by
    firefly_move toward j, with the random term scaled by the box widths,
    and is clipped and evaluated at once. Moves are not greedy. After each
    iteration alpha is multiplied by delta. The best point ever evaluated
    is kept. Precondition: n >= 2, lower[j] < upper[j].
    Returns (best point, its value, history of the best value).
    Cost: O(iterations * n^2 * (D + c)) time, at most n (n - 1) moves and
    evaluations per iteration, and O(n D) space.
    """
    d = len(lower)
    scale = [upper[k] - lower[k] for k in range(d)]
    x = [[rng.uniform(lower[k], upper[k]) for k in range(d)] for _ in range(n)]  # @line L1
    fx = [f(p) for p in x]
    b = min(range(n), key=lambda i: fx[i])
    best, best_f = list(x[b]), fx[b]
    history = [best_f]
    for t in range(iterations):  # @line L2
        for i in range(n):  # @line L3
            for j in range(n):  # @line L4
                if fx[j] < fx[i]:  # @line L5
                    u = [rng.random() for _ in range(d)]
                    y = firefly_move(x[i], x[j], beta0, gamma, alpha, u, scale)  # @line L6
                    y = [min(upper[k], max(lower[k], y[k])) for k in range(d)]
                    if on_move is not None:
                        on_move(t, i, list(x[i]), list(x[j]), u)
                    x[i], fx[i] = y, f(y)  # @line L7
                    if fx[i] < best_f:
                        best, best_f = list(x[i]), fx[i]
        alpha *= delta  # @line L8
        history.append(best_f)
    return best, best_f, history  # @line L9


def sphere(x: Sequence[float]) -> float:
    return sum(v * v for v in x)


def rastrigin(x: Sequence[float]) -> float:
    return 10.0 * len(x) + sum(v * v - 10.0 * math.cos(2 * math.pi * v) for v in x)
