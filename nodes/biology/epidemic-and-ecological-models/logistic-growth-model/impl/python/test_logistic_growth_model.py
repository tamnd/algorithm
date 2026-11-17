# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logistic-growth-model/. The authors are listed in prov/SN0SST.jsonl.

import math

from logistic_growth_model import (
    closed_form,
    euler_step,
    exact_step,
    harvest_equilibria,
    inflection_time,
    rate,
    rk4,
    time_to_reach,
)

R, K, N0 = 1.0, 100.0, 10.0


def test_closed_form_values() -> None:
    # r = 1 per day, K = 100, N0 = 10.
    expected = {1: 23.196932, 2: 45.085306, 3: 69.056786, 5: 94.282562, 10: 99.959157}
    for t, v in expected.items():
        assert abs(closed_form(N0, R, K, t) - v) < 1e-6
    assert closed_form(0.0, R, K, 5.0) == 0.0
    assert closed_form(K, R, K, 5.0) == K


def test_closed_form_solves_the_ode() -> None:
    # A centered difference of the closed form matches r N (1 - N / K).
    h = 1e-5
    for n0 in (1.0, 10.0, 60.0, 150.0):
        for t in (0.3, 1.0, 2.5, 4.0):
            d = (closed_form(n0, R, K, t + h) - closed_form(n0, R, K, t - h)) / (2 * h)
            assert abs(d - rate(closed_form(n0, R, K, t), R, K)) < 1e-4


def test_rk4_against_closed_form_and_order() -> None:
    # dt = 0.1 and 0.05 up to t = 5; RK4 is fourth order, so the error ratio is near 16.
    exact = closed_form(N0, R, K, 5.0)
    e1 = abs(rk4(N0, R, K, 0.1, 50) - exact)
    e2 = abs(rk4(N0, R, K, 0.05, 100) - exact)
    assert e1 < 1e-5 and e2 < 1e-6
    assert 12.0 < e1 / e2 < 20.0


def test_monotone_convergence_from_both_sides() -> None:
    for n0 in (1.0, 50.0, 99.0, 101.0, 300.0):
        values = [closed_form(n0, R, K, t / 2) for t in range(60)]
        diffs = [b - a for a, b in zip(values, values[1:])]
        if n0 < K:
            assert all(d > 0 for d in diffs)
        else:
            assert all(d < 0 for d in diffs)
        assert abs(values[-1] - K) < 1e-6 * K * max(1.0, abs(n0 - K))


def test_time_to_reach_and_inflection() -> None:
    assert abs(inflection_time(N0, R, K) - math.log(9.0)) < 1e-12
    assert abs(closed_form(N0, R, K, inflection_time(N0, R, K)) - K / 2) < 1e-9
    t = time_to_reach(N0, 80.0, R, K)
    assert abs(closed_form(N0, R, K, t) - 80.0) < 1e-9
    # The fastest growth, r K / 4, happens at N = K / 2.
    best = max(rate(K * i / 1000, R, K) for i in range(1001))
    assert abs(best - R * K / 4) < 1e-12


def test_exact_step_is_the_time_h_map() -> None:
    n = N0
    for _ in range(10):
        n = exact_step(n, R, K, 0.5)
    assert abs(n - closed_form(N0, R, K, 5.0)) < 1e-9


def test_euler_map_is_a_logistic_map() -> None:
    # x = h r N / ((1 + h r) K) turns the Euler step into x -> (1 + h r) x (1 - x).
    for h in (0.5, 2.2, 2.7):
        mu = 1 + h * R
        for n in (5.0, 40.0, 90.0, 120.0):
            x = h * R * n / (mu * K)
            x_next = h * R * euler_step(n, R, K, h) / (mu * K)
            assert abs(x_next - mu * x * (1 - x)) < 1e-12


def test_euler_large_step_oscillates() -> None:
    # h r = 2.2 > 2: K is unstable for the Euler map, and a 2-cycle appears.
    n = N0
    for _ in range(400):
        n = euler_step(n, R, K, 2.2)
    a = n
    b = euler_step(a, R, K, 2.2)
    assert abs(euler_step(b, R, K, 2.2) - a) < 1e-9
    assert abs(a - b) > 40.0
    # h r = 0.5: the Euler iteration converges to K.
    n = N0
    for _ in range(200):
        n = euler_step(n, R, K, 0.5)
    assert abs(n - K) < 1e-9


def test_harvest_threshold() -> None:
    assert harvest_equilibria(R, K, 30.0) == []
    eq = harvest_equilibria(R, K, 16.0)
    assert len(eq) == 2 and abs(eq[0] - 20.0) < 1e-9 and abs(eq[1] - 80.0) < 1e-9
    eq = harvest_equilibria(R, K, R * K / 4)
    assert len(eq) == 1 and abs(eq[0] - K / 2) < 1e-9
