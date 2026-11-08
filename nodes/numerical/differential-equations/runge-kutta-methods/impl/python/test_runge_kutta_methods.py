# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-methods/. The authors are listed in prov/EV2XHR.jsonl.

import math
from fractions import Fraction

import pytest

from runge_kutta_methods import (EULER, HEUN, KUTTA3, MIDPOINT, RK4, RULE38, Tableau, order,
                                 order_conditions, rk_step, runge_kutta, stability_polynomial,
                                 step_count)

F = Fraction


def f_quad(t, y):
    return -2 * t * y * y  # y(t) = 1/(1 + t^2) for y(0) = 1


def test_worked_example_rk4():
    r = runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.2, RK4, keep_path=True)
    want = [1.0, 0.96153275, 0.86205242, 0.73527834, 0.60975183, 0.50000720]
    assert [round(y, 8) for _, y in r.path] == want
    assert r.steps == 5 and r.f_evals == 20 and r.t == 1.0


@pytest.mark.parametrize("tab,p", [(EULER, 1), (HEUN, 2), (MIDPOINT, 2), (KUTTA3, 3), (RK4, 4), (RULE38, 4)])
def test_observed_order(tab, p):
    errs = [abs(runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.1 / 2 ** k, tab).y - 0.5) for k in range(1, 5)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert abs(orders[-1] - p) < 0.1


@pytest.mark.parametrize("tab,p", [(EULER, 1), (HEUN, 2), (MIDPOINT, 2), (KUTTA3, 3), (RK4, 4), (RULE38, 4)])
def test_order_conditions_exact(tab, p):
    assert order(tab) == p


def test_rk4_conditions_values():
    for name, v, want in order_conditions(RK4):
        assert isinstance(v, Fraction) and v == want, name


def test_stability_polynomials_exact():
    assert stability_polynomial(RK4) == [F(1), F(1), F(1, 2), F(1, 6), F(1, 24)]
    assert stability_polynomial(RULE38) == [F(1), F(1), F(1, 2), F(1, 6), F(1, 24)]
    assert stability_polynomial(HEUN) == [F(1), F(1), F(1, 2)]
    assert stability_polynomial(EULER) == [F(1), F(1)]


def test_linear_problem_gives_stability_polynomial_exactly():
    lam, h = F(-3, 2), F(1, 4)
    z = h * lam
    R = sum(c * z ** k for k, c in enumerate(stability_polynomial(RK4)))
    r = runge_kutta(lambda t, y: lam * y, F(0), F(1), F(2), h, RK4)
    assert r.y == R ** 8


def test_stiff_problem_explicit_fails():
    lam = -10.0  # stability limit of RK4 on the negative axis is about -2.785
    ok = runge_kutta(lambda t, y: lam * y, 0.0, 1.0, 10.0, 0.27, RK4).y
    bad = runge_kutta(lambda t, y: lam * y, 0.0, 1.0, 10.0, 0.3, RK4).y
    assert abs(ok) < 0.01 and abs(bad) > 1e4


def test_harmonic_oscillator_vector():
    f = lambda t, y: [y[1], -y[0]]
    r = runge_kutta(f, 0.0, [1.0, 0.0], 2 * math.pi, 2 * math.pi / 64, RK4)
    assert abs(r.y[0] - 1) < 1e-5 and abs(r.y[1]) < 1e-5
    # RK4 is not symplectic: the energy decays like |R(ih)|^(2N) < 1
    h = 2 * math.pi / 64
    R = complex(1 - h ** 2 / 2 + h ** 4 / 24, h - h ** 3 / 6)
    assert abs(r.y[0] ** 2 + r.y[1] ** 2 - abs(R) ** 128) < 1e-12


def test_linear_system_matrix_exponential():
    # y' = A y with A = [[0, 1], [0, 0]]: exp(tA) = [[1, t], [0, 1]], polynomial, so RK4 is exact
    f = lambda t, y: [y[1], 0.0]
    r = runge_kutta(f, 0.0, [1.0, 2.0], 3.0, 0.7, RK4)
    assert abs(r.y[0] - 7.0) < 1e-12 and r.y[1] == 2.0


def test_logistic():
    f = lambda t, y: y * (1 - y)
    exact = 1 / (1 + 9 * math.exp(-5.0))
    assert abs(runge_kutta(f, 0.0, 0.1, 5.0, 0.05, RK4).y - exact) < 1e-8


def test_edge_cases():
    r = runge_kutta(f_quad, 0.0, 1.0, 0.0, 0.1)
    assert r.steps == 0 and r.f_evals == 0 and r.y == 1.0
    r = runge_kutta(f_quad, 0.0, 1.0, 0.3, 1.0)  # h larger than the interval: one step
    assert r.steps == 1 and r.t == 0.3
    r = runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.3, keep_path=True)  # last step 0.1
    assert r.steps == 4 and abs(r.path[-2][0] - 0.9) < 1e-15 and r.t == 1.0
    assert step_count(0.0, 1.0, 0.1) == 10
    with pytest.raises(ValueError):
        runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        runge_kutta(f_quad, 1.0, 1.0, 0.0, 0.1)
    with pytest.raises(ValueError):
        rk_step(f_quad, 0.0, 1.0, 0.1, Tableau([[F(1)]], [F(1)], [F(1)]))
    with pytest.raises(ValueError):
        order(Tableau([[F(0), F(0)], [F(1), F(0)]], [F(1, 2), F(1, 2)], [F(0), F(1, 2)]))
