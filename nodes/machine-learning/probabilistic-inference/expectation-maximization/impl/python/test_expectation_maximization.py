# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectation-maximization/. The authors are listed in prov/X3E38Q.jsonl.

import math
import random

from expectation_maximization import (DO_BATZOGLOU, coins_e_step, coins_em, coins_loglik,
                                      coins_m_step, linkage_e_step, linkage_em, linkage_loglik,
                                      linkage_m_step, linkage_mle)


def test_linkage_iterates():
    th = 0.5
    seen = []
    for _ in range(4):
        seen.append(round(th, 6))
        th = linkage_m_step(linkage_e_step(th))
    assert seen == [0.5, 0.608247, 0.624321, 0.626489]


def test_linkage_fixed_point_is_the_grid_maximum():
    th, hist = linkage_em(0.5)
    best = max(range(1, 100000), key=lambda i: linkage_loglik(i / 100000)) / 100000
    assert abs(th - best) <= 1e-5
    assert abs(th - linkage_mle()) < 1e-7
    # the rate of convergence: the error shrinks by about 0.1328 in each step
    a = 0.6
    b = linkage_m_step(linkage_e_step(a))
    c = linkage_m_step(linkage_e_step(b))
    m = linkage_mle()
    assert abs((c - m) / (b - m) - 0.1328) < 0.002


def test_linkage_from_many_starts():
    for i in range(1, 20):
        th, hist = linkage_em(i / 20)
        assert abs(th - linkage_mle()) < 1e-6
        assert all(b >= a - 1e-12 for a, b in zip(hist, hist[1:]))


def test_do_batzoglou_numbers():
    th = (0.5, 0.6, 0.5)
    th = coins_m_step(coins_e_step(th, DO_BATZOGLOU), learn_lambda=False)
    assert (round(th[1], 2), round(th[2], 2)) == (0.71, 0.58)
    for _ in range(9):
        th = coins_m_step(coins_e_step(th, DO_BATZOGLOU), learn_lambda=False)
    assert (round(th[1], 2), round(th[2], 2)) == (0.80, 0.52)


def test_monotone_log_likelihood_on_seeded_runs():
    rng = random.Random(42)
    for _ in range(30):
        pa, pb, lam = rng.uniform(0.1, 0.9), rng.uniform(0.1, 0.9), rng.uniform(0.2, 0.8)
        data = []
        while not data or sum(h for h, _ in data) in (0, sum(n for _, n in data)):
            data = []
            for _ in range(rng.randint(3, 12)):
                n = rng.randint(5, 20)
                p = pa if rng.random() < lam else pb
                data.append((sum(rng.random() < p for _ in range(n)), n))
        start = (rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.95), rng.uniform(0.05, 0.95))
        th, hist = coins_em(start, data, learn_lambda=True, eps=-1.0, max_iter=60)
        for a, b in zip(hist, hist[1:]):
            assert b >= a - 1e-9


def _grad(f, th, h=1e-6):
    g = []
    for j in range(len(th)):
        up = list(th)
        dn = list(th)
        up[j] += h
        dn[j] -= h
        g.append((f(up) - f(dn)) / (2 * h))
    return g


def test_fixed_point_is_stationary():
    th, hist = coins_em((0.5, 0.6, 0.5), DO_BATZOGLOU, learn_lambda=True)
    g = _grad(lambda t: coins_loglik(t, DO_BATZOGLOU), th)
    assert max(abs(x) for x in g) < 1e-4


def test_symmetric_start_stops_at_a_saddle():
    # With equal coins the responsibilities are 1/2, so both coins get the pooled frequency 0.66.
    th, hist = coins_em((0.5, 0.6, 0.6), DO_BATZOGLOU, learn_lambda=False)
    assert abs(th[1] - 0.66) < 1e-12 and abs(th[2] - 0.66) < 1e-12
    f = lambda a, b: coins_loglik((0.5, a, b), DO_BATZOGLOU)
    h = 1e-4
    assert abs((f(0.66 + h, 0.66) - f(0.66 - h, 0.66)) / (2 * h)) < 1e-5
    # along (1, -1) the log likelihood curves up, so this is not a maximum
    assert f(0.66 + 0.01, 0.66 - 0.01) > f(0.66, 0.66)
    best, _ = coins_em((0.5, 0.6, 0.5), DO_BATZOGLOU, learn_lambda=False)
    assert coins_loglik(best, DO_BATZOGLOU) > coins_loglik(th, DO_BATZOGLOU) + 0.4


def test_m_step_maximizes_q():
    rng = random.Random(3)
    data = DO_BATZOGLOU
    th = (0.4, 0.3, 0.8)
    resp, _ = coins_e_step(th, data)

    def q(t):
        lam, pa, pb = t
        return sum(r * (math.log(lam) + h * math.log(pa) + (n - h) * math.log(1 - pa))
                   + (1 - r) * (math.log(1 - lam) + h * math.log(pb) + (n - h) * math.log(1 - pb))
                   for r, (h, n) in zip(resp, data))

    best = coins_m_step((resp, data))
    for _ in range(500):
        other = (rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99))
        assert q(other) <= q(best) + 1e-12
