# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitening/. The authors are listed in prov/H04HKR.jsonl.

"""Whitening of data: PCA whitening, ZCA (Mahalanobis) whitening and Cholesky whitening.

fit_whitening(x, choose_q, eps) follows the template of the page:
W = Q diag((lambda_j + eps)^(-1/2)) V^T, where C = V diag(lambda) V^T is the
covariance (divisor n) and Q = choose_q(V) is orthogonal. With eps = 0 the
whitened data z_i = W (x_i - mu) have the identity as covariance.
"""

import math


def mean(x):
    n, d = len(x), len(x[0])
    return [sum(row[j] for row in x) / n for j in range(d)]


def covariance(x, mu):
    n, d = len(x), len(mu)
    return [[sum((row[a] - mu[a]) * (row[b] - mu[b]) for row in x) / n for b in range(d)] for a in range(d)]


def mean_and_covariance(x):
    mu = mean(x)
    return mu, covariance(x, mu)


def jacobi_eigen(a, tol=1e-13, max_sweeps=100):
    """Cyclic Jacobi method for a symmetric matrix. Returns (values, vectors), values in
    decreasing order, vectors[j] the unit eigenvector of values[j]."""
    d = len(a)
    m = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(max_sweeps):
        off = math.sqrt(sum(m[i][j] ** 2 for i in range(d) for j in range(d) if i != j))
        if off <= tol * max(1.0, math.sqrt(sum(m[i][i] ** 2 for i in range(d)))):
            break
        for p in range(d - 1):
            for q in range(p + 1, d):
                if m[p][q] == 0.0:
                    continue
                theta = (m[q][q] - m[p][p]) / (2.0 * m[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for r in range(d):
                    mp, mq = m[r][p], m[r][q]
                    m[r][p], m[r][q] = c * mp - s * mq, s * mp + c * mq
                    vp, vq = v[r][p], v[r][q]
                    v[r][p], v[r][q] = c * vp - s * vq, s * vp + c * vq
                for r in range(d):
                    mp, mq = m[p][r], m[q][r]
                    m[p][r], m[q][r] = c * mp - s * mq, s * mp + c * mq
    order = sorted(range(d), key=lambda j: -m[j][j])
    values = [m[j][j] for j in order]
    vectors = []
    for j in order:
        col = [v[r][j] for r in range(d)]
        big = max(range(d), key=lambda r: abs(col[r]))
        if col[big] < 0:
            col = [-t for t in col]
        vectors.append(col)
    return values, vectors


def pca_q(vectors):
    """Q = I: the whitened coordinates are the scaled principal component scores."""
    d = len(vectors)
    return [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]


def zca_q(vectors):
    """Q = V: rotate back, which gives W = C^(-1/2) (ZCA or Mahalanobis whitening)."""
    d = len(vectors)
    return [[vectors[j][i] for j in range(d)] for i in range(d)]


def fit_whitening(x, choose_q=zca_q, eps=0.0):
    """Return (mu, w) such that z = w (x - mu) is white for the training data x."""
    mu = mean(x)  # @line L1
    c = covariance(x, mu)  # @line L2
    d = len(c)
    values, vectors = jacobi_eigen(c)  # @line L3
    if min(values) + eps <= 1e-12 * max(1.0, values[0]):
        raise ValueError("the covariance matrix is singular; use eps > 0 or fewer features")
    w_pca = [[vectors[j][i] / math.sqrt(values[j] + eps) for i in range(d)] for j in range(d)]  # @line L4
    q = choose_q(vectors)  # @line L5
    w = [[sum(q[i][t] * w_pca[t][j] for t in range(d)) for j in range(d)] for i in range(d)]  # @line L6
    return mu, w  # @line L7


def cholesky_whitening(x):
    """W = L^(-1) where C = L L^T. The result is lower triangular."""
    mu, c = mean_and_covariance(x)
    d = len(c)
    low = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            s = c[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("the covariance matrix is singular")
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    inv = [[0.0] * d for _ in range(d)]
    for col in range(d):
        for i in range(d):
            rhs = (1.0 if i == col else 0.0) - sum(low[i][t] * inv[t][col] for t in range(i))
            inv[i][col] = rhs / low[i][i]
    return mu, inv


def transform(x, mu, w):
    """Apply a fitted whitening (mu, w) to the rows of x, also to new data."""
    d = len(mu)
    return [[sum(w[i][j] * (row[j] - mu[j]) for j in range(d)) for i in range(d)] for row in x]
