# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ridders-method/. The authors are listed in prov/AGQH37.jsonl.

import math
import random
from decimal import Decimal, getcontext

from ridders_method import ridders

ROOT = 1.5213797068045676  # x^3 - x - 2


def cubic(x):
    return x ** 3 - x - 2


def test_example_cubic():
    r = ridders(cubic, 1.0, 2.0)
    assert r.root == ROOT and r.reason == "root"
    assert (r.iterations, r.evaluations) == (4, 10)
    assert r.trial[:3] == [1.5220755392844174, 1.5213797263830957, 1.5213797068047001]


def test_cos_stops_by_step_test_with_wide_bracket():
    r = ridders(lambda x: math.cos(x) - x, 0.0, 1.0)
    assert r.reason == "converged" and (r.iterations, r.evaluations) == (6, 14)
    assert abs(r.root - 0.7390851332151607) <= 2.3e-16
    assert r.a <= 0.7390851332151607 <= r.b and r.b - r.a > 1e-3


def test_bracket_kept_and_halved_every_pass():
    rng = random.Random(7)
    for _ in range(200):
        c = rng.uniform(-5, 5)
        g = lambda x, c=c: math.atan(x - c) + 0.1 * (x - c) ** 3
        a, b = -10.0, 10.0
        w = b - a
        for k in range(1, 30):
            r = ridders(g, a, b, max_iter=k)
            if r.reason == "root":
                break
            assert g(r.a) * g(r.b) <= 0
            assert r.b - r.a <= w / 2 ** r.iterations * (1 + 1e-12)


def test_one_sided_convergence_in_high_precision():
    # in exact arithmetic one bracket end stays at the midpoint side for x^3 - x - 2:
    # the bracket only halves while the Ridders point converges superlinearly
    getcontext().prec = 200
    f = lambda x: x ** 3 - x - 2
    R = Decimal("1.5")
    for _ in range(40):
        R -= f(R) / (3 * R * R - 1)
    a, b = Decimal(1), Decimal(2)
    fa, fb = f(a), f(b)
    sg = lambda v: (v > 0) - (v < 0)
    errs, widths = [], []
    for _ in range(7):
        m = (a + b) / 2
        fm = f(m)
        x = m + (m - a) * sg(fa - fb) * fm / (fm * fm - fa * fb).sqrt()
        fx = f(x)
        if sg(fm) != sg(fx):
            a, fa, b, fb = (m, fm, x, fx) if m < x else (x, fx, m, fm)
        elif sg(fa) != sg(fx):
            b, fb = x, fx
        else:
            a, fa = x, fx
        errs.append(abs(x - R))
        widths.append(b - a)
    for k in range(2, 7):
        assert abs(widths[k] / widths[k - 1] - Decimal("0.5")) < Decimal("1e-3")
    ratios = [errs[k] / errs[k - 1] for k in range(1, 7)]
    for k in range(1, 6):
        assert ratios[k] < ratios[k - 1] / 3  # superlinear, but order 1


def test_endpoint_roots_and_no_sign_change():
    r = ridders(cubic, ROOT, 2.0)
    assert r.root == ROOT and r.reason == "root" and r.evaluations == 2
    r = ridders(lambda x: x - 2.0, 1.0, 2.0)
    assert r.root == 2.0 and r.reason == "root"
    r = ridders(lambda x: x * x + 1, -1.0, 1.0)
    assert r.reason == "no sign change" and r.evaluations == 2


def test_exact_zero_at_midpoint():
    r = ridders(lambda x: x, -1.0, 1.0)
    assert r.root == 0.0 and r.reason == "root" and r.evaluations == 3


def test_tolerance_and_kmax():
    r = ridders(lambda x: x * math.exp(x) - 1, 0.0, 1.0, tol=1e-12)
    assert r.reason == "bracket" and r.b - r.a <= 2e-12
    assert r.a <= 0.5671432904097838 <= r.b
    r = ridders(lambda x: (x - 1) ** 3, 0.0, 3.0, max_iter=3)
    assert r.reason == "kmax reached" and r.evaluations == 8


def test_triple_root_is_at_most_bisection_rate():
    r = ridders(lambda x: (x - 1) ** 3, 0.0, 3.0, tol=1e-12)
    assert r.converged and abs(r.root - 1) < 1e-12
    assert r.evaluations <= 2 + 2 * 42


def test_nan_and_overflow():
    r = ridders(lambda x: float("nan") if x > 0.5 else x - 0.7, 0.0, 1.0)
    assert r.reason == "failure"
    r = ridders(lambda x: math.exp(x) - 1e300, 0.0, 700.0, tol=1e-9)
    assert r.converged and abs(r.root - math.log(1e300)) < 1e-9
    r = ridders(lambda x: math.inf if x > 1 else -1.0, 0.0, 2.0)
    assert r.reason == "failure"


def test_random_brackets():
    rng = random.Random(20261108)
    for _ in range(500):
        z = rng.uniform(-3, 3)
        c = rng.uniform(0.1, 3)
        g = lambda x, z=z, c=c: (x - z) * (1 + c * (x - z) ** 2) + 0.5 * math.sin(x - z)
        a, b = z - rng.uniform(0.01, 4), z + rng.uniform(0.01, 4)
        r = ridders(g, a, b, tol=1e-13)
        assert r.converged and abs(r.root - z) < 1e-12
        assert r.a <= r.root <= r.b
        assert r.evaluations <= 2 + 2 * 60


def test_exact_for_exponential_times_line():
    r = ridders(lambda x: math.exp(2 * x) * (3 * x - 1), 0.0, 1.0, max_iter=1)
    assert abs(r.trial[0] - 1 / 3) < 1e-15
