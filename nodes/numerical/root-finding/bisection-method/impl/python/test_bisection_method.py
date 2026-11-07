# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bisection-method/. The authors are listed in prov/QXCMB9.jsonl.

import math
import random
from fractions import Fraction

import pytest

from bisection_method import bisection

CUBIC_ROOT = 1.5213797068045676  # root of x^3 - x - 2


def cubic(x):
    return x ** 3 - x - 2


def test_worked_example_table():
    mids = []

    def g(x):
        mids.append(x)
        return cubic(x)

    bisection(g, 1.0, 2.0, tol=2.0 ** -11, max_iter=100)
    assert mids[2:12] == [1.5, 1.75, 1.625, 1.5625, 1.53125, 1.515625, 1.5234375,
                          1.51953125, 1.521484375, 1.5205078125]


def test_tolerance_and_evaluation_count():
    r = bisection(cubic, 1.0, 2.0, tol=1e-6)
    assert abs(r.root - CUBIC_ROOT) <= 1e-6
    assert r.iterations == 19 and r.evaluations == 21
    assert r.a <= CUBIC_ROOT <= r.b


def test_count_is_exact_for_dyadic_widths():
    for j in range(1, 40):
        r = bisection(lambda x: x - 0.3, 0.0, 2.0, tol=2.0 ** -j)
        expected = max(0, math.ceil(math.log2(2.0 / (2 * 2.0 ** -j))))
        assert r.iterations == expected
        assert r.evaluations == expected + 2


def test_bracket_is_kept_and_halves():
    seen = []
    a0, b0 = 0.0, 1.0
    f = lambda x: math.cos(x) - x
    r = bisection(f, a0, b0, tol=1e-9)
    for k in range(1, r.iterations + 1):
        rk = bisection(f, a0, b0, tol=0.0, max_iter=k)
        assert f(rk.a) > 0 > f(rk.b)
        seen.append(rk.b - rk.a)
    for w0, w1 in zip(seen, seen[1:]):
        assert w1 == w0 / 2
    assert abs(r.root - 0.7390851332151607) <= 1e-9


def test_root_at_endpoint():
    r = bisection(lambda x: x - 1.0, 1.0, 3.0)
    assert r.root == 1.0 and r.evaluations == 2
    r = bisection(lambda x: x - 3.0, 1.0, 3.0)
    assert r.root == 3.0


def test_exact_zero_at_midpoint():
    r = bisection(lambda x: x - 0.5, 0.0, 1.0, tol=1e-15)
    assert r.root == 0.5 and r.iterations == 1 and r.evaluations == 3


def test_no_sign_change_and_even_multiplicity():
    with pytest.raises(ValueError):
        bisection(lambda x: x * x + 1, -1.0, 1.0)
    with pytest.raises(ValueError):
        bisection(lambda x: (x - 0.3) ** 2, 0.0, 1.0)


def test_odd_multiplicity_three():
    r = bisection(lambda x: (x - 0.3) ** 3, 0.0, 1.0, tol=1e-6)
    assert abs(r.root - 0.3) <= 1e-5  # limited by rounding of (x - 0.3)**3 near the root


def test_max_iterations():
    r = bisection(cubic, 1.0, 2.0, tol=1e-12, max_iter=5)
    assert not r.converged and r.iterations == 5 and r.evaluations == 7
    assert r.a <= CUBIC_ROOT <= r.b


def test_zero_tolerance_terminates_at_adjacent_floats():
    exact = lambda x: float(Fraction(x) ** 2 - 2)  # never 0 at a float
    r = bisection(exact, 1.0, 2.0, tol=0.0)
    assert r.converged and r.iterations == 52
    assert math.nextafter(r.a, math.inf) == r.b
    r = bisection(cubic, 1.0, 2.0, tol=0.0)  # here the computed f hits 0 exactly
    assert r.converged and (r.a == r.b or math.nextafter(r.a, math.inf) == r.b)
    assert r.iterations <= 53


def test_tiny_root_with_zero_tolerance_terminates():
    r = bisection(lambda x: x - 1e-300, 0.0, 1.0, tol=0.0)
    assert r.converged and abs(r.root - 1e-300) <= 1e-315


def test_nan_and_infinite_values():
    with pytest.raises(ValueError):
        bisection(lambda x: math.nan, 0.0, 1.0)
    with pytest.raises(ValueError):
        bisection(lambda x: math.nan if 0.4 < x < 0.6 else x - 0.5, 0.0, 1.0)
    r = bisection(lambda x: -math.inf if x == 0.0 else x - 0.25, 0.0, 1.0, tol=1e-12)
    assert abs(r.root - 0.25) <= 1e-12


def test_pole_is_found_instead_of_root():
    r = bisection(lambda x: 1.0 / (x - 1.0 / 3.0), 0.0, 1.0, tol=1e-12)
    assert abs(r.root - 1.0 / 3.0) <= 1e-12
    assert abs(1.0 / (r.root - 1.0 / 3.0)) > 1e10


def test_product_test_pitfall_is_avoided():
    # f(a) * f(c) underflows to 0 here, but the sign test still works
    r = bisection(lambda x: 1e-200 * (x - 0.7), 0.0, 1.0, tol=1e-12)
    assert abs(r.root - 0.7) <= 1e-12


def test_random_cubics_with_known_roots():
    rng = random.Random(1234)
    for _ in range(500):
        r0 = rng.uniform(-5, 5)
        lo, hi = r0 - rng.uniform(0.01, 3), r0 + rng.uniform(0.01, 3)
        c = rng.uniform(0.5, 4)  # x^2 + c > 0 keeps r0 the only real root
        f = lambda x: (x - r0) * (x * x + c)
        tol = 10.0 ** rng.randint(-12, -3)
        r = bisection(f, lo, hi, tol=tol)
        assert abs(r.root - r0) <= tol + 4e-16 * max(1.0, abs(r0))
        assert r.evaluations <= max(0, math.ceil(math.log2((hi - lo) / (2 * tol)))) + 2
