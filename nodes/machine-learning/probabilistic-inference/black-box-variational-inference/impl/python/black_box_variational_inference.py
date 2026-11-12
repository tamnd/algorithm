# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/black-box-variational-inference/. The authors are listed in prov/3YYRHH.jsonl.

"""Black-box variational inference (Ranganath, Gerrish and Blei 2014) with a
mean-field Gaussian family, and the reparameterization estimator for contrast.

The model is given only through a function log_p_i(z, i): the terms of
log p(x, z) that depend on z_i (its Markov blanket terms), and the whole
log p(x, z) for i = None. The test model is a
Gaussian target, log p(x, z) = -z^T L z / 2 + eta^T z + const, so that the
exact gradient of the ELBO is known.

The family is q(z) = prod_i N(z_i; mu_i, sigma_i^2) with sigma_i = exp(omega_i),
and lambda_i = (mu_i, omega_i). The score of factor i is
    d log q_i / d mu_i = (z_i - mu_i) / sigma_i^2,
    d log q_i / d omega_i = (z_i - mu_i)^2 / sigma_i^2 - 1.
"""

import math


def log_q_i(z_i, mu_i, om_i):
    s = math.exp(om_i)
    return -0.5 * math.log(2 * math.pi) - om_i - 0.5 * ((z_i - mu_i) / s) ** 2


def score_i(z_i, mu_i, om_i):
    s2 = math.exp(2 * om_i)
    u = z_i - mu_i
    return (u / s2, u * u / s2 - 1.0)


def sample_q(mu, om, rng):
    return [m + math.exp(o) * rng.gauss(0.0, 1.0) for m, o in zip(mu, om)]


def score_gradient(log_p_i, mu, om, S, rng, rao_blackwell=True, control_variate=True):
    """The BBVI estimate of the ELBO gradient from S samples, as a list of
    (d/d mu_i, d/d omega_i). With rao_blackwell, factor i uses only the Markov
    blanket terms log p_i and log q_i; without it, the whole log p - log q. With
    control_variate, the score h_i is subtracted with the coefficient
    a_i = sum Cov(f, h) / sum Var(h). The coefficient for sample s is computed
    from the other S - 1 samples, so the estimate stays unbiased."""
    n = len(mu)
    zs = [sample_q(mu, om, rng) for _ in range(S)]  # @line L3
    grad = []
    for i in range(n):
        f, h = [], []
        for z in zs:  # @line L4
            sc = score_i(z[i], mu[i], om[i])
            if rao_blackwell:
                w = log_p_i(z, i) - log_q_i(z[i], mu[i], om[i])
            else:
                w = log_p_i(z, None) - sum(log_q_i(z[k], mu[k], om[k]) for k in range(n))
            f.append((sc[0] * w, sc[1] * w))
            h.append(sc)
        if control_variate and S > 2:
            a = _leave_one_out_coefficients(f, h)  # @line L5
            g = tuple(sum(f[s][d] - a[s] * h[s][d] for s in range(S)) / S for d in range(2))  # @line L6
        else:
            g = tuple(sum(f[s][d] for s in range(S)) / S for d in range(2))
        grad.append(g)
    return grad


def _leave_one_out_coefficients(f, h):
    """a for each sample s: sum_d Cov(f_d, h_d) / sum_d Var(h_d) over the samples other than s."""
    S = len(f)
    sf = [sum(x[d] for x in f) for d in range(2)]
    sh = [sum(x[d] for x in h) for d in range(2)]
    sfh = [sum(x[d] * y[d] for x, y in zip(f, h)) for d in range(2)]
    shh = [sum(y[d] * y[d] for y in h) for d in range(2)]
    out = []
    for s in range(S):
        m = S - 1
        cov = var = 0.0
        for d in range(2):
            mf = (sf[d] - f[s][d]) / m
            mh = (sh[d] - h[s][d]) / m
            cov += (sfh[d] - f[s][d] * h[s][d]) / m - mf * mh
            var += (shh[d] - h[s][d] ** 2) / m - mh * mh
        out.append(cov / var if var > 0 else 0.0)
    return out


def reparam_gradient(grad_log_p, mu, om, S, rng):
    """The reparameterization estimate: z = mu + sigma eps, and the entropy term
    sum_i omega_i is differentiated exactly."""
    n = len(mu)
    g = [[0.0, 1.0] for _ in range(n)]
    for _ in range(S):
        eps = [rng.gauss(0.0, 1.0) for _ in range(n)]
        z = [m + math.exp(o) * e for m, o, e in zip(mu, om, eps)]
        dz = grad_log_p(z)
        for i in range(n):
            g[i][0] += dz[i] / S
            g[i][1] += dz[i] * math.exp(om[i]) * eps[i] / S
    return [tuple(x) for x in g]


def bbvi(log_p_i, n, S, steps, rng, eta=0.5, mu0=None, om0=None):
    """BBVI with AdaGrad step sizes: lambda <- lambda + eta * g / sqrt(G), with G the
    running sum of squared gradient estimates. Return (mu, omega)."""
    mu = list(mu0) if mu0 else [0.0] * n  # @line L1
    om = list(om0) if om0 else [0.0] * n
    G = [[0.0, 0.0] for _ in range(n)]
    for _ in range(steps):  # @line L2
        g = score_gradient(log_p_i, mu, om, S, rng)
        for i in range(n):  # @line L7
            for d in range(2):
                G[i][d] += g[i][d] ** 2
            mu[i] += eta * g[i][0] / math.sqrt(G[i][0] + 1e-12)
            om[i] += eta * g[i][1] / math.sqrt(G[i][1] + 1e-12)
    return mu, om  # @line L8


class GaussianTarget:
    """log p(x, z) = -z^T L z / 2 + eta^T z, up to a constant."""

    def __init__(self, L, eta):
        self.L, self.eta = L, eta

    def log_p(self, z):
        n = len(z)
        return -0.5 * sum(z[i] * self.L[i][j] * z[j] for i in range(n) for j in range(n)) + \
            sum(e * x for e, x in zip(self.eta, z))

    def log_p_i(self, z, i):
        """The terms that hold z_i; with i = None, the whole log p."""
        if i is None:
            return self.log_p(z)
        L = self.L
        return -0.5 * L[i][i] * z[i] ** 2 - z[i] * sum(L[i][j] * z[j] for j in range(len(z)) if j != i) + \
            self.eta[i] * z[i]

    def grad_log_p(self, z):
        n = len(z)
        return [self.eta[i] - sum(self.L[i][j] * z[j] for j in range(n)) for i in range(n)]

    def exact_gradient(self, mu, om):
        """d ELBO / d mu = eta - L mu, d ELBO / d omega_i = 1 - L_ii sigma_i^2."""
        n = len(mu)
        return [(self.eta[i] - sum(self.L[i][j] * mu[j] for j in range(n)), 1.0 - self.L[i][i] * math.exp(2 * om[i]))
                for i in range(n)]

    def elbo(self, mu, om):
        n = len(mu)
        e = -0.5 * (sum(mu[i] * self.L[i][j] * mu[j] for i in range(n) for j in range(n)) +
                    sum(self.L[i][i] * math.exp(2 * om[i]) for i in range(n)))
        e += sum(a * b for a, b in zip(self.eta, mu))
        return e + sum(om) + 0.5 * n * (1 + math.log(2 * math.pi))
