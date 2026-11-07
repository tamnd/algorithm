# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regula-falsi/. The authors are listed in prov/2GQVTS.jsonl.

import math
import random
from decimal import Decimal, getcontext
from fractions import Fraction

from regula_falsi import regula_falsi

ROOT = 1.5213797068045676  # real root of x^3 - x - 2


def cubic(x):
    return x**3 - x - 2


def test_worked_example():
    r = regula_falsi(cubic, 1.0, 2.0, 1e-12)
    assert r.reason == "converged"
    assert r.iterations == 23 and r.evaluations == 25
    assert r.b == 2.0  # the right end never moves
    assert abs(r.root - ROOT) < 1e-12
    first = [regula_falsi(cubic, 1.0, 2.0, 0.0, max_iter=k).root for k in range(1, 5)]
    assert first == [1.3333333333333335, 1.462686567164179, 1.5040190039499488, 1.516330564760263]


def test_bracket_kept_each_step():
    for k in range(1, 30):
        r = regula_falsi(cubic, 1.0, 2.0, 0.0, max_iter=k)
        if r.reason == "kmax reached":
            assert r.a < r.b
            assert cubic(r.a) < 0 < cubic(r.b)
            assert r.a <= ROOT <= r.b
            assert r.evaluations == k + 2


def test_linear_rate():
    errs = [abs(regula_falsi(cubic, 1.0, 2.0, 0.0, max_iter=k).root - ROOT) for k in range(1, 17)]
    fd = 3 * ROOT * ROOT - 1
    rate = 1 - fd * (2 - ROOT) / cubic(2.0)
    assert abs(rate - 0.28880) < 1e-4
    for k in range(10, 15):
        assert abs(errs[k + 1] / errs[k] - rate) < 2e-3
    # observed order: log ratio of successive errors tends to 1
    q = math.log(errs[15] / errs[14]) / math.log(errs[14] / errs[13])
    assert abs(q - 1.0) < 0.01


def test_root_at_endpoint():
    r = regula_falsi(lambda x: x - 1.0, 1.0, 3.0)
    assert r.root == 1.0 and r.reason == "root" and r.evaluations == 2
    r = regula_falsi(lambda x: x - 3.0, 1.0, 3.0)
    assert r.root == 3.0 and r.reason == "root" and r.evaluations == 2


def test_exact_zero_at_iterate():
    r = regula_falsi(lambda x: x - 0.5, 0.0, 1.0)
    assert r.root == 0.5 and r.reason == "root" and r.iterations == 1 and r.evaluations == 3


def test_no_sign_change():
    r = regula_falsi(lambda x: x * x + 1, -1.0, 1.0)
    assert r.reason == "no bracket" and not r.converged and r.evaluations == 2


def test_nan_and_inf():
    assert regula_falsi(lambda x: math.nan, 0.0, 1.0).reason == "no bracket"
    assert regula_falsi(lambda x: math.inf if x == 0 else x - 0.5, 0.0, 1.0).reason == "no bracket"
    g = lambda x: math.nan if 0.2 < x < 0.8 else x - 0.4
    r = regula_falsi(g, 0.0, 1.0)
    assert r.reason == "failure" and r.evaluations == 3


def test_kmax_reached():
    r = regula_falsi(lambda x: x**10 - 1, 0.0, 1.3, 1e-10, max_iter=5)
    assert r.reason == "kmax reached" and r.iterations == 5 and r.evaluations == 7


def test_slow_one_sided_case():
    r = regula_falsi(lambda x: x**10 - 1, 0.0, 1.3, 1e-10)
    assert r.reason == "converged" and r.iterations == 91 and r.evaluations == 93
    assert r.b == 1.3
    # the step test is not certified: the error exceeds the tolerance
    assert 1e-10 < abs(r.root - 1.0) < 1e-9


def test_zero_tolerance_terminates():
    r = regula_falsi(cubic, 1.0, 2.0, 0.0, max_iter=10**6)
    assert r.converged and r.iterations < 100
    assert abs(r.root - ROOT) <= 4e-16


def test_bracket_flag_certifies():
    r = regula_falsi(lambda x: x - 0.3, 0.0, 1.0, 0.25)
    # the first chord hits 0.3 up to rounding; a large tol stops on the bracket test
    assert r.converged
    assert abs(r.root - 0.3) <= 0.25


def test_fraction_exact():
    r = regula_falsi(lambda x: x * x - 2, Fraction(1), Fraction(2), Fraction(0), max_iter=3)
    assert r.reason == "kmax reached"
    assert r.root == Fraction(24, 17)
    assert r.a * r.a < 2 < r.b * r.b


def test_decimal_against_cardano():
    getcontext().prec = 40
    s = (Decimal(26) / 27).sqrt()
    third = Decimal(1) / 3
    exact = (1 + s) ** third + (1 - s) ** third
    r = regula_falsi(lambda x: x**3 - x - 2, Decimal(1), Decimal(2), Decimal("1e-30"), max_iter=500)
    assert r.converged
    assert abs(r.root - exact) < Decimal("1e-28")


def test_random_cubics():
    rng = random.Random(20261107)
    for _ in range(500):
        r0 = rng.uniform(-1, 1)
        others = (r0 - rng.uniform(1.5, 4), r0 + rng.uniform(1.5, 4))
        sign = rng.choice((-1.0, 1.0))
        f = lambda x, r0=r0, o=others, s=sign: s * (x - r0) * (x - o[0]) * (x - o[1])
        a, b = r0 - rng.uniform(0.05, 1.0), r0 + rng.uniform(0.05, 1.0)
        res = regula_falsi(f, a, b, 1e-13)
        assert res.converged
        assert a <= res.root <= b
        assert abs(res.root - r0) < 1e-9
        assert res.evaluations == res.iterations + 2
