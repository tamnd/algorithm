# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-graphical-model/. The authors are listed in prov/65EW3P.jsonl.

"""Gaussian graphical models: exact precision and Schur complement facts in
rational arithmetic, partial correlations, and the graphical lasso of
Friedman, Hastie and Tibshirani (2008) by block coordinate descent.

Matrices are lists of rows.
"""

import math
from fractions import Fraction


def inverse(a):
    """Gauss-Jordan inverse; exact when the entries are Fractions."""
    n = len(a)
    m = [list(row) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        inv = 1 / m[c][c]
        m[c] = [x * inv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def sub(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def matmul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def conditional_covariance(sigma, A, S):
    """Cov(X_A | X_S) as the Schur complement Sigma_AA - Sigma_AS Sigma_SS^-1 Sigma_SA."""
    saa = sub(sigma, A, A)
    if not S:
        return saa
    k = matmul(matmul(sub(sigma, A, S), inverse(sub(sigma, S, S))), sub(sigma, S, A))
    return [[x - y for x, y in zip(r1, r2)] for r1, r2 in zip(saa, k)]


def partial_correlation(theta, i, j):
    """Correlation of X_i and X_j given all other variables."""
    return -theta[i][j] / math.sqrt(theta[i][i] * theta[j][j])


def edges_of(theta, tol=0):
    p = len(theta)
    return {(i, j) for i in range(p) for j in range(i + 1, p) if abs(theta[i][j]) > tol}


def soft(x, t):
    return math.copysign(max(abs(x) - t, 0.0), x)


def graphical_lasso(s, rho, tol=1e-10, max_sweeps=500):
    """Maximize log det(Theta) - tr(S Theta) - rho * sum_ij |Theta_ij| over positive definite Theta.

    Block coordinate descent on W = Theta^-1: for each column j, solve the lasso
    min_b 1/2 b' W11 b - b' s12 + rho |b|_1 by coordinate descent and put w12 = W11 b.
    The diagonal is penalized, so W_jj = S_jj + rho throughout. Returns (Theta, W).
    """
    p = len(s)
    w = [[float(s[i][j]) + (rho if i == j else 0.0) for j in range(p)] for i in range(p)]
    beta = [[0.0] * (p - 1) for _ in range(p)]
    for _ in range(max_sweeps):
        change = 0.0
        for j in range(p):
            idx = [k for k in range(p) if k != j]
            w11 = sub(w, idx, idx)
            s12 = [float(s[k][j]) for k in idx]
            b = beta[j]
            for _ in range(1000):  # inner lasso by coordinate descent
                delta = 0.0
                for k in range(p - 1):
                    r = s12[k] - sum(w11[k][l] * b[l] for l in range(p - 1) if l != k)
                    new = soft(r, rho) / w11[k][k]
                    delta = max(delta, abs(new - b[k]))
                    b[k] = new
                if delta < tol:
                    break
            w12 = [sum(w11[k][l] * b[l] for l in range(p - 1)) for k in range(p - 1)]
            for k, i in enumerate(idx):
                change = max(change, abs(w[i][j] - w12[k]))
                w[i][j] = w[j][i] = w12[k]
        if change < tol:
            break
    theta = [[0.0] * p for _ in range(p)]
    for j in range(p):
        idx = [k for k in range(p) if k != j]
        b = beta[j]
        t22 = 1.0 / (w[j][j] - sum(w[i][j] * b[k] for k, i in enumerate(idx)))
        theta[j][j] = t22
        for k, i in enumerate(idx):
            theta[i][j] = -b[k] * t22
    # the two columns of a pair give the same value up to the tolerance; symmetrize
    theta = [[(theta[i][j] + theta[j][i]) / 2 for j in range(p)] for i in range(p)]
    return theta, w
