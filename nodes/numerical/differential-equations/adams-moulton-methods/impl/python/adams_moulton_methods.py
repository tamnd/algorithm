# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-moulton-methods/. The authors are listed in prov/S41K1C.jsonl.

"""The k-step Adams-Moulton method for y' = f(t, y), y(t0) = y0.

    y_{n+1} = y_n + h * (b_{-1} f(t_{n+1}, y_{n+1}) + sum_{j=0}^{k-1} b_j f(t_{n-j}, y_{n-j}))

The weights are the integrals over [0, 1] of the Lagrange basis polynomials on the nodes
1, 0, -1, ..., -(k-1), computed exactly with Fraction. k = 0 is backward Euler and k = 1 is
the trapezoidal rule; the k-step method has order k + 1. The implicit equation is solved by
Newton's method with the Jacobian supplied by the caller or approximated by differences.
The first k - 1 steps use the classical Runge-Kutta method.
"""

import math
from collections import deque
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple, Union

Vector = List[float]
State = Union[float, Sequence[float]]


def adams_weights(nodes: Sequence[int]) -> List[Fraction]:
    """Integrals over [0, 1] of the Lagrange basis polynomials on the given integer nodes."""
    nodes = [Fraction(v) for v in nodes]
    weights = []
    for j, sj in enumerate(nodes):
        p = [Fraction(1)]  # coefficients, lowest degree first
        for m, sm in enumerate(nodes):
            if m != j:
                q = [Fraction(0)] * (len(p) + 1)
                for i, a in enumerate(p):
                    q[i + 1] += a / (sj - sm)
                    q[i] -= a * sm / (sj - sm)
                p = q
        weights.append(sum(a / (i + 1) for i, a in enumerate(p)))
    return weights


def am_coefficients(k: int) -> List[Fraction]:
    """[b_{-1}, b_0, ..., b_{k-1}]: the weights of f_{n+1}, f_n, ..., f_{n-k+1}."""
    if k < 0:
        raise ValueError("k must be at least 0")
    return adams_weights([1 - j for j in range(k + 1)])


def solve_linear(a: List[List[float]], b: Vector) -> Vector:
    """Solve a x = b by Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        if m[p][c] == 0.0:
            raise ZeroDivisionError("singular Newton matrix")
        m[c], m[p] = m[p], m[c]
        for i in range(c + 1, n):
            r = m[i][c] / m[c][c]
            if r != 0.0:
                for j in range(c, n + 1):
                    m[i][j] -= r * m[c][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def _fd_jacobian(f: Callable, t: float, y: Vector, fy: Vector) -> List[List[float]]:
    d = len(y)
    jac = [[0.0] * d for _ in range(d)]
    for j in range(d):
        dy = 1e-7 * max(1.0, abs(y[j]))
        yp = list(y)
        yp[j] += dy
        fp = f(t, yp)
        for i in range(d):
            jac[i][j] = (fp[i] - fy[i]) / dy
    return jac


def _rk4_step(f: Callable, t: float, y: Vector, h: float) -> Vector:
    k1 = f(t, y)
    k2 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
    k3 = f(t + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
    k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
    return [y[i] + h / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(len(y))]


def newton_solve(f: Callable, t1: float, g: Vector, hb: float, x: Vector, jac: Optional[Callable],
                 tol: float = 1e-12, max_newton: int = 50) -> Tuple[Vector, int]:
    """Solve x = g + hb * f(t1, x) by Newton's method from the guess x. Returns (x, iterations)."""
    d = len(x)
    for it in range(1, max_newton + 1):
        fx = f(t1, x)
        r = [g[i] + hb * fx[i] - x[i] for i in range(d)]
        jm = jac(t1, x) if jac is not None else _fd_jacobian(f, t1, x, fx)
        a = [[(1.0 if i == j else 0.0) - hb * jm[i][j] for j in range(d)] for i in range(d)]
        delta = solve_linear(a, r)
        x = [x[i] + delta[i] for i in range(d)]
        if max((abs(v) for v in delta), default=0.0) <= tol * max(1.0, max(abs(v) for v in x)):
            return x, it
    raise ArithmeticError("Newton iteration did not converge; try a smaller h")


def adams_moulton(f: Callable, t0: float, y0: State, t_end: float, h: float, k: int = 3,
                  jac: Optional[Callable] = None, tol: float = 1e-12) -> Tuple[List[float], list]:
    """Integrate from t0 to t_end with the k-step Adams-Moulton method (order k + 1).

    The step is reduced to (t_end - t0) / N with N = ceil((t_end - t0) / h). Returns (ts, ys).
    For a scalar y0 the ys are floats, and f and jac take and return floats.
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if not 0 <= k <= 10:
        raise ValueError("k must be between 0 and 10")
    scalar = isinstance(y0, (int, float))
    if scalar:
        fv = lambda t, y: [f(t, y[0])]
        jv = (lambda t, y: [[jac(t, y[0])]]) if jac is not None else None
        y = [float(y0)]
    else:
        fv = lambda t, y: [float(v) for v in f(t, y)]
        jv, y = jac, [float(v) for v in y0]
    span = t_end - t0
    N = math.ceil(span / h - 1e-9) if span > 0 else 0  # @line L1
    ts, ys = [t0], [y[0] if scalar else list(y)]
    if N == 0:
        return ts, ys
    h = span / N
    w = [float(b) for b in am_coefficients(k)]  # @line L2
    hist = deque([fv(t0, y)], maxlen=max(k, 1))  # @line L3: hist[0] is f_n
    n = 0
    while n < min(k - 1, N):  # @line L4: starting values
        y = _rk4_step(fv, t0 + n * h, y, h)  # @line L5
        n += 1
        hist.appendleft(fv(t0 + n * h, y))
        ts.append(t0 + n * h if n < N else t_end)
        ys.append(y[0] if scalar else list(y))
    while n < N:  # @line L6
        t1 = t0 + (n + 1) * h if n + 1 < N else t_end
        d = len(y)
        g = [y[i] + h * sum(w[j + 1] * hist[j][i] for j in range(k)) for i in range(d)]  # @line L7
        guess = [y[i] + h * hist[0][i] for i in range(d)]  # @line L8: explicit Euler guess
        y, _ = newton_solve(fv, t1, g, h * w[0], guess, jv, tol)  # @line L9
        n += 1
        hist.appendleft(fv(t1, y))  # @line L10
        ts.append(t1)
        ys.append(y[0] if scalar else list(y))
    return ts, ys  # @line L11
