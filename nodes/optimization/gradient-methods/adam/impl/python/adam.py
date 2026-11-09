# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adam/. The authors are listed in prov/F3F4VF.jsonl.

"""Adam (Kingma and Ba 2015) with bias correction.

m <- beta1 m + (1 - beta1) g,  v <- beta2 v + (1 - beta2) g^2,
m_hat = m / (1 - beta1^t),  v_hat = v / (1 - beta2^t),  x <- x - alpha_t m_hat / (sqrt(v_hat) + eps).

alpha may be a constant or a function of t = 1, 2, ...; an optional box [lower, upper] is applied by
clipping, as in the online convex setting of the paper. observer(t, m_hat, v_hat) sees the corrected moments.
"""

import math
from collections.abc import Callable

Vector = list[float]


def adam(
    grad: Callable[[int, Vector], Vector],
    x0: Vector,
    alpha: Callable[[int], float] | float,
    beta1: float,
    beta2: float,
    iters: int,
    eps: float = 1e-8,
    lower: Vector | None = None,
    upper: Vector | None = None,
    observer: Callable[[int, Vector, Vector], None] | None = None,
) -> list[Vector]:
    """Return [x_1, ..., x_(iters+1)]; grad(t, x) is the gradient used in round t (0-based)."""
    x, m, v = list(x0), [0.0] * len(x0), [0.0] * len(x0)  # @line L1
    xs = [x]
    for t in range(1, iters + 1):  # @line L2
        g = grad(t - 1, x)  # @line L3
        m = [beta1 * mi + (1 - beta1) * gi for mi, gi in zip(m, g)]  # @line L4
        v = [beta2 * vi + (1 - beta2) * gi * gi for vi, gi in zip(v, g)]  # @line L5
        m_hat = [mi / (1 - beta1**t) for mi in m]  # @line L6
        v_hat = [vi / (1 - beta2**t) for vi in v]
        if observer is not None:
            observer(t, m_hat, v_hat)
        step = alpha(t) if callable(alpha) else alpha
        x = [xi - step * mh / (math.sqrt(vh) + eps) if vh > 0 else xi for xi, mh, vh in zip(x, m_hat, v_hat)]  # @line L7
        if lower is not None and upper is not None:
            x = [min(max(xi, lo), hi) for xi, lo, hi in zip(x, lower, upper)]  # @line L8
        xs.append(x)
    return xs  # @line L9
