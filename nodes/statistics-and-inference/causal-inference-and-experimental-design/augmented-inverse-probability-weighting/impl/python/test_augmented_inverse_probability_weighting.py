# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/augmented-inverse-probability-weighting/. The authors are listed in prov/T508RZ.jsonl.

import math
import random
import statistics
from fractions import Fraction as Fr

import pytest

from augmented_inverse_probability_weighting import (
    aipw_ate,
    aipw_interval,
    aipw_scores,
    aipw_variance,
    fit_aipw,
    fit_least_squares,
    fit_logistic,
)

# The worked example of the page (the eight units of the inverse probability weighting page).
EX_X = [0, 0, 0, 0, 0, 1, 1, 1]
EX_T = [1, 1, 0, 0, 0, 1, 1, 0]
EX_Y = [8, 7, 6, 5, 7, 4, 3, 1]
EX_E = [Fr(1, 4)] * 5 + [Fr(3, 4)] * 3


def stratified(x, t, y):
    """Oracle: sum over strata of (stratum share) times (difference of the arm means)."""
    out = Fr(0)
    for v in set(x):
        idx = [i for i in range(len(x)) if x[i] == v]
        tr = [y[i] for i in idx if t[i] == 1]
        co = [y[i] for i in idx if t[i] == 0]
        out += len(idx) * (Fr(sum(tr), len(tr)) - Fr(sum(co), len(co)))
    return out / len(x)


def test_worked_example():
    zero = [0] * 8
    assert aipw_ate(EX_T, EX_Y, EX_E, zero, zero).tau == Fr(31, 6)  # the Horvitz-Thompson IPW form
    cells1 = [Fr(15, 2) if v == 0 else Fr(7, 2) for v in EX_X]
    cells0 = [Fr(6) if v == 0 else Fr(1) for v in EX_X]
    assert aipw_ate(EX_T, EX_Y, EX_E, cells1, cells0).tau == Fr(15, 8)
    arm1, arm0 = [Fr(11, 2)] * 8, [Fr(19, 4)] * 8
    assert aipw_ate(EX_T, EX_Y, EX_E, arm1, arm0).tau == Fr(10, 3)
    half = [Fr(1, 2)] * 8
    assert aipw_ate(EX_T, EX_Y, half, arm1, arm0).tau == Fr(3, 4)  # both wrong: the naive difference
    assert aipw_ate(EX_T, EX_Y, half, cells1, cells0).tau == Fr(15, 8)
    emp = [Fr(2, 5)] * 5 + [Fr(2, 3)] * 3
    assert aipw_ate(EX_T, EX_Y, emp, arm1, arm0).tau == Fr(15, 8)
    assert aipw_ate(EX_T, EX_Y, emp, zero, zero).tau == Fr(15, 8)


def test_scores_average_to_estimate_and_variance():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(2, 12)
        t = [rng.randint(0, 1) for _ in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        e = [Fr(rng.randint(1, 9), 10) for _ in range(n)]
        m1 = [Fr(rng.randint(-9, 9), 2) for _ in range(n)]
        m0 = [Fr(rng.randint(-9, 9), 3) for _ in range(n)]
        psi = aipw_scores(t, y, e, m1, m0)
        est = aipw_ate(t, y, e, m1, m0)
        assert sum(psi) / n == est.tau == est.mu1 - est.mu0
        mean = sum(psi) / n
        assert aipw_variance(t, y, e, m1, m0) == sum((p - mean) ** 2 for p in psi) / ((n - 1) * n)


def population_bias(px, e, et, mu1, mu0, m1, m0):
    """Exact E[psi] - tau over a discrete population, by direct expectation over X and T."""
    mean_psi = Fr(0)
    tau = Fr(0)
    for x, p in px.items():
        # E[psi | X = x] with E[T | X] = e(x) and E[Y | T = t, X] = mu_t(x)
        treated = m1[x] - m0[x] + (mu1[x] - m1[x]) / et[x]
        control = m1[x] - m0[x] - (mu0[x] - m0[x]) / (1 - et[x])
        mean_psi += p * (e[x] * treated + (1 - e[x]) * control)
        tau += p * (mu1[x] - mu0[x])
    return mean_psi - tau


def test_double_robustness_identity_exact():
    rng = random.Random(11)
    for _ in range(300):
        k = rng.randint(1, 4)
        w = [rng.randint(1, 5) for _ in range(k)]
        px = {x: Fr(w[x], sum(w)) for x in range(k)}
        e = {x: Fr(rng.randint(1, 9), 10) for x in range(k)}
        mu1 = {x: Fr(rng.randint(-9, 9)) for x in range(k)}
        mu0 = {x: Fr(rng.randint(-9, 9)) for x in range(k)}
        et = {x: Fr(rng.randint(1, 9), 10) for x in range(k)}
        m1 = {x: Fr(rng.randint(-9, 9)) for x in range(k)}
        m0 = {x: Fr(rng.randint(-9, 9)) for x in range(k)}
        # correct propensity, wrong outcome model
        assert population_bias(px, e, e, mu1, mu0, m1, m0) == 0
        # correct outcome model, wrong propensity
        assert population_bias(px, e, et, mu1, mu0, mu1, mu0) == 0
        # both wrong: the bias is the product formula of the page
        formula = sum(px[x] * ((e[x] / et[x] - 1) * (mu1[x] - m1[x]) - ((1 - e[x]) / (1 - et[x]) - 1) * (mu0[x] - m0[x])) for x in px)
        assert population_bias(px, e, et, mu1, mu0, m1, m0) == formula


def test_population_example_of_the_page():
    px = {0: Fr(1, 2), 1: Fr(1, 2)}
    e = {0: Fr(1, 4), 1: Fr(3, 4)}
    mu1 = {0: Fr(7), 1: Fr(4)}
    mu0 = {0: Fr(6), 1: Fr(1)}
    zero = {0: Fr(0), 1: Fr(0)}
    half = {0: Fr(1, 2), 1: Fr(1, 2)}
    assert population_bias(px, e, half, mu1, mu0, zero, zero) == -2
    assert population_bias(px, e, e, mu1, mu0, zero, zero) == 0
    assert population_bias(px, e, half, mu1, mu0, mu1, mu0) == 0


def test_discrete_covariate_sample_identities():
    """Empirical propensities give the stratified estimate for every outcome model that depends on x
    only; cell-mean outcome models give it for every propensity that depends on x only."""
    rng = random.Random(23)
    for _ in range(300):
        k = rng.randint(1, 3)
        x, t, y = [], [], []
        for v in range(k):
            n1, n0 = rng.randint(1, 4), rng.randint(1, 4)
            for _ in range(n1):
                x.append(v), t.append(1), y.append(Fr(rng.randint(0, 20)))
            for _ in range(n0):
                x.append(v), t.append(0), y.append(Fr(rng.randint(0, 20)))
        target = stratified(x, t, y)
        share = {v: Fr(sum(1 for i in range(len(x)) if x[i] == v and t[i]), x.count(v)) for v in range(k)}
        emp = [share[v] for v in x]
        g1 = {v: Fr(rng.randint(-5, 25)) for v in range(k)}
        g0 = {v: Fr(rng.randint(-5, 25)) for v in range(k)}
        assert aipw_ate(t, y, emp, [g1[v] for v in x], [g0[v] for v in x]).tau == target
        cm1 = {v: stratified_mean(x, t, y, v, 1) for v in range(k)}
        cm0 = {v: stratified_mean(x, t, y, v, 0) for v in range(k)}
        anyp = {v: Fr(rng.randint(1, 9), 10) for v in range(k)}
        assert aipw_ate(t, y, [anyp[v] for v in x], [cm1[v] for v in x], [cm0[v] for v in x]).tau == target


def stratified_mean(x, t, y, v, arm):
    vals = [y[i] for i in range(len(x)) if x[i] == v and t[i] == arm]
    return Fr(sum(vals), len(vals))


def test_positivity_and_input_checks():
    with pytest.raises(ValueError):
        aipw_ate([1, 0], [1, 2], [1, Fr(1, 2)], [0, 0], [0, 0])
    with pytest.raises(ValueError):
        aipw_ate([1, 2], [1, 2], [Fr(1, 2)] * 2, [0, 0], [0, 0])
    with pytest.raises(ValueError):
        aipw_ate([1], [1, 2], [Fr(1, 2)], [0], [0])
    with pytest.raises(ValueError):
        aipw_ate([], [], [], [], [])


def test_least_squares_and_logistic_fits():
    rows = [[Fr(1), Fr(v)] for v in range(5)]
    y = [Fr(3 + 2 * v) for v in range(5)]
    assert fit_least_squares(rows, y) == [3, 2]
    # logistic: the score equations hold at the fitted coefficients
    rng = random.Random(3)
    xs = [rng.uniform(-2, 2) for _ in range(300)]
    t = [1 if rng.random() < 1 / (1 + math.exp(-(0.5 + 1.5 * v))) else 0 for v in xs]
    b = fit_logistic([[1.0, v] for v in xs], t)
    q = [1 / (1 + math.exp(-(b[0] + b[1] * v))) for v in xs]
    assert abs(sum(ti - qi for ti, qi in zip(t, q))) < 1e-8
    assert abs(sum((ti - qi) * v for ti, qi, v in zip(t, q, xs))) < 1e-8


def expit(z):
    return 1 / (1 + math.exp(-z))


def simulate(n, rng):
    """X uniform on [0, 1]; e(x) = expit(-2 + 4x); Y(t) = x + 2x^2 + t(1 + x) + N(0, 1). True ATE 1.5."""
    x, t, y = [], [], []
    for _ in range(n):
        xi = rng.random()
        ti = 1 if rng.random() < expit(-2 + 4 * xi) else 0
        x.append(xi), t.append(ti), y.append(xi + 2 * xi * xi + ti * (1 + xi) + rng.gauss(0, 1))
    return x, t, y


def test_monte_carlo_one_wrong_model():
    """With r = 40 samples of n = 1000 (seed 2026), the mean estimate stays within 4 standard errors
    (plus 0.01 for the finite-n bias) of 1.5 when either model is right, and is far off when both are wrong."""
    rng = random.Random(2026)
    full_o = lambda v: [1.0, v, v * v]
    const = lambda v: [1.0]
    full_p = lambda v: [1.0, v]
    runs = {"both": [], "outcome wrong": [], "propensity wrong": [], "both wrong": []}
    configs = {"both": (full_o, full_p), "outcome wrong": (const, full_p), "propensity wrong": (full_o, const), "both wrong": (const, const)}
    r = 40
    for _ in range(r):
        x, t, y = simulate(1000, rng)
        for name, (of, pf) in configs.items():
            e, m1, m0 = fit_aipw(x, t, y, of, pf)
            runs[name].append(aipw_ate(t, y, e, m1, m0).tau)
    for name in ("both", "outcome wrong", "propensity wrong"):
        v = runs[name]
        tol = 4 * statistics.stdev(v) / math.sqrt(r) + 0.01
        assert abs(statistics.mean(v) - 1.5) < tol, name
    assert statistics.mean(runs["both wrong"]) - 1.5 > 0.7


def test_interval_shape():
    rng = random.Random(9)
    x, t, y = simulate(400, rng)
    e, m1, m0 = fit_aipw(x, t, y, lambda v: [1.0, v, v * v], lambda v: [1.0, v])
    est, lo, hi = aipw_interval(t, y, e, m1, m0, alpha=0.05)
    se = math.sqrt(aipw_variance(t, y, e, m1, m0))
    assert lo < est < hi
    assert abs((hi - lo) - 2 * 1.959963984540054 * se) < 1e-9
