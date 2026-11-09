# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adadelta/. The authors are listed in prov/V8X117.jsonl.

"""Adadelta (Zeiler 2012): the step is the gradient times RMS[dx]_(t-1) / RMS[g]_t.

E[g^2] <- rho E[g^2] + (1 - rho) g^2
dx     <- -lr * sqrt(E[dx^2] + eps) / sqrt(E[g^2] + eps_g) * g
E[dx^2] <- rho E[dx^2] + (1 - rho) dx^2
x      <- x + dx

Zeiler uses one eps for both roots and lr = 1. eps and eps_g may be given per coordinate.
"""

import math
from collections.abc import Callable

Vector = list[float]


def _vec(a: float | Vector, d: int) -> Vector:
    return list(a) if isinstance(a, list) else [float(a)] * d


def adadelta(
    grad: Callable[[int, Vector], Vector],
    x0: Vector,
    rho: float,
    iters: int,
    eps: float | Vector = 1e-6,
    eps_g: float | Vector | None = None,
    lr: float = 1.0,
) -> list[Vector]:
    """Return [x_1, ..., x_(iters+1)]; grad(t, x) is the gradient used in round t (0-based)."""
    d = len(x0)
    ex, eg = _vec(eps, d), _vec(eps if eps_g is None else eps_g, d)
    x, acc_g, acc_dx = list(x0), [0.0] * d, [0.0] * d  # @line L1
    xs = [x]
    for t in range(iters):  # @line L2
        g = grad(t, x)  # @line L3
        acc_g = [rho * a + (1 - rho) * gi * gi for a, gi in zip(acc_g, g)]  # @line L4
        dx = [
            -lr * math.sqrt(a + e) / math.sqrt(b + f) * gi if b + f > 0 else 0.0
            for a, e, b, f, gi in zip(acc_dx, ex, acc_g, eg, g)
        ]  # @line L5
        acc_dx = [rho * a + (1 - rho) * di * di for a, di in zip(acc_dx, dx)]  # @line L6
        x = [xi + di for xi, di in zip(x, dx)]  # @line L7
        xs.append(x)
    return xs  # @line L8
