# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heuns-method/. The authors are listed in prov/G2M62V.jsonl.

import math
import random
from fractions import Fraction

import pytest

from heuns_method import (TABLEAU_A, TABLEAU_B, TABLEAU_C, heuns_method,
                          stability_function, step_count)


def f_quad(t, y):
    return -2 * t * y * y  # exact solution 1/(1 + t^2) for y(0) = 1


def test_worked_example_table():
    r = heuns_method(f_quad, 0.0, 1.0, 1.0, 0.2, keep_path=True)
    want = [1.0, 0.96, 0.860298, 0.735043, 0.611572, 0.503338]
    assert [round(y, 6) for _, y in r.path] == want
    assert r.steps == 5 and r.f_evals == 10 and r.t == 1.0


def test_observed_order_two():
    errs = [abs(heuns_method(f_quad, 0.0, 1.0, 1.0, 0.2 / 2 ** k).y - 0.5) for k in range(1, 7)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert all(abs(p - 2) < 0.05 for p in orders)


def test_logistic_order_two():
    exact = 0.1 * math.e / (0.9 + 0.1 * math.e)
    g = lambda t, y: y * (1 - y)
    errs = [abs(heuns_method(g, 0.0, 0.1, 1.0, 1 / n).y - exact) for n in (10, 20, 40, 80)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(abs(p - 2) < 0.05 for p in orders)


def test_order_conditions_exact():
    b, c, A = TABLEAU_B, TABLEAU_C, TABLEAU_A
    assert all(sum(row) == ci for row, ci in zip(A, c))  # row-sum condition
    assert sum(b) == 1  # order 1
    assert sum(bi * ci for bi, ci in zip(b, c)) == Fraction(1, 2)  # order 2
    # the two order-3 conditions fail, so the order is exactly 2
    assert sum(bi * ci * ci for bi, ci in zip(b, c)) != Fraction(1, 3)
    bac = sum(b[i] * A[i][j] * c[j] for i in range(2) for j in range(2))
    assert bac != Fraction(1, 6)


def test_test_equation_exact_random():
    rng = random.Random(20241108)
    for _ in range(300):
        lam = Fraction(rng.randint(-40, 40), rng.randint(1, 8))
        h = Fraction(1, rng.randint(1, 12))
        n = rng.randint(0, 12)
        y0 = Fraction(rng.randint(-9, 9), rng.randint(1, 5))
        r = heuns_method(lambda t, y: lam * y, Fraction(0), y0, n * h, h)
        assert r.y == stability_function(h * lam) ** n * y0
        assert r.steps == n and r.f_evals == 2 * n


def test_linear_system_matches_truncated_exponential():
    # y' = A y with A = [[0, 1], [-1, 0]]; one step multiplies by I + hA + (hA)^2/2.
    h = Fraction(1, 7)
    M = [[1 - h * h / 2, h], [-h, 1 - h * h / 2]]
    y = [Fraction(3), Fraction(-2)]
    want = list(y)
    for _ in range(9):
        want = [M[0][0] * want[0] + M[0][1] * want[1], M[1][0] * want[0] + M[1][1] * want[1]]
    r = heuns_method(lambda t, u: [u[1], -u[0]], Fraction(0), y, 9 * h, h)
    assert r.y == want


def test_harmonic_oscillator_energy_factor():
    # |R(i h)|^2 = 1 + h^4/4 exactly, so the energy grows by that factor per step.
    h = Fraction(1, 5)
    r = heuns_method(lambda t, u: [u[1], -u[0]], Fraction(0), [Fraction(1), Fraction(0)], 4 * h, h)
    assert r.y[0] ** 2 + r.y[1] ** 2 == (1 + h ** 4 / 4) ** 4
    rf = heuns_method(lambda t, u: [u[1], -u[0]], 0.0, [1.0, 0.0], 10.0, 0.1)
    assert abs(rf.y[0] ** 2 + rf.y[1] ** 2 - (1 + 0.1 ** 4 / 4) ** 100) < 1e-12


def test_global_error_bound_holds():
    # |e_n| <= C h^2 (exp(Lam (t_n - t0)) - 1)/Lam with C = M3/12 + L M2/4 on y' = -y.
    L, h = 1.0, 0.1
    M2 = M3 = 1.0
    lam_ = L * (1 + h * L / 2)
    C = M3 / 12 + L * M2 / 4
    r = heuns_method(lambda t, y: -y, 0.0, 1.0, 3.0, h, keep_path=True)
    for t, y in r.path:
        assert abs(math.exp(-t) - y) <= C * h * h * (math.exp(lam_ * t) - 1) / lam_ + 1e-15


def test_zero_steps_long_step_and_off_grid_end():
    r = heuns_method(f_quad, 0.0, 1.0, 0.0, 0.1)
    assert r.steps == 0 and r.f_evals == 0 and r.y == 1.0
    r = heuns_method(lambda t, y: y, Fraction(0), Fraction(1), Fraction(1, 2), Fraction(3))
    assert r.steps == 1 and r.t == Fraction(1, 2) and r.y == stability_function(Fraction(1, 2))
    r = heuns_method(lambda t, y: y, Fraction(0), Fraction(1), Fraction(7, 10), Fraction(1, 4))
    assert r.steps == 3 and r.t == Fraction(7, 10)
    q = Fraction(1, 4)
    assert r.y == stability_function(q) ** 2 * stability_function(Fraction(1, 5))
    r = heuns_method(f_quad, 0.0, 1.0, 0.7, 0.1, keep_path=True)
    assert r.steps == 7 and r.t == 0.7


def test_rounded_step_counts_and_errors():
    assert step_count(0.0, 0.3, 0.1) == 3
    assert step_count(Fraction(0), Fraction(1), Fraction(1, 3)) == 3
    with pytest.raises(ValueError):
        step_count(0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        step_count(1.0, 0.0, 0.1)


def test_stiff_problem_step_limit():
    g = lambda t, y: -50 * y
    # z = h lambda: |R(z)| <= 1 exactly for -2 <= z <= 0.
    assert stability_function(Fraction(-2)) == 1
    above = heuns_method(g, Fraction(0), Fraction(1), Fraction(1), Fraction(1, 24))
    below = heuns_method(g, Fraction(0), Fraction(1), Fraction(1), Fraction(1, 26))
    assert above.y == stability_function(Fraction(-50, 24)) ** 24 and above.y > 7
    assert below.y == stability_function(Fraction(-50, 26)) ** 26 and below.y < Fraction(1, 7)
    assert abs(heuns_method(g, 0.0, 1.0, 1.0, 0.05).y - 1.625 ** 20) < 1e-6 * 1.625 ** 20
    assert abs(heuns_method(g, 0.0, 1.0, 1.0, 0.025).y - 0.53125 ** 40) < 1e-20


def test_vector_input_is_not_mutated():
    y0 = [1.0, 0.0]
    heuns_method(lambda t, y: [y[1], -y[0]], 0.0, y0, 1.0, 0.1)
    assert y0 == [1.0, 0.0]
