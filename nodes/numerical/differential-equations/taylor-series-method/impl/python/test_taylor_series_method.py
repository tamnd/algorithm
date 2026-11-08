# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taylor-series-method/. The authors are listed in prov/9A499S.jsonl.

import math
from fractions import Fraction as F

import pytest

from taylor_series_method import (Series, cos, exp, sin, step_count, taylor_coefficients,
                                  taylor_method, taylor_step)

riccati = lambda t, y: -2 * t * y * y  # y(0) = 1: y = 1/(1 + t^2)
osc = lambda t, y: [y[1], -y[0]]


def test_exact_coefficients():
    assert taylor_coefficients(lambda t, y: y, F(0), F(1), 6) == [F(1, math.factorial(k)) for k in range(7)]
    assert taylor_coefficients(lambda t, y: y * y, F(0), F(1), 6) == [1] * 7  # 1/(1 - t)
    assert taylor_coefficients(riccati, F(0), F(1), 8) == [1, 0, -1, 0, 1, 0, -1, 0, 1]
    co = taylor_coefficients(osc, F(0), [F(1), F(0)], 5)
    assert [c[0] for c in co] == [1, 0, F(-1, 2), 0, F(1, 24), 0]
    # y' = t: coefficients 0, 0, 1/2 from the series of t itself
    assert taylor_coefficients(lambda t, y: t, F(0), F(0), 3) == [0, 0, F(1, 2), 0]


def test_series_arithmetic_and_functions():
    s = Series([F(0), F(1), F(0), F(0), F(0)])
    assert exp(s).c == [F(1, math.factorial(k)) for k in range(5)]
    assert (1 / (1 - s)).c == [1, 1, 1, 1, 1]
    x = Series([0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    assert sin(x).c == pytest.approx([0, 1, 0, -1 / 6, 0, 1 / 120])
    assert cos(x).c == pytest.approx([1, 0, -1 / 2, 0, 1 / 24, 0])
    assert (s ** 3).c == [0, 0, 0, 1, 0]
    with pytest.raises(ZeroDivisionError):
        Series([F(1)]) / Series([F(0)])


def test_first_step_example():
    assert taylor_step(riccati, F(0), F(1), F(1, 5), 4) == F(2404, 2500)  # 1 - h^2 + h^4 = 0.9616


@pytest.mark.parametrize("p", [1, 2, 3, 4, 6])
def test_observed_order(p):
    errs = [abs(taylor_method(riccati, 0.0, 1.0, 1.0, h, p).y - 0.5) for h in (0.2, 0.1, 0.05, 0.025)]
    last = math.log2(errs[2] / errs[3])
    assert p - 0.15 < last < p + 0.3


def test_high_order_large_steps():
    r = taylor_method(osc, 0.0, [1.0, 0.0], 10.0, 1.0, 20)
    assert abs(r.y[0] - math.cos(10)) < 1e-14 and r.steps == 10
    r = taylor_method(lambda t, y: exp(-y), 0.0, 0.0, 1.0, 0.1, 6)  # y = ln(1 + t)
    assert abs(r.y - math.log(2)) < 1e-7
    r = taylor_method(lambda t, y: [y[1], -sin(y[0])], 0.0, [1.0, 0.0], 3.0, 0.1, 10)
    E = lambda q, p: p * p / 2 - math.cos(q)
    assert abs(E(*r.y) - E(1.0, 0.0)) < 1e-12


def test_stiff_explicit_failure_at_the_limit():
    # p = 4: R(z) = 1 + z + ... + z^4/24, real stability limit -2.785; z = -100 h
    ok = taylor_method(lambda t, y: -100 * y, 0.0, 1.0, 2.0, 0.025, 4)
    bad = taylor_method(lambda t, y: -100 * y, 0.0, 1.0, 2.0, 0.03, 4)
    assert abs(ok.y) < 1e-10 and abs(bad.y) > 1e6


def test_edge_cases():
    r = taylor_method(riccati, 0.0, 1.0, 0.0, 0.1, 4)
    assert r.steps == 0 and r.y == 1.0
    r = taylor_method(riccati, F(0), F(1), F(1, 5), F(3), 4)  # h larger than the interval
    assert r.steps == 1 and r.y == F(2404, 2500)
    r = taylor_method(riccati, 0.0, 1.0, 1.05, 0.1, 6)  # last step off the grid
    assert r.steps == 11 and abs(r.y - 1 / (1 + 1.05 ** 2)) < 1e-7
    assert step_count(0.0, 1.0, 0.1) == 10
    with pytest.raises(ValueError):
        taylor_method(riccati, 0.0, 1.0, 1.0, 0.1, 0)
    with pytest.raises(ValueError):
        taylor_method(riccati, 0.0, 1.0, 1.0, 0.0, 4)
    assert taylor_coefficients(riccati, 0.0, 1.0, 0) == [1.0]
