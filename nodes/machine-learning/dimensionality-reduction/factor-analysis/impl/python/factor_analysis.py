# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factor-analysis/. The authors are listed in prov/7FPPGW.jsonl.

"""Factor analysis x = mu + Lambda z + eps, z ~ N(0, I_k), eps ~ N(0, Psi) with Psi diagonal.

The maximum likelihood fit of mu is the sample mean, and Lambda and Psi depend on the
data only through the covariance S (divisor n). em_step is the EM update of Rubin and
Thayer (1982); each step does not decrease the log likelihood. varimax is the rotation
of Kaiser (1958), done by plane rotations of pairs of factors.
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
    """log det of a symmetric positive definite matrix by the Cholesky factor."""
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


def model_covariance(lam, psi):
    d, k = len(lam), len(lam[0])
    return [[sum(lam[i][t] * lam[j][t] for t in range(k)) + (psi[i] if i == j else 0.0) for j in range(d)] for i in range(d)]


def log_likelihood(s, n, lam, psi):
    """-n/2 (d log 2 pi + log det Sigma + tr(Sigma^-1 S)) with Sigma = Lambda Lambda^T + Psi."""
    d = len(s)
    sigma = model_covariance(lam, psi)
    inv = inverse(sigma)
    tr = sum(inv[i][j] * s[j][i] for i in range(d) for j in range(d))
    return -0.5 * n * (d * math.log(2.0 * math.pi) + logdet_spd(sigma) + tr)


def em_step(s, lam, psi, psi_min=1e-6):
    """One EM step of Rubin and Thayer. Returns the new (lam, psi)."""
    d, k = len(lam), len(lam[0])
    beta = matmul(transpose(lam), inverse(model_covariance(lam, psi)))  # @line L3
    bs = matmul(beta, s)
    bl = matmul(beta, lam)
    g = [[(1.0 if a == b else 0.0) - bl[a][b] + sum(bs[a][t] * beta[b][t] for t in range(d)) for b in range(k)] for a in range(k)]  # @line L4
    new_lam = matmul(transpose(bs), inverse(g))  # @line L5
    lbs = matmul(new_lam, bs)
    new_psi = [max(psi_min, s[i][i] - lbs[i][i]) for i in range(d)]  # @line L6
    return new_lam, new_psi


def fit(s, n, k, rng, max_iter=1000, tol=1e-10, psi_min=1e-6):
    """Fit Lambda (d x k) and the diagonal Psi to the covariance s of n points by EM.
    Returns (lam, psi, history) where history lists the log likelihood after each step."""
    d = len(s)
    lam = [[rng.gauss(0.0, 1.0) * math.sqrt(s[i][i] / (2 * k)) for _ in range(k)] for i in range(d)]  # @line L1
    psi = [s[i][i] / 2.0 for i in range(d)]
    history = [log_likelihood(s, n, lam, psi)]
    for _ in range(max_iter):  # @line L2
        lam, psi = em_step(s, lam, psi, psi_min)
        history.append(log_likelihood(s, n, lam, psi))
        if history[-1] - history[-2] < tol * abs(history[-2]):  # @line L7
            break
    return lam, psi, history  # @line L8


def varimax_criterion(lam):
    """Sum over factors of the variance of the squared loadings (raw varimax)."""
    d, k = len(lam), len(lam[0])
    total = 0.0
    for j in range(k):
        sq = [lam[i][j] ** 2 for i in range(d)]
        m = sum(sq) / d
        total += sum((q - m) ** 2 for q in sq) / d
    return total


def varimax(lam, normalize=True, max_sweeps=100, tol=1e-12):
    """Kaiser's varimax by plane rotations. Returns (rotated loadings, rotation R),
    with rotated = lam R and R orthogonal."""
    d, k = len(lam), len(lam[0])
    h = [math.sqrt(sum(t * t for t in row)) if normalize else 1.0 for row in lam]
    a = [[lam[i][j] / h[i] if h[i] > 0 else 0.0 for j in range(k)] for i in range(d)]
    r = [[1.0 if i == j else 0.0 for j in range(k)] for i in range(k)]
    for _ in range(max_sweeps):
        largest = 0.0
        for p in range(k - 1):
            for q in range(p + 1, k):
                u = [a[i][p] ** 2 - a[i][q] ** 2 for i in range(d)]
                v = [2.0 * a[i][p] * a[i][q] for i in range(d)]
                su, sv = sum(u), sum(v)
                num = 2.0 * sum(ui * vi for ui, vi in zip(u, v)) - 2.0 * su * sv / d
                den = sum(ui * ui - vi * vi for ui, vi in zip(u, v)) - (su * su - sv * sv) / d
                phi = math.atan2(num, den) / 4.0
                largest = max(largest, abs(phi))
                c, sn = math.cos(phi), math.sin(phi)
                for i in range(d):
                    x, y = a[i][p], a[i][q]
                    a[i][p], a[i][q] = c * x + sn * y, -sn * x + c * y
                for i in range(k):
                    x, y = r[i][p], r[i][q]
                    r[i][p], r[i][q] = c * x + sn * y, -sn * x + c * y
        if largest < tol:
            break
    return [[a[i][j] * h[i] for j in range(k)] for i in range(d)], r
