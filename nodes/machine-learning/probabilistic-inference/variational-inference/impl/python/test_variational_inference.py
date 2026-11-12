# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-inference/. The authors are listed in prov/63JY8R.jsonl.

import math
import random

from variational_inference import (
    cavi_gaussian_2d,
    cavi_normal_gamma,
    cavi_step_trace,
    digamma,
    elbo_normal_gamma,
    exact_posterior_normal_gamma,
    update_q_mu,
    update_q_tau,
)

XS = [1.2, 2.3, 1.8, 2.9, 1.8]
PRIOR = (0.0, 1.0, 1.0, 1.0)  # mu0, lam0, a0, b0


def test_digamma_known_values():
    assert abs(digamma(1.0) + 0.5772156649015329) < 1e-9
    assert abs(digamma(0.5) + 1.9635100260214235) < 1e-9
    assert abs(digamma(10.0) - 2.251752589066721) < 1e-9


def test_updates_match_bishop_closed_forms():
    # One sweep from E[tau] = 10, by hand: m = 10/6, l = 6 * 10,
    # a = 1 + 6/2 = 4, b = 1 + (1.62 + 5 * (2 - 10/6)^2 + 5/60 + (10/6)^2 + 1/60) / 2.
    m, l = update_q_mu(XS, PRIOR, 10.0)
    assert abs(m - 10 / 6) < 1e-12 and abs(l - 60.0) < 1e-12
    a, b = update_q_tau(XS, PRIOR, m, l)
    s = sum((x - m) ** 2 for x in XS)
    assert a == 4.0
    assert abs(b - (1 + 0.5 * (s + 5 / 60 + (10 / 6) ** 2 + 1 / 60))) < 1e-12


def test_fixed_point_against_exact_posterior():
    q, _ = cavi_normal_gamma(XS, PRIOR, e_tau0=10.0)
    m, l, a, b = q
    mu_n, lam_n, a_n, b_n = exact_posterior_normal_gamma(XS, PRIOR)
    # The CAVI mean of mu is the exact posterior mean.
    assert abs(m - mu_n) < 1e-12
    # At the fixed point E_q[tau] = a_n / b_n, the exact posterior mean of tau.
    assert abs(a / b - a_n / b_n) < 1e-10
    # q(mu) has variance 1 / (lam_n E[tau]) = b_n / (lam_n a_n), which is smaller
    # than the exact marginal variance b_n / (lam_n (a_n - 1)).
    assert abs(1 / l - b_n / (lam_n * a_n)) < 1e-10
    assert 1 / l < b_n / (lam_n * (a_n - 1))
    assert a == PRIOR[2] + (len(XS) + 1) / 2


def test_elbo_never_decreases_per_factor_update():
    for start in (0.01, 1.0, 10.0, 300.0):
        trace = cavi_step_trace(XS, PRIOR, start, 20)
        for u, v in zip(trace, trace[1:]):
            assert v >= u - 1e-12


def test_elbo_below_log_evidence():
    # log p(x) for the Normal-Gamma model in closed form.
    mu0, lam0, a0, b0 = PRIOR
    mu_n, lam_n, a_n, b_n = exact_posterior_normal_gamma(XS, PRIOR)
    n = len(XS)
    log_px = (math.lgamma(a_n) - math.lgamma(a0) + a0 * math.log(b0) - a_n * math.log(b_n)
              + 0.5 * math.log(lam0 / lam_n) - 0.5 * n * math.log(2 * math.pi))
    q, hist = cavi_normal_gamma(XS, PRIOR)
    assert hist[-1] < log_px
    assert log_px - hist[-1] < 0.5


def test_random_data_sets():
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(2, 30)
        xs = [rng.gauss(rng.uniform(-3, 3), rng.uniform(0.2, 3)) for _ in range(n)]
        prior = (rng.uniform(-1, 1), rng.uniform(0.1, 5), rng.uniform(0.5, 4), rng.uniform(0.5, 4))
        q, hist = cavi_normal_gamma(xs, prior, e_tau0=rng.uniform(0.1, 10))
        mu_n, lam_n, a_n, b_n = exact_posterior_normal_gamma(xs, prior)
        assert abs(q[0] - mu_n) < 1e-9
        assert abs(q[2] / q[3] - a_n / b_n) < 1e-8 * (a_n / b_n)
        assert all(v >= u - 1e-9 for u, v in zip(hist, hist[1:]))


def test_contraction_rate_is_one_over_two_a():
    # The error in E[tau] shrinks by the factor 1 / (2a) per sweep.
    mu_n, lam_n, a_n, b_n = exact_posterior_normal_gamma(XS, PRIOR)
    target = a_n / b_n
    e = 10.0
    errs = []
    for _ in range(6):
        m, l = update_q_mu(XS, PRIOR, e)
        a, b = update_q_tau(XS, PRIOR, m, l)
        e = a / b
        errs.append(abs(e - target))
    assert abs(errs[-1] / errs[-2] - 1 / (2 * a)) < 1e-3


def test_two_dimensional_gaussian():
    mu = (1.0, -1.0)
    lam = [[1.0, 0.9], [0.9, 1.0]]
    path, var = cavi_gaussian_2d(mu, lam, sweeps=200)
    assert abs(path[-1][0] - 1.0) < 1e-9 and abs(path[-1][1] + 1.0) < 1e-9
    # The exact marginal variance is (lam^-1)_11 = 1 / (1 - 0.81); q gives 1 / lam_11 = 1.
    assert var == (1.0, 1.0)
    assert var[0] < 1 / (1 - 0.81)


def test_elbo_function_is_finite():
    assert math.isfinite(elbo_normal_gamma(XS, PRIOR, (0.0, 1.0, 2.0, 2.0)))
