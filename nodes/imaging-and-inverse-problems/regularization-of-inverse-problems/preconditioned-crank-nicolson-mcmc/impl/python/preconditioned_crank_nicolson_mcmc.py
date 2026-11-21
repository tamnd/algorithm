# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preconditioned-crank-nicolson-mcmc/. The authors are listed in prov/63HRT4.jsonl.
"""Preconditioned Crank-Nicolson (pCN) MCMC.

Target: the posterior mu^y with d mu^y / d mu_0 (u) proportional to
exp(-Phi(u)), where mu_0 = N(m0, C) is a Gaussian prior and Phi is the
negative log-likelihood (the data misfit). The proposal

    v = m0 + sqrt(1 - beta^2) (u - m0) + beta xi,   xi ~ N(0, C),

leaves mu_0 invariant and is reversible with respect to it, so the
Metropolis-Hastings acceptance probability is min(1, exp(Phi(u) - Phi(v))).
The prior density never appears.
"""

import math

from imgla import cholesky, matvec


def gaussian_sampler(cov):
    """Return a function rng -> xi with xi ~ N(0, cov), using a Cholesky factor."""
    low = cholesky(cov)
    n = len(cov)

    def draw(rng):
        return matvec(low, [rng.gauss(0.0, 1.0) for _ in range(n)])

    return draw


def diagonal_sampler(variances):
    """Return a function rng -> xi with independent N(0, variances[k]) entries."""
    sd = [math.sqrt(c) for c in variances]

    def draw(rng):
        return [s * rng.gauss(0.0, 1.0) for s in sd]

    return draw


def pcn(phi, draw_prior, u0, beta, steps, rng, m0=None):
    """Run pCN for the given number of steps.

    phi: function u -> Phi(u), the negative log-likelihood.
    draw_prior: function rng -> xi ~ N(0, C).
    Returns (chain, acceptance_rate); chain[k] is the state after step k + 1.
    """
    if not 0.0 < beta <= 1.0:
        raise ValueError("beta must be in (0, 1]")
    n = len(u0)
    if m0 is None:
        m0 = [0.0] * n
    rho = math.sqrt(1.0 - beta * beta)
    u = list(u0)
    phi_u = phi(u)  # @line L1
    chain = []
    accepted = 0
    for _ in range(steps):  # @line L2
        xi = draw_prior(rng)  # @line L3
        v = [m + rho * (ui - m) + beta * x for m, ui, x in zip(m0, u, xi)]  # @line L4
        phi_v = phi(v)  # @line L5
        if math.log(1.0 - rng.random()) < phi_u - phi_v:  # @line L6
            u, phi_u = v, phi_v  # @line L7
            accepted += 1
        chain.append(u)  # @line L8
    return chain, accepted / steps  # @line L9


def random_walk_metropolis(phi, prior_precision_diag, u0, beta, steps, rng, draw_prior):
    """Random-walk Metropolis with proposal v = u + beta xi, xi ~ N(0, C), for a
    centred Gaussian prior with diagonal covariance (given by its inverse
    diagonal). Used only for comparison with pCN."""
    u = list(u0)

    def log_target(w):
        return -phi(w) - 0.5 * sum(p * wi * wi for p, wi in zip(prior_precision_diag, w))

    lu = log_target(u)
    chain = []
    accepted = 0
    for _ in range(steps):
        xi = draw_prior(rng)
        v = [ui + beta * x for ui, x in zip(u, xi)]
        lv = log_target(v)
        if math.log(1.0 - rng.random()) < lv - lu:
            u, lu = v, lv
            accepted += 1
        chain.append(u)
    return chain, accepted / steps


def linear_gaussian_misfit(a, y, sigma):
    """Phi(u) = ||A u - y||^2 / (2 sigma^2)."""

    def phi(u):
        r = matvec(a, u)
        return sum((ri - yi) ** 2 for ri, yi in zip(r, y)) / (2.0 * sigma * sigma)

    return phi


def mean_and_covariance(chain):
    """Sample mean and sample covariance (divisor N - 1) of a list of vectors."""
    k = len(chain)
    n = len(chain[0])
    mean = [sum(c[i] for c in chain) / k for i in range(n)]
    cov = [[sum((c[i] - mean[i]) * (c[j] - mean[j]) for c in chain) / (k - 1) for j in range(n)] for i in range(n)]
    return mean, cov
