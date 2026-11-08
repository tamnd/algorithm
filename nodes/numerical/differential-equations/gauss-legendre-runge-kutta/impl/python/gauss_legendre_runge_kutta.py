# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-legendre-runge-kutta/. The authors are listed in prov/XS4SMM.jsonl.

"""Gauss-Legendre Runge-Kutta methods: s-stage implicit collocation at Gauss points, order 2s.

Stage equations Z_i = h sum_j a_ij f(t + c_j h, y + Z_j) are solved by simplified Newton
iteration with the Jacobian frozen at the start of each step.
"""

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence

GRID_SLACK = 1e-9


def _legendre(s: int, x: float):
    """P_s(x) and P_s'(x) by the three-term recurrence."""
    p0, p1 = 1.0, x
    if s == 0:
        return 1.0, 0.0
    for k in range(2, s + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    dp = s * (x * p1 - p0) / (x * x - 1.0)
    return p1, dp


def _poly_mul(p, q):
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _poly_integral(p, x):
    return sum(a * x ** (k + 1) / (k + 1) for k, a in enumerate(p))


def gauss_legendre_tableau(s: int):
    """Butcher tableau (A, b, c) of the s-stage Gauss-Legendre method, c in increasing order."""
    if s < 1:
        raise ValueError("s must be at least 1")
    roots = []
    for k in range(1, s + 1):
        x = math.cos(math.pi * (k - 0.25) / (s + 0.5))
        for _ in range(100):
            p, dp = _legendre(s, x)
            dx = p / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        roots.append(x)
    c = sorted((1.0 + x) / 2.0 for x in roots)
    A = [[0.0] * s for _ in range(s)]
    b = [0.0] * s
    for j in range(s):
        ell = [1.0]  # coefficients of the Lagrange basis polynomial for node c_j
        for m in range(s):
            if m != j:
                ell = _poly_mul(ell, [-c[m] / (c[j] - c[m]), 1.0 / (c[j] - c[m])])
        b[j] = _poly_integral(ell, 1.0)
        for i in range(s):
            A[i][j] = _poly_integral(ell, c[i])
    return A, b, c


def _solve(M, r):
    """Gaussian elimination with partial pivoting (M is copied)."""
    n = len(r)
    M = [row[:] + [r[i]] for i, row in enumerate(M)]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(M[i][k]))
        if M[p][k] == 0:
            raise ZeroDivisionError("singular Newton matrix")
        M[k], M[p] = M[p], M[k]
        for i in range(k + 1, n):
            m = M[i][k] / M[k][k]
            if m:
                for j in range(k, n + 1):
                    M[i][j] -= m * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def _fd_jacobian(f, t, y, fy):
    d = len(y)
    J = [[0.0] * d for _ in range(d)]
    for k in range(d):
        e = 1e-7 * max(1.0, abs(y[k]))
        yp = list(y)
        yp[k] += e
        col = f(t, yp)
        for i in range(d):
            J[i][k] = (col[i] - fy[i]) / e
    return J


@dataclass
class GLResult:
    t: float
    y: object          # float for scalar input, list otherwise
    steps: int
    f_evals: int
    jac_evals: int
    newton_iters: int  # total simplified Newton iterations
    lin_solves: int


def gauss_legendre_rk(f: Callable, t0: float, y0, t_end: float, h: float, s: int = 2,
                      jac: Optional[Callable] = None, tol: float = 1e-13,
                      max_newton: int = 50) -> GLResult:
    """Integrate y' = f(t, y) from t0 to t_end with the s-stage Gauss method, step h.

    y0 may be a float (then f maps floats to floats) or a sequence of floats.
    jac(t, y) returns the d x d Jacobian; if None, forward differences are used.
    """
    if not h > 0:
        raise ValueError("h must be positive")
    if t_end < t0:
        raise ValueError("t_end must be >= t0")
    scalar = not isinstance(y0, (list, tuple))
    F = (lambda t, y: [f(t, y[0])]) if scalar else (lambda t, y: list(f(t, y)))
    Jf = None
    if jac is not None:
        Jf = (lambda t, y: [[jac(t, y[0])]]) if scalar else jac
    A, b, c = gauss_legendre_tableau(s)  # @line L1
    y = [float(y0)] if scalar else [float(v) for v in y0]
    d = len(y)
    span = t_end - t0
    N = 0 if span == 0 else max(1, math.ceil(span / h - GRID_SLACK))  # @line L2
    t = t0
    fe = je = it_total = ls = 0
    for n in range(N):  # @line L3
        t_next = t_end if n == N - 1 else t0 + (n + 1) * h
        k = t_next - t
        if Jf is not None:  # @line L4
            J = Jf(t, y)
        else:
            fy = F(t, y)
            fe += 1 + d
            J = _fd_jacobian(F, t, y, fy)
        je += 1
        sd = s * d
        M = [[(1.0 if r == q else 0.0) - k * A[r // d][q // d] * J[r % d][q % d]
              for q in range(sd)] for r in range(sd)]
        Z = [0.0] * sd  # @line L5
        for it in range(max_newton):  # @line L6
            fs = [F(t + c[j] * k, [y[i] + Z[j * d + i] for i in range(d)]) for j in range(s)]
            fe += s
            G = [-Z[r] + k * sum(A[r // d][j] * fs[j][r % d] for j in range(s)) for r in range(sd)]
            dZ = _solve(M, G)
            ls += 1
            Z = [Z[r] + dZ[r] for r in range(sd)]
            it_total += 1
            scale = max(1.0, max(abs(v) for v in y))
            if max(abs(v) for v in dZ) <= tol * scale:
                break
        else:
            raise ArithmeticError("simplified Newton iteration did not converge; reduce h")
        fs = [F(t + c[j] * k, [y[i] + Z[j * d + i] for i in range(d)]) for j in range(s)]
        fe += s
        y = [y[i] + k * sum(b[j] * fs[j][i] for j in range(s)) for i in range(d)]  # @line L7
        t = t_next
    return GLResult(t, y[0] if scalar else y, N, fe, je, it_total, ls)  # @line L8
