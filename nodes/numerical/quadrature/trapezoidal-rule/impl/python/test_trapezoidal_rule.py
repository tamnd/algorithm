# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trapezoidal-rule/. The authors are listed in prov/K7MAWR.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from trapezoidal_rule import trapezoidal_rule

I0_1 = 1.2660658777520083  # modified Bessel function I_0(1)


def counted(f):
    calls = [0]

    def g(x):
        calls[0] += 1
        return f(x)

    return g, calls


def order(errs):
    return [math.log2(abs(e1 / e2)) for e1, e2 in zip(errs, errs[1:])]


def test_example() -> None:
    t = trapezoidal_rule(math.exp, 0.0, 1.0, 4)
    assert abs(t - 1.7272219046) < 1e-10
    assert abs((math.e - 1 - t) - (-8.9401e-03)) < 1e-7


def test_degree_of_exactness_is_one() -> None:
    for a, b in [(F(0), F(1)), (F(-1, 3), F(5, 2))]:
        for m in (1, 2, 3, 7):
            h = (b - a) / m
            for k in (0, 1):
                exact = (b ** (k + 1) - a ** (k + 1)) / (k + 1)
                assert trapezoidal_rule(lambda x, k=k: x**k, a, b, m) == exact
            # x^2 fails, with the error -(b - a) h^2 f''/12 and f'' = 2
            exact2 = (b**3 - a**3) / 3
            err = exact2 - trapezoidal_rule(lambda x: x * x, a, b, m)
            assert err == -(b - a) * h * h / 6
            assert err != 0


def test_random_cubics_against_euler_maclaurin() -> None:
    # For a cubic p, T_m(p) - I(p) = h^2/12 (p'(b) - p'(a)) exactly.
    rng = random.Random(20260101)
    for _ in range(500):
        c = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(4)]
        a = F(rng.randint(-20, 20), rng.randint(1, 4))
        b = a + F(rng.randint(-20, 20), rng.randint(1, 4))
        m = rng.randint(1, 12)

        def p(x):
            return c[0] + c[1] * x + c[2] * x * x + c[3] * x**3

        def dp(x):
            return c[1] + 2 * c[2] * x + 3 * c[3] * x * x

        def big_p(x):
            return c[0] * x + c[1] * x**2 / 2 + c[2] * x**3 / 3 + c[3] * x**4 / 4

        h = (b - a) / m
        expected = big_p(b) - big_p(a) + h * h / 12 * (dp(b) - dp(a))
        assert trapezoidal_rule(p, a, b, m) == expected


def test_second_order_convergence_and_bound() -> None:
    cases = [
        (math.exp, 0.0, 1.0, math.e - 1, math.e),
        (math.sin, 0.0, 2.0, 1 - math.cos(2.0), 1.0),
        (lambda x: 1 / (1 + x * x), 0.0, 1.0, math.pi / 4, 2.0),
    ]
    for f, a, b, exact, m2 in cases:
        errs = []
        for m in (8, 16, 32, 64):
            e = exact - trapezoidal_rule(f, a, b, m)
            h = (b - a) / m
            assert abs(e) <= (b - a) * h * h / 12 * m2 * (1 + 1e-9)
            errs.append(e)
        for p in order(errs):
            assert 1.95 < p < 2.05


def test_asymptotic_error_constant() -> None:
    # E ~ -h^2/12 (f'(b) - f'(a))
    for m in (16, 64):
        h = 1.0 / m
        e = math.e - 1 - trapezoidal_rule(math.exp, 0.0, 1.0, m)
        est = -h * h / 12 * (math.e - 1)
        assert abs(e / est - 1) < 2 * h * h


def test_periodic_geometric_convergence() -> None:
    f = lambda x: math.exp(math.cos(x))  # noqa: E731
    exact = 2 * math.pi * I0_1
    for m in (4, 8, 12, 16, 24):
        e = abs(exact - trapezoidal_rule(f, 0.0, 2 * math.pi, m))
        # Trefethen-Weideman bound 4 pi M / (e^(alpha m) - 1), M = e^cosh(alpha)
        bound = min(
            4 * math.pi * math.exp(math.cosh(al)) / math.expm1(al * m)
            for al in [k / 20 for k in range(1, 100)]
        )
        assert e <= bound + 1e-14
    assert abs(exact - trapezoidal_rule(f, 0.0, 2 * math.pi, 16)) < 1e-14


def test_function_evaluations() -> None:
    for m in (1, 2, 5, 100):
        g, calls = counted(math.sin)
        trapezoidal_rule(g, 0.0, 1.0, m)
        assert calls[0] == m + 1


def test_edges() -> None:
    assert trapezoidal_rule(math.exp, 2.0, 2.0, 5) == 0.0
    fw = trapezoidal_rule(math.exp, 0.0, 1.0, 10)
    bw = trapezoidal_rule(math.exp, 1.0, 0.0, 10)
    assert abs(fw + bw) < 1e-15
    assert trapezoidal_rule(math.exp, 0.0, 2.0, 1) == pytest.approx(1 + math.exp(2.0))
    with pytest.raises(ValueError):
        trapezoidal_rule(math.exp, 0.0, 1.0, 0)


def test_jump_kink_and_endpoint_singularity() -> None:
    c = 1 / 3
    for m in (10, 100, 1000):
        h = 1.0 / m
        e_jump = (1 - c) - trapezoidal_rule(lambda x: 1.0 if x > c else 0.0, 0.0, 1.0, m)
        assert abs(e_jump) <= h / 2 + 1e-15
        e_kink = (c * c + (1 - c) ** 2) / 2 - trapezoidal_rule(lambda x: abs(x - c), 0.0, 1.0, m)
        assert abs(e_kink) <= h * h / 4 + 1e-15
    errs = [2 / 3 - trapezoidal_rule(math.sqrt, 0.0, 1.0, m) for m in (256, 512, 1024, 2048)]
    for p in order(errs):
        assert 1.45 < p < 1.55


def test_long_sum_is_accurate() -> None:
    # 10^5 terms of 0.1: the fsum keeps the rounding error at the level of u.
    t = trapezoidal_rule(lambda x: 0.1, 0.0, 1.0, 100000)
    assert abs(t - 0.1) <= 4e-17
