# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-rule/. The authors are listed in prov/YFXF32.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from midpoint_rule import midpoint_rule


def order(errs):
    return [math.log2(abs(e1 / e2)) for e1, e2 in zip(errs, errs[1:])]


def test_example() -> None:
    q = midpoint_rule(math.exp, 0.0, 1.0, 4)
    assert abs(q - 1.7138152798) < 1e-10
    assert abs((math.e - 1 - q) - 4.4665e-03) < 1e-7


def test_degree_of_exactness_is_one() -> None:
    for a, b in [(F(0), F(1)), (F(-2, 3), F(7, 4))]:
        for m in (1, 2, 5):
            h = (b - a) / m
            for k in (0, 1):
                exact = (b ** (k + 1) - a ** (k + 1)) / (k + 1)
                assert midpoint_rule(lambda x, k=k: x**k, a, b, m) == exact
            err = (b**3 - a**3) / 3 - midpoint_rule(lambda x: x * x, a, b, m)
            assert err == (b - a) * h * h / 12  # (b - a) h^2 f''/24 with f'' = 2
            assert err != 0


def test_random_cubics_against_euler_maclaurin() -> None:
    # For a cubic p, I(p) - M_m(p) = h^2/24 (p'(b) - p'(a)) exactly.
    rng = random.Random(4242)
    for _ in range(500):
        c = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4)]
        a = F(rng.randint(-20, 20), rng.randint(1, 4))
        b = a + F(rng.randint(-20, 20), rng.randint(1, 4))
        m = rng.randint(1, 12)
        h = (b - a) / m

        def p(x):
            return c[0] + c[1] * x + c[2] * x * x + c[3] * x**3

        def dp(x):
            return c[1] + 2 * c[2] * x + 3 * c[3] * x * x

        def big_p(x):
            return c[0] * x + c[1] * x**2 / 2 + c[2] * x**3 / 3 + c[3] * x**4 / 4

        exact = big_p(b) - big_p(a)
        assert exact - midpoint_rule(p, a, b, m) == h * h / 24 * (dp(b) - dp(a))


def test_second_order_and_bound() -> None:
    cases = [
        (math.exp, 0.0, 1.0, math.e - 1, math.e),
        (math.sin, 0.0, 2.0, 1 - math.cos(2.0), 1.0),
        (lambda x: 1 / (1 + x * x), 0.0, 1.0, math.pi / 4, 2.0),
    ]
    for f, a, b, exact, m2 in cases:
        errs = []
        for m in (8, 16, 32, 64):
            h = (b - a) / m
            e = exact - midpoint_rule(f, a, b, m)
            assert abs(e) <= (b - a) * h * h / 24 * m2 * (1 + 1e-9)
            errs.append(e)
        for p in order(errs):
            assert 1.95 < p < 2.05


def test_opposite_sign_to_trapezoid_for_convex() -> None:
    for m in (1, 3, 10):
        h = 1.0 / m
        mid = midpoint_rule(math.exp, 0.0, 1.0, m)
        trap = h * (0.5 + 0.5 * math.e + sum(math.exp(i * h) for i in range(1, m)))
        assert mid < math.e - 1 < trap


def test_endpoint_singularities() -> None:
    # Open rule: f is never evaluated at 0.
    errs = [2.0 - midpoint_rule(lambda x: x**-0.5, 0.0, 1.0, m) for m in (256, 512, 1024, 2048)]
    for p in order(errs):
        assert 0.45 < p < 0.55
    errs = [-1.0 - midpoint_rule(math.log, 0.0, 1.0, m) for m in (256, 512, 1024, 2048)]
    for p in order(errs):
        assert 0.95 < p < 1.05


def test_evaluations_and_edges() -> None:
    calls = [0]

    def g(x):
        calls[0] += 1
        return math.cos(x)

    for m in (1, 4, 99):
        calls[0] = 0
        midpoint_rule(g, 0.0, 1.0, m)
        assert calls[0] == m
    assert midpoint_rule(math.exp, 1.5, 1.5, 3) == 0.0
    assert abs(midpoint_rule(math.exp, 0.0, 1.0, 9) + midpoint_rule(math.exp, 1.0, 0.0, 9)) < 1e-15
    assert midpoint_rule(math.exp, 0.0, 2.0, 1) == 2 * math.exp(1.0)
    with pytest.raises(ValueError):
        midpoint_rule(math.exp, 0.0, 1.0, 0)


def test_jump_and_kink() -> None:
    c = 1 / 3
    for m in (10, 100, 1000):
        h = 1.0 / m
        e = (1 - c) - midpoint_rule(lambda x: 1.0 if x > c else 0.0, 0.0, 1.0, m)
        assert abs(e) <= h / 2 + 1e-15
        e = (c * c + (1 - c) ** 2) / 2 - midpoint_rule(lambda x: abs(x - c), 0.0, 1.0, m)
        assert abs(e) <= h * h / 4 + 1e-15
