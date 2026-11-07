# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-bisection-hybrid/. The authors are listed in prov/STTPS1.jsonl.

import math
import random

from newton_bisection_hybrid import safe_newton

ROOT = -1.7692923542386314  # real root of x^3 - 2x + 2


def f(x):
    return x**3 - 2 * x + 2


def df(x):
    return 3 * x * x - 2


def test_worked_example():
    r = safe_newton(f, df, -3.0, 2.0, 1e-12)
    assert r.reason == "converged"
    assert r.root == ROOT
    assert r.iterations == 5 and r.f_evals == 7 and r.df_evals == 5
    assert r.steps == ["bisect", "newton", "newton", "newton", "newton"]
    first = safe_newton(f, df, -3.0, 2.0, 0.0, max_iter=1)
    assert first.root == -1.75 and (first.a, first.b) == (-3.0, -0.5)


def test_plain_newton_cycles_here():
    x = 0.0
    for _ in range(10):
        x = x - f(x) / df(x)
    assert x == 0.0  # 0 -> 1 -> 0 -> ...
    r = safe_newton(f, df, -1.0 - 1e-9 - 1.0, 1.0, 1e-12)
    assert r.converged and abs(r.root - ROOT) < 1e-12


def test_bracket_kept_each_pass():
    for k in range(1, 6):
        r = safe_newton(f, df, -3.0, 2.0, 0.0, max_iter=k)
        if r.reason == "kmax reached":
            assert r.a < r.b and f(r.a) < 0 < f(r.b) and r.a <= ROOT <= r.b
            assert r.f_evals == k + 2 and r.df_evals == k


def test_quadratic_order_observed():
    errs = [abs(safe_newton(f, df, -3.0, 2.0, 0.0, max_iter=k).root - ROOT) for k in (2, 3, 4)]
    q = math.log(errs[2] / errs[1]) / math.log(errs[1] / errs[0])
    assert 1.8 < q < 2.2


def test_arctan_where_newton_diverges():
    x = 5.0
    x = x - math.atan(x) * (1 + x * x)
    assert abs(x) > 30  # plain Newton from the midpoint runs away
    r = safe_newton(math.atan, lambda t: 1 / (1 + t * t), -10.0, 20.0, 1e-12)
    assert r.converged and abs(r.root) < 1e-12
    assert r.steps[:3] == ["bisect", "bisect", "bisect"]


def test_triple_root_alternates():
    r = safe_newton(lambda x: (x - 1) ** 3, lambda x: 3 * (x - 1) ** 2, 0.0, 3.0, 1e-12)
    assert r.converged and abs(r.root - 1) < 1e-11
    assert r.iterations == 63 and r.f_evals == 65
    assert r.steps.count("bisect") == 31


def test_endpoint_root_and_exact_zero():
    r = safe_newton(lambda x: x - 2.0, lambda x: 1.0, 0.0, 2.0)
    assert r.root == 2.0 and r.reason == "root" and r.f_evals == 2 and r.df_evals == 0
    r = safe_newton(lambda x: x - 1.0, lambda x: 1.0, 0.0, 2.0)
    assert r.root == 1.0 and r.reason == "root" and r.iterations == 1


def test_zero_derivative_falls_back():
    # f'(midpoint) = 0: x^3 - 1/8 on [-1, 1], midpoint 0
    r = safe_newton(lambda x: x**3 - 0.125, lambda x: 3 * x * x, -1.0, 1.0, 1e-14)
    assert r.steps[0] == "bisect" and r.converged and abs(r.root - 0.5) < 1e-14


def test_no_sign_change_and_nan():
    assert safe_newton(lambda x: x * x + 1, lambda x: 2 * x, -1.0, 1.0).reason == "no bracket"
    assert safe_newton(lambda x: math.nan, lambda x: 1.0, -1.0, 1.0).reason == "no bracket"
    g = lambda x: math.nan if -0.5 < x < 0.5 else x
    assert safe_newton(g, lambda x: 1.0, -1.0, 2.0).reason == "failure"
    r = safe_newton(lambda x: x - 0.3, lambda x: math.nan, 0.0, 1.0, 1e-12)
    assert r.converged and all(s == "bisect" for s in r.steps)


def test_kmax_reached():
    r = safe_newton(f, df, -3.0, 2.0, 0.0, max_iter=3)
    assert r.reason == "kmax reached" and r.iterations == 3 and r.f_evals == 5


def test_zero_tolerance_terminates():
    r = safe_newton(lambda x: math.cos(x) - x, lambda x: -math.sin(x) - 1, 0.0, 1.0, 0.0, max_iter=10**6)
    assert r.converged and r.iterations < 20


def test_pass_bound():
    # (N + 1)^2 with N = ceil(log2(3 / 1e-12)) = 42
    r = safe_newton(lambda x: (x - 1) ** 3, lambda x: 3 * (x - 1) ** 2, 0.0, 3.0, 1e-12)
    assert r.iterations <= 43**2


def test_random_cubics():
    rng = random.Random(20261107)
    for _ in range(500):
        r0 = rng.uniform(-1, 1)
        o1, o2 = r0 - rng.uniform(1.5, 4), r0 + rng.uniform(1.5, 4)
        g = lambda x, r0=r0, o1=o1, o2=o2: (x - r0) * (x - o1) * (x - o2)
        dg = lambda x, r0=r0, o1=o1, o2=o2: (x - o1) * (x - o2) + (x - r0) * (x - o2) + (x - r0) * (x - o1)
        a, b = r0 - rng.uniform(0.05, 1.4), r0 + rng.uniform(0.05, 1.4)
        res = safe_newton(g, dg, a, b, 1e-13)
        assert res.converged and a <= res.root <= b
        assert abs(res.root - r0) < 1e-10
        assert res.f_evals == res.iterations + 2 or res.reason == "root"
