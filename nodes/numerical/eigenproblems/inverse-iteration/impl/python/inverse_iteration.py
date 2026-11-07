# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-iteration/. The authors are listed in prov/GR2E1P.jsonl.

"""Inverse iteration for the eigenvalue of A nearest a shift sigma.

The matrix is a dense list of rows of floats or complex numbers. The shifted
matrix is factored once by Gaussian elimination with partial pivoting; each
step then costs two triangular solves. Standard library only.
"""

import math

U = 2.0 ** -53  # unit roundoff of IEEE double


def norm2(x):
    return math.sqrt(sum(abs(t) ** 2 for t in x))


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def norm_frobenius(a):
    return math.sqrt(sum(abs(t) ** 2 for row in a for t in row))


def lu_factor(m, tiny):
    """LU with partial pivoting of a copy of m. A zero pivot is replaced by tiny."""
    n = len(m)
    a = [list(row) for row in m]
    perm = list(range(n))
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if p != k:
            a[k], a[p] = a[p], a[k]
            perm[k], perm[p] = perm[p], perm[k]
        if abs(a[k][k]) <= tiny:
            a[k][k] = tiny  # sigma is (numerically) an eigenvalue: perturb it
        piv = a[k][k]
        for i in range(k + 1, n):
            f = a[i][k] / piv
            if f != 0:
                a[i][k] = f
                ri, rk = a[i], a[k]
                for j in range(k + 1, n):
                    ri[j] -= f * rk[j]
            else:
                a[i][k] = 0.0
    return a, perm


def lu_solve(lu, perm, b):
    n = len(lu)
    y = [b[perm[i]] for i in range(n)]
    for i in range(n):
        s = y[i]
        row = lu[i]
        for j in range(i):
            s -= row[j] * y[j]
        y[i] = s
    for i in range(n - 1, -1, -1):
        s = y[i]
        row = lu[i]
        for j in range(i + 1, n):
            s -= row[j] * y[j]
        y[i] = s / row[i]
    return y


def inverse_iteration(a, sigma, x0=None, tol=None, kmax=100):
    """Return (theta, x, steps, converged).

    theta is the Rayleigh quotient of the unit vector x, and converged means
    that the residual satisfies ||A x - theta x||_2 <= tol * ||A||_F. The
    default tolerance is 10 n u.
    """
    n = len(a)
    anorm = norm_frobenius(a)
    scale = anorm if anorm > 0 else 1.0
    if tol is None:
        tol = 10 * n * U
    shifted = [[a[i][j] - (sigma if i == j else 0) for j in range(n)] for i in range(n)]
    lu, perm = lu_factor(shifted, U * scale)  # @line L1
    if x0 is None:
        x0 = [1.0 / math.sqrt(k + 1.0) for k in range(n)]  # a fixed start with no zero entry
    nx = norm2(x0)
    x = [t / nx for t in x0]  # @line L2
    theta = sigma
    for k in range(1, kmax + 1):  # @line L3
        y = lu_solve(lu, perm, x)  # @line L4
        ny = norm2(y)
        x = [t / ny for t in y]  # @line L5
        ax = matvec(a, x)
        theta = sum(xi.conjugate() * t for xi, t in zip(x, ax))  # @line L6: x is a unit vector
        r = [t - theta * xi for t, xi in zip(ax, x)]  # @line L7
        if norm2(r) <= tol * scale:  # @line L8
            return theta, x, k, True
    return theta, x, kmax, False  # @line L9
