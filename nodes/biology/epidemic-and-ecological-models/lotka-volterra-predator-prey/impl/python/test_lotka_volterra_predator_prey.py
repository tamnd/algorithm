# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lotka-volterra-predator-prey/. The authors are listed in prov/JXS149.jsonl.

import math

from lotka_volterra_predator_prey import (
    field,
    first_integral,
    period_and_means,
    simulate,
    small_orbit_period,
)

P = (1.0, 0.1, 0.02, 0.5)  # a, b, c, d; the equilibrium is (25, 10)


def test_equilibrium_is_a_rest_point() -> None:
    assert field(25.0, 10.0, *P) == (0.0, 0.0)


def test_first_integral_is_conserved() -> None:
    # dt = 0.01 up to t = 40 (more than four periods); RK4 keeps V within 1e-9.
    traj = simulate(40.0, 10.0, 0.01, 4000, P)
    v0 = first_integral(40.0, 10.0, *P)
    assert abs(v0 - (-2.347025)) < 1e-6
    assert max(abs(first_integral(x, y, *P) - v0) for x, y in traj) < 1e-9
    xs = [x for x, _ in traj]
    ys = [y for _, y in traj]
    assert abs(min(xs) - 14.3207) < 1e-3 and abs(max(ys) - 14.0512) < 1e-3
    assert abs(min(ys) - 6.8142) < 1e-3


def test_derivative_of_v_is_zero() -> None:
    # The chain rule: dV/dt = (c - d/x) x' + (b - a/y) y' = 0 at any positive point.
    a, b, c, d = P
    for x in (1.0, 13.0, 25.0, 70.0):
        for y in (0.5, 10.0, 31.0):
            fx, fy = field(x, y, *P)
            assert abs((c - d / x) * fx + (b - a / y) * fy) < 1e-12


def test_period_and_volterra_averages() -> None:
    period, mx, my = period_and_means(40.0, 10.0, 0.01, 25.0, P)
    assert abs(period - 9.031) < 2e-3
    # The time averages over one period equal the equilibrium (25, 10).
    assert abs(mx - 25.0) < 2e-2 and abs(my - 10.0) < 2e-2


def test_small_orbits_have_the_linear_period() -> None:
    lin = small_orbit_period(1.0, 0.5)
    assert abs(lin - 8.885766) < 1e-6
    period, _, _ = period_and_means(25.5, 10.0, 0.01, 25.0, P)
    assert abs(period - lin) < 5e-3
    big, _, _ = period_and_means(60.0, 10.0, 0.01, 40.0, P)
    assert big > period + 0.5


def test_logistic_prey_damps_the_cycles() -> None:
    # With prey capacity K = 100, the coexistence point is (25, 7.5) and it attracts.
    p = P + (100.0,)
    traj = simulate(40.0, 10.0, 0.01, 20000, p)
    x, y = traj[-1]
    assert abs(x - 25.0) < 1e-3 and abs(y - 7.5) < 1e-3
    # The Lyapunov function with y* = 7.5 in place of a / b decreases along the path.
    a, b, c, d = P
    w = [c * x - d * math.log(x) + b * y - b * 7.5 * math.log(y) for x, y in traj[::100]]
    assert all(v2 <= v1 + 1e-12 for v1, v2 in zip(w, w[1:]))
