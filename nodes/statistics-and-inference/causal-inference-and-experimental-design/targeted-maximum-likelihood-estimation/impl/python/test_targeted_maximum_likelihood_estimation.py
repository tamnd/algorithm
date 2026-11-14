# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/targeted-maximum-likelihood-estimation/. The authors are listed in prov/SKN7EC.jsonl.

import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from targeted_maximum_likelihood_estimation import (
    aipw_estimate,
    clever_covariate,
    fit_nuisances,
    tmle_ate,
    tmle_interval,
)

# The worked example of the page: the eight units of the IPW page with a binary outcome.
EX_T = [1, 1, 0, 0, 0, 1, 1, 0]
EX_Y = [1, 1, 1, 1, 1, 0, 0, 0]
EX_E = [Fr(1, 4)] * 5 + [Fr(3, 4)] * 3


def test_worked_example_linear_fluctuation_exact():
    q1, q0 = [Fr(1, 2)] * 8, [Fr(3, 4)] * 8
    assert aipw_estimate(EX_T, EX_Y, EX_E, q1, q0) == Fr(1, 3)
    r = tmle_ate(EX_T, EX_Y, EX_E, q1, q0, fluctuation="linear")
    assert r.eps == Fr(21, 256)
    assert r.q1_star[0] == Fr(53, 64) and r.q1_star[7] == Fr(39, 64)
    assert r.q0_star[0] == Fr(41, 64) and r.q0_star[7] == Fr(27, 64)
    assert (r.mu1, r.mu0, r.tau) == (Fr(191, 256), Fr(143, 256), Fr(3, 16))
    assert aipw_estimate(EX_T, EX_Y, EX_E, r.q1_star, r.q0_star) == Fr(3, 16)


def test_worked_example_logistic_fluctuation():
    e = [float(v) for v in EX_E]
    r = tmle_ate(EX_T, EX_Y, e, [0.5] * 8, [0.75] * 8)
    assert abs(r.eps - 0.3735756) < 1e-6
    assert abs(r.tau - 0.1892179) < 1e-6
    assert abs(aipw_estimate(EX_T, EX_Y, e, r.q1_star, r.q0_star) - r.tau) < 1e-12


def test_linear_fluctuation_solves_score_exactly():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(2, 10)
        t = [rng.randint(0, 1) for _ in range(n)]
        if len(set(t)) < 2:
            t[0], t[1] = 0, 1
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        e = [Fr(rng.randint(1, 9), 10) for _ in range(n)]
        q1 = [Fr(rng.randint(-9, 9), 2) for _ in range(n)]
        q0 = [Fr(rng.randint(-9, 9), 3) for _ in range(n)]
        r = tmle_ate(t, y, e, q1, q0, fluctuation="linear")
        h = clever_covariate(t, e)
        resid = [yi - (a if ti == 1 else b) for ti, yi, a, b in zip(t, y, r.q1_star, r.q0_star)]
        assert sum(hi * ri for hi, ri in zip(h, resid)) == 0
        assert r.tau == aipw_estimate(t, y, e, r.q1_star, r.q0_star)


def expit(z):
    return 1 / (1 + math.exp(-z))


TRUE_ATE = math.log((1 + math.e) / 2) - 0.5  # integral over [0, 1] of expit(x) - expit(-1 + 2x)


def simulate(n, rng):
    """X uniform on [0, 1]; e(x) = expit(-2 + 4x); Pr[Y = 1 | T, X] = expit(-1 + 2x + T(1 - x))."""
    x, t, y = [], [], []
    for _ in range(n):
        xi = rng.random()
        ti = 1 if rng.random() < expit(-2 + 4 * xi) else 0
        yi = 1 if rng.random() < expit(-1 + 2 * xi + ti * (1 - xi)) else 0
        x.append(xi), t.append(ti), y.append(yi)
    return x, t, y


def test_logistic_score_equation_and_plug_in_identity():
    rng = random.Random(8)
    x, t, y = simulate(800, rng)
    e, q1, q0 = fit_nuisances(x, t, y, lambda v: [1.0], lambda v: [1.0, v])
    r = tmle_ate(t, y, e, q1, q0)
    h = clever_covariate(t, e)
    score = sum(hi * (yi - (a if ti == 1 else b)) for hi, yi, ti, a, b in zip(h, y, t, r.q1_star, r.q0_star))
    assert abs(score) < 1e-8
    assert abs(r.tau - aipw_estimate(t, y, e, r.q1_star, r.q0_star)) < 1e-10
    assert all(0 < v < 1 for v in r.q1_star + r.q0_star)


def test_constant_propensity_needs_no_update():
    """With a constant propensity, H is constant in each arm, and a logistic outcome fit with an
    intercept in each arm already solves the score equation: eps = 0 and TMLE = AIPW = plug-in."""
    rng = random.Random(12)
    x, t, y = simulate(500, rng)
    e, q1, q0 = fit_nuisances(x, t, y, lambda v: [1.0, v], lambda v: [1.0])
    r = tmle_ate(t, y, e, q1, q0)
    assert abs(r.eps) < 1e-9
    plug = sum(a - b for a, b in zip(q1, q0)) / len(t)
    assert abs(r.tau - plug) < 1e-9 and abs(r.tau - aipw_estimate(t, y, e, q1, q0)) < 1e-9


def test_agreement_with_aipw_and_double_robustness():
    """r = 30 samples of n = 1000 (seed 2026). Stated tolerance: in every sample, |TMLE - AIPW| < 0.01
    on the same nuisance fits; the mean over samples is within 4 SE + 0.005 of the true ATE when
    either model is right."""
    rng = random.Random(2026)
    full = lambda v: [1.0, v]
    const = lambda v: [1.0]
    configs = {"both": (full, full), "outcome wrong": (const, full), "propensity wrong": (full, const)}
    est = {k: [] for k in configs}
    r = 30
    for _ in range(r):
        x, t, y = simulate(1000, rng)
        for name, (of, pf) in configs.items():
            e, q1, q0 = fit_nuisances(x, t, y, of, pf)
            res = tmle_ate(t, y, e, q1, q0)
            assert abs(res.tau - aipw_estimate(t, y, e, q1, q0)) < 0.01, name
            est[name].append(res.tau)
    for name, v in est.items():
        assert abs(statistics.mean(v) - TRUE_ATE) < 4 * statistics.stdev(v) / math.sqrt(r) + 0.005, name


def test_stays_in_range_near_positivity_limit():
    t, y, e, q = [1, 1, 0, 0], [1, 0, 0, 1], [0.05, 0.5, 0.5, 0.5], [0.2] * 4
    a = aipw_estimate(t, y, e, q, q)
    assert abs(a - 3.6) < 1e-12  # AIPW: E[Y(1)] estimated as 4.1 for a binary outcome
    r = tmle_ate(t, y, e, q, q)
    assert 0 < r.mu1 < 1 and 0 < r.mu0 < 1 and -1 < r.tau < 1
    assert abs(r.tau - 0.26994310) < 1e-7


def test_bounds_scaling_matches_rescaled_data():
    rng = random.Random(3)
    t = [rng.randint(0, 1) for _ in range(50)]
    t[0], t[1] = 0, 1
    y01 = [rng.random() for _ in range(50)]
    e = [0.2 + 0.6 * rng.random() for _ in range(50)]
    q1 = [0.1 + 0.8 * rng.random() for _ in range(50)]
    q0 = [0.1 + 0.8 * rng.random() for _ in range(50)]
    base = tmle_ate(t, y01, e, q1, q0)
    a, b = -3.0, 7.0
    sc = lambda v: a + (b - a) * v
    scaled = tmle_ate(t, [sc(v) for v in y01], e, [sc(v) for v in q1], [sc(v) for v in q0], bounds=(a, b))
    assert abs(scaled.tau - 10 * base.tau) < 1e-9 and abs(scaled.se - 10 * base.se) < 1e-9
    lo, hi = tmle_interval(scaled)
    assert lo < scaled.tau < hi


def test_input_checks():
    with pytest.raises(ValueError):
        tmle_ate([1, 0], [1, 0], [1.0, 0.5], [0.5, 0.5], [0.5, 0.5])
    with pytest.raises(ValueError):
        tmle_ate([1, 0], [1, 0], [0.5, 0.5], [1.0, 0.5], [0.5, 0.5])
    with pytest.raises(ValueError):
        tmle_ate([1, 0], [2, 0], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5])
    with pytest.raises(ArithmeticError):
        tmle_ate([1, 0, 0, 0], [1, 0, 0, 0], [0.05, 0.5, 0.5, 0.5], [0.2] * 4, [0.2] * 4)  # H separates Y
