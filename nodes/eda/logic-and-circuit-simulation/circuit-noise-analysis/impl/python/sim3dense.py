# SPDX-License-Identifier: MIT
# Shared helper of the sim3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small dense linear algebra for Fraction, float or complex entries.

The circuit pages of group sim3 use this module as a reference solver and for
the small dense systems inside their tests. It holds no sparse method and no
circuit method. Matrices are lists of rows.
"""

from fractions import Fraction


class SingularMatrixError(ValueError):
    """The matrix has no inverse (a zero pivot in exact arithmetic)."""


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def solve(a, b, tol=0.0):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    With Fraction entries the result is exact. b is a vector or a matrix
    (a list of rows); the result has the same shape.
    """
    n = len(a)
    m = [[_exact(x) for x in row] for row in a]
    vec = not (b and isinstance(b[0], list))
    rhs = [[_exact(x)] for x in b] if vec else [[_exact(x) for x in row] for row in b]
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[p][k]) <= tol:
            raise SingularMatrixError(f"zero pivot in column {k}")
        m[k], m[p] = m[p], m[k]
        rhs[k], rhs[p] = rhs[p], rhs[k]
        for i in range(k + 1, n):
            if m[i][k] != 0:
                f = m[i][k] / m[k][k]
                for j in range(k, n):
                    m[i][j] -= f * m[k][j]
                for j in range(len(rhs[i])):
                    rhs[i][j] -= f * rhs[k][j]
    x = [[0] * len(rhs[0]) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(len(rhs[0])):
            s = rhs[i][j] - sum(m[i][k] * x[k][j] for k in range(i + 1, n))
            x[i][j] = s / m[i][i]
    return [r[0] for r in x] if vec else x


def transpose(a):
    return [list(r) for r in zip(*a)]


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def identity(n, one=1):
    return [[one if i == j else 0 * one for j in range(n)] for i in range(n)]


def inverse(a):
    return solve(a, identity(len(a)))
