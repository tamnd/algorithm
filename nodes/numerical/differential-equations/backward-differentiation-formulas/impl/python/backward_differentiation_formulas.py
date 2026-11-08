# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-differentiation-formulas/. The authors are listed in prov/NRVHTE.jsonl.

"""The k-step backward differentiation formula (BDF), k = 1, ..., 6, for y' = f(t, y).

The method sets the derivative of the polynomial through y_{n+1}, y_n, ..., y_{n+1-k} at
t_{n+1} equal to f(t_{n+1}, y_{n+1}):

    sum_{j=1}^{k} (1/j) nabla^j y_{n+1} = h f(t_{n+1}, y_{n+1}).

Each step solves this equation for y_{n+1} by Newton's method, with the Jacobian of f given
by the caller or approximated by forward differences. The k - 1 starting values come from
the 3-stage Gauss-Legendre Runge-Kutta method (order 6, A-stable). y0 may be a float or a
list of floats.
"""

import math
from collections import deque
from fractions import Fraction
from typing import Callable, List, Optional, Sequence, Tuple, Union

Vector = List[float]
State = Union[float, Sequence[float]]


def bdf_coefficients(k: int) -> List[Fraction]:
    """[alpha_0, ..., alpha_k]: alpha_i is the coefficient of y_{n+1-i} in sum_j nabla^j y_{n+1} / j."""
    if k < 1:
        raise ValueError("k must be at least 1")
    alpha = [Fraction(0)] * (k + 1)
    for j in range(1, k + 1):
        for i in range(j + 1):
            alpha[i] += Fraction((-1) ** i * math.comb(j, i), j)
    return alpha


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


_R15 = math.sqrt(15.0)
_GC = [0.5 - _R15 / 10, 0.5, 0.5 + _R15 / 10]
_GA = [[5 / 36, 2 / 9 - _R15 / 15, 5 / 36 - _R15 / 30],
       [5 / 36 + _R15 / 24, 2 / 9, 5 / 36 - _R15 / 24],
       [5 / 36 + _R15 / 30, 2 / 9 + _R15 / 15, 5 / 36]]
_GB = [5 / 18, 4 / 9, 5 / 18]


def gauss3_step(f: Callable, t: float, y: Vector, h: float, jac: Optional[Callable],
                tol: float = 1e-13, max_iter: int = 60) -> Vector:
    """One step of the 3-stage Gauss method (order 6); the stage equations are solved by Newton."""
    d, s = len(y), 3
    z = [0.0] * (s * d)  # stage increments Z_i = Y_i - y
    for _ in range(max_iter):
        ys_ = [[y[p] + z[i * d + p] for p in range(d)] for i in range(s)]
        fs = [f(t + _GC[i] * h, ys_[i]) for i in range(s)]
        js = [jac(t + _GC[i] * h, ys_[i]) if jac is not None else _fd_jacobian(f, t + _GC[i] * h, ys_[i], fs[i])
              for i in range(s)]
        big = [[0.0] * (s * d) for _ in range(s * d)]
        for i in range(s):
            for j in range(s):
                for p in range(d):
                    for q in range(d):
                        big[i * d + p][j * d + q] = (1.0 if (i == j and p == q) else 0.0) - h * _GA[i][j] * js[j][p][q]
        r = [h * sum(_GA[i][j] * fs[j][p] for j in range(s)) - z[i * d + p] for i in range(s) for p in range(d)]
        dz = solve_linear(big, r)
        z = [z[i] + dz[i] for i in range(s * d)]
        if max(abs(v) for v in dz) <= tol * max(1.0, max(abs(v) for v in y)):
            fs = [f(t + _GC[i] * h, [y[p] + z[i * d + p] for p in range(d)]) for i in range(s)]
            return [y[p] + h * sum(_GB[i] * fs[i][p] for i in range(s)) for p in range(d)]
    raise ArithmeticError("Gauss stage iteration did not converge; try a smaller h")


def newton_solve(f: Callable, t1: float, g: Vector, hb: float, x: Vector, jac: Optional[Callable],
                 tol: float = 1e-12, max_newton: int = 50) -> Tuple[Vector, int]:
    """Solve x = g + hb * f(t1, x) by Newton's method from x. Returns (x, iterations)."""
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


def bdf(f: Callable, t0: float, y0: State, t_end: float, h: float, k: int = 2,
        jac: Optional[Callable] = None, tol: float = 1e-12) -> Tuple[List[float], list]:
    """Integrate from t0 to t_end with BDF of order k (1 <= k <= 6).

    The step is reduced to (t_end - t0) / N with N = ceil((t_end - t0) / h). Returns (ts, ys);
    for a scalar y0 the ys are floats and f, jac take and return floats.
    """
    if h <= 0.0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be at least t0")
    if not 1 <= k <= 6:
        raise ValueError("BDF is zero-stable only for 1 <= k <= 6")
    scalar = isinstance(y0, (int, float))
    if scalar:
        fv = lambda t, y: [f(t, y[0])]
        jv = (lambda t, y: [[jac(t, y[0])]]) if jac is not None else None
        y = [float(y0)]
    else:
        fv = lambda t, y: [float(v) for v in f(t, y)]
        jv, y = jac, [float(v) for v in y0]
    d = len(y)
    span = t_end - t0
    N = math.ceil(span / h - 1e-9) if span > 0 else 0  # @line L1
    ts, ys = [t0], [y[0] if scalar else list(y)]
    if N == 0:
        return ts, ys
    h = span / N
    alpha = bdf_coefficients(k)  # @line L2
    a = [float(-alpha[i] / alpha[0]) for i in range(k + 1)]  # y_{n+1} = sum_{i>=1} a_i y_{n+1-i} + h b f_{n+1}
    b = float(1 / alpha[0])
    hist = deque([list(y)], maxlen=k)  # @line L3: hist[0] is y_n
    n = 0
    while n < min(k - 1, N):  # @line L4: starting values
        y = gauss3_step(fv, t0 + n * h, y, h, jv)
        n += 1
        hist.appendleft(list(y))
        ts.append(t0 + n * h if n < N else t_end)
        ys.append(y[0] if scalar else list(y))
    while n < N:  # @line L5
        t1 = t0 + (n + 1) * h if n + 1 < N else t_end
        g = [sum(a[i] * hist[i - 1][p] for i in range(1, k + 1)) for p in range(d)]  # @line L6
        guess = list(hist[0])  # @line L7
        y, _ = newton_solve(fv, t1, g, h * b, guess, jv, tol)  # @line L8
        n += 1
        hist.appendleft(list(y))  # @line L9
        ts.append(t1)
        ys.append(y[0] if scalar else list(y))
    return ts, ys  # @line L10
