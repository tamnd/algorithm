# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-checking/. The authors are listed in prov/3WZDG5.jsonl.
"""Gradient checking: compare an analytic gradient with finite differences.

numerical_gradient uses the central difference (f(t + h e_i) - f(t - h e_i)) / 2h,
whose truncation error is O(h^2), or the forward difference
(f(t + h e_i) - f(t)) / h, whose error is O(h). The default steps are the ones
that balance truncation against rounding: cbrt(eps) for central and sqrt(eps)
for forward differences, scaled by max(1, |t_i|).

check_gradient returns the largest relative error
|g_i - n_i| / max(|g_i|, |n_i|, tiny) over the coordinates.
"""

import sys
from typing import Callable, Sequence

EPS = sys.float_info.epsilon  # 2^-52
TINY = 1e-300


def default_step(scheme: str) -> float:
    return EPS ** (1.0 / 3.0) if scheme == "central" else EPS ** 0.5


def numerical_gradient(f: Callable[[list[float]], float], theta: Sequence[float],
                       h: float | None = None, scheme: str = "central") -> list[float]:
    if h is None:
        h = default_step(scheme)
    t = list(theta)
    f0 = f(t) if scheme == "forward" else 0.0
    out = []
    for i in range(len(t)):  # @line L1
        ti = t[i]
        hi = h * max(1.0, abs(ti))
        t[i] = ti + hi  # @line L2
        fp = f(t)
        up = t[i] - ti  # the step that was actually taken, after rounding
        if scheme == "central":
            t[i] = ti - hi  # @line L2
            fm = f(t)
            down = ti - t[i]
            out.append((fp - fm) / (up + down))  # @line L3
        else:
            out.append((fp - f0) / up)
        t[i] = ti
    return out


def relative_error(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), TINY)  # @line L4


def check_gradient(f: Callable[[list[float]], float], grad: Callable[[list[float]], list[float]],
                   theta: Sequence[float], tol: float = 1e-6,
                   h: float | None = None, scheme: str = "central"):
    """Return (ok, worst, errors): ok is worst <= tol."""
    g = grad(list(theta))
    n = numerical_gradient(f, theta, h, scheme)
    errors = [relative_error(a, b) for a, b in zip(g, n)]
    worst = max(errors) if errors else 0.0
    return worst <= tol, worst, errors  # @line L5
