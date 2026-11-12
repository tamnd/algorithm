# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-prior/. The authors are listed in prov/6PNECN.jsonl.

import math
from fractions import Fraction as F

from conjugate_prior import (
    beta_binomial,
    dirichlet_multinomial,
    exponential_family_conjugate,
    gamma_poisson,
    normal_inverse_gamma,
    normal_known_variance,
)

XS = [F(21, 10), F(13, 10), F(3), F(26, 10)]


def grid_moments(logdens, lo, hi, m=20000):
    """Mean and variance of the density exp(logdens) on (lo, hi) by the midpoint rule."""
    h = (hi - lo) / m
    pts = [lo + (i + 0.5) * h for i in range(m)]
    lw = [logdens(t) for t in pts]
    top = max(lw)
    w = [math.exp(v - top) for v in lw]
    z = sum(w)
    mean = sum(t * x for t, x in zip(pts, w)) / z
    var = sum((t - mean) ** 2 * x for t, x in zip(pts, w)) / z
    return mean, var


def test_beta_binomial_against_grid() -> None:
    data = [1, 1, 0, 1, 1, 0, 1, 1]
    a, b = beta_binomial(F(2), F(2), data)
    assert (a, b) == (8, 4)
    s, f = 6, 2
    mean, var = grid_moments(lambda t: (2 - 1 + s) * math.log(t) + (2 - 1 + f) * math.log(1 - t), 0.0, 1.0)
    assert abs(mean - float(a / (a + b))) < 1e-6
    assert abs(var - float(a * b / ((a + b) ** 2 * (a + b + 1)))) < 1e-6


def test_gamma_poisson_against_grid() -> None:
    data = [3, 1, 4, 1, 5]
    alpha, beta = gamma_poisson(F(2), F(1), data)
    assert (alpha, beta) == (16, 6)

    def logpost(lam):
        prior = (2 - 1) * math.log(lam) - 1 * lam
        lik = sum(x * math.log(lam) - lam - math.lgamma(x + 1) for x in data)
        return prior + lik

    mean, var = grid_moments(logpost, 0.0, 12.0)
    assert abs(mean - float(alpha / beta)) < 1e-6
    assert abs(var - float(alpha / beta ** 2)) < 1e-6


def test_normal_known_variance_against_grid() -> None:
    mu_n, tau_n_sq = normal_known_variance(F(0), F(1), F(4), XS)
    assert (mu_n, tau_n_sq) == (F(9, 8), F(1, 2))
    xs = [float(x) for x in XS]

    def logpost(t):
        return -t * t / 2 - sum((x - t) ** 2 for x in xs) / 8

    mean, var = grid_moments(logpost, -8.0, 10.0)
    assert abs(mean - 1.125) < 1e-6 and abs(var - 0.5) < 1e-6


def test_normal_inverse_gamma_against_2d_grid() -> None:
    mu0, k0, a0, b0 = F(0), F(1), F(2), F(2)
    mu_n, k_n, a_n, b_n = normal_inverse_gamma(mu0, k0, a0, b0, XS)
    assert (mu_n, k_n, a_n, b_n) == (F(9, 5), F(5), F(4), F(483, 100))
    xs = [float(x) for x in XS]
    # joint posterior of (mu, s2) on a grid; the exact marginal moments are
    # E[mu] = mu_n, E[s2] = b_n / (a_n - 1), Var[mu] = b_n / ((a_n - 1) k_n)
    m_mu, m_s = 300, 300
    mus = [-3 + 8 * (i + 0.5) / m_mu for i in range(m_mu)]
    s2s = [0.02 + 30 * (j + 0.5) / m_s for j in range(m_s)]
    tot = e_mu = e_s2 = e_mu2 = 0.0
    for s2 in s2s:
        log_prior_s2 = -(2 + 1) * math.log(s2) - 2 / s2
        for mu in mus:
            lp = log_prior_s2 - 0.5 * math.log(s2) - mu * mu / (2 * s2)
            lp += sum(-0.5 * math.log(s2) - (x - mu) ** 2 / (2 * s2) for x in xs)
            w = math.exp(lp)
            tot += w
            e_mu += w * mu
            e_mu2 += w * mu * mu
            e_s2 += w * s2
    e_mu, e_mu2, e_s2 = e_mu / tot, e_mu2 / tot, e_s2 / tot
    assert abs(e_mu - float(mu_n)) < 2e-3
    assert abs(e_s2 - float(b_n / (a_n - 1))) / float(b_n / (a_n - 1)) < 2e-2
    assert abs((e_mu2 - e_mu ** 2) - float(b_n / ((a_n - 1) * k_n))) < 1e-2


def test_dirichlet_multinomial_against_2d_grid() -> None:
    post = dirichlet_multinomial([F(1), F(1), F(1)], [5, 2, 3])
    assert post == [6, 3, 4]
    m = 400
    tot = e1 = e2 = 0.0
    for i in range(m):
        p1 = (i + 0.5) / m
        for j in range(m):
            p2 = (j + 0.5) / m
            p3 = 1 - p1 - p2
            if p3 <= 0:
                continue
            w = p1 ** 5 * p2 ** 2 * p3 ** 3
            tot += w
            e1 += w * p1
            e2 += w * p2
    assert abs(e1 / tot - 6 / 13) < 3e-3
    assert abs(e2 / tot - 3 / 13) < 3e-3


def test_generic_exponential_family_matches_special_cases() -> None:
    # Bernoulli: T(x) = x, A(eta) = log(1 + e^eta). The prior exp(eta chi - nu A)
    # on eta is Beta(chi, nu - chi) on theta = sigmoid(eta).
    data = [1, 1, 0, 1, 1, 0, 1, 1]
    chi, nu = exponential_family_conjugate([F(2)], F(4), [[x] for x in data])
    assert (chi[0], nu - chi[0]) == beta_binomial(F(2), F(2), data)
    # Poisson: T(x) = x, A(eta) = e^eta: prior on lambda = e^eta is Gamma(chi, nu).
    data = [3, 1, 4, 1, 5]
    chi, nu = exponential_family_conjugate([F(2)], F(1), [[x] for x in data])
    assert (chi[0], nu) == gamma_poisson(F(2), F(1), data)
    # Diaconis-Ylvisaker: the posterior mean of the mean parameter is (chi + sum T) / (nu + n)
    assert chi[0] / nu == F(16, 6)


def test_sequential_updates_compose() -> None:
    a = normal_inverse_gamma(F(0), F(1), F(2), F(2), XS[:2])
    b = normal_inverse_gamma(*a, XS[2:])
    assert b == normal_inverse_gamma(F(0), F(1), F(2), F(2), XS)
