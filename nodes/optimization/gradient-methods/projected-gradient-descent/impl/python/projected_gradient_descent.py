# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projected-gradient-descent/. The authors are listed in prov/XQJ388.jsonl.

"""Projected gradient descent: a gradient step, then the Euclidean projection onto C.

Vectors are lists of floats. The module gives the method and three projections:
onto a box, onto a Euclidean ball, and onto the probability simplex.
"""

import math
from collections.abc import Callable

Vector = list[float]


def projected_gradient_descent(
    grad: Callable[[Vector], Vector],
    project: Callable[[Vector], Vector],
    x0: Vector,
    step: Callable[[int], float] | float,
    iters: int,
) -> list[Vector]:
    """Return [x_0, x_1, ..., x_iters] with x_(k+1) = project(x_k - step_k * grad(x_k)).

    step is a constant or a function of k. For a smooth f use the constant 1/L_f; for
    a nonsmooth f, grad may return any subgradient and step should shrink.
    """
    x = project(list(x0))  # @line L1
    xs = [x]
    for k in range(iters):  # @line L2
        t = step(k) if callable(step) else step
        g = grad(x)
        y = [xi - t * gi for xi, gi in zip(x, g)]  # @line L3
        x = project(y)  # @line L4
        xs.append(x)
    return xs  # @line L5


def project_box(lo: Vector, hi: Vector) -> Callable[[Vector], Vector]:
    """The projection onto {x : lo <= x <= hi}: clip each coordinate."""

    def project(v: Vector) -> Vector:
        return [min(max(a, l), h) for a, l, h in zip(v, lo, hi)]

    return project


def project_ball(center: Vector, radius: float) -> Callable[[Vector], Vector]:
    """The projection onto the Euclidean ball: scale v - center down to the radius."""

    def project(v: Vector) -> Vector:
        d = [a - c for a, c in zip(v, center)]
        norm = math.sqrt(sum(a * a for a in d))
        if norm <= radius:
            return list(v)
        return [c + radius * a / norm for a, c in zip(d, center)]

    return project


def project_simplex(v: Vector) -> Vector:
    """The projection onto {x : x >= 0, sum x = 1}, by sorting (O(n log n)).

    The answer is max(v_i - theta, 0) with theta chosen so that the entries sum to 1.
    """
    u = sorted(v, reverse=True)
    total, theta = 0.0, 0.0
    for j, a in enumerate(u, 1):
        total += a
        t = (total - 1.0) / j
        if a - t > 0:
            theta = t
    return [max(a - theta, 0.0) for a in v]
