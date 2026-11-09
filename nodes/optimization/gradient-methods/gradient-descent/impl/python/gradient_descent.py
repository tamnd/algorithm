# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-descent/. The authors are listed in prov/WZ9ATZ.jsonl.

import math
from typing import Callable

Vector = list[float]


def norm(v: Vector) -> float:
    """Euclidean norm of v."""
    return math.sqrt(sum(t * t for t in v))


def gradient_descent(
    grad: Callable[[Vector], Vector],
    x0: Vector,
    step: float,
    iterations: int,
    tol: float = 0.0,
) -> list[Vector]:
    """Run gradient descent with the fixed step size `step`.

    Each iteration computes g = grad(x) and moves to x - step * g. The loop
    stops after `iterations` steps, or earlier when the norm of the gradient
    is at most `tol`. The result is the list of iterates x_0, x_1, ..., x_k.

    Precondition: grad returns a list of the same length as x0, and step > 0.
    For an L-smooth function, a step in (0, 2/L) makes f decrease at each
    iteration, and 1/L is the standard choice.
    Cost: one gradient evaluation and O(n) arithmetic per iteration.
    """
    x = list(x0)  # @line L1
    path = [list(x)]
    for _ in range(iterations):  # @line L2
        g = grad(x)  # @line L3
        if norm(g) <= tol:  # @line L4
            return path
        x = [xi - step * gi for xi, gi in zip(x, g)]  # @line L5
        path.append(list(x))
    return path  # @line L6
