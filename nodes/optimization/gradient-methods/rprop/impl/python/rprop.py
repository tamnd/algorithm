# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rprop/. The authors are listed in prov/TRX7X7.jsonl.

"""Rprop in the iRprop- form (Igel and Huesken 2000): only the signs of the gradient are used.

Each coordinate has its own step size delta_i. If the gradient keeps its sign, delta_i grows by eta_plus
(up to delta_max) and x_i moves by delta_i against the sign. If the sign flips, delta_i shrinks by eta_minus
(down to delta_min), the stored gradient is set to 0 and x_i does not move in that iteration.
"""

from collections.abc import Callable

Vector = list[float]


def _sign(a: float) -> float:
    return 1.0 if a > 0 else -1.0 if a < 0 else 0.0


def rprop(
    grad: Callable[[int, Vector], Vector],
    x0: Vector,
    iters: int,
    delta0: float = 0.1,
    eta_plus: float = 1.2,
    eta_minus: float = 0.5,
    delta_min: float = 1e-6,
    delta_max: float = 50.0,
) -> list[Vector]:
    """Return [x_1, ..., x_(iters+1)]; grad(t, x) is the gradient at iteration t (0-based)."""
    x, delta, prev = list(x0), [delta0] * len(x0), [0.0] * len(x0)  # @line L1
    xs = [x]
    for t in range(iters):  # @line L2
        g = list(grad(t, x))  # @line L3
        x = list(x)
        for i in range(len(x)):
            if g[i] * prev[i] > 0:
                delta[i] = min(delta[i] * eta_plus, delta_max)  # @line L4
            elif g[i] * prev[i] < 0:
                delta[i] = max(delta[i] * eta_minus, delta_min)  # @line L5
                g[i] = 0.0
            x[i] -= _sign(g[i]) * delta[i]  # @line L6
        prev = g  # @line L7
        xs.append(x)
    return xs  # @line L8
