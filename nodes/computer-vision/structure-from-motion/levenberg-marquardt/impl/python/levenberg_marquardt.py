# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levenberg-marquardt/. The authors are listed in prov/MSS87Z.jsonl.

"""The Levenberg-Marquardt algorithm for nonlinear least squares.

The problem is to minimize F(x) = 1/2 ||r(x)||^2 for r: R^n -> R^m. Each
step solves the damped normal equations (J^T J + mu D) h = -J^T r, with
D = I (Levenberg) or D = diag(J^T J) (Marquardt). The damping mu is updated
from the gain ratio rho by the rule of Madsen, Nielsen and Tingleff (2004,
Algorithm 3.16): after an accepted step mu <- mu max(1/3, 1 - (2 rho - 1)^3),
after a rejected step mu <- mu nu and nu <- 2 nu.
"""

import math
from typing import Callable, List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def cost(r: Sequence[float]) -> float:
    """F = 1/2 ||r||^2."""
    return 0.5 * sum(v * v for v in r)


def normal_equations(jac: Sequence[Sequence[float]], r: Sequence[float]) -> Tuple[Matrix, Vector]:
    """Return A = J^T J and g = J^T r."""
    m, n = len(jac), len(jac[0])
    a = [[sum(jac[k][i] * jac[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    g = [sum(jac[k][i] * r[k] for k in range(m)) for i in range(n)]
    return a, g


def cholesky_solve(a: Sequence[Sequence[float]], b: Sequence[float]) -> Vector:
    """Solve a x = b for a symmetric positive definite a by a = L L^T."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if d <= 0.0:
            raise ValueError("matrix is not positive definite")
        low[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def damped_step(a: Matrix, g: Vector, mu: float, marquardt: bool = False) -> Vector:
    """Solve (A + mu D) h = -g, with D = I or D = diag(A)."""
    n = len(a)
    b = [row[:] for row in a]
    for i in range(n):
        b[i][i] += mu * (a[i][i] if marquardt else 1.0)
    return cholesky_solve(b, [-v for v in g])


def levenberg_marquardt(residual: Callable[[Vector], Vector],
                        jacobian: Callable[[Vector], Matrix],
                        x0: Sequence[float], tau: float = 1e-3,
                        eps1: float = 1e-12, eps2: float = 1e-14,
                        max_iter: int = 200, marquardt: bool = False):
    """Run Levenberg-Marquardt from x0.

    Returns (x, info). info["costs"] holds F at x0 and after each accepted
    step, info["mus"] the damping used at each step, info["iterations"] the
    number of steps tried (accepted or rejected)."""
    x = [float(v) for v in x0]  # @line L1
    nu = 2.0
    r = residual(x)
    a, g = normal_equations(jacobian(x), r)  # @line L2
    f = cost(r)
    mu = tau * max(a[i][i] for i in range(len(x)))  # @line L3
    info = {"costs": [f], "mus": [], "iterations": 0}
    for k in range(max_iter):  # @line L4
        if max(abs(v) for v in g) <= eps1:  # @line L5
            break
        info["iterations"] = k + 1
        h = damped_step(a, g, mu, marquardt)  # @line L6
        info["mus"].append(mu)
        if math.sqrt(sum(v * v for v in h)) <= eps2 * (math.sqrt(sum(v * v for v in x)) + eps2):  # @line L7
            break
        x_new = [xi + hi for xi, hi in zip(x, h)]
        r_new = residual(x_new)
        f_new = cost(r_new)
        dmu = [mu * (a[i][i] if marquardt else 1.0) * h[i] for i in range(len(h))]
        predicted = 0.5 * sum(hi * (di - gi) for hi, di, gi in zip(h, dmu, g))  # L(0) - L(h)
        rho = (f - f_new) / predicted  # @line L8
        if rho > 0:  # @line L9
            x, r, f = x_new, r_new, f_new  # @line L10
            a, g = normal_equations(jacobian(x), r)
            info["costs"].append(f)
            mu *= max(1.0 / 3.0, 1.0 - (2.0 * rho - 1.0) ** 3)  # @line L11
            nu = 2.0
        else:
            mu *= nu  # @line L12
            nu *= 2.0
    return x, info  # @line L13
