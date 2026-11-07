# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subspace-iteration/. The authors are listed in prov/1HMDCT.jsonl.

"""Subspace iteration with Rayleigh-Ritz for a real symmetric matrix.

subspace_iteration(a, p, x0, tol, maxit) multiplies an orthonormal block of p
vectors by A, solves the small projected eigenproblem of H = Q^T A Q (the
Rayleigh-Ritz step), and orthonormalizes A X for the next step. It stops when
every Ritz residual r_i = A x_i - theta_i x_i satisfies
||r_i|| <= tol * max_j |theta_j|. Then (Theta, X) is an exact block of
eigenpairs of the symmetric matrix A + E with ||E||_2 = ||R||_2.

Blocks are stored as lists of columns. Standard library only.
"""

import math
import random
from typing import NamedTuple


class SubspaceResult(NamedTuple):
    values: list  # Ritz values, ordered by decreasing modulus
    vectors: list  # Ritz vectors, as columns (lists of length n)
    iterations: int  # the number of block steps
    converged: bool
    residuals: list  # ||A x_i - theta_i x_i||_2 for each Ritz pair
    matvecs: int  # the number of products A v
    history: list  # Ritz values of each step, for rate measurements


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def dot(x, y):
    return sum(xi * yi for xi, yi in zip(x, y))


def norm2(x):
    return math.sqrt(sum(t * t for t in x))


def combine(cols, coeffs):
    """sum_j coeffs[j] * cols[j]."""
    n = len(cols[0])
    out = [0.0] * n
    for c, w in zip(cols, coeffs):
        if w != 0.0:
            for i in range(n):
                out[i] += w * c[i]
    return out


def orthonormalize(cols, rng):
    """Modified Gram-Schmidt, applied twice, on a list of columns.

    A column that loses almost all of its norm is replaced by a random vector
    orthogonalized against the earlier ones. Returns (q, replaced).
    """
    q = []
    replaced = 0
    n = len(cols[0])
    for c in cols:
        v = list(c)
        start = norm2(v)
        for attempt in range(3):
            for _ in range(2):  # twice is enough
                for w in q:
                    h = dot(w, v)
                    for i in range(n):
                        v[i] -= h * w[i]
            nv = norm2(v)
            if nv > 1e-10 * start and nv > 0.0:
                break
            v = [rng.uniform(-1.0, 1.0) for _ in range(n)]
            start = norm2(v)
            replaced += 1
        q.append([t / nv for t in v])
    return q, replaced


def jacobi_eig(h, tol=1e-15, max_sweeps=60):
    """Cyclic Jacobi for a small symmetric matrix. Returns (values, Y columns)."""
    p = len(h)
    a = [list(row) for row in h]
    y = [[float(i == j) for j in range(p)] for i in range(p)]  # rows of Y
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(p) for j in range(p) if i != j))
        scale = math.sqrt(sum(a[i][j] ** 2 for i in range(p) for j in range(p)))
        if off <= tol * scale or off == 0.0:
            break
        for i in range(p - 1):
            for j in range(i + 1, p):
                if a[i][j] == 0.0:
                    continue
                tau = (a[j][j] - a[i][i]) / (2.0 * a[i][j])
                t = (1.0 if tau >= 0 else -1.0) / (abs(tau) + math.sqrt(1.0 + tau * tau))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                for k in range(p):  # A <- A J (columns i, j)
                    aki, akj = a[k][i], a[k][j]
                    a[k][i] = c * aki - s * akj
                    a[k][j] = s * aki + c * akj
                for k in range(p):  # A <- J^T A (rows i, j)
                    aik, ajk = a[i][k], a[j][k]
                    a[i][k] = c * aik - s * ajk
                    a[j][k] = s * aik + c * ajk
                for k in range(p):  # Y <- Y J
                    yki, ykj = y[k][i], y[k][j]
                    y[k][i] = c * yki - s * ykj
                    y[k][j] = s * yki + c * ykj
    values = [a[i][i] for i in range(p)]
    cols = [[y[k][i] for k in range(p)] for i in range(p)]
    return values, cols


def subspace_iteration(a, p, x0=None, tol=1e-12, maxit=5000, seed=0, monitor=None):
    """Return a SubspaceResult for the p eigenvalues of largest modulus of a symmetric A.

    x0 is an optional list of p start columns. monitor(k, q) is called with
    the orthonormal basis q of A^k span(x0) at the start of step k + 1.
    """
    n = len(a)
    if n == 0 or not 1 <= p <= n:
        raise ValueError("need 1 <= p <= n")
    if maxit < 1:
        raise ValueError("maxit must be at least 1")
    rng = random.Random(seed)
    if x0 is None:
        x0 = [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(p)]
    if len(x0) != p:
        raise ValueError("x0 must have p columns")
    q, _ = orthonormalize(x0, rng)  # @line L1
    history = []
    matvecs = 0
    for k in range(1, maxit + 1):  # @line L2
        if monitor is not None:
            monitor(k - 1, q)
        z = [matvec(a, c) for c in q]  # @line L3
        matvecs += p
        h = [[dot(q[i], z[j]) for j in range(p)] for i in range(p)]  # @line L4
        h = [[0.5 * (h[i][j] + h[j][i]) for j in range(p)] for i in range(p)]
        theta, y = jacobi_eig(h)  # @line L5
        order = sorted(range(p), key=lambda i: -abs(theta[i]))
        theta = [theta[i] for i in order]
        y = [y[i] for i in order]
        history.append(theta)
        x = [combine(q, yi) for yi in y]  # @line L6
        w = [combine(z, yi) for yi in y]
        res = [norm2([wi - t * xi for wi, xi in zip(wc, xc)]) for wc, xc, t in zip(w, x, theta)]  # @line L7
        bound = tol * max(abs(t) for t in theta)
        if max(res) <= bound:  # @line L8
            return SubspaceResult(theta, x, k, True, res, matvecs, history)
        if k == maxit:  # @line L9
            return SubspaceResult(theta, x, k, False, res, matvecs, history)
        q, _ = orthonormalize(w, rng)  # @line L10
    raise AssertionError("unreachable")
