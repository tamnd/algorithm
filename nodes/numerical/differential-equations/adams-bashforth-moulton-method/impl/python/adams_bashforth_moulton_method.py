# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-bashforth-moulton-method/. The authors are listed in prov/VJTC0J.jsonl.

"""Adams-Bashforth-Moulton predictor-corrector of order k in PECE mode (or PE(CE)^m).

Predict with the k-step Adams-Bashforth method (order k), evaluate f, correct with the
(k-1)-step Adams-Moulton method (order k), evaluate again. Each step after the start costs
two evaluations of f and no equation solving. Milne's device turns the difference between
corrector and predictor into an estimate of the local error of the corrector. The first
k - 1 steps use the classical Runge-Kutta method. y0 may be a float or a list of floats.
"""

import math
from collections import deque
from fractions import Fraction
from typing import Callable, List, Sequence, Tuple, Union

State = Union[float, Sequence[float]]


def adams_weights(nodes: Sequence[int]) -> List[Fraction]:
    """Integrals over [0, 1] of the Lagrange basis polynomials on the given integer nodes."""
    nodes = [Fraction(v) for v in nodes]
    weights = []
    for j, sj in enumerate(nodes):
        p = [Fraction(1)]
        for m, sm in enumerate(nodes):
            if m != j:
                q = [Fraction(0)] * (len(p) + 1)
                for i, a in enumerate(p):
                    q[i + 1] += a / (sj - sm)
                    q[i] -= a * sm / (sj - sm)
                p = q
        weights.append(sum(a / (i + 1) for i, a in enumerate(p)))
    return weights


def _poly_integral_01(roots: Sequence[int], denom: int) -> Fraction:
    """Integral over [0, 1] of prod (s - r) / denom."""
    p = [Fraction(1)]
    for r in roots:
        q = [Fraction(0)] * (len(p) + 1)
        for i, a in enumerate(p):
            q[i + 1] += a
            q[i] -= a * r
        p = q
    return sum(a / (i + 1) for i, a in enumerate(p)) / denom


def abm_coefficients(k: int) -> Tuple[List[Fraction], List[Fraction], Fraction]:
    """(AB weights beta_0..beta_{k-1}, AM weights b_{-1}..b_{k-2}, Milne factor).

    Milne factor = g* / (g - g*), where g and g* are the error constants of the predictor and
    the corrector, both of order k.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    ab = adams_weights([-j for j in range(k)])
    am = adams_weights([1 - j for j in range(k)])
    g = _poly_integral_01([-j for j in range(k)], math.factorial(k))
    gs = _poly_integral_01([1 - j for j in range(k)], math.factorial(k))
    return ab, am, gs / (g - gs)


def _rk4_step(f: Callable, t: float, y: List[float], h: float) -> List[float]:
    k1 = f(t, y)
    k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
    k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
    k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]


def abm(f: Callable, t0: float, y0: State, t_end: float, h: float, k: int = 4,
        corrections: int = 1) -> Tuple[List[float], list, List[float]]:
    """Integrate from t0 to t_end with the order-k ABM pair in PE(CE)^m mode, m = corrections.

    The step is reduced to (t_end - t0) / N with N = ceil((t_end - t0) / h). Returns
    (ts, ys, est), where est[n] is Milne's estimate of the norm (max norm) of the local error
    of step n (0.0 for the starting steps).
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if not 1 <= k <= 10 or corrections < 1:
        raise ValueError("need 1 <= k <= 10 and corrections >= 1")
    scalar = isinstance(y0, (int, float))
    fv = (lambda t, y: [f(t, y[0])]) if scalar else (lambda t, y: [float(v) for v in f(t, y)])
    y = [float(y0)] if scalar else [float(v) for v in y0]
    d = len(y)
    span = t_end - t0
    N = math.ceil(span / h - 1e-9) if span > 0 else 0  # @line L1
    ts, ys, est = [t0], [y[0] if scalar else list(y)], [0.0]
    if N == 0:
        return ts, ys, est
    h = span / N
    ab, am, milne = abm_coefficients(k)  # @line L2
    ab, am, milne = [float(v) for v in ab], [float(v) for v in am], float(milne)
    hist = deque([fv(t0, y)], maxlen=k)  # @line L3: hist[0] is f_n
    n = 0
    while n < min(k - 1, N):  # @line L4: starting values
        y = _rk4_step(fv, t0 + n * h, y, h)  # @line L5
        n += 1
        hist.appendleft(fv(t0 + n * h, y))
        ts.append(t0 + n * h if n < N else t_end)
        ys.append(y[0] if scalar else list(y))
        est.append(0.0)
    while n < N:  # @line L6
        t1 = t0 + (n + 1) * h if n + 1 < N else t_end
        yp = [y[i] + h * sum(ab[j] * hist[j][i] for j in range(k)) for i in range(d)]  # @line L7
        fp = fv(t1, yp)  # @line L8
        known = [y[i] + h * sum(am[j + 1] * hist[j][i] for j in range(k - 1)) for i in range(d)]
        for _ in range(corrections):
            yc = [known[i] + h * am[0] * fp[i] for i in range(d)]  # @line L9
            fp = fv(t1, yc)  # @line L10
        est.append(abs(milne) * max(abs(yc[i] - yp[i]) for i in range(d)))  # @line L11
        y = yc
        n += 1
        hist.appendleft(fp)
        ts.append(t1)
        ys.append(y[0] if scalar else list(y))
    return ts, ys, est  # @line L12
