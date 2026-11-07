# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rayleigh-quotient-iteration/. The authors are listed in prov/DCQZQB.jsonl.

"""Rayleigh quotient iteration for one eigenpair of a square matrix.

rqi(a, x0, tol, maxit) runs inverse iteration with the shift rho = x* A x,
updated at every step. It stops when ||A x - rho x||_2 <= tol ||A||_F, so the
returned pair is an exact eigenpair of A + E with ||E||_2 <= tol ||A||_F.
Each step solves (A - rho I) y = x by Gaussian elimination with partial
pivoting; an exactly zero pivot is replaced by u ||A||_F, which gives the
same direction that the singular system would. Real or complex entries.
Standard library only.
"""

import math
from typing import NamedTuple

U = 2.0**-53


class RQIResult(NamedTuple):
    value: complex | float
    vector: list
    iterations: int  # the number of linear solves
    converged: bool
    residual: float
    history: list  # (rho, ||r||) before each solve and at the end


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def dot(x, y):
    return sum(xi.conjugate() * yi for xi, yi in zip(x, y))


def norm2(x):
    return math.sqrt(sum(abs(t) ** 2 for t in x))


def shifted_solve(a, sigma, b, tiny):
    """Solve (A - sigma I) y = b by elimination with partial pivoting."""
    n = len(a)
    m = [[a[i][j] - (sigma if i == j else 0) for j in range(n)] + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        m[c], m[p] = m[p], m[c]
        if m[c][c] == 0:
            m[c][c] = tiny
        piv = m[c][c]
        for i in range(c + 1, n):
            f = m[i][c] / piv
            if f != 0:
                row_i, row_c = m[i], m[c]
                for j in range(c, n + 1):
                    row_i[j] -= f * row_c[j]
    y = [0] * n
    for i in range(n - 1, -1, -1):
        s = m[i][n] - sum(m[i][j] * y[j] for j in range(i + 1, n))
        y[i] = s / m[i][i]
    return y


def rqi(a, x0, tol=1e-13, maxit=50):
    """Return an RQIResult. x0 must be nonzero; use a complex x0 to reach complex eigenvalues."""
    if not a or maxit < 0:
        raise ValueError("empty matrix or negative maxit")
    scale = math.sqrt(sum(abs(t) ** 2 for row in a for t in row))
    tiny = U * scale if scale > 0 else U
    nx = norm2(x0)
    if nx == 0:
        raise ValueError("the start vector is zero")
    x = [t / nx for t in x0]  # @line L1
    rho = dot(x, matvec(a, x))  # @line L2
    history = []
    for k in range(maxit + 1):  # @line L3
        r = [p - rho * q for p, q in zip(matvec(a, x), x)]  # @line L4
        nr = norm2(r)
        history.append((rho, nr))
        if nr <= tol * scale:  # @line L5
            return RQIResult(rho, x, k, True, nr, history)
        if k == maxit:  # @line L6
            return RQIResult(rho, x, k, False, nr, history)
        y = shifted_solve(a, rho, x, tiny)  # @line L7
        ny = norm2(y)
        x = [t / ny for t in y]  # @line L8
        rho = dot(x, matvec(a, x))  # @line L9
