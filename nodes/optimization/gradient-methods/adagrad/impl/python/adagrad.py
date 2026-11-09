# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adagrad/. The authors are listed in prov/M591DH.jsonl.

"""Diagonal AdaGrad: x_i <- clip(x_i - eta g_i / sqrt(sum of past g_i^2)) on an optional box.

grad(t, x) returns the (sub)gradient of the loss of round t at x; in a stochastic setting it is
a sample gradient. With eps = 0 a coordinate whose gradients have all been 0 does not move,
which is the version with the regret bound; eps > 0 is the usual guard in practice.
"""

import math
from collections.abc import Callable

Vector = list[float]


def adagrad(
    grad: Callable[[int, Vector], Vector],
    x0: Vector,
    eta: float,
    iters: int,
    lower: Vector | None = None,
    upper: Vector | None = None,
    eps: float = 0.0,
) -> list[Vector]:
    """Return [x_1, ..., x_(iters+1)], where x_1 = x0 is played in round 1."""
    x = list(x0)  # @line L1
    s = [0.0] * len(x)
    xs = [x]
    for t in range(iters):  # @line L2
        g = grad(t, x)  # @line L3
        s = [a + b * b for a, b in zip(s, g)]  # @line L4
        x = [xi - eta * gi / (math.sqrt(si) + eps) if si > 0 else xi for xi, gi, si in zip(x, g, s)]  # @line L5
        if lower is not None and upper is not None:
            x = [min(max(xi, lo), hi) for xi, lo, hi in zip(x, lower, upper)]  # @line L6
        xs.append(x)
    return xs  # @line L7
