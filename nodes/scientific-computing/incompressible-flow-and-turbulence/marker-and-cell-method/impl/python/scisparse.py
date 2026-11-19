# SPDX-License-Identifier: MIT
# Shared helper of the scientific-computing pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Tridiagonal solvers, sparse matrices and simple iterative solvers.

A vector is a list. A sparse matrix is a list of rows, and each row is a
dict that maps a column index to a value. Entries may be int, float or
fractions.Fraction. thomas, thomas_periodic, spmatvec, from_dense and
to_dense keep Fraction entries exact. cg takes square roots and works in
float.

API (fixed; other pages copy this file byte for byte):
    thomas(a, b, c, d)             solve a tridiagonal system. Row i reads
                                   a[i] x[i-1] + b[i] x[i] + c[i] x[i+1] = d[i];
                                   a[0] and c[n-1] are not used.
    thomas_periodic(a, b, c, d)    solve a cyclic tridiagonal system: as
                                   thomas, but a[0] multiplies x[n-1] and
                                   c[n-1] multiplies x[0]. Uses the
                                   Sherman-Morrison formula. n >= 3.
    from_dense(A)                  sparse copy of a dense matrix (drops zeros)
    to_dense(A, ncols=None)        dense copy of a sparse matrix
    spmatvec(A, x)                 A times x
    poisson2d(nx, ny, dx, dy, bc="dirichlet")
                                   the matrix of MINUS the 5-point Laplacian
                                   on nx by ny unknowns, numbered
                                   k = i + nx * j (i along x, j along y).
                                   bc = "dirichlet": unknowns at the interior
                                   nodes ((i + 1) dx, (j + 1) dy) with zero
                                   values outside; the matrix is symmetric
                                   positive definite.
                                   bc = "periodic": the grid wraps around in
                                   both directions; the matrix is symmetric
                                   positive semidefinite, and its null space
                                   is the constant vectors.
                                   bc = "neumann": unknowns at cell centers,
                                   zero normal derivative at the walls (a
                                   missing neighbor drops out of the
                                   stencil); null space as for "periodic".
    cg(A, b, tol=1e-10, maxit=None, x0=None)
                                   conjugate gradient for a symmetric
                                   positive (semi)definite A. Stops when
                                   ||b - A x||_2 <= tol * ||b||_2. Returns
                                   (x, iterations). For a singular A, b must
                                   be in the range of A (for the Poisson
                                   matrices above: sum(b) = 0).
    gauss_seidel(A, b, iters, x0=None)
                                   iters forward Gauss-Seidel sweeps; every
                                   row needs a nonzero diagonal entry.
"""

import math


def thomas(a, b, c, d):
    n = len(d)
    if n == 0:
        return []
    cp = [0] * n
    dp = [0] * n
    cp[0] = c[0] / b[0] if n > 1 else 0
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        if i < n - 1:
            cp[i] = c[i] / m
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0] * n
    x[n - 1] = dp[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def thomas_periodic(a, b, c, d):
    """Cyclic tridiagonal solve. A = T + u v^T with u = (gamma, 0, .., 0, c[n-1])
    and v = (1, 0, .., 0, a[0] / gamma), so T is tridiagonal."""
    n = len(d)
    if n < 3:
        raise ValueError("thomas_periodic needs n >= 3")
    gamma = -b[0]
    bb = list(b)
    bb[0] = b[0] - gamma
    bb[n - 1] = b[n - 1] - c[n - 1] * a[0] / gamma
    y = thomas(a, bb, c, d)
    u = [0] * n
    u[0] = gamma
    u[n - 1] = c[n - 1]
    z = thomas(a, bb, c, u)
    vy = y[0] + a[0] * y[n - 1] / gamma
    vz = z[0] + a[0] * z[n - 1] / gamma
    f = vy / (1 + vz)
    return [y[i] - f * z[i] for i in range(n)]


def from_dense(A):
    return [{j: v for j, v in enumerate(row) if v != 0} for row in A]


def to_dense(A, ncols=None):
    if ncols is None:
        ncols = len(A)
    out = []
    for row in A:
        r = [0] * ncols
        for j, v in row.items():
            r[j] = v
        out.append(r)
    return out


def spmatvec(A, x):
    return [sum(v * x[j] for j, v in row.items()) for row in A]


def poisson2d(nx, ny, dx, dy, bc="dirichlet"):
    if bc not in ("dirichlet", "periodic", "neumann"):
        raise ValueError("bc must be dirichlet, periodic or neumann")
    cx = 1 / (dx * dx)
    cy = 1 / (dy * dy)
    A = []
    for j in range(ny):
        for i in range(nx):
            row = {}
            k = i + nx * j
            for (ii, jj, w) in ((i - 1, j, cx), (i + 1, j, cx), (i, j - 1, cy), (i, j + 1, cy)):
                inside = 0 <= ii < nx and 0 <= jj < ny
                if bc == "periodic":
                    ii %= nx
                    jj %= ny
                    inside = True
                if bc == "neumann" and not inside:
                    continue
                row[k] = row.get(k, 0) + w
                if inside:
                    m = ii + nx * jj
                    row[m] = row.get(m, 0) - w
            A.append({m: v for m, v in row.items() if v != 0})
    return A


def cg(A, b, tol=1e-10, maxit=None, x0=None):
    n = len(b)
    if maxit is None:
        maxit = 10 * n
    x = [0.0] * n if x0 is None else [float(v) for v in x0]
    if x0 is None:
        r = [float(v) for v in b]
    else:
        ax = spmatvec(A, x)
        r = [b[i] - ax[i] for i in range(n)]
    bnorm = math.sqrt(sum(float(v) * float(v) for v in b))
    stop = tol * bnorm
    rr = sum(v * v for v in r)
    if math.sqrt(rr) <= stop:
        return x, 0
    p = list(r)
    for it in range(1, maxit + 1):
        ap = spmatvec(A, p)
        pap = sum(p[i] * ap[i] for i in range(n))
        if pap <= 0:
            return x, it
        alpha = rr / pap
        for i in range(n):
            x[i] += alpha * p[i]
            r[i] -= alpha * ap[i]
        rr_new = sum(v * v for v in r)
        if math.sqrt(rr_new) <= stop:
            return x, it
        beta = rr_new / rr
        rr = rr_new
        p = [r[i] + beta * p[i] for i in range(n)]
    return x, maxit


def gauss_seidel(A, b, iters, x0=None):
    n = len(b)
    x = [0] * n if x0 is None else list(x0)
    for _ in range(iters):
        for i in range(n):
            row = A[i]
            s = b[i]
            diag = 0
            for j, v in row.items():
                if j == i:
                    diag = v
                else:
                    s -= v * x[j]
            x[i] = s / diag
    return x
