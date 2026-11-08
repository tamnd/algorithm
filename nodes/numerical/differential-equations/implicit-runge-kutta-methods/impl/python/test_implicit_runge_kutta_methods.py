# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-runge-kutta-methods/. The authors are listed in prov/W7X2PW.jsonl.

import math
import random
from fractions import Fraction

import pytest

from implicit_runge_kutta_methods import (METHODS, ORDERS, implicit_runge_kutta, lu_factor,
                                          lu_solve, stability_function, step_count, weights_d)


def f_quad(t, y):
    return -2 * t * y * y  # exact 1/(1 + t^2) for y(0) = 1


def j_quad(t, y):
    return -4 * t * y


IMPLICIT = ["backward-euler", "implicit-midpoint", "gauss2", "radau2a", "lobatto3a", "lobatto3c"]


@pytest.mark.parametrize("m", IMPLICIT)
def test_observed_orders(m):
    errs = [abs(implicit_runge_kutta(f_quad, 0.0, 1.0, 1.0, 1 / n, m, jac=j_quad).y - 0.5)
            for n in (10, 20, 40, 80)]
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert abs(orders[-1] - ORDERS[m]) < 0.05


def test_worked_example_gauss_and_radau():
    r = implicit_runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.2, "gauss2", jac=j_quad, keep_path=True)
    assert [round(v, 6) for _, v in r.path] == [1.0, 0.961534, 0.862057, 0.735281, 0.609747, 0.499994]
    r = implicit_runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.2, "radau2a", jac=j_quad, keep_path=True)
    assert [round(v, 6) for _, v in r.path] == [1.0, 0.961696, 0.862323, 0.735553, 0.609953, 0.50012]
    assert r.jac_evals == 5 and r.lu_factorizations == 5


def _trees(a, b, c):
    s = len(b)
    ac = [sum(a[i][j] * c[j] for j in range(s)) for i in range(s)]
    ac2 = [sum(a[i][j] * c[j] ** 2 for j in range(s)) for i in range(s)]
    aac = [sum(a[i][j] * ac[j] for j in range(s)) for i in range(s)]
    bs = lambda v: sum(b[i] * v[i] for i in range(s))
    return [(bs([1] * s), Fraction(1)), (bs(c), Fraction(1, 2)),
            (bs([x ** 2 for x in c]), Fraction(1, 3)), (bs(ac), Fraction(1, 6)),
            (bs([x ** 3 for x in c]), Fraction(1, 4)), (bs([c[i] * ac[i] for i in range(s)]), Fraction(1, 8)),
            (bs(ac2), Fraction(1, 12)), (bs(aac), Fraction(1, 24))]


def test_order_conditions_exact():
    counts = {1: 1, 2: 2, 3: 4, 4: 8}
    for m in ["backward-euler", "implicit-midpoint", "radau2a", "lobatto3a", "lobatto3c"]:
        a, b, c = METHODS[m]
        conds = _trees(a, b, c)
        p = ORDERS[m]
        assert all(lhs == rhs for lhs, rhs in conds[:counts[p]]), m
        if p < 4:
            assert any(lhs != rhs for lhs, rhs in conds[counts[p]:counts[p + 1]]), m
        assert all(sum(a[i]) == c[i] for i in range(len(b)))  # row sums


def test_gauss2_order_conditions_float():
    a, b, c = METHODS["gauss2"]
    for lhs, rhs in _trees(a, b, c):
        assert abs(lhs - rhs) < 1e-15


def test_stability_functions_exact():
    for z in [Fraction(-1), Fraction(-7, 3), Fraction(5, 2), Fraction(-1000)]:
        assert stability_function(z, "radau2a") == (1 + z / 3) / (1 - 2 * z / 3 + z * z / 6)
        assert stability_function(z, "lobatto3a") == (1 + z / 2 + z * z / 12) / (1 - z / 2 + z * z / 12)
        assert stability_function(z, "implicit-midpoint") == (1 + z / 2) / (1 - z / 2)
        assert stability_function(z, "lobatto3c") == 1 / (1 - z + z * z / 2)
    big = Fraction(-10 ** 9)
    assert abs(stability_function(big, "radau2a")) < Fraction(1, 10 ** 8)
    assert abs(stability_function(big, "lobatto3a") - 1) < Fraction(1, 10 ** 7)
    # R(infinity) = 1 - b^T A^(-1) 1 = 0 for the stiffly accurate radau2a
    a, b, _ = METHODS["radau2a"]
    assert 1 - sum(weights_d(a, b)) == 0
    assert weights_d(*METHODS["lobatto3a"][:2]) is None


def test_one_step_is_R_times_y_exactly():
    lam, h = Fraction(-3), Fraction(1, 4)
    r = implicit_runge_kutta(lambda t, y: lam * y, Fraction(0), Fraction(1), Fraction(1), h,
                             "radau2a", jac=lambda t, y: lam)
    assert r.y == stability_function(h * lam, "radau2a") ** 4


def test_symplectic_condition():
    for m in ["implicit-midpoint"]:
        a, b, _ = METHODS[m]
        s = len(b)
        assert all(b[i] * a[i][j] + b[j] * a[j][i] - b[i] * b[j] == 0 for i in range(s) for j in range(s))
    a, b, _ = METHODS["gauss2"]
    assert all(abs(b[i] * a[i][j] + b[j] * a[j][i] - b[i] * b[j]) < 1e-15 for i in range(2) for j in range(2))
    a, b, _ = METHODS["radau2a"]
    assert b[0] * a[0][0] * 2 - b[0] * b[0] != 0


def test_energy_conservation_gauss_vs_radau():
    f = lambda t, y: [y[1], -y[0]]
    jac = lambda t, y: [[0.0, 1.0], [-1.0, 0.0]]
    g = implicit_runge_kutta(f, 0.0, [1.0, 0.0], 100.0, 0.5, "gauss2", jac=jac)
    r = implicit_runge_kutta(f, 0.0, [1.0, 0.0], 100.0, 0.5, "radau2a", jac=jac)
    assert abs(g.y[0] ** 2 + g.y[1] ** 2 - 1) < 1e-12
    assert g.y[0] ** 2 + g.y[1] ** 2 > 0.999999999
    # Radau IIA damps: each step multiplies the energy by |R(i/2)|^2 < 1
    energy = r.y[0] ** 2 + r.y[1] ** 2
    assert abs(energy - abs(stability_function(0.5j, "radau2a")) ** 400) < 1e-9
    assert energy < 0.72


def test_stiff_problem_explicit_fails_implicit_works():
    lam = -1e6
    f = lambda t, y: lam * (y - math.cos(t)) - math.sin(t)
    jac = lambda t, y: lam
    ex = implicit_runge_kutta(f, 0.0, 0.0, 1.0, 0.1, "explicit-euler", jac=jac)
    assert abs(ex.y) > 1e40
    rd = implicit_runge_kutta(f, 0.0, 0.0, 1.0, 0.1, "radau2a", jac=jac)
    assert abs(rd.y - math.cos(1.0)) < 1e-8
    gs = implicit_runge_kutta(f, 0.0, 0.0, 1.0, 0.1, "gauss2", jac=jac)
    assert abs(gs.y - math.cos(1.0)) > 0.9  # A-stable but not L-stable: the jump survives
    assert rd.newton_iterations == 20 and rd.f_evals == 40


def test_vector_stiff_system_with_fd_jacobian():
    # y1' = -1000 y1 + y2, y2' = -y2: y2 = e^-t, y1 = e^-t/999 + (1 - 1/999) e^-1000t
    f = lambda t, y: [-1000 * y[0] + y[1], -y[1]]
    r = implicit_runge_kutta(f, 0.0, [1.0, 1.0], 1.0, 0.05, "radau2a")
    assert abs(r.y[1] - math.exp(-1)) < 1e-5
    assert abs(r.y[0] - math.exp(-1) / 999) < 1e-7
    assert r.jac_evals == 20


def test_edge_cases_grid():
    r = implicit_runge_kutta(f_quad, 0.0, 1.0, 0.0, 0.1, "gauss2", jac=j_quad)
    assert r.steps == 0 and r.y == 1.0 and r.f_evals == 0
    r = implicit_runge_kutta(f_quad, 0.0, 1.0, 0.3, 5.0, "radau2a", jac=j_quad)
    assert r.steps == 1 and r.t == 0.3
    r = implicit_runge_kutta(f_quad, 0.0, 1.0, 1.0, 0.3, "radau2a", jac=j_quad, keep_path=True)
    assert r.steps == 4 and [round(t, 12) for t, _ in r.path] == [0.0, 0.3, 0.6, 0.9, 1.0]
    assert step_count(0.0, 0.3, 0.1) == 3
    with pytest.raises(ValueError):
        step_count(0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        step_count(1.0, 0.0, 0.1)


def test_newton_failure_is_reported():
    with pytest.raises(RuntimeError):
        implicit_runge_kutta(lambda t, y: y * y, 0.0, 1.0, 2.0, 2.0, "backward-euler",
                             jac=lambda t, y: 2 * y)


def test_lu_random_systems():
    rng = random.Random(7)
    for n in range(1, 7):
        m = [[Fraction(rng.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            m[i][i] += 40
        x = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        rhs = [sum(m[i][j] * x[j] for j in range(n)) for i in range(n)]
        assert lu_solve(lu_factor(m), rhs) == x
