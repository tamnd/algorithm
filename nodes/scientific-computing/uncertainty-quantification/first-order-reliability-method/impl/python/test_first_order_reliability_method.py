# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-order-reliability-method/. The authors are listed in prov/B2CCS2.jsonl.
import math
import random
from statistics import NormalDist

import pytest

from first_order_reliability_method import (
    breitung,
    form,
    gradient,
    lognormal_marginal,
    normal_marginal,
    phi_cdf,
    uniform_marginal,
)

STD = [normal_marginal(0.0, 1.0)]


def trap(f, a, b, n=20000):
    h = (b - a) / n
    return h * (0.5 * f(a) + 0.5 * f(b) + sum(f(a + i * h) for i in range(1, n)))


def pdf(t):
    return math.exp(-0.5 * t * t) / math.sqrt(2 * math.pi)


def test_phi_matches_reference_values():
    assert abs(phi_cdf(-3.0) - 0.0013498980316301) < 1e-15
    nd = NormalDist()
    for t in (-2.5, -1.0, 0.0, 0.7, 2.0):
        assert abs(phi_cdf(t) - nd.cdf(t)) < 1e-14


def test_linear_limit_state_is_exact():
    rng = random.Random(1)
    for _ in range(5):
        a = [rng.uniform(-2, 2) for _ in range(4)]
        a0 = rng.uniform(1, 4)
        res = form(lambda u: a0 + sum(x * y for x, y in zip(a, u)), STD * 4)
        na = math.sqrt(sum(t * t for t in a))
        assert abs(res["beta"] - a0 / na) < 1e-8
        assert res["steps"] <= 3
        assert max(abs(ui + a0 * ai / na**2) for ui, ai in zip(res["u"], a)) < 1e-8
        assert abs(res["pf"] - phi_cdf(-a0 / na)) < 1e-12


def test_normal_resistance_minus_normal_load():
    res = form(lambda x: x[0] - x[1], [normal_marginal(10.0, 1.0), normal_marginal(6.0, 1.5)])
    assert abs(res["beta"] - 4.0 / math.sqrt(1.0 + 2.25)) < 1e-8


def test_design_point_satisfies_the_optimality_conditions():
    res = form(lambda x: x[0] - x[1], [lognormal_marginal(math.log(10.0), 0.2), normal_marginal(5.0, 1.5)])
    u, alpha, beta = res["u"], res["alpha"], res["beta"]
    assert abs(res["G"](u)) < 1e-9
    assert max(abs(ui - beta * ai) for ui, ai in zip(u, alpha)) < 1e-7
    grad = gradient(res["G"], u)
    assert abs(grad[0] * u[1] - grad[1] * u[0]) < 1e-7


def test_formulation_invariance():
    marg = [lognormal_marginal(math.log(10.0), 0.2), normal_marginal(5.0, 1.5)]
    b1 = form(lambda x: x[0] - x[1], marg)["beta"]
    b2 = form(lambda x: math.log(x[0]) - math.log(x[1]), marg)["beta"]
    b3 = form(lambda x: x[0] / x[1] - 1.0, marg)["beta"]
    assert abs(b1 - b2) < 1e-7 and abs(b1 - b3) < 1e-7


def test_lognormal_resistance_against_exact_integral():
    lam, zeta = math.log(10.0), 0.2
    res = form(lambda x: x[0] - x[1], [lognormal_marginal(lam, zeta), normal_marginal(5.0, 1.5)])
    exact = trap(lambda s: pdf((s - 5.0) / 1.5) / 1.5 * phi_cdf((math.log(s) - lam) / zeta), 0.01, 20.0)
    assert abs(exact - 1.289177e-2) < 1e-7
    assert abs(res["beta"] - 2.1964205) < 1e-6
    assert 0.05 < res["pf"] / exact - 1.0 < 0.12
    assert abs(breitung(res) / exact - 1.0) < 0.02


def test_parabolic_limit_state_and_breitung():
    for k in (0.05, 0.1, 0.2, 0.5):
        res = form(lambda u: 3.0 - u[0] + 0.5 * k * u[1] ** 2, STD * 2)
        exact = trap(lambda t: pdf(t) * phi_cdf(-(3.0 + 0.5 * k * t * t)), -12.0, 12.0, 4000)
        assert abs(res["beta"] - 3.0) < 1e-8
        assert abs(res["pf"] - phi_cdf(-3.0)) < 1e-12
        assert res["pf"] > exact
        sorm = breitung(res)
        assert abs(sorm - phi_cdf(-3.0) / math.sqrt(1.0 + 3.0 * k)) < 1e-7
        assert abs(sorm - exact) < abs(res["pf"] - exact)


def test_origin_in_failure_domain_gives_negative_beta():
    res = form(lambda u: -1.0 - u[0], STD * 2)
    assert abs(res["beta"] + 1.0) < 1e-8
    assert abs(res["pf"] - phi_cdf(1.0)) < 1e-9


def test_uniform_marginal_map():
    t = uniform_marginal(2.0, 5.0)
    assert abs(t(0.0) - 3.5) < 1e-15
    assert abs(t(1.0) - (2.0 + 3.0 * phi_cdf(1.0))) < 1e-15


def test_zero_gradient_is_rejected():
    with pytest.raises(ValueError):
        form(lambda u: 1.0 + u[0] ** 2, STD)
