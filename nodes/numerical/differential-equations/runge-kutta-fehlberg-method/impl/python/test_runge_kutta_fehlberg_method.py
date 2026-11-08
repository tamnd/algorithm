# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/runge-kutta-fehlberg-method/. The authors are listed in prov/37PW24.jsonl.

import math
from fractions import Fraction as F

import pytest

from runge_kutta_fehlberg_method import A, B4, B5, C, E, rkf45, rkf45_step, tree_conditions


def f_quad(t, y):
    return -2 * t * y * y  # y = 1/(1 + t^2)


def test_tableau_row_sums_and_error_weights():
    assert all(sum(row) == c for row, c in zip(A, C))
    assert E == [F(1, 360), F(0), F(-128, 4275), F(-2197, 75240), F(1, 50), F(2, 55)]
    assert sum(E) == 0


def test_order_conditions_exact():
    c4 = tree_conditions(B4)
    assert all(v == w for _, v, w in c4[:8])  # order 4
    assert any(v != w for _, v, w in c4[8:])  # not order 5
    assert all(v == w for _, v, w in tree_conditions(B5))  # order 5


def test_worked_trace():
    r = rkf45(f_quad, 0.0, 1.0, 1.0, rtol=1e-6, atol=1e-6, h0=0.5, keep_path=True)
    assert r.accepted == 6 and r.rejected == 2 and r.f_evals == 48
    assert [round(t, 4) for t, _ in r.path] == [0.0, 0.2036, 0.3541, 0.5226, 0.6871, 0.8788, 1.0]
    assert abs(r.y - 0.5) < 1e-6 and r.t == 1.0


def test_tolerance_proportionality():
    errs = [abs(rkf45(f_quad, 0.0, 1.0, 2.0, rtol=tol, atol=tol).y - 0.2) for tol in (1e-5, 1e-7, 1e-9)]
    assert errs[0] < 1e-4 and errs[1] < 1e-6 and errs[2] < 1e-8
    assert errs[0] > errs[1] > errs[2]


def test_fixed_step_orders():
    # the fourth-order part, with fixed h, has observed order 4; the estimate is O(h^5)
    def run(h):
        t, y = 0.0, [1.0]
        n = round(1.0 / h)
        est_max = 0.0
        for _ in range(n):
            y, est = rkf45_step(f_quad, t, y, h)
            est_max = max(est_max, abs(est[0]))
            t += h
        return abs(y[0] - 0.5), est_max
    r = [run(0.2 / 2 ** k) for k in range(5)]
    orders = [math.log2(r[i][0] / r[i + 1][0]) for i in range(4)]
    est_orders = [math.log2(r[i][1] / r[i + 1][1]) for i in range(4)]
    assert orders == sorted(orders, reverse=True) and 3.9 < orders[-1] < 4.6  # tends to 4 from above
    assert all(abs(q - 5) < 0.2 for q in est_orders)


def test_exponential_and_vector():
    r = rkf45(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 2 * math.pi, rtol=1e-9, atol=1e-12)
    assert abs(r.y[0] - 1) < 1e-7 and abs(r.y[1]) < 1e-7
    r = rkf45(lambda t, y: -3 * y, 0.0, 1.0, 1.0, rtol=1e-8, atol=1e-12)
    assert abs(r.y - math.exp(-3)) < 1e-7


def test_logistic():
    r = rkf45(lambda t, y: y * (1 - y), 0.0, 0.1, 5.0, rtol=1e-8, atol=1e-10)
    assert abs(r.y - 1 / (1 + 9 * math.exp(-5.0))) < 1e-7


def test_stiff_steps_set_by_stability():
    lam = -1000.0
    g = lambda t, y: lam * (y - math.cos(t)) - math.sin(t)
    n3 = rkf45(g, 0.0, 1.0, 1.0, rtol=1e-3, atol=1e-3).accepted
    n6 = rkf45(g, 0.0, 1.0, 1.0, rtol=1e-6, atol=1e-6).accepted
    assert 250 < n3 < 400 and 250 < n6 < 400  # about 1/(3.02/1000) whatever the tolerance


def test_edge_cases():
    r = rkf45(f_quad, 0.0, 1.0, 0.0)
    assert r.accepted == 0 and r.f_evals == 0 and r.y == 1.0
    r = rkf45(f_quad, 0.0, 1.0, 0.3, h0=10.0)  # h larger than the interval
    assert r.t == 0.3 and abs(r.y - 1 / 1.09) < 1e-5
    with pytest.raises(ValueError):
        rkf45(f_quad, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        rkf45(f_quad, 0.0, 1.0, 1.0, rtol=0.0, atol=0.0)
    with pytest.raises(RuntimeError):
        rkf45(lambda t, y: 1.0 / (1.0 - t), 0.0, 0.0, 2.0, max_steps=2000)
