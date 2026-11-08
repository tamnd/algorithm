# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-quadrature/. The authors are listed in prov/AB3WK9.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from adaptive_quadrature import adaptive_quadrature, adaptive_simpson_local


def poly_eval(c, x):
    s = 0.0
    for a in reversed(c):
        s = s * x + a
    return s


def poly_integral_exact(c, a, b):
    """Oracle: exact integral of sum c[k] x^k over [a, b] in rational arithmetic."""
    a, b = F(a), F(b)
    return sum(F(ck) * (b ** (k + 1) - a ** (k + 1)) / (k + 1) for k, ck in enumerate(c))


def besseli0(x):
    s, t, k = 0.0, 1.0, 0
    while t > 1e-18:
        s += t
        k += 1
        t = (x / 2) ** (2 * k) / math.factorial(k) ** 2
    return s


def test_worked_example_trace():
    r = adaptive_quadrature(math.sqrt, 0.0, 1.0, 3e-6)
    assert r.converged
    assert r.evaluations == 37
    assert abs(r.value - 0.66666032) < 1e-8
    assert abs(r.error_estimate - 2.012e-6) < 1e-9
    # the estimate is a heuristic: here it is about three times too small
    assert abs(r.value - 2 / 3) > r.error_estimate


def test_degree_of_the_returned_rule():
    # with a huge tolerance there is no split, so the value is one panel of Q = S2 + (S2 - S1)/15
    for k in range(0, 8):
        r = adaptive_quadrature(lambda x, k=k: x ** k, 0.0, 1.0, tau=1e300)
        assert r.evaluations == 5
        exact = 1.0 / (k + 1)
        if k <= 5:
            assert abs(r.value - exact) < 1e-15
        else:
            assert abs(r.value - exact) > 1e-6


def test_cubics_need_no_split():
    rng = random.Random(11)
    for _ in range(200):
        c = [rng.uniform(-5, 5) for _ in range(4)]
        a = rng.uniform(-3, 3)
        b = a + rng.uniform(0.1, 4)
        r = adaptive_quadrature(lambda x: poly_eval(c, x), a, b, tau=1e-8)
        assert r.evaluations == 5
        ex = float(poly_integral_exact(c, a, b))
        assert abs(r.value - ex) <= 1e-12 * (1 + abs(ex))


def test_random_polynomials_against_exact_integral():
    rng = random.Random(2024)
    for _ in range(500):
        deg = rng.randint(0, 9)
        c = [rng.randint(-9, 9) for _ in range(deg + 1)]
        a = rng.randint(-4, 3)
        b = a + rng.randint(1, 3)
        ex = float(poly_integral_exact(c, a, b))
        r = adaptive_quadrature(lambda x: poly_eval(c, x), float(a), float(b), tau=1e-11 * (1 + abs(ex)))
        assert r.converged
        assert abs(r.value - ex) <= 1e-8 * (1 + abs(ex))


@pytest.mark.parametrize("f,a,b,exact", [
    (math.exp, 0.0, 1.0, math.e - 1),
    (math.sin, 0.0, math.pi, 2.0),
    (lambda x: 1 / (1 + x * x), 0.0, 1.0, math.pi / 4),
    (math.sqrt, 0.0, 1.0, 2 / 3),
    (math.log, 1.0, math.e, 1.0),
    (lambda x: math.exp(math.cos(x)), 0.0, 2 * math.pi, 2 * math.pi * besseli0(1.0)),
    (lambda x: math.cos(50 * x), 0.0, 1.0, math.sin(50.0) / 50),
    (lambda x: abs(x - 1 / 3), 0.0, 1.0, 5 / 18),
])
def test_closed_forms(f, a, b, exact):
    r = adaptive_quadrature(f, a, b, 1e-11)
    assert r.converged
    assert abs(r.value - exact) < 1e-9


def test_jump_converges_slowly_but_converges():
    r = adaptive_quadrature(lambda x: 1.0 if x > 1 / 3 else 0.0, 0.0, 1.0, 1e-10)
    assert r.converged
    assert abs(r.value - 2 / 3) < 1e-8


def test_empty_and_reversed_interval():
    assert adaptive_quadrature(math.exp, 2.0, 2.0) == (0.0, 0.0, 0, True)
    r1 = adaptive_quadrature(math.exp, 0.0, 1.0, 1e-10)
    r2 = adaptive_quadrature(math.exp, 1.0, 0.0, 1e-10)
    assert r2.value == -r1.value and r2.evaluations == r1.evaluations


def test_evaluation_count_formula():
    for tau in (1e-4, 1e-7, 1e-10):
        r = adaptive_quadrature(math.sqrt, 0.0, 1.0, tau)
        assert r.evaluations % 4 == 1


def test_unreachable_tolerance_stops_at_budget():
    r = adaptive_quadrature(math.sqrt, 0.0, 1.0, tau=0.0, max_evals=2000)
    assert not r.converged
    assert r.evaluations <= 2000
    assert abs(r.value - 2 / 3) < 1e-11


def test_panel_too_small_to_split():
    # a jump between two neighbouring floats can never be resolved
    x0 = 0.1
    r = adaptive_quadrature(lambda x: 1e20 if x > x0 else 0.0, 0.0, 1.0, tau=1e-30, max_evals=10 ** 6)
    assert not r.converged
    assert r.evaluations < 10 ** 6


def test_endpoint_singularity_needs_a_transform():
    with pytest.raises(ZeroDivisionError):
        adaptive_quadrature(lambda x: x ** -0.5, 0.0, 1.0)
    # x = t^2 turns the integral of x^(-1/2) cos x into 2 * integral of cos(t^2)
    r = adaptive_quadrature(lambda t: 2 * math.cos(t * t), 0.0, 1.0, 1e-12)
    ref = adaptive_simpson_local(lambda t: 2 * math.cos(t * t), 0.0, 1.0, 1e-13)[0]
    assert abs(r.value - ref) < 1e-11


def test_infinite_interval_rejected():
    with pytest.raises(ValueError):
        adaptive_quadrature(math.exp, 0.0, math.inf)


def test_heuristic_can_be_fooled():
    spike = lambda x: math.exp(-(((x - 0.3) / 0.001) ** 2))
    r = adaptive_quadrature(spike, 0.0, 1.0, 1e-8)
    assert r.converged and r.value < 1e-20  # true value is about 1.77e-3
    p = lambda x: (x * (x - 0.25) * (x - 0.5) * (x - 0.75) * (x - 1)) ** 2
    r = adaptive_quadrature(p, 0.0, 1.0, 1e-12)
    assert r.value == 0.0 and r.evaluations == 5  # true value is positive


def test_observed_cost_rate():
    n1 = adaptive_quadrature(math.exp, 0.0, 1.0, 1e-6).evaluations
    n2 = adaptive_quadrature(math.exp, 0.0, 1.0, 1e-10).evaluations
    assert 4 <= n2 / n1 <= 20  # about (10^4)^(1/4) = 10


def test_local_variant_agrees():
    for f, ex in ((math.exp, math.e - 1), (math.sqrt, 2 / 3)):
        v, n = adaptive_simpson_local(f, 0.0, 1.0, 1e-10)
        assert abs(v - ex) < 1e-9 and n % 4 == 1
    assert adaptive_simpson_local(math.exp, 1.0, 1.0) == (0.0, 0)
