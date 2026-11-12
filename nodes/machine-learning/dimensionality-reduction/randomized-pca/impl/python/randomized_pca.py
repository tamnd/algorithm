# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-pca/. The authors are listed in prov/A8T6DS.jsonl.

"""Randomized PCA by the randomized range finder with power (subspace) iterations,
Halko, Martinsson and Tropp (2011), Algorithms 4.4 and 5.1, applied to the centered data.

randomized_pca(x, k, p, q, rng) returns the mean, the k components (rows of length d),
the eigenvalues sigma_j^2 / n of the covariance (divisor n) and the basis Q of the range.
"""

import math


def dot(a, b):
    return sum(s * t for s, t in zip(a, b))


def orth_columns(cols, tol=1e-13):
    """Orthonormal basis of the span of the given columns: modified Gram-Schmidt, applied
    twice. A column whose norm falls below tol times its original norm is dropped."""
    basis = []
    for col in cols:
        w = list(col)
        start = math.sqrt(dot(w, w))
        for _ in range(2):
            for b in basis:
                c = dot(b, w)
                w = [s - c * t for s, t in zip(w, b)]
        norm = math.sqrt(dot(w, w))
        if start > 0 and norm > tol * start:
            basis.append([s / norm for s in w])
    return basis


def mat_cols(x, cols):
    """x (n x d, rows) times the d-vectors in cols: returns n-vectors."""
    return [[dot(row, c) for row in x] for c in cols]


def mat_t_cols(x, cols):
    """x^T times the n-vectors in cols: returns d-vectors."""
    d = len(x[0])
    out = []
    for c in cols:
        acc = [0.0] * d
        for ci, row in zip(c, x):
            if ci != 0.0:
                for j in range(d):
                    acc[j] += ci * row[j]
        out.append(acc)
    return out


def one_sided_jacobi(cols, tol=1e-15, max_sweeps=60):
    """Hestenes one-sided Jacobi. cols are the columns of a matrix A. Returns (v, s, a)
    where a holds the columns of A V (mutually orthogonal), s their norms, v the columns of V."""
    a = [list(c) for c in cols]
    c = len(a)
    v = [[1.0 if i == j else 0.0 for i in range(c)] for j in range(c)]
    for _ in range(max_sweeps):
        rotated = False
        for p in range(c - 1):
            for q in range(p + 1, c):
                alpha, beta, gamma = dot(a[p], a[p]), dot(a[q], a[q]), dot(a[p], a[q])
                if gamma == 0.0 or abs(gamma) <= tol * math.sqrt(alpha * beta):
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                cs = 1.0 / math.sqrt(1.0 + t * t)
                sn = cs * t
                for vec in (a, v):
                    xp, xq = vec[p], vec[q]
                    vec[p] = [cs * s - sn * u for s, u in zip(xp, xq)]
                    vec[q] = [sn * s + cs * u for s, u in zip(xp, xq)]
        if not rotated:
            break
    return v, [math.sqrt(dot(col, col)) for col in a], a


def randomized_pca(x, k, rng, p=5, q=1):
    """Top k principal components of the rows of x with oversampling p and q power iterations."""
    n, d = len(x), len(x[0])
    mu = [sum(row[j] for row in x) / n for j in range(d)]  # @line L1
    xc = [[row[j] - mu[j] for j in range(d)] for row in x]
    ell = min(k + p, d, n)
    omega = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(ell)]  # @line L2
    qb = orth_columns(mat_cols(xc, omega))  # @line L3
    for _ in range(q):  # @line L4
        qhat = orth_columns(mat_t_cols(xc, qb))  # @line L5
        qb = orth_columns(mat_cols(xc, qhat))  # @line L6
    bt = mat_t_cols(xc, qb)  # @line L7
    # B = Q^T X_c has the rows bt[i]. One-sided Jacobi on the columns of B^T gives
    # B^T V = A, so B = V diag(s) (A diag(1/s))^T: the right singular vectors of B are A / s.
    v, s, a = one_sided_jacobi(bt)  # @line L8
    order = sorted(range(len(s)), key=lambda j: -s[j])[:k]
    components = []
    for j in order:
        comp = [t / s[j] for t in a[j]] if s[j] > 0 else [0.0] * d
        big = max(range(d), key=lambda i: abs(comp[i]))
        components.append([-t for t in comp] if comp[big] < 0 else comp)
    values = [s[j] ** 2 / n for j in order]
    return mu, components, values, qb  # @line L9


def range_error(x, mu, qb, rng, iters=200):
    """Spectral norm of (I - Q Q^T) X_c, by power iteration on its Gram matrix."""
    n, d = len(x), len(x[0])
    xc = [[row[j] - mu[j] for j in range(d)] for row in x]

    def residual(vec):  # (I - Q Q^T) X_c vec
        y = [dot(row, vec) for row in xc]
        for b in qb:
            c = dot(b, y)
            y = [s - c * t for s, t in zip(y, b)]
        return y

    v = [rng.gauss(0.0, 1.0) for _ in range(d)]
    est = 0.0
    for _ in range(iters):
        nv = math.sqrt(dot(v, v))
        if nv == 0.0:
            return 0.0
        v = [t / nv for t in v]
        y = residual(v)
        est = math.sqrt(dot(y, y))
        # apply the transpose: X_c^T (I - Q Q^T) y, and (I - QQ^T) y = y already
        v = mat_t_cols(xc, [y])[0]
    return est
