# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bulirsch-stoer-method/. The authors are listed in prov/FA09JN.jsonl.

"""Gragg-Bulirsch-Stoer extrapolation with a fixed number k of extrapolation stages.

A big step H is done k times by Gragg's modified midpoint rule with n_j = 2 j substeps
(j = 1..k). The results T_{j,1} have an error expansion in even powers of H / n_j, and
Aitken-Neville extrapolation to step size 0 gives T_{k,k} of order 2k. The difference
T_{k,k} - T_{k,k-1} (order 2k - 2) is the error estimate for step size control.
This is polynomial extrapolation with the sequence 2, 4, 6, ... (as in the code ODEX of
Hairer, Norsett and Wanner); Bulirsch and Stoer used rational extrapolation.
"""

import math
from typing import Callable, List, Optional, Sequence, Tuple, Union

State = Union[float, Sequence[float]]


def modified_midpoint(f: Callable, t: float, y: List[float], f0: List[float], big_h: float,
                      n: int) -> List[float]:
    """Gragg's rule: z1 = y + h f0, z_{m+1} = z_{m-1} + 2 h f(t_m, z_m), return z_n (n >= 1)."""
    h = big_h / n
    z_prev = list(y)
    z = [y[i] + h * f0[i] for i in range(len(y))]
    for m in range(1, n):
        fz = f(t + m * h, z)
        z_prev, z = z, [z_prev[i] + 2 * h * fz[i] for i in range(len(y))]
    return z


def extrapolate(rows: List[List[List[float]]], ns: Sequence[int]) -> None:
    """Add the extrapolated entries T_{j,2..j} to the last row (Aitken-Neville in h^2)."""
    j = len(rows) - 1
    row = rows[j]
    for l in range(1, j + 1):
        q = (ns[j] / ns[j - l]) ** 2 - 1
        row.append([row[l - 1][i] + (row[l - 1][i] - rows[j - 1][l - 1][i]) / q for i in range(len(row[0]))])


def bs_step(f: Callable, t: float, y: List[float], big_h: float, k: int,
            f0: Optional[List[float]] = None) -> Tuple[List[float], List[float]]:
    """One extrapolation step. Returns (T_{k,k}, T_{k,k} - T_{k,k-1}); for k = 1 the estimate is 0."""
    ns = [2 * (j + 1) for j in range(k)]
    if f0 is None:
        f0 = f(t, y)
    rows: List[List[List[float]]] = []
    for j in range(k):  # @line L4: k runs of the modified midpoint rule
        rows.append([modified_midpoint(f, t, y, f0, big_h, ns[j])])
        extrapolate(rows, ns)  # @line L5: Aitken-Neville extrapolation in h^2
    best = rows[-1][-1]
    est = [best[i] - rows[-1][-2][i] for i in range(len(y))] if k > 1 else [0.0] * len(y)
    return best, est


def bulirsch_stoer(f: Callable, t0: float, y0: State, t_end: float, rtol: float = 1e-8,
                   atol: float = 1e-10, k: int = 4, h0: Optional[float] = None,
                   max_steps: int = 100_000) -> Tuple[List[float], list, dict]:
    """Integrate adaptively from t0 to t_end >= t0 with order 2k (k >= 2).

    Returns (ts, ys, stats) with stats = {"accepted", "rejected", "evaluations"}.
    Every attempted step costs k * k + 1 evaluations of f.
    """
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if k < 2 or (rtol <= 0 and atol <= 0):
        raise ValueError("need k >= 2 and a positive tolerance")
    scalar = isinstance(y0, (int, float))
    calls = [0]

    def fv(t, y):
        calls[0] += 1
        return [f(t, y[0])] if scalar else [float(v) for v in f(t, y)]

    y = [float(y0)] if scalar else [float(v) for v in y0]
    ts, ys = [t0], [y[0] if scalar else list(y)]
    stats = {"accepted": 0, "rejected": 0, "evaluations": 0}
    if t_end == t0:
        return ts, ys, stats
    t = t0
    big_h = min(h0 if h0 is not None else 0.1 * (t_end - t0), t_end - t0)  # @line L1
    while t < t_end:  # @line L2
        if stats["accepted"] + stats["rejected"] >= max_steps:
            raise ArithmeticError("too many steps; the problem may be stiff")
        last = t + big_h >= t_end - 1e-12 * max(1.0, abs(t_end))
        if last:
            big_h = t_end - t  # @line L3: the final step ends exactly at t_end
        y_new, e = bs_step(fv, t, y, big_h, k)
        err = max(abs(e[i]) / (atol + rtol * max(abs(y[i]), abs(y_new[i]))) for i in range(len(y)))  # @line L6
        if err <= 1.0:  # @line L7
            t = t_end if last else t + big_h
            y = y_new
            ts.append(t)
            ys.append(y[0] if scalar else list(y))
            stats["accepted"] += 1
        else:
            stats["rejected"] += 1
        fac = 4.0 if err == 0.0 else min(4.0, max(0.2, 0.9 * err ** (-1.0 / (2 * k - 1))))
        if err > 1.0:
            fac = min(fac, 1.0)
        big_h *= fac  # @line L8
    stats["evaluations"] = calls[0]
    return ts, ys, stats  # @line L9
