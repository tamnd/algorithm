# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hermite-n-body-integrator/. The authors are listed in prov/M1QQTQ.jsonl.
import math
import random

import pytest

from hermite_n_body_integrator import aarseth_step, acc_jerk, energy, hermite_step, integrate


def kepler_pair(e):
    """Two bodies of mass 1/2 at apocenter of an orbit with semi-major axis 1 and eccentricity e.
    G M = 1, so the period is 2 pi."""
    r = 1.0 + e
    vrel = math.sqrt((1.0 - e) / (1.0 + e))
    m = [0.5, 0.5]
    x = [(-r / 2, 0.0, 0.0), (r / 2, 0.0, 0.0)]
    v = [(0.0, -vrel / 2, 0.0), (0.0, vrel / 2, 0.0)]
    return m, x, v


def period_error(e, steps):
    m, x, v = kepler_pair(e)
    x1, _ = integrate(m, x, v, 2 * math.pi / steps, steps)
    return math.dist(x1[1], x[1])


def test_jerk_is_time_derivative_of_acceleration():
    rng = random.Random(2)
    m = [rng.uniform(0.5, 1.5) for _ in range(8)]
    x = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(8)]
    v = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(8)]
    _, jerk = acc_jerk(m, x, v, eps=0.05)
    dt = 1e-5
    ap, _ = acc_jerk(m, [[x[i][k] + v[i][k] * dt for k in range(3)] for i in range(8)], v, eps=0.05)
    am, _ = acc_jerk(m, [[x[i][k] - v[i][k] * dt for k in range(3)] for i in range(8)], v, eps=0.05)
    for i in range(8):
        for k in range(3):
            assert (ap[i][k] - am[i][k]) / (2 * dt) == pytest.approx(jerk[i][k], rel=1e-6, abs=1e-7)


def test_fourth_order_on_eccentric_kepler_orbit():
    e1 = period_error(0.5, 400)
    e2 = period_error(0.5, 800)
    assert e1 < 1e-4
    assert 12 < e1 / e2 < 20  # 2^4 = 16 for a fourth-order method


def test_period_and_energy_on_circular_orbit():
    m, x, v = kepler_pair(0.0)
    x1, v1 = integrate(m, x, v, 2 * math.pi / 200, 200)
    assert math.dist(x1[1], x[1]) < 1e-6
    e0 = energy(m, x, v)
    assert e0 == pytest.approx(-0.125, rel=1e-15)
    assert abs(energy(m, x1, v1) - e0) / abs(e0) < 1e-8


def test_momentum_is_conserved():
    rng = random.Random(5)
    n = 6
    m = [rng.uniform(0.5, 1.5) for _ in range(n)]
    x = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
    v = [[rng.uniform(-0.3, 0.3) for _ in range(3)] for _ in range(n)]
    p0 = [sum(m[i] * v[i][k] for i in range(n)) for k in range(3)]
    x1, v1 = integrate(m, x, v, 1e-3, 300, eps=0.05)
    for k in range(3):
        assert sum(m[i] * v1[i][k] for i in range(n)) == pytest.approx(p0[k], abs=1e-12)


def test_three_bodies_against_fine_reference():
    rng = random.Random(9)
    m = [1.0, 0.8, 0.6]
    x = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    v = [[rng.uniform(-0.3, 0.3) for _ in range(3)] for _ in range(3)]
    ref, _ = integrate(m, x, v, 1e-3 / 4, 4000, eps=0.1)
    coarse, _ = integrate(m, x, v, 2e-3, 500, eps=0.1)
    fine, _ = integrate(m, x, v, 1e-3, 1000, eps=0.1)
    err_coarse = max(math.dist(p, q) for p, q in zip(coarse, ref))
    err_fine = max(math.dist(p, q) for p, q in zip(fine, ref))
    assert err_fine < 1e-6
    assert err_coarse / err_fine > 12  # at least fourth order


def test_aarseth_step_on_circular_orbit():
    # On a circular orbit with angular frequency 1, |j| = |a|, |a2| = |a| and |a3| = |a|,
    # so the criterion gives sqrt(eta).
    m, x, v = kepler_pair(0.0)
    x = [list(p) for p in x]
    v = [list(q) for q in v]
    a, j = acc_jerk(m, x, v)
    h = 2 * math.pi / 1000
    _, _, a1, j1, snap, crackle = hermite_step(m, x, v, a, j, h)
    assert aarseth_step(a1[0], j1[0], snap[0], crackle[0], eta=0.01) == pytest.approx(0.1, rel=1e-3)
