# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wall-functions/. The authors are listed in prov/7MSEKR.jsonl.

import math
import random

import pytest

from wall_functions import (
    B,
    C_MU,
    KAPPA,
    crossover,
    friction_velocity,
    launder_spalding_stress,
    log_law,
    spalding_u_plus,
    spalding_y_plus,
    wall_shear_stress,
    wall_values,
)

NU_AIR = 1.5e-5


def bisect_u_tau(u_p, y_p, nu):
    lo, hi = 1e-6, u_p
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * log_law(y_p * mid / nu) < u_p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def test_crossover():
    y = crossover()
    assert y == pytest.approx(11.0623, abs=1e-4)
    assert log_law(y) == pytest.approx(y, abs=1e-12)


def test_air_example():
    u = friction_velocity(10.0, 1e-3, NU_AIR)
    assert u == pytest.approx(0.688155, abs=1e-6)
    assert 1e-3 * u / NU_AIR == pytest.approx(45.877, abs=1e-3)
    assert wall_shear_stress(10.0, 1e-3, NU_AIR, 1.2) == pytest.approx(0.56827, abs=1e-5)
    k, eps, omega = wall_values(u, 1e-3)
    assert k == pytest.approx(1.57852, abs=1e-5)
    assert eps == pytest.approx(794.83, abs=1e-2)
    # omega = eps / (C_mu k)
    assert omega == pytest.approx(eps / (C_MU * k))


def test_round_trip_and_bisection():
    rng = random.Random(7)
    for _ in range(50):
        u_p = rng.uniform(0.5, 50.0)
        y_p = 10 ** rng.uniform(-4, -1)
        u = friction_velocity(u_p, y_p, NU_AIR)
        y_plus = y_p * u / NU_AIR
        if y_plus > crossover():
            assert u * log_law(y_plus) == pytest.approx(u_p, rel=1e-10)
            assert u == pytest.approx(bisect_u_tau(u_p, y_p, NU_AIR), rel=1e-9)
        else:
            assert u * y_plus == pytest.approx(u_p, rel=1e-12)


def test_laminar_branch_and_continuity():
    u = friction_velocity(0.1, 1e-3, NU_AIR)
    assert u == pytest.approx(math.sqrt(NU_AIR * 0.1 / 1e-3))
    # at the crossover both laws give the same u_tau
    y_c = crossover()
    u_tau = 0.2
    y_p = y_c * NU_AIR / u_tau
    u_p = u_tau * y_c
    assert friction_velocity(u_p * (1 - 1e-9), y_p, NU_AIR) == pytest.approx(u_tau, rel=1e-6)
    assert friction_velocity(u_p * (1 + 1e-9), y_p, NU_AIR) == pytest.approx(u_tau, rel=1e-6)


def test_launder_spalding_agrees_in_equilibrium():
    for u_p, y_p in ((10.0, 1e-3), (3.0, 5e-3), (40.0, 2e-4)):
        u = friction_velocity(u_p, y_p, NU_AIR)
        k, _, _ = wall_values(u, y_p)
        assert launder_spalding_stress(u_p, k, y_p, NU_AIR) == pytest.approx(u * u, rel=1e-10)


def test_spalding_law_limits():
    assert spalding_u_plus(1.0) == pytest.approx(1.0, abs=1e-3)
    for y in (300.0, 1000.0):
        assert spalding_u_plus(y) == pytest.approx(log_law(y), abs=0.05)
    for up in (0.5, 5.0, 15.0, 25.0):
        assert spalding_u_plus(spalding_y_plus(up)) == pytest.approx(up, abs=1e-9)
    prev = 0.0
    for i in range(1, 200):
        cur = spalding_y_plus(0.15 * i)
        assert cur > prev
        prev = cur
    assert math.exp(-KAPPA * B) == pytest.approx(0.11860, abs=1e-5)


def test_bad_input():
    with pytest.raises(ValueError):
        friction_velocity(0.0, 1e-3, NU_AIR)
