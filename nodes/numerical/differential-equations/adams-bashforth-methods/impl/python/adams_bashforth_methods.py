# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-bashforth-methods/. The authors are listed in prov/4QMRZ8.jsonl.

"""The k-step Adams-Bashforth method for y' = f(t, y), y(t0) = y0.

    y_{n+1} = y_n + h * sum_{j=0}^{k-1} beta_j * f(t_{n-j}, y_{n-j})

The weights beta_j are the integrals over [0, 1] of the Lagrange basis polynomials on the
nodes 0, -1, ..., -(k-1) (in units of h), computed exactly with Fraction. The first k - 1
steps are taken with the classical Runge-Kutta method. After that, each step costs one
evaluation of f. y0 may be a float or a list of floats.
"""

import math
from collections import deque
from fractions import Fraction
from typing import Callable, List, Sequence, Tuple, Union

State = Union[float, Sequence[float]]


def _poly_mul_linear(p: List[Fraction], root: Fraction, scale: Fraction) -> List[Fraction]:
    """Multiply the polynomial p (coefficients, lowest degree first) by (s - root) / scale."""
    out = [Fraction(0)] * (len(p) + 1)
    for i, a in enumerate(p):
        out[i + 1] += a / scale
        out[i] -= a * root / scale
    return out


def adams_weights(nodes: Sequence[int]) -> List[Fraction]:
    """Integrals over [0, 1] of the Lagrange basis polynomials on the given integer nodes."""
    nodes = [Fraction(v) for v in nodes]
    weights = []
    for j, sj in enumerate(nodes):
        p = [Fraction(1)]
        for m, sm in enumerate(nodes):
            if m != j:
                p = _poly_mul_linear(p, sm, sj - sm)
        weights.append(sum(a / (i + 1) for i, a in enumerate(p)))
    return weights


def ab_coefficients(k: int) -> List[Fraction]:
    """beta_0, ..., beta_{k-1}, the weight of f_{n-j} in the k-step Adams-Bashforth method."""
    if k < 1:
        raise ValueError("k must be at least 1")
    return adams_weights([-j for j in range(k)])


def _rk4_step(f: Callable, t: float, y: List[float], h: float) -> List[float]:
    k1 = f(t, y)
    k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
    k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
    k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]


def adams_bashforth(f: Callable, t0: float, y0: State, t_end: float, h: float, k: int = 4) -> Tuple[List[float], list]:
    """Integrate from t0 to t_end with the k-step Adams-Bashforth method (order k).

    The step is reduced to (t_end - t0) / N with N = ceil((t_end - t0) / h), so the uniform
    grid ends exactly at t_end. Returns (ts, ys); for a scalar y0 the ys are floats.
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if not 1 <= k <= 12:
        raise ValueError("k must be between 1 and 12")
    scalar = isinstance(y0, (int, float))
    fv = (lambda t, y: [f(t, y[0])]) if scalar else (lambda t, y: [float(v) for v in f(t, y)])
    y = [float(y0)] if scalar else [float(v) for v in y0]
    span = t_end - t0
    N = math.ceil(span / h - 1e-9) if span > 0 else 0  # @line L1
    ts, ys = [t0], [y[0] if scalar else list(y)]
    if N == 0:
        return ts, ys
    h = span / N
    beta = [float(b) for b in ab_coefficients(k)]  # @line L2
    hist = deque([fv(t0, y)], maxlen=k)  # @line L3: hist[0] is the newest value f_n
    n = 0
    while n < min(k - 1, N):  # @line L4: starting values
        y = _rk4_step(fv, t0 + n * h, y, h)  # @line L5
        n += 1
        hist.appendleft(fv(t0 + n * h, y))
        ts.append(t0 + n * h if n < N else t_end)
        ys.append(y[0] if scalar else list(y))
    while n < N:  # @line L6
        y = [y[i] + h * sum(beta[j] * hist[j][i] for j in range(k)) for i in range(len(y))]  # @line L7
        n += 1
        t = t0 + n * h if n < N else t_end
        if n < N:
            hist.appendleft(fv(t, y))  # @line L8
        ts.append(t)
        ys.append(y[0] if scalar else list(y))
    return ts, ys  # @line L9
