# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fista/. The authors are listed in prov/KTPH6E.jsonl.

"""FISTA, the accelerated proximal gradient method of Beck and Teboulle (2009).

It minimizes F(x) = f(x) + h(x), where f is convex and L_f-smooth and h is closed,
convex and has a cheap proximal operator. Vectors are lists of floats.
"""

import math
from collections.abc import Callable

Vector = list[float]


def soft_threshold(v: Vector, tau: float) -> Vector:
    """The prox of tau * ||.||_1."""
    return [a - tau if a > tau else a + tau if a < -tau else 0.0 for a in v]


def fista(
    grad_f: Callable[[Vector], Vector],
    prox_h: Callable[[Vector, float], Vector],
    x0: Vector,
    step: float,
    iters: int,
) -> tuple[list[Vector], list[float]]:
    """Run iters steps with a constant step (at most 1/L_f).

    Return (xs, taus): xs = [x_0, x_1, ..., x_iters] and taus = [t_1, ..., t_(iters+1)],
    the momentum sequence, so that x_k comes with taus[k - 1] = t_k.
    prox_h(v, s) must return prox_{s h}(v).
    """
    y = list(x0)  # @line L1
    x_prev = list(x0)
    tau = 1.0
    xs, taus = [list(x0)], [tau]
    for _ in range(iters):  # @line L2
        g = grad_f(y)
        x = prox_h([yi - step * gi for yi, gi in zip(y, g)], step)  # @line L3
        tau_next = (1.0 + math.sqrt(1.0 + 4.0 * tau * tau)) / 2.0  # @line L4
        beta = (tau - 1.0) / tau_next
        y = [xi + beta * (xi - pi) for xi, pi in zip(x, x_prev)]  # @line L5
        x_prev, tau = x, tau_next  # @line L6
        xs.append(x)
        taus.append(tau)
    return xs, taus  # @line L7
