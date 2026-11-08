# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosenbrock-methods/. The authors are listed in prov/B4P23E.jsonl.

import math
from fractions import Fraction as F

import pytest

from rosenbrock_methods import (LINEARLY_IMPLICIT_EULER, ROS2, ROS2_HALF, ROW3_HALF, order_condition_residuals,
                                rosenbrock, stability_function, w_order2_residual)

ROB = lambda t, y: [-0.04 * y[0] + 1e4 * y[1] * y[2], 0.04 * y[0] - 1e4 * y[1] * y[2] - 3e7 * y[1] ** 2,
                    3e7 * y[1] ** 2]
ROB_J = lambda t, y: [[-0.04, 1e4 * y[2], 1e4 * y[1]], [0.04, -1e4 * y[2] - 6e7 * y[1], -1e4 * y[1]],
                      [0.0, 6e7 * y[1], 0.0]]
ROB_REF = [0.7158270687193, 9.185534764e-6, 0.2841637457]
ZERO3 = lambda t, y: [0.0, 0.0, 0.0]


def test_order_conditions_exact():
    assert order_condition_residuals(LINEARLY_IMPLICIT_EULER)[:1] == [0]
    assert order_condition_residuals(LINEARLY_IMPLICIT_EULER)[1] != 0
    r = order_condition_residuals(ROS2_HALF)
    assert r[:2] == [0, 0] and r[2] != 0
    assert order_condition_residuals(ROW3_HALF) == [0, 0, 0, 0]
    assert all(abs(x) < 1e-15 for x in order_condition_residuals(ROS2)[:2])
    assert w_order2_residual(ROS2_HALF) == 0 and abs(w_order2_residual(ROS2)) < 1e-15
    assert w_order2_residual(LINEARLY_IMPLICIT_EULER) == F(-1, 2)


def test_stability_functions_exact():
    for z in (F(-3), F(1, 5), F(-7, 2), F(10 ** 9)):
        assert stability_function(LINEARLY_IMPLICIT_EULER, z) == 1 / (1 - z)
        assert stability_function(ROS2_HALF, z) == (1 + z / 2) / (1 - z / 2)  # the trapezoidal rule
        assert stability_function(ROW3_HALF, z) == (1 - z / 2 - z ** 2 / 4 + z ** 3 / 24) / (1 - z / 2) ** 3
    g = ROS2.g
    for z in (-3.0, 0.2, -50.0):
        assert abs(stability_function(ROS2, z) - (1 + (1 - 2 * g) * z) / (1 - g * z) ** 2) < 1e-14
    assert abs(stability_function(ROS2, -1e12)) < 1e-11  # L-stable
    assert abs(stability_function(ROW3_HALF, F(-10 ** 12)) + F(1, 3)) < F(1, 10 ** 10)
    for m in (LINEARLY_IMPLICIT_EULER, ROS2, ROS2_HALF, ROW3_HALF):
        assert all(abs(stability_function(m, complex(-x, y))) <= 1 + 1e-12
                   for x in (0.0, 0.3, 4.0) for y in (0.05, 0.7, 3.0, 40.0))


def test_observed_orders_and_w_property():
    f = lambda t, y: y * math.cos(t)
    jac = lambda t, y: math.cos(t)
    dfdt = lambda t, y: -y * math.sin(t)
    exact = math.exp(math.sin(2.0))

    def orders(m, **kw):
        e = [abs(rosenbrock(f, 0, 1.0, 2.0, h, m, **kw).y - exact) for h in (0.05, 0.025, 0.0125)]
        return [math.log2(e[i] / e[i + 1]) for i in range(2)]

    assert all(abs(q - 1) < 0.2 for q in orders(LINEARLY_IMPLICIT_EULER, jac=jac, dfdt=dfdt))
    assert all(abs(q - 2) < 0.15 for q in orders(ROS2, jac=jac, dfdt=dfdt))
    assert all(abs(q - 3) < 0.15 for q in orders(ROW3_HALF, jac=jac, dfdt=dfdt))
    assert all(abs(q - 2) < 0.15 for q in orders(ROS2))  # finite-difference J and f_t
    assert all(abs(q - 2) < 0.2 for q in orders(ROS2, jac=lambda t, y: 0.0))  # W-method: any J
    assert all(q < 2.5 for q in orders(ROW3_HALF, jac=lambda t, y: 0.0))  # not a W-method of order 3


def test_stiff_curtiss_hirschfelder():
    g = lambda t, y: -50 * (y - math.cos(t))
    ex = (2500 * math.cos(1.2) + 50 * math.sin(1.2)) / 2501 - 2500 / 2501 * math.exp(-60)
    e_l = abs(rosenbrock(g, 0, 0.0, 1.2, 0.4, ROS2).y - ex)
    e_a = abs(rosenbrock(g, 0, 0.0, 1.2, 0.4, ROS2_HALF).y - ex)
    assert e_l < 0.05 and e_a > 0.3  # R(-20) is about 0.04 for ROS2 but -0.82 for g = 1/2


def test_robertson_with_graded_steps_and_invariant():
    for m, tol in ((ROS2, 1e-4), (ROW3_HALF, 1e-6)):
        y, t = [1.0, 0.0, 0.0], 0.0
        for T, h in ((1e-3, 1e-5), (1.0, 1e-3), (40.0, 0.1)):
            r = rosenbrock(ROB, t, y, T, h, m, jac=ROB_J, dfdt=ZERO3)
            y, t = r.y, r.t
            assert abs(sum(y) - 1) < 1e-12  # linear invariants are preserved
        assert max(abs(a - b) / b for a, b in zip(y, ROB_REF)) < tol
    r = rosenbrock(ROB, 0.0, [1.0, 0.0, 0.0], 1.0, 0.01, ROS2, jac=ROB_J, dfdt=ZERO3)
    assert min(r.y) < 0  # a large first step from t = 0 lands on a wrong, negative state


def test_edge_cases():
    f = lambda t, y: -y
    r = rosenbrock(f, 2.0, 3.0, 2.0, 0.1)
    assert (r.steps, r.y, r.t) == (0, 3.0, 2.0)
    r = rosenbrock(f, 0.0, 1.0, 0.25, 10.0, LINEARLY_IMPLICIT_EULER, jac=lambda t, y: -1.0,
                   dfdt=lambda t, y: 0.0)
    assert r.steps == 1 and abs(r.y - 1 / 1.25) < 1e-15
    r = rosenbrock(f, 0.0, 1.0, 1.0, 0.3, ROW3_HALF, keep_path=True)
    assert r.steps == 4 and r.t == 1.0 and abs(r.path[-2][0] - 0.9) < 1e-15
    osc = lambda t, y: [y[1], -y[0]]
    rv = rosenbrock(osc, 0.0, [1.0, 0.0], 1.0, 0.01, ROS2)
    rs = rosenbrock(lambda t, y: -2 * y, 0.0, 1.0, 1.0, 0.01, ROS2)
    assert abs(rv.y[0] - math.cos(1)) < 1e-3 and abs(rs.y - math.exp(-2)) < 1e-3
    with pytest.raises(ValueError):
        rosenbrock(f, 0.0, 1.0, 1.0, -0.1)
    with pytest.raises(ValueError):
        rosenbrock(f, 1.0, 1.0, 0.0, 0.1)


def test_costs():
    osc = lambda t, y: [y[1], -y[0]]
    r = rosenbrock(osc, 0.0, [1.0, 0.0], 1.0, 0.25, ROW3_HALF, jac=lambda t, y: [[0.0, 1.0], [-1.0, 0.0]],
                   dfdt=lambda t, y: [0.0, 0.0])
    assert (r.steps, r.f_evals, r.solves, r.lu_factorizations, r.jac_evals) == (4, 12, 12, 4, 4)
    r = rosenbrock(osc, 0.0, [1.0, 0.0], 1.0, 0.25, ROW3_HALF)
    assert r.f_evals == (3 + 2 + 2) * 4  # s stages, d + 1 for J, 1 for f_t
