# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-newton-algorithm/. The authors are listed in prov/77QE67.jsonl.

"""The Gauss-Newton algorithm for nonlinear least squares.

The problem is to minimize F(x) = 1/2 ||r(x)||^2 for a residual function
r: R^n -> R^m with m >= n. The caller gives r and its Jacobian J (an m x n
matrix as a list of rows). Each step solves the normal equations
(J^T J) h = -J^T r by a Cholesky factorization and sets x <- x + h, with no
line search and no damping (the classical, full-step method).
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
    """Solve a x = b for a symmetric positive definite a by a = L L^T.

    Raises ValueError when a pivot is not positive, that is when J does not
    have full column rank (to working precision)."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        d = a[j][j] - sum(low[j][k] ** 2 for k in range(j))
        if d <= 0.0:
            raise ValueError("J^T J is not positive definite: J is rank deficient")
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


def gauss_newton(residual: Callable[[Vector], Vector],
                 jacobian: Callable[[Vector], Matrix],
                 x0: Sequence[float], max_iter: int = 50,
                 eps: float = 1e-12) -> Tuple[Vector, List[Vector]]:
    """Run the Gauss-Newton iteration from x0.

    Returns (x, path), where path holds x0 and every iterate. Stops when
    ||J^T r||_inf <= eps, when the step is small relative to x, or after
    max_iter steps. The iteration can diverge; the caller checks the cost."""
    x = [float(v) for v in x0]  # @line L1
    path = [list(x)]
    for _ in range(max_iter):  # @line L2
        r, jac = residual(x), jacobian(x)  # @line L3
        a, g = normal_equations(jac, r)  # @line L4
        if max(abs(v) for v in g) <= eps:  # @line L5
            break
        h = cholesky_solve(a, [-v for v in g])  # @line L6
        x = [xi + hi for xi, hi in zip(x, h)]  # @line L7
        path.append(list(x))
        if math.sqrt(sum(v * v for v in h)) <= eps * (math.sqrt(sum(v * v for v in x)) + eps):  # @line L8
            break
    return x, path  # @line L9
