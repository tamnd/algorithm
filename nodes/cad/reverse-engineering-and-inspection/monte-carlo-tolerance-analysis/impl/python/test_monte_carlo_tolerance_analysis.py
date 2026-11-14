# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-tolerance-analysis/. The authors are listed in prov/XCJC4F.jsonl.

import math
import random

import pytest

from monte_carlo_tolerance_analysis import simulate, wilson_interval, zero_reject_upper_bound

STACK = {"A": 50.0, "B": 20.0, "C": 15.0, "D": 14.8}
STACK_T = {"A": 0.10, "B": 0.05, "C": 0.05, "D": 0.05}
COEF = {"A": 1.0, "B": -1.0, "C": -1.0, "D": -1.0}


def gap(x):
    return x["A"] - x["B"] - x["C"] - x["D"]


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def dlm_linear(sd):
    """DLM on the linear stack: mean = nominal output, variance = sum a_j^2 sd_j^2."""
    mean = sum(COEF[n] * STACK[n] for n in STACK)
    var = sum((COEF[n] * sd[n]) ** 2 for n in STACK)
    return mean, var


@pytest.mark.parametrize("kind,div", [("normal", 3.0), ("uniform", math.sqrt(3.0))])
def test_linear_stack_agrees_with_dlm(kind, div):
    n = 200_000
    specs = {k: (kind, STACK[k], STACK_T[k]) for k in STACK}
    res = simulate(gap, specs, n, seed=2026)
    mean, var = dlm_linear({k: STACK_T[k] / div for k in STACK})
    se_mean = math.sqrt(var / n)
    # For a normal output the sample variance has standard error var * sqrt(2 / (n - 1)).
    # A sum of uniforms has lighter tails, so this bound is conservative for it.
    se_var = var * math.sqrt(2.0 / (n - 1))
    assert abs(res["mean"] - mean) <= 4 * se_mean
    assert abs(res["var"] - var) <= 4 * se_var
    assert res["assembled"] == n


def test_reject_rate_matches_exact_normal_probability():
    n = 200_000
    specs = {k: ("normal", STACK[k], STACK_T[k]) for k in STACK}
    res = simulate(gap, specs, n, seed=7, lower=0.1)
    mean, var = dlm_linear({k: STACK_T[k] / 3 for k in STACK})
    p = phi((0.1 - mean) / math.sqrt(var))
    assert 0.011 < p < 0.012
    assert abs(res["p"] - p) <= 4 * math.sqrt(p * (1 - p) / n)
    lo, hi = res["wilson"]
    assert lo < p < hi


def test_estimator_is_unbiased_with_the_stated_standard_error():
    """Many short runs: the average of p_hat is p and its spread is sqrt(p(1-p)/N)."""
    p_true, n, runs = 0.1, 500, 400
    specs = {"x": ("uniform", 0.5, 0.5)}  # uniform on [0, 1]
    ests, covered = [], 0
    for r in range(runs):
        res = simulate(lambda x: x["x"], specs, n, seed=1000 + r, upper=1 - p_true)
        ests.append(res["p"])
        lo, hi = res["wilson"]
        covered += lo <= p_true <= hi
    avg = sum(ests) / runs
    var = sum((e - avg) ** 2 for e in ests) / (runs - 1)
    se_true = math.sqrt(p_true * (1 - p_true) / n)
    assert abs(avg - p_true) <= 4 * se_true / math.sqrt(runs)
    assert abs(var / se_true ** 2 - 1) <= 0.3
    assert covered / runs >= 0.90


def test_zero_rejects_upper_bound():
    n = 3000
    res = simulate(lambda x: x["x"], {"x": ("uniform", 0.0, 1.0)}, n, seed=1, lower=-2, upper=2)
    assert res["rejects"] == 0 and res["p"] == 0 and res["se"] == 0
    u = res["upper_if_zero"]
    assert u == pytest.approx(zero_reject_upper_bound(n))
    assert (1 - u) ** n == pytest.approx(0.05)
    assert 0.9 * 3 / n < u < 3 / n


def test_parts_that_do_not_fit_are_rejects():
    n = 20_000
    specs = {"x": ("normal", 0.0, 3.0)}
    res = simulate(lambda x: None if x["x"] > 1 else x["x"], specs, n, seed=5)
    rng = random.Random(5)
    expected = sum(rng.gauss(0.0, 1.0) > 1 for _ in range(n))
    assert res["no_fit"] == expected == res["rejects"]
    assert res["assembled"] == n - expected
    assert abs(res["p"] - (1 - phi(1.0))) <= 4 * math.sqrt(0.16 * 0.84 / n)


def test_same_seed_same_result():
    specs = {k: ("normal", STACK[k], STACK_T[k]) for k in STACK}
    a = simulate(gap, specs, 5000, seed=99, lower=0.1)
    b = simulate(gap, specs, 5000, seed=99, lower=0.1)
    assert a == b


CLUTCH = {"a": 27.645, "c": 11.43, "e": 50.8}


def clutch_phi(x):
    q = (x["a"] + x["c"]) / (x["e"] - x["c"])
    return math.acos(q) if q <= 1 else None


def test_nonlinear_mean_shift_matches_second_order_estimate():
    """On the clutch the output mean moves by about 1/2 sum H_jj sigma_j^2, which DLM does not see."""
    T = 0.05
    sd = T / 3
    n = 100_000
    specs = {k: ("normal", CLUTCH[k], T) for k in CLUTCH}
    res = simulate(clutch_phi, specs, n, seed=31)
    phi0 = clutch_phi(CLUTCH)
    h = 1e-3
    bias = 0.0
    for k in CLUTCH:
        xp, xm = dict(CLUTCH), dict(CLUTCH)
        xp[k] += h
        xm[k] -= h
        hkk = (clutch_phi(xp) - 2 * phi0 + clutch_phi(xm)) / (h * h)
        bias += 0.5 * hkk * sd * sd
    se = math.sqrt(res["var"] / n)
    assert abs(bias) > 8 * se
    assert abs((res["mean"] - phi0) - bias) <= 4 * se + 0.15 * abs(bias)


def test_wilson_interval_endpoints():
    lo, hi = wilson_interval(0, 100)
    assert lo == pytest.approx(0, abs=1e-15) and 0.03 < hi < 0.04
    lo, hi = wilson_interval(50, 100)
    assert lo == pytest.approx(1 - hi)
