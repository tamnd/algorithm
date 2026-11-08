# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simpsons-rule/. The authors are listed in prov/CWAN1Z.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from simpsons_rule import simpsons_rule


def order(errs):
    return [math.log2(abs(e1 / e2)) for e1, e2 in zip(errs, errs[1:])]


def test_example() -> None:
    s = simpsons_rule(math.exp, 0.0, 1.0, 4)
    assert abs(s - 1.7183188419) < 1e-10
    assert abs((math.e - 1 - s) - (-3.7013e-05)) < 1e-9


def test_degree_of_exactness_is_three() -> None:
    for a, b in [(F(0), F(1)), (F(-5, 3), F(2, 7))]:
        for m in (2, 4, 6):
            h = (b - a) / m
            for k in range(4):
                exact = (b ** (k + 1) - a ** (k + 1)) / (k + 1)
                assert simpsons_rule(lambda x, k=k: x**k, a, b, m) == exact
            err = (b**5 - a**5) / 5 - simpsons_rule(lambda x: x**4, a, b, m)
            assert err == -(b - a) * h**4 * 24 / 180
            assert err != 0


def test_random_quintics_exact_error() -> None:
    # For a polynomial p of degree <= 5: I - S_m = -h^4/180 (p'''(b) - p'''(a)).
    rng = random.Random(777)
    for _ in range(500):
        c = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(6)]
        a = F(rng.randint(-10, 10), rng.randint(1, 4))
        b = a + F(rng.randint(-10, 10), rng.randint(1, 4))
        m = 2 * rng.randint(1, 6)
        h = (b - a) / m

        def p(x):
            return sum(ck * x**k for k, ck in enumerate(c))

        def d3(x):
            return sum(ck * k * (k - 1) * (k - 2) * x ** (k - 3) for k, ck in enumerate(c) if k >= 3)

        exact = sum(ck * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))
        assert exact - simpsons_rule(p, a, b, m) == -(h**4) / 180 * (d3(b) - d3(a))


def test_fourth_order_and_bound() -> None:
    cases = [
        (math.exp, 0.0, 1.0, math.e - 1, math.e),
        (math.sin, 0.0, 2.0, 1 - math.cos(2.0), 1.0),
        (math.cos, -1.0, 3.0, math.sin(3.0) + math.sin(1.0), 1.0),
    ]
    for f, a, b, exact, m4 in cases:
        errs = []
        for m in (8, 16, 32, 64):
            h = (b - a) / m
            e = exact - simpsons_rule(f, a, b, m)
            assert abs(e) <= (b - a) * h**4 / 180 * m4 * (1 + 1e-6) + 1e-15
            errs.append(e)
        for p in order(errs):
            assert 3.9 < p < 4.1


def test_low_smoothness() -> None:
    errs = [2 / 3 - simpsons_rule(math.sqrt, 0.0, 1.0, m) for m in (256, 512, 1024, 2048)]
    for p in order(errs):
        assert 1.45 < p < 1.55
    c = 1 / 3
    for m in (10, 100, 1000):
        h = 1.0 / m
        e = (1 - c) - simpsons_rule(lambda x: 1.0 if x > c else 0.0, 0.0, 1.0, m)
        assert abs(e) <= 4 * h / 3 + 1e-14


def test_evaluations_and_edges() -> None:
    calls = [0]

    def g(x):
        calls[0] += 1
        return math.sin(x)

    for m in (2, 10, 50):
        calls[0] = 0
        simpsons_rule(g, 0.0, 1.0, m)
        assert calls[0] == m + 1
    assert simpsons_rule(math.exp, 3.0, 3.0, 4) == 0.0
    assert abs(simpsons_rule(math.exp, 0.0, 1.0, 8) + simpsons_rule(math.exp, 1.0, 0.0, 8)) < 1e-15
    assert simpsons_rule(math.exp, 0.0, 2.0, 2) == pytest.approx((1 + 4 * math.e + math.exp(2.0)) / 3)
    for bad in (0, 1, 3, -2):
        with pytest.raises(ValueError):
            simpsons_rule(math.exp, 0.0, 1.0, bad)


def test_richardson_relation_with_trapezoid() -> None:
    def trap(f, a, b, m):
        h = (b - a) / m
        return h * ((f(a) + f(b)) / 2 + sum(f(a + i * h) for i in range(1, m)))

    a, b = F(0), F(2)
    fr = lambda x: 1 / (1 + x)  # noqa: E731
    for m in (2, 4, 8):
        assert simpsons_rule(fr, a, b, m) == (4 * trap(fr, a, b, m) - trap(fr, a, b, m // 2)) / 3
