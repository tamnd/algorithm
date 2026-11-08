# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/euler-method/. The authors are listed in prov/P0J8GY.jsonl.

import math
import random
from fractions import Fraction

import pytest

from euler_method import euler_method, step_count


def f_quad(t, y):
    return -2 * t * y * y  # exact solution 1/(1 + t^2) for y(0) = 1


def test_worked_example_table():
    r = euler_method(f_quad, 0.0, 1.0, 1.0, 0.2, keep_path=True)
    want = [1.0, 1.0, 0.92, 0.784576, 0.636842, 0.507060]
    assert [round(y, 6) for _, y in r.path] == want
    assert r.steps == 5 and r.f_evals == 5 and r.t == 1.0


def test_observed_order_one():
    errs = []
    for k in range(1, 6):
        h = 0.2 / 2 ** k
        errs.append(abs(euler_method(f_quad, 0.0, 1.0, 1.0, h).y - 0.5))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert all(abs(p - 1) < 0.05 for p in orders)


def test_exact_arithmetic_on_test_equation_random():
    rng = random.Random(20240601)
    for _ in range(500):
        lam = Fraction(rng.randint(-40, 40), rng.randint(1, 8))
        h = Fraction(1, rng.randint(1, 12))
        n = rng.randint(0, 15)
        y0 = Fraction(rng.randint(-9, 9), rng.randint(1, 5))
        r = euler_method(lambda t, y: lam * y, Fraction(0), y0, n * h, h)
        assert r.steps == n
        assert r.y == y0 * (1 + h * lam) ** n


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def test_linear_system_matches_matrix_power():
    rng = random.Random(7)
    for _ in range(100):
        a = [[Fraction(rng.randint(-5, 5), 2) for _ in range(2)] for _ in range(2)]
        h = Fraction(1, rng.randint(2, 6))
        n = rng.randint(0, 8)
        m = [[1 + h * a[0][0], h * a[0][1]], [h * a[1][0], 1 + h * a[1][1]]]
        p = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
        for _ in range(n):
            p = matmul(m, p)
        y0 = [Fraction(1), Fraction(-2)]
        f = lambda t, y: [a[0][0] * y[0] + a[0][1] * y[1], a[1][0] * y[0] + a[1][1] * y[1]]
        r = euler_method(f, Fraction(0), y0, n * h, h)
        assert r.y == [p[0][0] - 2 * p[0][1], p[1][0] - 2 * p[1][1]]


def test_harmonic_oscillator_energy_grows_by_one_plus_h_squared():
    h = Fraction(1, 10)
    f = lambda t, y: [y[1], -y[0]]
    r = euler_method(f, Fraction(0), [Fraction(1), Fraction(0)], 20 * h, h)
    assert r.y[0] ** 2 + r.y[1] ** 2 == (1 + h * h) ** 20


def test_error_bound_holds_at_every_step():
    lam, L, m2 = -1.0, 1.0, 1.0
    for h in (0.5, 0.25, 0.1, 0.01):
        r = euler_method(lambda t, y: lam * y, 0.0, 1.0, 2.0, h, keep_path=True)
        for t, y in r.path:
            bound = h * m2 / (2 * L) * (math.exp(L * t) - 1)
            assert abs(math.exp(-t) - y) <= bound + 1e-15


def test_zero_steps_and_long_step_and_off_grid_end():
    r = euler_method(f_quad, 0.0, 1.0, 0.0, 0.1)
    assert (r.steps, r.f_evals, r.y, r.t) == (0, 0, 1.0, 0.0)
    r = euler_method(lambda t, y: y, 0.0, 1.0, 0.5, 2.0)
    assert r.steps == 1 and r.y == 1.5
    r = euler_method(lambda t, y: 1.0, 0.0, 0.0, 1.0, 0.3, keep_path=True)
    assert r.steps == 4 and r.t == 1.0 and abs(r.y - 1.0) < 1e-15
    assert abs(r.path[-1][0] - r.path[-2][0] - 0.1) < 1e-15


def test_rounded_step_counts():
    assert step_count(0.0, 0.3, 0.1) == 3
    assert step_count(0.0, 0.7, 0.1) == 7
    assert step_count(Fraction(0), Fraction(1), Fraction(1, 3)) == 3
    with pytest.raises(ValueError):
        step_count(0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        step_count(1.0, 0.0, 0.1)


def test_stiff_problem_explicit_step_limit():
    f = lambda t, y: -50.0 * y
    assert abs(euler_method(f, 0.0, 1.0, 1.0, 0.05).y - 1.5 ** 20) < 1e-6
    assert abs(euler_method(f, 0.0, 1.0, 1.0, 0.04).y + 1.0) < 1e-12
    assert abs(euler_method(f, 0.0, 1.0, 1.0, 0.025).y) < 1e-20


def test_vector_input_is_not_mutated():
    y0 = [1.0, 0.0]
    euler_method(lambda t, y: [y[1], -y[0]], 0.0, y0, 1.0, 0.1)
    assert y0 == [1.0, 0.0]
