# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/henderson-mixed-model-equations/. The authors are listed in prov/3AX196.jsonl.
"""Henderson's mixed model equations for the linear mixed model y = X b + Z u + e.

u ~ N(0, G) and e ~ N(0, R) are independent, with G (q x q) and R (n x n)
known and positive definite. The equations

    [ X^T R^-1 X    X^T R^-1 Z          ] [b]   [ X^T R^-1 y ]
    [ Z^T R^-1 X    Z^T R^-1 Z + G^-1   ] [u] = [ Z^T R^-1 y ]

have order p + q, not n. Their solution b is the generalized least squares
estimate with V = Z G Z^T + R, and u is the best linear unbiased predictor
(BLUP) of the random effects. The inverse of the coefficient matrix gives
Cov(b-hat) in its top-left block and the prediction error covariance
Cov(u-hat - u) in its bottom-right block.

The solver is a symmetric LDL^T factorization without square roots, so the
arithmetic is generic: Fraction input gives exact results.
"""

from typing import NamedTuple


def transpose(a):
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def ldl(a):
    """Unit lower triangular L and diagonal d with A = L diag(d) L^T. Raises ValueError unless A is positive definite."""
    n = len(a)
    l = [[0] * n for _ in range(n)]
    d = [0] * n
    for j in range(n):
        dj = a[j][j] - sum(l[j][k] * l[j][k] * d[k] for k in range(j))
        if not dj > 0:
            raise ValueError("matrix is not positive definite")
        d[j] = dj
        l[j][j] = 1
        for i in range(j + 1, n):
            l[i][j] = (a[i][j] - sum(l[i][k] * l[j][k] * d[k] for k in range(j))) / dj
    return l, d


def ldl_solve(l, d, b):
    """Solve L diag(d) L^T x = b by forward substitution, a diagonal scaling and back substitution."""
    n = len(d)
    z = [0] * n
    for i in range(n):
        z[i] = b[i] - sum(l[i][k] * z[k] for k in range(i))
    w = [z[i] / d[i] for i in range(n)]
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = w[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))
    return x


def inverse_spd(a):
    """The inverse of a symmetric positive definite matrix, by LDL^T."""
    l, d = ldl(a)
    n = len(a)
    cols = [ldl_solve(l, d, [1 if i == j else 0 for i in range(n)]) for j in range(n)]
    return transpose(cols)


def _is_diagonal(a):
    return all(a[i][j] == 0 for i in range(len(a)) for j in range(len(a)) if i != j)


class MMEFit(NamedTuple):
    b: list     # fixed effects, length p (the GLS estimate)
    u: list     # predicted random effects, length q (the BLUP)
    c: list     # the (p + q) x (p + q) coefficient matrix
    rhs: list   # the right-hand side


def mixed_model_equations(x, z, g, r, y):
    """Build and solve Henderson's mixed model equations."""
    n, p, q = len(y), len(x[0]), len(z[0])
    if len(x) != n or len(z) != n or len(r) != n or len(g) != q:
        raise ValueError("dimensions do not match")
    w = [xr + zr for xr, zr in zip(x, z)]  # @line L1
    if _is_diagonal(r):
        for i in range(n):
            if not r[i][i] > 0:
                raise ValueError("R is not positive definite")
        rinv_w = [[row[j] / r[i][i] for j in range(len(row))] for i, row in enumerate(w)]  # @line L2
        rinv_y = [y[i] / r[i][i] for i in range(n)]  # @line L2
    else:
        l, d = ldl(r)
        cols = [ldl_solve(l, d, [w[i][j] for i in range(n)]) for j in range(p + q)]  # @line L2
        rinv_w = transpose(cols)
        rinv_y = ldl_solve(l, d, list(y))  # @line L2
    wt = transpose(w)
    c = matmul(wt, rinv_w)  # @line L3
    if _is_diagonal(g):
        if not all(g[i][i] > 0 for i in range(q)):
            raise ValueError("G is not positive definite")
        ginv = [[1 / g[i][i] if i == j else 0 for j in range(q)] for i in range(q)]
    else:
        ginv = inverse_spd(g)
    for i in range(q):
        for j in range(q):
            c[p + i][p + j] += ginv[i][j]  # @line L4
    rhs = [sum(wt[i][k] * rinv_y[k] for k in range(n)) for i in range(p + q)]  # @line L5
    l, d = ldl(c)  # @line L6
    sol = ldl_solve(l, d, rhs)  # @line L7
    return MMEFit(sol[:p], sol[p:], c, rhs)  # @line L8


def mme_inverse_blocks(fit, p):
    """(Cov(b-hat), Cov(u-hat - u)) from the inverse of the coefficient matrix: its top-left and bottom-right blocks."""
    ci = inverse_spd(fit.c)  # @line L9
    return [row[:p] for row in ci[:p]], [row[p:] for row in ci[p:]]  # @line L9


def one_way_design(groups):
    """X (a column of ones) and Z (group indicators) for a one-way random effects layout given as lists of responses."""
    x, z, y = [], [], []
    for gi, values in enumerate(groups):
        for v in values:
            x.append([1])
            z.append([1 if k == gi else 0 for k in range(len(groups))])
            y.append(v)
    return x, z, y
