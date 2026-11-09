# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nesterov-accelerated-gradient/. The authors are listed in prov/FR184S.jsonl.

"""Nesterov's accelerated gradient method for an L-smooth convex function.

x_k = y_k - grad f(y_k) / L, then y_{k+1} = x_k + beta_k (x_k - x_{k-1}), with y_1 = x_0.
For convex f, beta_k = (t_k - 1) / t_{k+1} with t_1 = 1 and t_{k+1} = (1 + sqrt(1 + 4 t_k^2)) / 2.
For mu-strongly convex f, beta_k is the constant (sqrt(kappa) - 1) / (sqrt(kappa) + 1), kappa = L / mu.

Vectors are lists of floats. All arithmetic is in floating point.
"""

import math
from typing import Callable, List

Vector = List[float]


def nesterov_accelerated_gradient(
    grad: Callable[[Vector], Vector],
    x0: Vector,
    lipschitz: float,
    iterations: int,
    mu: float = 0.0,
    tol: float = 0.0,
) -> List[Vector]:
    """Return the iterates x_0, x_1, ..., x_K (the points reached by gradient steps).

    lipschitz is the smoothness constant L. If mu > 0 the constant momentum for
    mu-strongly convex functions is used. Stop after `iterations` gradient steps or when
    the gradient norm at the current extrapolated point y is at most tol.
    """
    if not lipschitz > 0.0:
        raise ValueError("need L > 0")
    if not (0.0 <= mu <= lipschitz):
        raise ValueError("need 0 <= mu <= L")
    constant_beta = None
    if mu > 0.0:
        root_kappa = math.sqrt(lipschitz / mu)
        constant_beta = (root_kappa - 1.0) / (root_kappa + 1.0)
    x_prev, y, t = list(x0), list(x0), 1.0  # @line L1
    path = [list(x0)]
    for _ in range(iterations):  # @line L2
        g = grad(y)
        if math.sqrt(sum(v * v for v in g)) <= tol:
            break
        x = [yi - gi / lipschitz for yi, gi in zip(y, g)]  # @line L3
        t_next = (1.0 + math.sqrt(1.0 + 4.0 * t * t)) / 2.0  # @line L4
        beta = (t - 1.0) / t_next if constant_beta is None else constant_beta  # @line L5
        y = [xi + beta * (xi - pi) for xi, pi in zip(x, x_prev)]  # @line L6
        x_prev, t = x, t_next  # @line L7
        path.append(list(x))
    return path  # @line L8
