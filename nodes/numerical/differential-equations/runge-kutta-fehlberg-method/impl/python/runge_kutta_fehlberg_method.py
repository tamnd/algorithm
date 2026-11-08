# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-fehlberg-method/. The authors are listed in prov/37PW24.jsonl.

"""The Runge-Kutta-Fehlberg 4(5) pair with adaptive step size control.

The step is advanced with the fourth-order formula, as Fehlberg proposed; the difference to
the fifth-order formula estimates its local error.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction as F
from typing import Any, Callable, List, Tuple

C = [F(0), F(1, 4), F(3, 8), F(12, 13), F(1), F(1, 2)]
A = [
    [],
    [F(1, 4)],
    [F(3, 32), F(9, 32)],
    [F(1932, 2197), F(-7200, 2197), F(7296, 2197)],
    [F(439, 216), F(-8), F(3680, 513), F(-845, 4104)],
    [F(-8, 27), F(2), F(-3544, 2565), F(1859, 4104), F(-11, 40)],
]
B4 = [F(25, 216), F(0), F(1408, 2565), F(2197, 4104), F(-1, 5), F(0)]
B5 = [F(16, 135), F(0), F(6656, 12825), F(28561, 56430), F(-9, 50), F(2, 55)]
E = [b5 - b4 for b4, b5 in zip(B4, B5)]  # error weights: 1/360, 0, -128/4275, -2197/75240, 1/50, 2/55

_Cf = [float(x) for x in C]
_Af = [[float(x) for x in row] for row in A]
_B4f = [float(x) for x in B4]
_Ef = [float(x) for x in E]


@dataclass
class RKFResult:
    """The final time and value and the work done."""

    t: float
    y: Any
    accepted: int
    rejected: int
    f_evals: int
    path: List[Tuple[float, Any]] = field(default_factory=list)


def _as_list(y: Any) -> List[float]:
    return list(y) if isinstance(y, (list, tuple)) else [y]


def rkf45_step(f: Callable, t: float, y: List[float], h: float) -> Tuple[List[float], List[float]]:
    """One step: the fourth-order value and the error estimate y5 - y4 (6 evaluations of f)."""
    d = len(y)
    ks: List[List[float]] = []
    for i in range(6):  # @line L4
        Y = list(y)
        for j, a in enumerate(_Af[i]):
            if a != 0.0:
                kj = ks[j]
                for m in range(d):
                    Y[m] += h * a * kj[m]
        ks.append(_as_list(f(t + _Cf[i] * h, Y if d > 1 else Y[0])))
    y4 = [y[m] + h * sum(_B4f[i] * ks[i][m] for i in range(6)) for m in range(d)]  # @line L5
    est = [h * sum(_Ef[i] * ks[i][m] for i in range(6)) for m in range(d)]
    return y4, est


def rkf45(f: Callable, t0: float, y0: Any, t_end: float, rtol: float = 1e-6, atol: float = 1e-9,
          h0: float = 0.0, max_steps: int = 100000, keep_path: bool = False) -> RKFResult:
    """Integrate y' = f(t, y) from t0 to t_end with error control.

    A step is accepted when err = RMS_i |est_i| / (atol + rtol max(|y_i|, |y4_i|)) <= 1.
    The new step is h * min(5, max(0.2, 0.9 err^(-1/5))). y0 is a number or a list.
    """
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    if not (rtol >= 0 and atol >= 0 and rtol + atol > 0):
        raise ValueError("the tolerances must be non-negative and not both zero")
    scalar = not isinstance(y0, (list, tuple))
    t, y = t0, _as_list(y0)  # @line L1
    d = len(y)
    span = t_end - t0
    h = h0 if h0 > 0 else min(span, 0.01 * max(1.0, span)) if span > 0 else 0.0
    path = [(t, y[0] if scalar else list(y))] if keep_path else []
    acc = rej = 0
    while t < t_end:  # @line L2
        if acc + rej >= max_steps:
            raise RuntimeError("too many steps")
        last = h >= t_end - t
        if last:
            h = t_end - t  # @line L3
        elif h <= 1e-14 * max(1.0, abs(t)):
            raise RuntimeError("step size underflow")
        y4, est = rkf45_step(f, t, y, h)
        err = math.sqrt(sum((est[m] / (atol + rtol * max(abs(y[m]), abs(y4[m])))) ** 2
                            for m in range(d)) / d)  # @line L6
        if err <= 1.0:  # @line L7
            t = t_end if last else t + h
            y = y4
            acc += 1
            if keep_path:
                path.append((t, y[0] if scalar else list(y)))
        else:
            rej += 1
        fac = 5.0 if err == 0.0 else min(5.0, max(0.2, 0.9 * err ** -0.2))  # @line L8
        h = h * fac
    return RKFResult(t, y[0] if scalar else y, acc, rej, 6 * (acc + rej), path)  # @line L9


# Exact order conditions (rooted trees up to order 5) for testing the tableau.
def tree_conditions(b: List[F]) -> List[Tuple[str, F, F]]:
    s = len(b)
    Am = [row + [F(0)] * (s - len(row)) for row in A]
    c = [sum(r) for r in Am]
    mv = lambda v: [sum(Am[i][j] * v[j] for j in range(s)) for i in range(s)]
    dot = lambda u, v: sum(x * w for x, w in zip(u, v))
    pw = lambda k: [x ** k for x in c]
    Ac = mv(c)
    one = [F(1)] * s
    mul = lambda u, v: [x * w for x, w in zip(u, v)]
    return [
        ("1", dot(b, one), F(1)),
        ("c", dot(b, c), F(1, 2)),
        ("c^2", dot(b, pw(2)), F(1, 3)), ("Ac", dot(b, Ac), F(1, 6)),
        ("c^3", dot(b, pw(3)), F(1, 4)), ("c.Ac", dot(b, mul(c, Ac)), F(1, 8)),
        ("Ac^2", dot(b, mv(pw(2))), F(1, 12)), ("AAc", dot(b, mv(Ac)), F(1, 24)),
        ("c^4", dot(b, pw(4)), F(1, 5)), ("c^2.Ac", dot(b, mul(pw(2), Ac)), F(1, 10)),
        ("c.Ac^2", dot(b, mul(c, mv(pw(2)))), F(1, 15)), ("c.AAc", dot(b, mul(c, mv(Ac))), F(1, 30)),
        ("(Ac)^2", dot(b, mul(Ac, Ac)), F(1, 20)), ("Ac^3", dot(b, mv(pw(3))), F(1, 20)),
        ("A(c.Ac)", dot(b, mv(mul(c, Ac))), F(1, 40)), ("AAc^2", dot(b, mv(mv(pw(2)))), F(1, 60)),
        ("AAAc", dot(b, mv(mv(Ac))), F(1, 120)),
    ]
