# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-kpp-equation/. The authors are listed in prov/2NM058.jsonl.

import math

from fisher_kpp_equation import (
    EXACT_SPEED,
    discrete_linear_speed,
    exact_wave,
    linear_speed,
    minimal_speed,
    simulate,
    step_start,
    wave_start,
)


def test_minimal_speed_is_the_minimum_of_the_linear_speeds() -> None:
    for d, r in [(1.0, 1.0), (0.5, 2.0), (3.0, 0.1)]:
        lam_star = math.sqrt(r / d)
        assert abs(linear_speed(lam_star, d, r) - minimal_speed(d, r)) < 1e-12
        for lam in (0.3 * lam_star, 0.9 * lam_star, 1.1 * lam_star, 4.0 * lam_star):
            assert linear_speed(lam, d, r) > minimal_speed(d, r)
    assert minimal_speed(1.0, 1.0) == 2.0


def test_exact_wave_solves_the_wave_equation() -> None:
    # D U'' + c U' + r U (1 - U) = 0 with D = r = 1 and c = 5 / sqrt 6.
    assert abs(EXACT_SPEED - 2.041241) < 1e-6 and EXACT_SPEED > 2.0
    h = 1e-3
    worst = 0.0
    for i in range(-200, 201):
        z = i * 0.05
        u = exact_wave(z)
        up = (exact_wave(z + h) - exact_wave(z - h)) / (2 * h)
        upp = (exact_wave(z + h) - 2 * u + exact_wave(z - h)) / h ** 2
        worst = max(worst, abs(upp + EXACT_SPEED * up + u * (1 - u)))
    assert worst < 1e-6
    assert abs(exact_wave(-40.0) - 1.0) < 1e-6 and exact_wave(40.0) < 1e-6


def test_step_start_spreads_just_below_the_minimal_speed() -> None:
    dx, dt = 0.25, 0.01
    u, fronts = simulate(step_start(100.0, dx), dx, dt, 40.0, marks=(10.0, 20.0, 30.0, 40.0))
    # The scheme keeps u in [0, 1] because 2 D dt / dx^2 + r dt <= 1.
    assert 2 * dt / dx ** 2 + dt <= 1 and min(u) >= 0.0 and max(u) <= 1.0
    assert abs(fronts[10.0] - 24.27) < 0.01 and abs(fronts[40.0] - 81.60) < 0.01
    speed = (fronts[40.0] - fronts[30.0]) / 10.0
    cap = discrete_linear_speed(dx, dt)
    assert abs(cap - 1.9854) < 1e-3
    # The front from compact data approaches the linear speed of the scheme from below.
    assert 1.9 < speed < cap < 2.0
    assert (fronts[20.0] - fronts[10.0]) / 10 < (fronts[40.0] - fronts[30.0]) / 10


def test_steep_and_shallow_starts() -> None:
    # The exact wave decays like exp(-2 z / sqrt 6), a tail less steep than exp(-z), and keeps its own speed 5 / sqrt 6.
    dx, dt = 0.25, 0.01
    _, fronts = simulate(wave_start(80.0, dx), dx, dt, 20.0, marks=(5.0, 20.0))
    speed = (fronts[20.0] - fronts[5.0]) / 15.0
    assert abs(speed - EXACT_SPEED) < 0.03
    assert speed > 2.0
