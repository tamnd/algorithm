# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-search/. The authors are listed in prov/TQA8RV.jsonl.

import math
import random
from collections.abc import Callable, Sequence

Vector = list[float]


def mantegna_sigma(beta: float) -> float:
    """sigma_u of Mantegna's method: (Gamma(1+b) sin(pi b / 2) / (Gamma((1+b)/2) b 2^((b-1)/2)))^(1/b)."""
    num = math.gamma(1 + beta) * math.sin(math.pi * beta / 2)
    den = math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)
    return (num / den) ** (1 / beta)


def levy_step(beta: float, rng: random.Random) -> float:
    """Mantegna's step u / |v|^(1/beta), with u ~ N(0, sigma_u^2) and v ~ N(0, 1)."""
    u = rng.gauss(0.0, mantegna_sigma(beta))
    v = rng.gauss(0.0, 1.0)
    return u / abs(v) ** (1 / beta)


def clip(x: Sequence[float], lower: Sequence[float], upper: Sequence[float]) -> Vector:
    return [min(hi, max(lo, v)) for v, lo, hi in zip(x, lower, upper)]


def levy_move(x: Sequence[float], g: Sequence[float], alpha: float, beta: float, rng: random.Random) -> Vector:
    """y_j = x_j + alpha * L_j * (x_j - g_j) * N_j, with L_j a Mantegna step and N_j ~ N(0, 1), as in Yang's code."""
    return [xj + alpha * levy_step(beta, rng) * (xj - gj) * rng.gauss(0.0, 1.0) for xj, gj in zip(x, g)]


def de_move(x: Sequence[float], xp: Sequence[float], xq: Sequence[float], r: float, mask: Sequence[bool]) -> Vector:
    """y_j = x_j + r (xp_j - xq_j) where mask[j] is True, and y_j = x_j elsewhere."""
    return [xj + r * (a - b) if m else xj for xj, a, b, m in zip(x, xp, xq, mask)]


def cuckoo_search(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    nests: int,
    p_a: float,
    alpha: float,
    beta: float,
    iterations: int,
    rng: random.Random,
    on_iteration: Callable[[int, list[Vector], list[float]], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """Cuckoo search (Yang and Deb 2009) for minimizing f on a box.

    Phase 1: every nest x_i proposes levy_move(x_i, best) and keeps it if
    better. Phase 2: every nest proposes de_move with two random nests, a
    uniform r and a mask that changes each coordinate with probability p_a,
    and keeps it if better. Proposals are clipped to the box.
    Precondition: nests >= 2, 0 <= p_a <= 1, 0 < beta <= 2, lower[j] < upper[j].
    Returns (best point, its value, history of the best value).
    Cost: O(iterations * nests * (D + c)) time and O(nests * D) space.
    """
    d = len(lower)
    x = [[rng.uniform(lower[j], upper[j]) for j in range(d)] for _ in range(nests)]  # @line L1
    fx = [f(p) for p in x]
    b = min(range(nests), key=lambda i: fx[i])
    g, fg = list(x[b]), fx[b]
    history = [fg]
    for t in range(iterations):  # @line L2
        for i in range(nests):
            y = clip(levy_move(x[i], g, alpha, beta, rng), lower, upper)  # @line L3
            fy = f(y)
            if fy < fx[i]:  # @line L4
                x[i], fx[i] = y, fy
        b = min(range(nests), key=lambda i: fx[i])
        if fx[b] < fg:  # @line L5
            g, fg = list(x[b]), fx[b]
        for i in range(nests):
            p, q = rng.randrange(nests), rng.randrange(nests)
            r = rng.random()
            mask = [rng.random() < p_a for _ in range(d)]
            y = clip(de_move(x[i], x[p], x[q], r, mask), lower, upper)  # @line L6
            fy = f(y)
            if fy < fx[i]:  # @line L7
                x[i], fx[i] = y, fy
        b = min(range(nests), key=lambda i: fx[i])
        if fx[b] < fg:  # @line L8
            g, fg = list(x[b]), fx[b]
        history.append(fg)
        if on_iteration is not None:
            on_iteration(t, [list(p) for p in x], list(fx))
    return g, fg, history  # @line L9


def sphere(x: Sequence[float]) -> float:
    return sum(v * v for v in x)


def rastrigin(x: Sequence[float]) -> float:
    return 10.0 * len(x) + sum(v * v - 10.0 * math.cos(2 * math.pi * v) for v in x)
