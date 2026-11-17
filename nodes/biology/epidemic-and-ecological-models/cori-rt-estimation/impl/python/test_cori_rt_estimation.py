# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cori-rt-estimation/. The authors are listed in prov/FC6CRV.jsonl.

import math
import random

from biostoch import chi2_sf
from cori_rt_estimation import estimate, gamma_cdf, gamma_quantile, simulate, total_infectiousness

W = [0, 0.2, 0.5, 0.3]
INC = [10, 4, 8, 9, 11, 14, 15, 21, 24, 16, 18, 15, 13]


def test_total_infectiousness_by_hand():
    lam = total_infectiousness(INC, W)
    assert lam[:5] == [0.0, 2.0, 5.8, 6.6, 7.0]
    # Day 6: 0.2 * 11 + 0.5 * 9 + 0.3 * 8
    assert abs(lam[5] - 9.1) < 1e-12


def test_window_posterior_by_hand():
    first = estimate(INC, W, tau=4, a=1.0, b=5.0)[0]
    assert (first.t_start, first.t_end) == (2, 5)
    assert first.shape == 1 + 4 + 8 + 9 + 11
    assert abs(first.rate - (0.2 + 2.0 + 5.8 + 6.6 + 7.0)) < 1e-12
    assert abs(first.mean - 33 / 21.6) < 1e-12
    assert abs(first.cv - 1 / math.sqrt(33)) < 1e-12


def test_posterior_matches_grid_integration():
    a, b, tau = 1.0, 5.0, 4
    lam = total_infectiousness(INC, W)
    est = estimate(INC, W, tau=tau, a=a, b=b, probs=(0.025, 0.5, 0.975))
    for e in (est[0], est[-1]):
        days = range(e.t_start - 1, e.t_end)

        def log_post(r):
            v = (a - 1) * math.log(r) - r / b
            for d in days:
                v += INC[d] * math.log(r * lam[d]) - r * lam[d]
            return v

        n, top = 40000, 6.0
        h = top / n
        grid = [(k + 0.5) * h for k in range(n)]
        lp = [log_post(r) for r in grid]
        m = max(lp)
        dens = [math.exp(x - m) for x in lp]
        z = sum(dens)
        mean = sum(r * d for r, d in zip(grid, dens)) / z
        assert abs(mean - e.mean) < 1e-6
        acc, qi, probs, found = 0.0, 0, (0.025, 0.5, 0.975), []
        for r, d in zip(grid, dens):
            acc += d / z
            while qi < 3 and acc >= probs[qi]:
                found.append(r)
                qi += 1
        for q_grid, q in zip(found, e.quantiles):
            assert abs(q_grid - q) < 2e-3


def test_gamma_quantile():
    for p in (0.025, 0.5, 0.9):
        assert abs(gamma_quantile(p, 1.0, 2.0) + math.log(1 - p) / 2.0) < 1e-9
    q = gamma_quantile(0.975, 50.0, 10.0)
    assert abs(gamma_cdf(q, 50.0, 10.0) - 0.975) < 1e-9


def test_no_cases_gives_the_prior():
    e = estimate([0] * 10, W, tau=7, a=2.0, b=3.0)[0]
    assert e.shape == 2.0 and abs(e.rate - 1 / 3) < 1e-12


def test_simulation_based_calibration():
    # R from the prior, a fixed seed on days 1 to 5, and the window of days
    # 6 to 12. The posterior CDF at the true R must then be Uniform(0, 1).
    rng = random.Random(20261118)
    a, b, runs, bins = 2.0, 0.75, 1000, 10
    seed = [3, 5, 4, 6, 5]
    counts = [0] * bins
    for _ in range(runs):
        r = rng.gammavariate(a, b)
        inc = simulate(rng, seed, [r] * 7, W)
        (e,) = estimate(inc, W, tau=7, a=a, b=b, probs=(), first_day=6)
        u = gamma_cdf(r, e.shape, e.rate)
        counts[min(bins - 1, int(u * bins))] += 1
    stat = sum((c - runs / bins) ** 2 / (runs / bins) for c in counts)
    assert chi2_sf(stat, bins - 1) > 0.001


def test_step_change_is_recovered():
    rng = random.Random(20261118)
    w = [0, 0.05, 0.15, 0.25, 0.2, 0.15, 0.1, 0.06, 0.04]
    inc = simulate(rng, [20] * 5, [1.8] * 25 + [0.7] * 25, w)
    est = {e.t_end: e for e in estimate(inc, w, tau=7)}
    lo, _, hi = est[30].quantiles
    assert lo < 1.8 < hi
    lo, _, hi = est[55].quantiles
    assert lo < 0.7 < hi
    # A window that straddles the change gives a value in between.
    assert 0.7 < est[35].mean < 1.8
