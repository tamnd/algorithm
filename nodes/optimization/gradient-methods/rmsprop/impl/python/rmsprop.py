# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rmsprop/. The authors are listed in prov/DDRZ14.jsonl.

"""RMSProp: divide each gradient coordinate by the root of an exponential moving average of its squares.

v <- beta v + (1 - beta) g^2,  x <- x - eta_t g / (sqrt(v) + eps).

eta and beta may be constants or functions of the round t = 1, 2, ...; an optional box [lower, upper]
is applied by clipping, as in the online convex setting.
"""

import math
from collections.abc import Callable

Vector = list[float]
Schedule = Callable[[int], float] | float


def _at(s: Schedule, t: int) -> float:
    return s(t) if callable(s) else s


def rmsprop(
    grad: Callable[[int, Vector], Vector],
    x0: Vector,
    eta: Schedule,
    beta: Schedule,
    iters: int,
    eps: float = 0.0,
    lower: Vector | None = None,
    upper: Vector | None = None,
) -> list[Vector]:
    """Return [x_1, ..., x_(iters+1)]; grad(t, x) is the gradient used in round t (0-based)."""
    x = list(x0)  # @line L1
    v = [0.0] * len(x)
    xs = [x]
    for t in range(1, iters + 1):  # @line L2
        g = grad(t - 1, x)  # @line L3
        b = _at(beta, t)
        v = [b * vi + (1 - b) * gi * gi for vi, gi in zip(v, g)]  # @line L4
        step = _at(eta, t)
        x = [xi - step * gi / (math.sqrt(vi) + eps) if vi > 0 else xi for xi, gi, vi in zip(x, g, v)]  # @line L5
        if lower is not None and upper is not None:
            x = [min(max(xi, lo), hi) for xi, lo, hi in zip(x, lower, upper)]  # @line L6
        xs.append(x)
    return xs  # @line L7
