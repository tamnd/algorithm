# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-mixture-model/. The authors are listed in prov/4RQ4DM.jsonl.

"""Gaussian mixture model with full covariances, fitted by EM.

A model is (weights, means, covs) with k components in d dimensions.
The regularization lam > 0 gives the M step
    Sigma_j = (sum_i r_ij (x_i - mu_j)(x_i - mu_j)^T + lam I) / N_j,
which is the exact maximizer of the penalized log likelihood
    log L - (lam / 2) sum_j trace(Sigma_j^{-1}),
so EM never decreases that objective, and it stays bounded when a
component collapses on one point. With lam = 0 this is plain EM.
"""

import math


def cholesky(A):
    d = len(A)
    L = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            s = A[i][j] - sum(L[i][t] * L[j][t] for t in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("covariance is not positive definite")
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def forward(L, b):
    y = []
    for i in range(len(L)):
        y.append((b[i] - sum(L[i][t] * y[t] for t in range(i))) / L[i][i])
    return y


def log_normal(x, mu, cov):
    """log N(x | mu, cov) through the Cholesky factor cov = L L^T."""
    L = cholesky(cov)
    z = forward(L, [a - b for a, b in zip(x, mu)])
    logdet = 2 * sum(math.log(L[i][i]) for i in range(len(L)))
    return -0.5 * (len(x) * math.log(2 * math.pi) + logdet + sum(t * t for t in z))


def trace_inverse(cov):
    L = cholesky(cov)
    d = len(L)
    # trace(cov^{-1}) = sum of squares of the entries of L^{-1}
    return sum(sum(t * t for t in forward(L, [1.0 if r == c else 0.0 for r in range(d)])) for c in range(d))


def logsumexp(v):
    m = max(v)
    return m + math.log(sum(math.exp(t - m) for t in v))


def log_likelihood(points, model):
    weights, means, covs = model
    return sum(
        logsumexp([math.log(w) + log_normal(x, m, c) for w, m, c in zip(weights, means, covs)])
        for x in points
    )


def penalized(points, model, lam):
    value = log_likelihood(points, model)
    if lam:
        value -= lam / 2 * sum(trace_inverse(c) for c in model[2])
    return value


def e_step(points, model):
    """Responsibilities r_ij = pi_j N(x_i|mu_j,S_j) / sum_l pi_l N(x_i|mu_l,S_l)."""
    weights, means, covs = model
    R = []
    for x in points:
        logs = [math.log(w) + log_normal(x, m, c) for w, m, c in zip(weights, means, covs)]  # @line L3
        z = logsumexp(logs)
        R.append([math.exp(t - z) for t in logs])
    return R


def m_step(points, R, lam, old):
    n, d, k = len(points), len(points[0]), len(R[0])
    weights, means, covs = [], [], []
    for j in range(k):
        Nj = sum(R[i][j] for i in range(n))  # @line L4
        if Nj < 1e-12:  # an empty component keeps its old parameters
            weights.append(max(Nj / n, 1e-300))
            means.append(list(old[1][j]))
            covs.append([list(r) for r in old[2][j]])
            continue
        weights.append(Nj / n)
        mu = [sum(R[i][j] * points[i][t] for i in range(n)) / Nj for t in range(d)]  # @line L5
        S = [[lam if a == b else 0.0 for b in range(d)] for a in range(d)]
        for i in range(n):
            diff = [points[i][t] - mu[t] for t in range(d)]
            for a in range(d):
                for b in range(d):
                    S[a][b] += R[i][j] * diff[a] * diff[b]
        means.append(mu)
        covs.append([[S[a][b] / Nj for b in range(d)] for a in range(d)])  # @line L6
    s = sum(weights)
    return [w / s for w in weights], means, covs


def initial_model(points, k, rng):
    n, d = len(points), len(points[0])
    mean = [sum(p[t] for p in points) / n for t in range(d)]
    cov = [[sum((p[a] - mean[a]) * (p[b] - mean[b]) for p in points) / n for b in range(d)] for a in range(d)]
    means = [list(points[i]) for i in rng.sample(range(n), k)]
    return [1.0 / k] * k, means, [[list(r) for r in cov] for _ in range(k)]


def em(points, k, rng=None, init=None, lam=1e-6, tol=1e-10, max_iter=500, trace=None):
    """Fit a k-component GMM by EM. Returns (model, R, objective)."""
    model = init if init is not None else initial_model(points, k, rng)  # @line L1
    value = penalized(points, model, lam)
    if trace is not None:
        trace.append(value)
    R = e_step(points, model)
    for _ in range(max_iter):  # @line L2
        model = m_step(points, R, lam, model)
        R = e_step(points, model)
        new = penalized(points, model, lam)
        if trace is not None:
            trace.append(new)
        done = new - value <= tol * (1 + abs(value))  # @line L7
        value = new
        if done:
            break
    return model, R, value  # @line L8


def num_params(k, d):
    """Free parameters of a k-component GMM with full covariances."""
    return (k - 1) + k * d + k * d * (d + 1) // 2


def bic(points, model):
    k, d = len(model[0]), len(points[0])
    return -2 * log_likelihood(points, model) + num_params(k, d) * math.log(len(points))


def sample(model, n, rng):
    weights, means, covs = model
    out, labels = [], []
    for _ in range(n):
        j = rng.choices(range(len(weights)), weights)[0]
        L = cholesky(covs[j])
        z = [rng.gauss(0, 1) for _ in means[j]]
        out.append([means[j][a] + sum(L[a][b] * z[b] for b in range(a + 1)) for a in range(len(z))])
        labels.append(j)
    return out, labels
