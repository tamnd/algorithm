# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bogacki-shampine-method/. The authors are listed in prov/34RG05.jsonl.

"""The Bogacki-Shampine 3(2) embedded Runge-Kutta pair with adaptive step size (BS23, ode23).

    0   |
    1/2 | 1/2
    3/4 | 0     3/4
    1   | 2/9   1/3   4/9
    ----+-----------------------
    b   | 2/9   1/3   4/9   0       order 3 (the solution that is kept)
    b^  | 7/24  1/4   1/3   1/8     order 2 (used only for the error estimate)

The fourth stage is f at the new solution, so it is the first stage of the next step
(FSAL): an accepted step costs three new evaluations of f. y0 may be a float or a list.
"""

import math
from fractions import Fraction as Fr
from typing import Callable, List, Optional, Sequence, Tuple, Union

State = Union[float, Sequence[float]]

A = [[Fr(0)] * 4, [Fr(1, 2), Fr(0), Fr(0), Fr(0)], [Fr(0), Fr(3, 4), Fr(0), Fr(0)],
     [Fr(2, 9), Fr(1, 3), Fr(4, 9), Fr(0)]]
B = [Fr(2, 9), Fr(1, 3), Fr(4, 9), Fr(0)]
BHAT = [Fr(7, 24), Fr(1, 4), Fr(1, 3), Fr(1, 8)]
C = [Fr(0), Fr(1, 2), Fr(3, 4), Fr(1)]
_E = [float(B[i] - BHAT[i]) for i in range(4)]  # -5/72, 1/12, 1/9, -1/8


def bs23_step(f: Callable, t: float, y: List[float], h: float, k1: List[float]):
    """One step from (t, y) with k1 = f(t, y). Returns (y_new, k4, err_vector)."""
    k2 = f(t + h / 2, [y[i] + h / 2 * k1[i] for i in range(len(y))])  # @line L4
    k3 = f(t + 3 * h / 4, [y[i] + 3 * h / 4 * k2[i] for i in range(len(y))])  # @line L5
    y_new = [y[i] + h * (2 / 9 * k1[i] + 1 / 3 * k2[i] + 4 / 9 * k3[i]) for i in range(len(y))]  # @line L6
    k4 = f(t + h, y_new)  # @line L7
    err = [h * (_E[0] * k1[i] + _E[1] * k2[i] + _E[2] * k3[i] + _E[3] * k4[i]) for i in range(len(y))]
    return y_new, k4, err


def _initial_step(f, t0, y, k1, rtol, atol, span):
    """A starting step from the size of y and f (after Hairer, Norsett and Wanner, Section II.4)."""
    sc = [atol + rtol * abs(v) for v in y]
    d0 = max(abs(y[i]) / sc[i] for i in range(len(y)))
    d1 = max(abs(k1[i]) / sc[i] for i in range(len(y)))
    h = 1e-6 if d0 < 1e-5 or d1 < 1e-5 else 0.01 * d0 / d1
    return min(h, span)


def bogacki_shampine(f: Callable, t0: float, y0: State, t_end: float, rtol: float = 1e-3,
                     atol: float = 1e-6, h0: Optional[float] = None, h_max: float = math.inf,
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
    k1 = fv(t, y)  # @line L1
    h = min(h0 if h0 is not None else _initial_step(fv, t0, y, k1, rtol, atol, span), h_max)
    while t < t_end:  # @line L2
        if stats["accepted"] + stats["rejected"] >= max_steps:
            raise ArithmeticError("too many steps; the problem may be stiff")
        last = t + h >= t_end - 1e-12 * max(1.0, abs(t_end))
        if last:
            h = t_end - t  # @line L3: the final step ends exactly at t_end
        y_new, k4, e = bs23_step(fv, t, y, h, k1)  # lines L4 to L7, in bs23_step
        err = max(abs(e[i]) / (atol + rtol * max(abs(y[i]), abs(y_new[i]))) for i in range(len(y)))  # @line L8
        if err <= 1.0:  # @line L9
            t = t_end if last else t + h
            y, k1 = y_new, k4  # FSAL: the last stage is the next first stage
            ts.append(t)
            ys.append(y[0] if scalar else list(y))
            stats["accepted"] += 1
        else:
            stats["rejected"] += 1
        fac = 5.0 if err == 0.0 else min(5.0, max(0.2, 0.9 * err ** (-1.0 / 3.0)))
        if err > 1.0:
            fac = min(fac, 1.0)
        h = min(h * fac, h_max)  # @line L10
    stats["evaluations"] = calls[0]
    return ts, ys, stats  # @line L11
