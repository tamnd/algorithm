# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-pca/. The authors are listed in prov/V9B0Y7.jsonl.

"""Probabilistic PCA (Tipping and Bishop 1999): x = W z + mu + eps, z ~ N(0, I_q), eps ~ N(0, sigma2 I).

closed_form gives the maximum likelihood fit from the eigenpairs of the covariance S (divisor n):
    sigma2 = mean of the d - q smallest eigenvalues,  W = U_q (L_q - sigma2 I)^(1/2).
em_step is the EM update of Tipping and Bishop, which reaches the same likelihood.
"""

import math


def mean_and_covariance(x):
    n, d = len(x), len(x[0])
    mu = [sum(row[j] for row in x) / n for j in range(d)]
    s = [[sum((row[a] - mu[a]) * (row[b] - mu[b]) for row in x) / n for b in range(d)] for a in range(d)]
    return mu, s


def matmul(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(col) for col in zip(*a)]


def inverse(a):
    """Gauss-Jordan elimination with partial pivoting."""
    d = len(a)
    m = [list(map(float, row)) + [1.0 if i == j else 0.0 for j in range(d)] for i, row in enumerate(a)]
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0.0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [t / piv for t in m[c]]
        for r in range(d):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [t - f * u for t, u in zip(m[r], m[c])]
    return [row[d:] for row in m]


def logdet_spd(a):
    d = len(a)
    low = [[0.0] * d for _ in range(d)]
    total = 0.0
    for i in range(d):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("matrix is not positive definite")
                low[i][i] = math.sqrt(s)
                total += math.log(low[i][i])
            else:
                low[i][j] = s / low[j][j]
    return 2.0 * total


def jacobi_eigen(a, tol=1e-14, max_sweeps=100):
    """Cyclic Jacobi method; eigenvalues in decreasing order and unit eigenvectors."""
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
    vectors = []
    for j in order:
        col = [v[r][j] for r in range(d)]
        big = max(range(d), key=lambda r: abs(col[r]))
        vectors.append([-t for t in col] if col[big] < 0 else col)
    return [m[j][j] for j in order], vectors


def model_covariance(w, sigma2):
    d, q = len(w), len(w[0])
    return [[sum(w[i][t] * w[j][t] for t in range(q)) + (sigma2 if i == j else 0.0) for j in range(d)] for i in range(d)]


def log_likelihood(s, n, w, sigma2):
    """-n/2 (d log 2 pi + log det C + tr(C^-1 S)) with C = W W^T + sigma2 I."""
    d = len(s)
    c = model_covariance(w, sigma2)
    inv = inverse(c)
    tr = sum(inv[i][j] * s[j][i] for i in range(d) for j in range(d))
    return -0.5 * n * (d * math.log(2.0 * math.pi) + logdet_spd(c) + tr)


def closed_form(s, q):
    """Maximum likelihood (W, sigma2, eigenvalues) with the rotation R = I."""
    d = len(s)
    values, vectors = jacobi_eigen(s)
    sigma2 = sum(values[q:]) / (d - q)
    w = [[vectors[j][i] * math.sqrt(max(values[j] - sigma2, 0.0)) for j in range(q)] for i in range(d)]
    return w, sigma2, values


def max_log_likelihood(values, n, q):
    """-n/2 (d log 2 pi + sum_{j <= q} log lambda_j + (d - q) log sigma2 + d)."""
    d = len(values)
    sigma2 = sum(values[q:]) / (d - q)
    return -0.5 * n * (d * math.log(2.0 * math.pi) + sum(math.log(v) for v in values[:q]) + (d - q) * math.log(sigma2) + d)


def em_step(s, w, sigma2):
    """One EM step of Tipping and Bishop. Returns the new (w, sigma2)."""
    d, q = len(w), len(w[0])
    m = matmul(transpose(w), w)  # @line L3
    for t in range(q):
        m[t][t] += sigma2
    minv = inverse(m)
    sw = matmul(s, w)
    inner = matmul(minv, matmul(transpose(w), sw))
    for t in range(q):
        inner[t][t] += sigma2
    new_w = matmul(sw, inverse(inner))  # @line L4
    corr = matmul(matmul(sw, minv), transpose(new_w))
    new_sigma2 = sum(s[i][i] - corr[i][i] for i in range(d)) / d  # @line L5
    return new_w, new_sigma2  # @line L6


def fit_em(s, n, q, rng, max_iter=5000, tol=1e-13):
    """EM from a random start. Returns (w, sigma2, history of the log likelihood)."""
    d = len(s)
    scale = math.sqrt(sum(s[i][i] for i in range(d)) / d)
    w = [[rng.gauss(0.0, scale) for _ in range(q)] for _ in range(d)]  # @line L1
    sigma2 = sum(s[i][i] for i in range(d)) / d
    history = [log_likelihood(s, n, w, sigma2)]
    for _ in range(max_iter):  # @line L2
        w, sigma2 = em_step(s, w, sigma2)
        history.append(log_likelihood(s, n, w, sigma2))
        if history[-1] - history[-2] < tol * abs(history[-2]):  # @line L7
            break
    return w, sigma2, history  # @line L8


def posterior_mean(x, mu, w, sigma2):
    """E[z | x] = M^-1 W^T (x - mu) with M = W^T W + sigma2 I."""
    q = len(w[0])
    m = matmul(transpose(w), w)
    for t in range(q):
        m[t][t] += sigma2
    y = [[xi - mi] for xi, mi in zip(x, mu)]
    return [r[0] for r in matmul(inverse(m), matmul(transpose(w), y))]
