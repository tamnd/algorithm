# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/explicit-midpoint-method/. The authors are listed in prov/WJ3SQA.jsonl.

import math
import random
from fractions import Fraction

import pytest

from explicit_midpoint_method import (TABLEAU_A, TABLEAU_B, TABLEAU_C, explicit_midpoint_method,
                                      stability_function, step_count)


def f_quad(t, y):
    return -2 * t * y * y  # exact solution 1/(1 + t^2) for y(0) = 1


def test_worked_example_table():
    r = explicit_midpoint_method(f_quad, 0.0, 1.0, 1.0, 0.2, keep_path=True)
    want = [1.0, 0.96, 0.857738, 0.730096, 0.605852, 0.498088]
    assert [round(y, 6) for _, y in r.path] == want
    assert (r.steps, r.f_evals) == (5, 10)


def test_observed_order_two():
    errs = [abs(explicit_midpoint_method(f_quad, 0.0, 1.0, 1.0, 0.2 / 2 ** k).y - 0.5)
            for k in range(1, 6)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(4)]
    assert all(1.95 < p < 2.25 for p in orders)
    assert abs(orders[-1] - 2) < 0.05


def test_order_conditions_exactly():
    b, c, a = TABLEAU_B, TABLEAU_C, TABLEAU_A
    assert all(c[i] == sum(a[i]) for i in range(2))
    assert sum(b) == 1
    assert sum(bi * ci for bi, ci in zip(b, c)) == Fraction(1, 2)
    # the two conditions of order 3 fail, so the order is exactly 2
    assert sum(bi * ci * ci for bi, ci in zip(b, c)) != Fraction(1, 3)
    assert sum(b[i] * a[i][j] * c[j] for i in range(2) for j in range(2)) != Fraction(1, 6)


def test_exact_test_equation_random():
    rng = random.Random(4242)
    for _ in range(500):
        lam = Fraction(rng.randint(-30, 30), rng.randint(1, 6))
        h = Fraction(1, rng.randint(1, 10))
        n = rng.randint(0, 12)
        y0 = Fraction(rng.randint(-9, 9), rng.randint(1, 4))
        r = explicit_midpoint_method(lambda t, y: lam * y, Fraction(0), y0, n * h, h)
        z = h * lam
        assert r.y == y0 * (1 + z + z * z / 2) ** n
        assert stability_function(z) == 1 + z + z * z / 2


def test_time_dependent_quadrature_is_midpoint_rule():
    # y' = g(t) gives y_N = sum of h g(t_n + h/2), the composite midpoint rule
    h = Fraction(1, 4)
    r = explicit_midpoint_method(lambda t, y: t ** 3, Fraction(0), Fraction(0), Fraction(1), h)
    assert r.y == sum(h * (n * h + h / 2) ** 3 for n in range(4))


def test_harmonic_oscillator_energy_factor():
    h = Fraction(1, 5)
    r = explicit_midpoint_method(lambda t, y: [y[1], -y[0]], Fraction(0),
                                 [Fraction(1), Fraction(0)], 10 * h, h)
    assert r.y[0] ** 2 + r.y[1] ** 2 == (1 + h ** 4 / 4) ** 10


def test_vector_logistic_and_rotation():
    # logistic y' = y (1 - y), y(0) = 1/2: y(t) = 1/(1 + e^-t); rotation exact cos, sin
    f = lambda t, y: [y[0] * (1 - y[0]), y[2], -y[1]]
    r = explicit_midpoint_method(f, 0.0, [0.5, 1.0, 0.0], 2.0, 0.01)
    assert abs(r.y[0] - 1 / (1 + math.exp(-2))) < 1e-5
    assert abs(r.y[1] - math.cos(2)) < 1e-4 and abs(r.y[2] + math.sin(2)) < 1e-4


def test_edges():
    r = explicit_midpoint_method(f_quad, 0.0, 1.0, 0.0, 0.1)
    assert (r.steps, r.f_evals, r.y) == (0, 0, 1.0)
    r = explicit_midpoint_method(lambda t, y: y, 0.0, 1.0, 0.5, 3.0)
    assert r.steps == 1 and r.y == 1 + 0.5 + 0.125
    r = explicit_midpoint_method(lambda t, y: 2 * t, 0.0, 0.0, 1.0, 0.3)
    assert r.steps == 4 and r.t == 1.0 and abs(r.y - 1.0) < 1e-15
    assert step_count(0.0, 0.3, 0.1) == 3
    with pytest.raises(ValueError):
        explicit_midpoint_method(f_quad, 0.0, 1.0, 1.0, -0.1)


def test_stiff_limit():
    f = lambda t, y: -50.0 * y
    assert abs(explicit_midpoint_method(f, 0.0, 1.0, 1.0, 0.05).y - 1.625 ** 20) < 1e-6
    assert abs(explicit_midpoint_method(f, 0.0, 1.0, 1.0, 0.04).y - 1.0) < 1e-12
    assert abs(explicit_midpoint_method(f, 0.0, 1.0, 1.0, 0.025).y) < 1e-10
