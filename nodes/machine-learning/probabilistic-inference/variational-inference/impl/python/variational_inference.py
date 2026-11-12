# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-inference/. The authors are listed in prov/63JY8R.jsonl.

"""Coordinate ascent variational inference (CAVI) on two conjugate models.

1. The univariate Gaussian with unknown mean mu and precision tau
   (Bishop 2006, Section 10.1.3):
       tau ~ Gamma(a0, b0)        (shape a0, rate b0)
       mu | tau ~ N(mu0, 1 / (lam0 tau))
       x_i | mu, tau ~ N(mu, 1 / tau), i = 1..n
   The family is q(mu, tau) = q(mu) q(tau) with q(mu) = N(m, 1/l) and
   q(tau) = Gamma(a, b). CAVI updates the two factors in turn.

2. A correlated two-dimensional Gaussian target N(mu, Lambda^-1) with a
   fully factorized q(z1) q(z2) (Bishop 2006, Section 10.1.2).
"""

import math


def digamma(x):
    """psi(x) for x > 0, by the recurrence psi(x) = psi(x + 1) - 1/x and the
    asymptotic series for x >= 6."""
    acc = 0.0
    while x < 6.0:
        acc -= 1.0 / x
        x += 1.0
    f = 1.0 / (x * x)
    series = f * (1.0 / 12 - f * (1.0 / 120 - f * (1.0 / 252 - f * (1.0 / 240 - f / 132))))
    return acc + math.log(x) - 0.5 / x - series


def elbo_normal_gamma(xs, prior, q):
    """ELBO(q) = E_q[log p(x, mu, tau)] + H(q(mu)) + H(q(tau))."""
    mu0, lam0, a0, b0 = prior
    m, l, a, b = q
    n = len(xs)
    e_tau = a / b
    e_log_tau = digamma(a) - math.log(b)
    sq = sum((x - m) ** 2 for x in xs) + n / l
    lik = 0.5 * n * (e_log_tau - math.log(2 * math.pi)) - 0.5 * e_tau * sq
    pmu = 0.5 * (math.log(lam0) + e_log_tau - math.log(2 * math.pi)) - 0.5 * lam0 * e_tau * ((m - mu0) ** 2 + 1 / l)
    ptau = a0 * math.log(b0) - math.lgamma(a0) + (a0 - 1) * e_log_tau - b0 * e_tau
    h_mu = 0.5 * math.log(2 * math.pi * math.e / l)
    h_tau = a - math.log(b) + math.lgamma(a) + (1 - a) * digamma(a)
    return lik + pmu + ptau + h_mu + h_tau


def update_q_mu(xs, prior, e_tau):
    """The optimal q(mu) given q(tau): Bishop (10.26) and (10.27)."""
    mu0, lam0, _, _ = prior
    n = len(xs)
    m = (lam0 * mu0 + sum(xs)) / (lam0 + n)
    l = (lam0 + n) * e_tau
    return m, l


def update_q_tau(xs, prior, m, l):
    """The optimal q(tau) given q(mu): Bishop (10.29) and (10.30)."""
    mu0, lam0, a0, b0 = prior
    n = len(xs)
    a = a0 + (n + 1) / 2
    b = b0 + 0.5 * (sum((x - m) ** 2 for x in xs) + n / l + lam0 * ((m - mu0) ** 2 + 1 / l))
    return a, b


def cavi_normal_gamma(xs, prior, e_tau0=1.0, tol=1e-12, max_iter=1000):
    """Run CAVI from E[tau] = e_tau0. Return the final q = (m, l, a, b) and the
    ELBO after each full sweep (the first value is after the first sweep)."""
    e_tau = e_tau0
    history = []
    q = None
    for _ in range(max_iter):  # @line L1
        # The two blocks are mu and tau (the loop of L2).  # @line L2
        m, l = update_q_mu(xs, prior, e_tau)  # @line L3
        a, b = update_q_tau(xs, prior, m, l)
        q = (m, l, a, b)
        history.append(elbo_normal_gamma(xs, prior, q))  # @line L4
        new_e_tau = a / b
        done = abs(new_e_tau - e_tau) <= tol * max(1.0, abs(e_tau))
        e_tau = new_e_tau
        if done:  # @line L5
            break
    return q, history  # @line L6


def cavi_step_trace(xs, prior, e_tau0, sweeps):
    """ELBO after each single factor update, to check that no update lowers it.
    The first update of q(mu) needs a starting q(tau); we use Gamma(1, 1/e_tau0)."""
    a, b = 1.0, 1.0 / e_tau0
    trace = []
    m, l = update_q_mu(xs, prior, a / b)
    trace.append(elbo_normal_gamma(xs, prior, (m, l, a, b)))
    for _ in range(sweeps):
        a, b = update_q_tau(xs, prior, m, l)
        trace.append(elbo_normal_gamma(xs, prior, (m, l, a, b)))
        m, l = update_q_mu(xs, prior, a / b)
        trace.append(elbo_normal_gamma(xs, prior, (m, l, a, b)))
    return trace


def exact_posterior_normal_gamma(xs, prior):
    """The exact Normal-Gamma posterior (mu_n, lam_n, a_n, b_n)."""
    mu0, lam0, a0, b0 = prior
    n = len(xs)
    xbar = sum(xs) / n
    mu_n = (lam0 * mu0 + n * xbar) / (lam0 + n)
    lam_n = lam0 + n
    a_n = a0 + n / 2
    b_n = b0 + 0.5 * sum((x - xbar) ** 2 for x in xs) + lam0 * n * (xbar - mu0) ** 2 / (2 * (lam0 + n))
    return mu_n, lam_n, a_n, b_n


def cavi_gaussian_2d(mu, lam, m0=(0.0, 0.0), sweeps=100):
    """Factorized q(z1) q(z2) for the target N(mu, lam^-1), with lam the 2x2
    precision matrix. Each q(z_j) is N(m_j, 1 / lam[j][j]). Returns the means
    after each sweep and the fixed variances."""
    m1, m2 = m0
    path = []
    for _ in range(sweeps):
        m1 = mu[0] - lam[0][1] / lam[0][0] * (m2 - mu[1])
        m2 = mu[1] - lam[1][0] / lam[1][1] * (m1 - mu[0])
        path.append((m1, m2))
    return path, (1 / lam[0][0], 1 / lam[1][1])
