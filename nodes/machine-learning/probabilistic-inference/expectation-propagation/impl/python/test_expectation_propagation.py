# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-propagation/. The authors are listed in prov/6W6NCV.jsonl.

import math
import random

from expectation_propagation import (clutter_data, ep_clutter, ep_sites, integrate_moments, log_posterior, normal_pdf,
                                     tilted_moments)

W, A, B = 0.5, 10.0, 100.0


def data(seed, n=20):
    return clutter_data(n, 2.0, W, A, random.Random(seed))


def exact_moments(xs, w=W):
    return integrate_moments(lambda t: log_posterior(t, xs, w, A, B), -20.0, 20.0, 40000)


def test_mean_matches_the_numerically_integrated_posterior():
    for seed in (0, 2, 3, 4):
        xs = data(seed)
        m, v, _, ok, skipped = ep_clutter(xs)
        em, ev = exact_moments(xs)
        assert ok and skipped == 0
        assert abs(m - em) < 1e-3
        assert abs(v - ev) / ev < 0.1


def test_page_example():
    xs = data(0)
    m, v, sweeps, ok, _ = ep_clutter(xs)
    em, ev = exact_moments(xs)
    assert ok and sweeps == 13
    assert (round(m, 4), round(v, 4)) == (2.0146, 0.2561)
    assert (round(em, 4), round(ev, 4)) == (2.0145, 0.2503)


def test_no_clutter_is_exact():
    xs = data(5)
    m, v, sweeps, ok, _ = ep_clutter(xs, w=0.0)
    prec = 1 / B + len(xs)
    assert ok and abs(v - 1 / prec) < 1e-12 and abs(m - sum(xs) / prec) < 1e-12
    assert sweeps == 2  # the second sweep only confirms the first


def test_update_is_moment_matching():
    rng = random.Random(7)
    for _ in range(5):
        x, m_c, v_c = rng.uniform(-6, 6), rng.uniform(-3, 3), rng.uniform(0.2, 4.0)

        def log_tilted(t):
            return math.log((1 - W) * normal_pdf(x, t, 1.0) + W * normal_pdf(x, 0.0, A)) - \
                0.5 * (t - m_c) ** 2 / v_c - 0.5 * math.log(2 * math.pi * v_c)
        z, mean, var = tilted_moments(x, W, A, m_c, v_c)
        im, iv = integrate_moments(log_tilted, m_c - 30, m_c + 30, 60000)
        assert abs(mean - im) < 1e-7 and abs(var - iv) < 1e-7
        h = 60.0 / 60000
        iz = sum(math.exp(log_tilted(m_c - 30 + k * h)) for k in range(60001)) * h
        assert abs(z - iz) < 1e-6


def test_fixed_point_matches_every_tilted_distribution():
    xs = data(3)
    tau, nu, prec, pm = ep_sites(xs)
    m, v = pm / prec, 1 / prec
    for i, x in enumerate(xs):
        prec_c, pm_c = prec - tau[i], pm - nu[i]
        _, tm, tv = tilted_moments(x, W, A, pm_c / prec_c, 1 / prec_c)
        assert abs(tm - m) < 1e-9 and abs(tv - v) < 1e-9


def test_no_convergence_on_a_bimodal_posterior():
    xs = data(1)
    _, ev = exact_moments(xs)
    assert ev > 2.5  # clutter on both sides: a wide posterior with several bumps
    for damping in (0.0, 0.5):
        _, _, _, ok, skipped = ep_clutter(xs, damping=damping, max_sweeps=500)
        assert not ok and skipped > 0
