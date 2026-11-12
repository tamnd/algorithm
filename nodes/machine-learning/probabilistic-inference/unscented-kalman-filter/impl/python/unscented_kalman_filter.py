# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unscented-kalman-filter/.

"""Unscented transform and unscented Kalman filter (additive noise form).

Model: x_0 ~ N(m0, P0), x_t = f(x_(t-1)) + q_t with q_t ~ N(0, Q),
y_t = h(x_t) + r_t with r_t ~ N(0, R), for t = 1..T.

f and h map a vector (a list of floats) to a vector. Matrices are lists of
rows. The scaling parameters are alpha, beta and kappa, with
lambda = alpha^2 (n + kappa) - n; the default kappa is 3 - n.
"""

import math


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mat_vec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b, sign=1):
    return [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def vec_add(a, b, sign=1):
    return [x + sign * y for x, y in zip(a, b)]


def inverse(a):
    """Gauss-Jordan elimination with partial pivoting."""
    n = len(a)
    m = [list(a[i]) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                g = m[r][c]
                m[r] = [x - g * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def cholesky(a):
    """Lower triangular L with L L^T = a, for a symmetric positive definite a."""
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("matrix is not positive definite")
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def sigma_points(m, P, alpha=1.0, beta=0.0, kappa=None):
    """Return the 2n + 1 sigma points and the mean and covariance weights."""
    n = len(m)
    if kappa is None:
        kappa = 3.0 - n
    lam = alpha * alpha * (n + kappa) - n
    c = n + lam
    L = cholesky([[c * x for x in row] for row in P])
    cols = transpose(L)
    X = [list(m)] + [vec_add(m, col) for col in cols] + [vec_add(m, col, -1) for col in cols]
    wm = [lam / c] + [1.0 / (2 * c)] * (2 * n)
    wc = [lam / c + 1 - alpha * alpha + beta] + [1.0 / (2 * c)] * (2 * n)
    return X, wm, wc


def unscented_transform(g, m, P, alpha=1.0, beta=0.0, kappa=None):
    """Approximate the mean and covariance of g(x) for x ~ N(m, P), and the
    cross-covariance Cov(x, g(x))."""
    X, wm, wc = sigma_points(m, P, alpha, beta, kappa)
    Y = [g(x) for x in X]
    mu = [sum(w * y[i] for w, y in zip(wm, Y)) for i in range(len(Y[0]))]
    dy = [vec_add(y, mu, -1) for y in Y]
    dx = [vec_add(x, m, -1) for x in X]
    S = [[sum(w * d[i] * d[j] for w, d in zip(wc, dy)) for j in range(len(mu))] for i in range(len(mu))]
    C = [[sum(w * a[i] * b[j] for w, a, b in zip(wc, dx, dy)) for j in range(len(mu))] for i in range(len(m))]
    return mu, S, C


def unscented_kalman_filter(f, h, Q, R, m0, P0, ys, alpha=1.0, beta=0.0, kappa=None):
    """Return the filtered means and covariances; index 0 is the prior and
    index t is the estimate of x_t given y_1..y_t."""
    m, P = list(m0), [list(r) for r in P0]  # @line L1
    means, covs = [m], [P]
    for y in ys:  # @line L2
        mp, Pp, _ = unscented_transform(f, m, P, alpha, beta, kappa)  # @line L3
        Pp = mat_add(Pp, Q)
        mu, S, C = unscented_transform(h, mp, Pp, alpha, beta, kappa)  # @line L4
        S = mat_add(S, R)
        K = mat_mul(C, inverse(S))  # @line L5
        m = vec_add(mp, mat_vec(K, vec_add(y, mu, -1)))  # @line L6
        P = mat_add(Pp, mat_mul(mat_mul(K, S), transpose(K)), -1)
        means.append(m)
        covs.append(P)
    return means, covs  # @line L7
