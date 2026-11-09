# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/momentum-method/. The authors are listed in prov/MHMX5D.jsonl.

"""Polyak's heavy ball method: x_{k+1} = x_k - alpha grad f(x_k) + beta (x_k - x_{k-1}), with x_{-1} = x_0.

Vectors are lists of floats. All arithmetic is in floating point.
"""

import math
from typing import Callable, List, Tuple

Vector = List[float]


def heavy_ball(
    grad: Callable[[Vector], Vector],
    x0: Vector,
    alpha: float,
    beta: float,
    iterations: int,
    tol: float = 0.0,
) -> List[Vector]:
    """Return the iterates x_0, x_1, ... of the heavy ball method.

    Stop after `iterations` steps or when the gradient norm at the current point is at most tol.
    """
    if not (alpha > 0.0 and 0.0 <= beta < 1.0):
        raise ValueError("need alpha > 0 and 0 <= beta < 1")
    x_prev, x = list(x0), list(x0)  # @line L1
    path = [list(x)]
    for _ in range(iterations):  # @line L2
        g = grad(x)  # @line L3
        if math.sqrt(sum(t * t for t in g)) <= tol:
            break
        x_next = [xi - alpha * gi + beta * (xi - pi) for xi, gi, pi in zip(x, g, x_prev)]  # @line L4
        x_prev, x = x, x_next  # @line L5
        path.append(list(x))
    return path  # @line L6


def heavy_ball_velocity(
    grad: Callable[[Vector], Vector], x0: Vector, alpha: float, beta: float, iterations: int
) -> List[Vector]:
    """The same method in velocity form: v_{k+1} = beta v_k - alpha grad f(x_k), x_{k+1} = x_k + v_{k+1}, v_0 = 0."""
    x, v = list(x0), [0.0] * len(x0)
    path = [list(x)]
    for _ in range(iterations):
        g = grad(x)
        v = [beta * vi - alpha * gi for vi, gi in zip(v, g)]
        x = [xi + vi for xi, vi in zip(x, v)]
        path.append(list(x))
    return path


def tuned_parameters(mu: float, lipschitz: float) -> Tuple[float, float]:
    """Polyak's parameters for a quadratic with Hessian eigenvalues in [mu, L]:
    alpha = 4 / (sqrt(L) + sqrt(mu))^2 and beta = ((sqrt(kappa) - 1) / (sqrt(kappa) + 1))^2."""
    if not (0.0 < mu <= lipschitz):
        raise ValueError("need 0 < mu <= L")
    s_mu, s_l = math.sqrt(mu), math.sqrt(lipschitz)
    alpha = 4.0 / (s_l + s_mu) ** 2
    beta = ((s_l - s_mu) / (s_l + s_mu)) ** 2
    return alpha, beta
