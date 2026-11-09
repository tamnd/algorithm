# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coordinate-descent/. The authors are listed in prov/TFA12A.jsonl.

"""Coordinate descent: change one coordinate per step.

coordinate_descent is the coordinate gradient method with the steps 1/L_i, with a random
or a cyclic choice of the coordinate. lasso_coordinate_descent is the cyclic exact
minimization for the lasso, with soft thresholding and a running residual.
"""

import random
from collections.abc import Callable

Vector = list[float]


def coordinate_descent(
    partial: Callable[[Vector, int], float],
    lipschitz: Vector,
    x0: Vector,
    iters: int,
    rng: random.Random | None = None,
) -> tuple[list[Vector], list[int]]:
    """Return the iterates [x_0, ..., x_iters] and the chosen coordinates.

    partial(x, i) is the i-th partial derivative of f at x, and lipschitz[i] is L_i.
    With rng the coordinate is uniform at random; without it the order is cyclic.
    """
    n = len(x0)
    x = list(x0)  # @line L1
    xs, chosen = [list(x)], []
    for k in range(iters):  # @line L2
        i = rng.randrange(n) if rng is not None else k % n  # @line L3
        x[i] -= partial(x, i) / lipschitz[i]  # @line L4
        xs.append(list(x))
        chosen.append(i)
    return xs, chosen  # @line L5


def soft_threshold(v: float, t: float) -> float:
    """The minimizer of t |u| + (u - v)^2 / 2 over u."""
    if v > t:
        return v - t
    if v < -t:
        return v + t
    return 0.0


def lasso_coordinate_descent(a: list[Vector], b: Vector, lam: float, x0: Vector, sweeps: int) -> list[Vector]:
    """Cyclic coordinate minimization of 0.5 ||A x - b||^2 + lam ||x||_1.

    Returns the iterate after each single-coordinate update (1 + sweeps * n points).
    Each update costs O(m), because the residual r = A x - b is kept up to date.
    """
    m, n = len(a), len(x0)
    x = list(x0)
    r = [sum(a[i][j] * x[j] for j in range(n)) - b[i] for i in range(m)]
    col2 = [sum(a[i][j] ** 2 for i in range(m)) for j in range(n)]
    xs = [list(x)]
    for _ in range(sweeps):
        for j in range(n):
            if col2[j] == 0.0:
                xs.append(list(x))
                continue
            rho = col2[j] * x[j] - sum(a[i][j] * r[i] for i in range(m))  # a_j^T (b - A x + a_j x_j)
            new = soft_threshold(rho, lam) / col2[j]
            d = new - x[j]
            if d != 0.0:
                for i in range(m):
                    r[i] += a[i][j] * d
                x[j] = new
            xs.append(list(x))
    return xs
