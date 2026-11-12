# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-autoencoder/. The authors are listed in prov/GZ4VWM.jsonl.

"""A variational autoencoder with a linear Gaussian encoder and decoder (Kingma and Welling 2014).

Generative model: z ~ N(0, I_k), x | z ~ N(C z + c, s2 I_d) with s2 = exp(tau).
Encoder:          q(z | x) = N(mu, diag(exp(l))), mu = A x + a, l = B x + b (log variances).
ELBO(x) = E_q[log p(x | z)] - KL(q(z | x) || p(z)).
The estimate uses the reparameterization z = mu + exp(l/2) * eps with eps ~ N(0, I), and the
closed form KL = -1/2 sum_j (1 + l_j - mu_j^2 - exp(l_j)) (Kingma and Welling 2014, Appendix B).
Gradients are written out by hand (backpropagation through the reparameterization).
Training uses Adam (Kingma and Ba 2015) on minibatches.
"""

import math

LOG2PI = math.log(2.0 * math.pi)


def init_params(d, k, rng, scale=0.1):
    return {
        "A": [[rng.gauss(0.0, scale) for _ in range(d)] for _ in range(k)],
        "a": [0.0] * k,
        "B": [[0.0] * d for _ in range(k)],
        "b": [0.0] * k,
        "C": [[rng.gauss(0.0, scale) for _ in range(k)] for _ in range(d)],
        "c": [0.0] * d,
        "tau": [0.0],
    }


def _mv(m, v):
    return [sum(x * y for x, y in zip(row, v)) for row in m]


def encode(p, x):
    """Return (mu, log variances) of q(z | x)."""
    mu = [m + a for m, a in zip(_mv(p["A"], x), p["a"])]
    lv = [m + b for m, b in zip(_mv(p["B"], x), p["b"])]
    return mu, lv


def kl_diag_gaussian(mu, lv):
    """KL(N(mu, diag(exp(lv))) || N(0, I)) = -1/2 sum (1 + lv - mu^2 - exp(lv))."""
    return -0.5 * sum(1.0 + l - m * m - math.exp(l) for m, l in zip(mu, lv))


def log_normal_diag(z, mu, lv):
    return -0.5 * sum(LOG2PI + l + (zi - m) ** 2 / math.exp(l) for zi, m, l in zip(z, mu, lv))


def elbo_estimate(p, x, eps):
    """One-sample reparameterized ELBO: log p(x | mu + sigma eps) - KL (closed form)."""
    mu, lv = encode(p, x)
    z = [m + math.exp(l / 2.0) * e for m, l, e in zip(mu, lv, eps)]
    s2 = math.exp(p["tau"][0])
    r = [xi - cz - ci for xi, cz, ci in zip(x, _mv(p["C"], z), p["c"])]
    rec = -0.5 * len(x) * (LOG2PI + p["tau"][0]) - sum(v * v for v in r) / (2.0 * s2)
    return rec - kl_diag_gaussian(mu, lv)


def elbo_gradient(p, x, eps):
    """Gradient of elbo_estimate(p, x, eps) with respect to every parameter (same keys as p)."""
    d, k = len(x), len(p["a"])
    mu, lv = encode(p, x)
    sig = [math.exp(l / 2.0) for l in lv]
    z = [m + s * e for m, s, e in zip(mu, sig, eps)]
    s2 = math.exp(p["tau"][0])
    r = [xi - cz - ci for xi, cz, ci in zip(x, _mv(p["C"], z), p["c"])]
    gz = [sum(p["C"][i][j] * r[i] for i in range(d)) / s2 for j in range(k)]
    gmu = [g - m for g, m in zip(gz, mu)]
    glv = [0.5 * g * s * e - 0.5 * (math.exp(l) - 1.0) for g, s, e, l in zip(gz, sig, eps, lv)]
    return {
        "A": [[gmu[j] * xi for xi in x] for j in range(k)],
        "a": gmu,
        "B": [[glv[j] * xi for xi in x] for j in range(k)],
        "b": glv,
        "C": [[r[i] * z[j] / s2 for j in range(k)] for i in range(d)],
        "c": [v / s2 for v in r],
        "tau": [-0.5 * d + sum(v * v for v in r) / (2.0 * s2)],
    }


def elbo_exact(p, x):
    """The ELBO with the expectation over q done in closed form (possible because the model is linear)."""
    d = len(x)
    mu, lv = encode(p, x)
    s2 = math.exp(p["tau"][0])
    r = [xi - cz - ci for xi, cz, ci in zip(x, _mv(p["C"], mu), p["c"])]
    spread = sum(math.exp(lv[j]) * sum(p["C"][i][j] ** 2 for i in range(d)) for j in range(len(mu)))
    rec = -0.5 * d * (LOG2PI + p["tau"][0]) - (sum(v * v for v in r) + spread) / (2.0 * s2)
    return rec - kl_diag_gaussian(mu, lv)


def _cholesky(m):
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = m[i][j] - sum(low[i][t] * low[j][t] for t in range(j))
            low[i][j] = math.sqrt(s) if i == j else s / low[j][j]
    return low


def log_marginal(p, x):
    """Exact log p(x) = log N(x; c, C C^T + s2 I) of the linear Gaussian decoder."""
    d, k = len(x), len(p["a"])
    s2 = math.exp(p["tau"][0])
    cov = [[sum(p["C"][i][t] * p["C"][j][t] for t in range(k)) + (s2 if i == j else 0.0) for j in range(d)] for i in range(d)]
    low = _cholesky(cov)
    r = [xi - ci for xi, ci in zip(x, p["c"])]
    y = []
    for i in range(d):  # forward substitution L y = r
        y.append((r[i] - sum(low[i][t] * y[t] for t in range(i))) / low[i][i])
    logdet = 2.0 * sum(math.log(low[i][i]) for i in range(d))
    return -0.5 * (d * LOG2PI + logdet + sum(v * v for v in y))


def train(data, k, rng, steps=3000, batch=16, lr=0.01, fixed_tau=None):
    """Maximize the mean ELBO by Adam on one-sample reparameterized estimates. Returns the parameters."""
    d = len(data[0])
    p = init_params(d, k, rng)
    if fixed_tau is not None:
        p["tau"] = [fixed_tau]
    m = {key: _zeros_like(v) for key, v in p.items()}
    v = {key: _zeros_like(val) for key, val in p.items()}
    b1, b2, small = 0.9, 0.999, 1e-8
    for t in range(1, steps + 1):
        total = {key: _zeros_like(val) for key, val in p.items()}
        for _ in range(batch):
            x = data[rng.randrange(len(data))]
            g = elbo_gradient(p, x, [rng.gauss(0.0, 1.0) for _ in range(k)])
            for key in total:
                _axpy(total[key], g[key], 1.0 / batch)
        if fixed_tau is not None:
            total["tau"] = [0.0]
        for key in p:
            _adam(p[key], total[key], m[key], v[key], lr, b1, b2, small, t)
    return p


def _zeros_like(v):
    return [_zeros_like(e) for e in v] if isinstance(v[0], list) else [0.0] * len(v)


def _axpy(acc, g, scale):
    for i in range(len(acc)):
        if isinstance(acc[i], list):
            _axpy(acc[i], g[i], scale)
        else:
            acc[i] += scale * g[i]


def _adam(p, g, m, v, lr, b1, b2, small, t):
    """One Adam ascent step (we maximize the ELBO)."""
    for i in range(len(p)):
        if isinstance(p[i], list):
            _adam(p[i], g[i], m[i], v[i], lr, b1, b2, small, t)
        else:
            m[i] = b1 * m[i] + (1.0 - b1) * g[i]
            v[i] = b2 * v[i] + (1.0 - b2) * g[i] * g[i]
            p[i] += lr * (m[i] / (1.0 - b1 ** t)) / (math.sqrt(v[i] / (1.0 - b2 ** t)) + small)
