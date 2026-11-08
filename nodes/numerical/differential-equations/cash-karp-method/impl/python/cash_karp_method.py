# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cash-karp-method/. The authors are listed in prov/1KQDQK.jsonl.

"""The Cash-Karp 5(4) embedded Runge-Kutta pair with adaptive step size.

Six stages per attempted step. The order-5 solution (weights B) is kept; the difference to the
order-4 solution (weights BHAT) is the error estimate, which behaves like C h^5. There is no
FSAL property, so a step costs six evaluations of f. y0 may be a float or a list.
"""

import math
from fractions import Fraction as Fr
from typing import Callable, List, Optional, Sequence, Tuple, Union

State = Union[float, Sequence[float]]

C = [Fr(0), Fr(1, 5), Fr(3, 10), Fr(3, 5), Fr(1), Fr(7, 8)]
A = [
    [],
    [Fr(1, 5)],
    [Fr(3, 40), Fr(9, 40)],
    [Fr(3, 10), Fr(-9, 10), Fr(6, 5)],
    [Fr(-11, 54), Fr(5, 2), Fr(-70, 27), Fr(35, 27)],
    [Fr(1631, 55296), Fr(175, 512), Fr(575, 13824), Fr(44275, 110592), Fr(253, 4096)],
]
B = [Fr(37, 378), Fr(0), Fr(250, 621), Fr(125, 594), Fr(0), Fr(512, 1771)]
BHAT = [Fr(2825, 27648), Fr(0), Fr(18575, 48384), Fr(13525, 55296), Fr(277, 14336), Fr(1, 4)]

_A = [[float(v) for v in row] for row in A]
_C = [float(v) for v in C]
_B = [float(v) for v in B]
_E = [float(B[i] - BHAT[i]) for i in range(6)]


def ck_step(f: Callable, t: float, y: List[float], h: float) -> Tuple[List[float], List[float]]:
    """One Cash-Karp step. Returns (y_new of order 5, error estimate y_new - y_hat)."""
    d = len(y)
    k = []
    for i in range(6):  # @line L4: the six stages
        yi = [y[m] + h * sum(_A[i][j] * k[j][m] for j in range(i)) for m in range(d)]
        k.append(f(t + _C[i] * h, yi))
    y_new = [y[m] + h * sum(_B[i] * k[i][m] for i in range(6)) for m in range(d)]  # @line L5
    err = [h * sum(_E[i] * k[i][m] for i in range(6)) for m in range(d)]  # @line L6
    return y_new, err


def cash_karp(f: Callable, t0: float, y0: State, t_end: float, rtol: float = 1e-6, atol: float = 1e-9,
              h0: Optional[float] = None, h_max: float = math.inf,
              max_steps: int = 1_000_000) -> Tuple[List[float], list, dict]:
    """Integrate adaptively from t0 to t_end >= t0.

    A step is accepted when max_i |err_i| / (atol + rtol * max(|y_i|, |y_new_i|)) <= 1.
    Returns (ts, ys, stats) with stats = {"accepted", "rejected", "evaluations"}.
    """
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if rtol <= 0 and atol <= 0:
        raise ValueError("rtol or atol must be positive")
    scalar = isinstance(y0, (int, float))
    calls = [0]

    def fv(t, y):
        calls[0] += 1
        return [f(t, y[0])] if scalar else [float(v) for v in f(t, y)]

    y = [float(y0)] if scalar else [float(v) for v in y0]
    ts, ys = [t0], [y[0] if scalar else list(y)]
    stats = {"accepted": 0, "rejected": 0, "evaluations": 0}
    span = t_end - t0
    if span == 0:
        return ts, ys, stats
    t = t0
    if h0 is None:  # @line L1: a starting step from the sizes of y and f (Hairer, Norsett and Wanner, II.4)
        f0 = fv(t0, y)
        sc = [atol + rtol * abs(v) for v in y]
        d0 = max(abs(y[i]) / sc[i] for i in range(len(y)))
        d1 = max(abs(f0[i]) / sc[i] for i in range(len(y)))
        h0 = 1e-6 if d0 < 1e-5 or d1 < 1e-5 else 0.01 * d0 / d1
    h = min(h0, span, h_max)
    while t < t_end:  # @line L2
        if stats["accepted"] + stats["rejected"] >= max_steps:
            raise ArithmeticError("too many steps; the problem may be stiff")
        last = t + h >= t_end - 1e-12 * max(1.0, abs(t_end))
        if last:
            h = t_end - t  # @line L3: the final step ends exactly at t_end
        y_new, e = ck_step(fv, t, y, h)
        err = max(abs(e[i]) / (atol + rtol * max(abs(y[i]), abs(y_new[i]))) for i in range(len(y)))  # @line L7
        if err <= 1.0:  # @line L8
            t = t_end if last else t + h
            y = y_new
            ts.append(t)
            ys.append(y[0] if scalar else list(y))
            stats["accepted"] += 1
        else:
            stats["rejected"] += 1
        fac = 5.0 if err == 0.0 else min(5.0, max(0.2, 0.9 * err ** (-0.2)))
        if err > 1.0:
            fac = min(fac, 1.0)
        h = min(h * fac, h_max)  # @line L9
    stats["evaluations"] = calls[0]
    return ts, ys, stats  # @line L10
