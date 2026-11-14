# SPDX-License-Identifier: MIT
# Shared helper of the sim2 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Dense LU factorization with partial pivoting, for Fraction or float entries.

The circuit pages build a matrix and then call this module to solve it. With
Fraction entries every step is exact, so a zero pivot means that the matrix is
singular. With float entries a pivot whose absolute value is at most ``tol``
counts as zero.

lu_factor returns factors with P A = L U. lu_solve solves A x = b and
lu_solve_transpose solves A^T z = c with the same factors, so a second right
hand side or a transposed system costs only two triangular solves.
"""

from fractions import Fraction


class SingularMatrixError(ValueError):
    """The matrix has no inverse (a zero pivot in exact arithmetic)."""


def _exact(x):
    # An int entry becomes a Fraction, so that int / int never turns into a float.
    return Fraction(x) if isinstance(x, int) else x


def lu_factor(a, tol=0):
    n = len(a)
    lu = [[_exact(x) for x in row] for row in a]
    for row in lu:
        if len(row) != n:
            raise ValueError("the matrix is not square")
    perm = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(lu[i][k]))
        if abs(lu[p][k]) <= tol:
            raise SingularMatrixError(f"zero pivot in column {k}")
        if p != k:
            lu[k], lu[p] = lu[p], lu[k]
            perm[k], perm[p] = perm[p], perm[k]
        piv = lu[k][k]
        rowk = lu[k]
        for i in range(k + 1, n):
            rowi = lu[i]
            f = rowi[k] / piv
            rowi[k] = f
            if f:
                for j in range(k + 1, n):
                    rowi[j] -= f * rowk[j]
    return lu, perm


def lu_solve(factors, b):
    lu, perm = factors
    n = len(lu)
    y = [b[perm[i]] for i in range(n)]
    for i in range(n):
        s = y[i]
        for j in range(i):
            s -= lu[i][j] * y[j]
        y[i] = s
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= lu[i][j] * y[j]
        y[i] = s / lu[i][i]
    return y


def lu_solve_transpose(factors, c):
    lu, perm = factors
    n = len(lu)
    w = list(c)
    for i in range(n):
        s = w[i]
        for j in range(i):
            s -= lu[j][i] * w[j]
        w[i] = s / lu[i][i]
    for i in range(n - 1, -1, -1):
        s = w[i]
        for j in range(i + 1, n):
            s -= lu[j][i] * w[j]
        w[i] = s
    z = [None] * n
    for i in range(n):
        z[perm[i]] = w[i]
    return z


def solve(a, b, tol=0):
    return lu_solve(lu_factor(a, tol), b)


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]
