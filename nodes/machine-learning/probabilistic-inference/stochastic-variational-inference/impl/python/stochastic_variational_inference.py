# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-variational-inference/. The authors are listed in prov/MB3DWW.jsonl.

"""Stochastic variational inference (Hoffman, Blei, Wang and Paisley 2013) on a
conditionally conjugate model: a one-dimensional Gaussian mixture with K
components of unit variance and equal weights, and a prior mu_k ~ N(0, s0^2).

Global variables: the means mu_k. Local variables: the assignments z_n.
q(mu_k) = N(m_k, v_k) is kept in natural parameters lam_k = (m_k / v_k, 1 / v_k),
the coefficients of mu and -mu^2 / 2 in log q. The complete conditional of mu_k
has natural parameter (sum_n z_nk x_n, 1 / s0^2 + sum_n z_nk).
"""

import math


def mean_var(lam):
    return lam[0] / lam[1], 1.0 / lam[1]


def local_step(x, lam):
    """phi_k proportional to exp(E[mu_k] x - E[mu_k^2] / 2)."""
    logits = []
    for l in lam:
        m, v = mean_var(l)
        logits.append(m * x - 0.5 * (m * m + v))
    top = max(logits)
    w = [math.exp(a - top) for a in logits]
    s = sum(w)
    return [a / s for a in w]


def intermediate(xs, batch, lam, s0, scale):
    """lam_hat = prior + scale * sum over the batch of the expected sufficient statistics."""
    K = len(lam)
    out = [[0.0, 1.0 / s0 ** 2] for _ in range(K)]
    for n in batch:
        phi = local_step(xs[n], lam)  # @line L4
        for k in range(K):
            out[k][0] += scale * phi[k] * xs[n]
            out[k][1] += scale * phi[k]
    return out


def svi(xs, K, s0, lam0, batch_size, steps, rng, tau=1.0, kappa=0.7):
    """Run SVI. Return the global natural parameters lam."""
    N = len(xs)
    lam = [list(l) for l in lam0]  # @line L1
    for t in range(1, steps + 1):  # @line L2
        batch = rng.sample(range(N), batch_size)  # @line L3
        lam_hat = intermediate(xs, batch, lam, s0, N / batch_size)  # @line L5
        rho = (t + tau) ** (-kappa)  # @line L6
        lam = [[(1 - rho) * a + rho * b for a, b in zip(l, lh)] for l, lh in zip(lam, lam_hat)]  # @line L7
    return lam  # @line L8


def cavi(xs, K, s0, lam0, tol=1e-12, max_iter=100000):
    """Batch coordinate ascent: all local steps, then the global step. Return (lam, sweeps)."""
    lam = [list(l) for l in lam0]
    for it in range(1, max_iter + 1):
        new = intermediate(xs, range(len(xs)), lam, s0, 1.0)
        delta = max(abs(a - b) for l, nl in zip(lam, new) for a, b in zip(l, nl))
        lam = new
        if delta < tol:
            return lam, it
    return lam, max_iter


def elbo(xs, lam, phis, s0):
    """The ELBO for q(mu) with natural parameters lam and fixed local factors phis."""
    K = len(lam)
    val = 0.0
    for l in lam:
        m, v = mean_var(l)
        val += -0.5 * math.log(2 * math.pi * s0 ** 2) - (m * m + v) / (2 * s0 ** 2)  # E log p(mu_k)
        val += 0.5 * math.log(2 * math.pi * math.e * v)  # H(q(mu_k))
    for x, phi in zip(xs, phis):
        for k in range(K):
            if phi[k] > 0:
                m, v = mean_var(lam[k])
                ll = -0.5 * math.log(2 * math.pi) - 0.5 * (x * x - 2 * x * m + m * m + v)
                val += phi[k] * (math.log(1.0 / K) + ll - math.log(phi[k]))
    return val


def fisher(lam_k):
    """The Fisher information of q(mu_k) in its natural parameters: the covariance
    of the sufficient statistics (mu, -mu^2 / 2) under N(m, v)."""
    m, v = mean_var(lam_k)
    return [[v, -m * v], [-m * v, m * m * v + 0.5 * v * v]]
