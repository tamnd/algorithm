# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delay-differential-solver/. The authors are listed in prov/J3P31B.jsonl.

import math
import random
from fractions import Fraction

import pytest

from delay_differential_solver import (breakpoints, dde_rk4, exact_unit_delay,
                                       hermite)


def neg_lag(t, y, z):
    return -z[0]


def one(s):
    return 1.0


def exact_linear(a, b, c, t):
    """Closed form of y' = a y(t) + b y(t - 1), y = c on [-1, 0], for 0 <= t <= 2."""
    if t <= 1:
        return c * (math.exp(a * t) * (1 + b / a) - b / a)
    s = t - 1
    y1 = exact_linear(a, b, c, 1.0)
    e = math.exp(a * s)
    return e * y1 + b * c * ((1 + b / a) * s * e - (b / a) * (e - 1) / a)


def test_worked_example_exact_fractions():
    r = dde_rk4(neg_lag, lambda s: Fraction(1), [Fraction(1)], Fraction(0),
                Fraction(4), Fraction(1, 2))
    assert r.y == Fraction(5, 24)
    assert [r.solution(Fraction(k)) for k in range(5)] == [
        1, 0, Fraction(-1, 2), Fraction(-1, 6), Fraction(5, 24)]
    for k in range(9):
        assert r.solution(Fraction(k, 2)) == exact_unit_delay(Fraction(k, 2))
    assert r.steps == 8 and r.f_evals == 4 * 8 + 1 and r.lookups == 1 + 2 * 8
    assert r.grid_breakpoints == [0, 1, 2, 3, 4]


def test_exact_solution_formula():
    # y' = -y(t - 1) checked on each piece by a central difference.
    for x in (0.3, 1.5, 2.25, 3.7, 6.4):
        d = 1e-5
        der = (exact_unit_delay(x + d) - exact_unit_delay(x - d)) / (2 * d)
        assert der == pytest.approx(-exact_unit_delay(x - 1), abs=1e-8)
    assert exact_unit_delay(Fraction(3)) == Fraction(-1, 6)


def test_hermite_reproduces_cubics():
    p = lambda t: 2 * t ** 3 - t ** 2 + 3 * t - 5
    dp = lambda t: 6 * t ** 2 - 2 * t + 3
    a, b = Fraction(1, 3), Fraction(7, 4)
    for k in range(11):
        s = a + (b - a) * Fraction(k, 10)
        assert hermite(a, [p(a)], [dp(a)], b, [p(b)], [dp(b)], s) == [p(s)]


def test_observed_order_four_with_breakpoints():
    errs = []
    for j in range(2, 7):
        r = dde_rk4(neg_lag, one, [1.0], 0.0, 10.0, 2.0 ** -j)
        errs.append(max(abs(r.solution(x / 8) - exact_unit_delay(x / 8))
                        for x in range(81)))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert all(3.8 < p < 4.8 for p in orders), orders


def test_order_two_without_breakpoints():
    errs, hs = [], []
    for m in (5, 11, 23, 47):
        h = 2 / (2 * m + 1)          # t = 1 falls in the middle of a step
        r = dde_rk4(neg_lag, one, [1.0], 0.0, 3.0, h, track_breakpoints=False)
        errs.append(max(abs(r.solution(x / 64) - exact_unit_delay(x / 64))
                        for x in range(193)))
        hs.append(h)
    orders = [math.log(errs[i] / errs[i + 1]) / math.log(hs[i] / hs[i + 1])
              for i in range(len(errs) - 1)]
    assert all(1.5 < p < 3.0 for p in orders), orders
    tracked = dde_rk4(neg_lag, one, [1.0], 0.0, 3.0, hs[0])
    assert abs(tracked.y - exact_unit_delay(3.0)) < 1e-14


def test_random_linear_against_closed_form():
    rng = random.Random(2024)
    for _ in range(500):
        a = rng.choice([-1, 1]) * rng.uniform(0.1, 2)
        b = rng.uniform(-2, 2)
        c = rng.uniform(-1, 1)
        h = rng.choice([1 / 8, 1 / 10, 0.07, 1 / 16, 0.03])
        T = rng.uniform(0.05, 2.0)
        r = dde_rk4(lambda t, y, z: a * y + b * z[0], lambda s: c, [1.0], 0.0, T, h)
        assert abs(r.y - exact_linear(a, b, c, T)) <= 60 * h ** 4
        assert r.t == T


def test_vector_two_delays_exact():
    # u' = -u(t - 1) and v' = -2 v(t - 1/2): v(t) = w(2t) with w' = -w(s - 1).
    f = lambda t, y, z: [-z[0][0], -2 * z[1][1]]
    r = dde_rk4(f, lambda s: [Fraction(1), Fraction(1)], [Fraction(1), Fraction(1, 2)],
                Fraction(0), Fraction(4), Fraction(1, 4))
    assert r.y[0] == Fraction(5, 24)
    assert r.solution(Fraction(2))[1] == Fraction(5, 24)
    assert r.solution(Fraction(3, 2))[1] == Fraction(-1, 6)
    assert Fraction(1, 2) in r.grid_breakpoints and Fraction(5, 2) in r.grid_breakpoints
    assert abs(float(r.y[1]) - exact_unit_delay(8.0)) < 1e-3


def test_hutchinson_stability_threshold():
    # y' = r y (1 - y(t - 1)): equilibrium 1 stable iff r < pi / 2.
    tails = {}
    for rr in (1.0, 2.0):
        r = dde_rk4(lambda t, y, z: rr * y * (1 - z[0]), lambda s: 0.5, [1.0],
                    0.0, 80.0, 0.05)
        tail = [r.solution(60 + x / 10) for x in range(201)]
        tails[rr] = max(tail) - min(tail)
    assert tails[1.0] < 1e-6
    assert tails[2.0] > 2.0


def test_breakpoint_set():
    assert breakpoints(0, 3, [1]) == [0, 1, 2, 3]
    assert breakpoints(0, 10, [1, 1.5])[:6] == [0, 1, 1.5, 2, 2.5, 3]
    assert breakpoints(Fraction(0), Fraction(5, 2), [Fraction(1)]) == [0, 1, 2, Fraction(5, 2)]


def test_zero_length_interval():
    r = dde_rk4(neg_lag, one, [1.0], 2.0, 2.0, 0.1)
    assert r.y == 1.0 and r.steps == 0 and r.f_evals == 0


def test_step_larger_than_interval_and_delay():
    big = dde_rk4(neg_lag, one, [1.0], 0.0, 2.5, 7.0)
    cap = dde_rk4(neg_lag, one, [1.0], 0.0, 2.5, 1.0)
    assert big.y == cap.y and big.steps == 3           # steps capped at the delay
    assert big.y == pytest.approx(exact_unit_delay(2.5), abs=1e-14)


def test_off_grid_final_time():
    r = dde_rk4(neg_lag, one, [1.0], 0.0, 2.3, 0.4)
    assert r.t == 2.3
    assert r.y == pytest.approx(exact_unit_delay(2.3), abs=1e-12)


def test_stiff_problem_needs_small_steps():
    # y' = -50 y + y(t - 1): RK4 is stable only for h*50 below about 2.785.
    f = lambda t, y, z: -50 * y + z[0]
    bad = dde_rk4(f, one, [1.0], 0.0, 5.0, 0.1)
    good = dde_rk4(f, one, [1.0], 0.0, 5.0, 0.05)
    fine = dde_rk4(f, one, [1.0], 0.0, 5.0, 0.0125)
    assert abs(bad.y) > 1e6
    assert good.y == pytest.approx(fine.y, abs=1e-4)


def test_invalid_input():
    with pytest.raises(ValueError):
        dde_rk4(neg_lag, one, [0.0], 0.0, 1.0, 0.1)
    with pytest.raises(ValueError):
        dde_rk4(neg_lag, one, [1.0], 0.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        dde_rk4(neg_lag, one, [1.0], 1.0, 0.0, 0.1)
