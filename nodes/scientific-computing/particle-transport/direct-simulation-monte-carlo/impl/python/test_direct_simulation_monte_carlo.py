# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-simulation-monte-carlo/. The authors are listed in prov/8HF9Q3.jsonl.
import math
import random

import pytest

from direct_simulation_monte_carlo import Gas, dsmc_step, maxwellian, momentum_and_energy, random_unit_vector, temperature


def test_conservation_is_exact():
    rng = random.Random(1)
    n = 300
    v = maxwellian(n, 1.0, rng)
    gas = Gas([rng.random() * 4.0 for _ in range(n)], v, 4.0, 4, 1.0, 0.01)
    p0, e0 = momentum_and_energy(gas.v)
    for _ in range(30):
        dsmc_step(gas, 0.2, rng)
    p1, e1 = momentum_and_energy(gas.v)
    assert gas.collisions > 100
    assert e1 == pytest.approx(e0, rel=1e-12)
    for k in range(3):
        assert abs(p1[k] - p0[k]) < 1e-10


def test_equilibrium_collision_rate():
    # In one cell with N particles the expected number of collisions per step is
    # 1/2 N (N - 1) F_N sigma <g> dt / V, with <g> = 4 sqrt(T / pi) for a Maxwellian.
    rng = random.Random(2)
    n, f_n, sigma, dt, steps = 400, 1.0, 0.002, 0.1, 150
    gas = Gas([rng.random() for _ in range(n)], maxwellian(n, 1.0, rng), 1.0, 1, f_n, sigma)
    t = temperature(gas.v)
    for _ in range(steps):
        dsmc_step(gas, dt, rng)
    expected = 0.5 * n * (n - 1) * f_n * sigma * 4.0 * math.sqrt(t / math.pi) * dt * steps / gas.cell_volume
    # The count is close to Poisson, so its sd is about sqrt(expected).
    assert abs(gas.collisions - expected) < 4.0 * math.sqrt(expected)


def test_relaxation_to_maxwellian():
    # All speeds equal: <c^4> / <c^2>^2 = 1. The Maxwellian value is 5/3.
    rng = random.Random(3)
    n = 1500
    v = []
    for _ in range(n):
        ux, uy, uz = random_unit_vector(rng)
        v.append([ux, uy, uz])
    gas = Gas([rng.random() for _ in range(n)], v, 1.0, 1, 1.0, 1.0 / n)
    for _ in range(25):
        dsmc_step(gas, 1.0, rng)
    assert gas.collisions / n > 5.0  # each particle has collided many times
    c2 = sum(u[0] ** 2 + u[1] ** 2 + u[2] ** 2 for u in gas.v) / n
    c4 = sum((u[0] ** 2 + u[1] ** 2 + u[2] ** 2) ** 2 for u in gas.v) / n
    assert c4 / (c2 * c2) == pytest.approx(5.0 / 3.0, abs=0.12)


def test_anisotropic_temperature_relaxes():
    rng = random.Random(4)
    n = 1500
    v = [[rng.gauss(0.0, math.sqrt(2.0)), rng.gauss(0.0, math.sqrt(0.5)), rng.gauss(0.0, math.sqrt(0.5))] for _ in range(n)]
    gas = Gas([rng.random() for _ in range(n)], v, 1.0, 1, 1.0, 1.0 / n)
    tx0 = sum(u[0] ** 2 for u in gas.v) / n
    ty0 = sum(u[1] ** 2 for u in gas.v) / n
    assert tx0 - ty0 > 1.2
    for _ in range(20):
        dsmc_step(gas, 1.0, rng)
    tx = sum(u[0] ** 2 for u in gas.v) / n
    ty = sum(u[1] ** 2 for u in gas.v) / n
    assert abs(tx - ty) < 0.15


def test_unit_vectors_are_isotropic():
    rng = random.Random(5)
    n = 20000
    s = [random_unit_vector(rng) for _ in range(n)]
    for k in range(3):
        assert abs(sum(u[k] for u in s) / n) < 4.0 / math.sqrt(3.0 * n)
        assert abs(sum(u[k] ** 2 for u in s) / n - 1.0 / 3.0) < 0.01
