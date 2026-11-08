# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dormand-prince-method/. The authors are listed in prov/Q8KN04.jsonl.

"""The Dormand-Prince 5(4) embedded Runge-Kutta pair (DOPRI5) with step size control.

Seven stages, the last one is FSAL (first same as last), so an accepted step costs six
evaluations of f. The fifth-order solution is propagated (local extrapolation) and the
difference to the fourth-order solution estimates the local error.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction as Fr
from typing import Any, Callable, List, Optional, Sequence, Tuple

C = [Fr(0), Fr(1, 5), Fr(3, 10), Fr(4, 5), Fr(8, 9), Fr(1), Fr(1)]
A = [
    [],
    [Fr(1, 5)],
    [Fr(3, 40), Fr(9, 40)],
    [Fr(44, 45), Fr(-56, 15), Fr(32, 9)],
    [Fr(19372, 6561), Fr(-25360, 2187), Fr(64448, 6561), Fr(-212, 729)],
    [Fr(9017, 3168), Fr(-355, 33), Fr(46732, 5247), Fr(49, 176), Fr(-5103, 18656)],
    [Fr(35, 384), Fr(0), Fr(500, 1113), Fr(125, 192), Fr(-2187, 6784), Fr(11, 84)],
]
B = [Fr(35, 384), Fr(0), Fr(500, 1113), Fr(125, 192), Fr(-2187, 6784), Fr(11, 84), Fr(0)]
B_HAT = [Fr(5179, 57600), Fr(0), Fr(7571, 16695), Fr(393, 640), Fr(-92097, 339200),
         Fr(187, 2100), Fr(1, 40)]
E = [b - bh for b, bh in zip(B, B_HAT)]  # weights of the error estimate

_A = [[float(x) for x in row] for row in A]
_C = [float(x) for x in C]
_E = [float(x) for x in E]

FAC, FAC_MIN, FAC_MAX = 0.9, 0.2, 5.0  # safety factor and limits of the step change


@dataclass
class DopriResult:
    """The final time and value and the work: accepted and rejected steps, evaluations of f."""

    t: float
    y: List[float]
    accepted: int
    rejected: int
    f_evals: int
    path: List[Tuple[float, List[float]]] = field(default_factory=list)


def _norm(e: Sequence[float], y: Sequence[float], y_new: Sequence[float],
          atol: float, rtol: float) -> float:
    """Root mean square of e_i / (atol + rtol max(|y_i|, |y_new_i|))."""
    s = 0.0
    for ei, a, b in zip(e, y, y_new):
        s += (ei / (atol + rtol * max(abs(a), abs(b)))) ** 2
    return math.sqrt(s / len(e))


def initial_step(f: Callable, t0: float, y0: List[float], f0: List[float], atol: float,
                 rtol: float, order: int = 5) -> float:
    """The starting step of Hairer, Norsett and Wanner (Section II.4); one evaluation of f."""
    d0 = math.sqrt(sum((a / (atol + rtol * abs(a))) ** 2 for a in y0) / len(y0))
    d1 = math.sqrt(sum((b / (atol + rtol * abs(a))) ** 2 for a, b in zip(y0, f0)) / len(y0))
    h0 = 1e-6 if d0 < 1e-5 or d1 < 1e-5 else 0.01 * d0 / d1
    y1 = [a + h0 * b for a, b in zip(y0, f0)]
    f1 = f(t0 + h0, y1)
    d2 = math.sqrt(sum(((c - b) / (atol + rtol * abs(a))) ** 2
                       for a, b, c in zip(y0, f0, f1)) / len(y0)) / h0
    m = max(d1, d2)
    h1 = max(1e-6, h0 * 1e-3) if m <= 1e-15 else (0.01 / m) ** (1.0 / (order + 1))
    return min(100 * h0, h1)


def dormand_prince_method(f: Callable[[float, List[float]], List[float]], t0: float,
                          y0: Sequence[float], t_end: float, atol: float = 1e-6,
                          rtol: float = 1e-6, h: Optional[float] = None,
                          max_steps: int = 100000, keep_path: bool = False) -> DopriResult:
    """Integrate y' = f(t, y), y(t0) = y0 (a list of floats) from t0 to t_end >= t0.

    Each step is accepted when the scaled error estimate err <= 1. The new step is
    h min(FAC_MAX, max(FAC_MIN, FAC err^(-1/5))), and FAC_MAX is 1 right after a rejection.
    The last step is cut to end exactly at t_end. Cost: 6 evaluations of f per attempted
    step, plus 1 for the first slope and 1 for the starting step when h is None;
    O(d) extra space, O(d) per step besides f.
    """
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    t, y = t0, [float(v) for v in y0]
    path = [(t, list(y))] if keep_path else []
    if t_end == t0:
        return DopriResult(t, y, 0, 0, 0, path)
    k1 = f(t, y)  # @line L1
    evals = 1
    if h is None:
        h = initial_step(f, t, y, k1, atol, rtol)
        evals += 1
    h = min(h, t_end - t0)
    fac_max = FAC_MAX
    accepted = rejected = 0
    while t < t_end:  # @line L2
        if accepted + rejected >= max_steps:
            raise RuntimeError("too many steps")
        last = t + h >= t_end - 1e-12 * abs(t_end)
        if last:
            h = t_end - t  # @line L3
        if h <= 1e-14 * max(1.0, abs(t)):
            raise RuntimeError("step size underflow")
        ks = [k1]
        for i in range(1, 6):  # @line L4
            yi = [y[m] + h * sum(_A[i][j] * ks[j][m] for j in range(i)) for m in range(len(y))]
            ks.append(f(t + _C[i] * h, yi))
        y_new = [y[m] + h * sum(_A[6][j] * ks[j][m] for j in range(6)) for m in range(len(y))]
        k7 = f(t + h, y_new)  # @line L5
        ks.append(k7)
        evals += 6
        e = [h * sum(_E[j] * ks[j][m] for j in range(7)) for m in range(len(y))]
        err = _norm(e, y, y_new, atol, rtol)  # @line L6
        if err <= 1.0:  # @line L7
            t = t_end if last else t + h
            y, k1 = y_new, k7
            accepted += 1
            fac_max = FAC_MAX
            if keep_path:
                path.append((t, list(y)))
        else:
            rejected += 1  # @line L8
            fac_max = 1.0
        factor = fac_max if err == 0.0 else min(fac_max, max(FAC_MIN, FAC * err ** -0.2))
        h = h * factor  # @line L9
    return DopriResult(t, y, accepted, rejected, evals, path)  # @line L10


def fixed_step(f: Callable, t0: float, y0: Sequence[float], h: float, n: int,
               weights: Sequence[Any] = B) -> List[float]:
    """n steps of constant length h with the given weights (B: order 5, B_HAT: order 4)."""
    w = [float(x) for x in weights]
    t, y = t0, [float(v) for v in y0]
    for s in range(n):
        ks = []
        for i in range(7):
            yi = [y[m] + h * sum(_A[i][j] * ks[j][m] for j in range(i)) for m in range(len(y))]
            ks.append(f(t + _C[i] * h, yi))
        y = [y[m] + h * sum(w[j] * ks[j][m] for j in range(7)) for m in range(len(y))]
        t = t0 + (s + 1) * h
    return y
