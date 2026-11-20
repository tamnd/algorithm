# SPDX-License-Identifier: MIT
# Shared helper of the scientific-computing pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small dense linear algebra and error norms for the scientific-computing pages.

A matrix is a list of rows and a vector is a list. Entries may be int,
float or fractions.Fraction. The routines that do not take a square root
(solve, inv, det and the arithmetic) keep Fraction entries exact.
cholesky, cholesky_solve and norm2 take square roots and return floats.

API (fixed; other pages copy this file byte for byte):
    zeros(m, n=None)        m by n zero matrix (n = m if not given)
    eye(n)                  n by n identity
    add(A, B), sub(A, B)    entrywise sum and difference (vectors or matrices)
    scale(c, A)             c times A (vector or matrix)
    matmul(A, B)            matrix product
    matvec(A, x)            matrix times vector
    transpose(A)            transpose
    dot(x, y)               inner product of two vectors
    norm2(x)                Euclidean norm of a vector, as a float
    outer(x, y)             outer product x y^T
    solve(A, b)             Gaussian elimination with partial pivoting;
                            b is a vector or a matrix of right sides
    inv(A)                  inverse of A
    det(A)                  determinant of A
    cholesky(A)             lower triangular L with A = L L^T (floats)
    cholesky_solve(L, b)    solve L L^T x = b for a vector b
    err_l1(e, dx=1)         sum |e_j| dx
    err_l2(e, dx=1)         sqrt(sum e_j^2 dx), as a float
    err_linf(e, dx=1)       max |e_j| (dx is not used)
    observed_order(errors)  [log2(E_i / E_(i+1)) for successive errors]
"""

import math


def zeros(m, n=None):
    """Return an m by n matrix of zeros (n = m if n is None)."""
    if n is None:
        n = m
    return [[0] * n for _ in range(m)]


def eye(n):
    """Return the n by n identity matrix."""
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = 1
    return out


def _is_matrix(a):
    return len(a) > 0 and isinstance(a[0], list)


def add(a, b):
    """Return a + b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x + y for x, y in zip(a, b)]


def sub(a, b):
    """Return a - b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x - y for x, y in zip(a, b)]


def scale(c, a):
    """Return c times a, for a vector or a matrix a."""
    if _is_matrix(a):
        return [[c * x for x in row] for row in a]
    return [c * x for x in a]


def transpose(a):
    """Return the transpose of the matrix a."""
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    """Return the matrix product a b."""
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    """Return the product of the matrix a and the vector x."""
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def dot(x, y):
    """Return the inner product of the vectors x and y."""
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    """Return the Euclidean norm of the vector x, as a float."""
    return math.sqrt(float(dot(x, x)))


def outer(x, y):
    """Return the outer product x y^T as a matrix."""
    return [[a * b for b in y] for a in x]


def _eliminate(a, rhs):
    """Reduce a to upper triangular form with partial pivoting.

    a is a copy of the square matrix, rhs a list of right side rows (one
    row per row of a) that receives the same row operations. Return the
    number of row swaps. Raise ValueError if a pivot is zero.
    """
    n = len(a)
    swaps = 0
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[p][k] == 0:
            raise ValueError("matrix is singular")
        if p != k:
            a[k], a[p] = a[p], a[k]
            rhs[k], rhs[p] = rhs[p], rhs[k]
            swaps += 1
        for i in range(k + 1, n):
            f = a[i][k] / a[k][k]
            if f == 0:
                continue
            for j in range(k, n):
                a[i][j] -= f * a[k][j]
            for j in range(len(rhs[i])):
                rhs[i][j] -= f * rhs[k][j]
    return swaps


def solve(a, b):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    b is a vector (the result is a vector) or a matrix with one column per
    right side (the result is a matrix). Fraction entries stay exact.
    Raise ValueError if a is singular.
    """
    n = len(a)
    work = [list(row) for row in a]
    vector = not _is_matrix(b)
    rhs = [[v] for v in b] if vector else [list(row) for row in b]
    _eliminate(work, rhs)
    m = len(rhs[0]) if n else 0
    x = [[0] * m for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(m):
            s = rhs[i][j]
            for k in range(i + 1, n):
                s -= work[i][k] * x[k][j]
            x[i][j] = s / work[i][i]
    if vector:
        return [row[0] for row in x]
    return x


def inv(a):
    """Return the inverse of the square matrix a."""
    return solve(a, eye(len(a)))


def det(a):
    """Return the determinant of the square matrix a (0 if singular)."""
    work = [list(row) for row in a]
    rhs = [[] for _ in a]
    try:
        swaps = _eliminate(work, rhs)
    except ValueError:
        return 0
    d = -1 if swaps % 2 else 1
    for i in range(len(a)):
        d *= work[i][i]
    return d


def cholesky(a):
    """Return the lower triangular L with a = L L^T, in floats.

    Raise ValueError if a is not symmetric positive definite.
    """
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = float(a[j][j]) - sum(low[j][k] ** 2 for k in range(j))
        if s <= 0.0:
            raise ValueError("matrix is not positive definite")
        low[j][j] = math.sqrt(s)
        for i in range(j + 1, n):
            t = float(a[i][j]) - sum(low[i][k] * low[j][k] for k in range(j))
            low[i][j] = t / low[j][j]
    return low


def cholesky_solve(low, b):
    """Solve L L^T x = b, with L from cholesky, for a vector b."""
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        y[i] = (float(b[i]) - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def err_l1(e, dx=1):
    """Return the discrete L1 norm sum |e_j| dx."""
    return sum(abs(v) for v in e) * dx


def err_l2(e, dx=1):
    """Return the discrete L2 norm sqrt(sum e_j^2 dx), as a float."""
    return math.sqrt(float(sum(v * v for v in e) * dx))


def err_linf(e, dx=1):
    """Return the max norm max |e_j|. dx is accepted for a uniform call and not used."""
    return max(abs(v) for v in e)


def observed_order(errors):
    """Return [log2(E_i / E_(i+1))] for a list of errors on meshes h, h/2, h/4, ..."""
    return [math.log2(float(errors[i]) / float(errors[i + 1])) for i in range(len(errors) - 1)]
