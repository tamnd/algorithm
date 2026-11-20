# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dissipative-particle-dynamics/. The authors are listed in prov/9VVD0G.jsonl.
import math
import random

import pytest

from dissipative_particle_dynamics import (conservative_energy, dpd_forces, dpd_step, initial_state,
                                           kinetic_temperature, run)

BOX = 4.0
N = 48  # density 3 in a 4 by 4 box


def test_two_beads_by_hand():
    # Beads at distance 0.5 on the x axis, closing at speed 1: w = 1/2, e.v = -1.
    x = [[1.5, 1.0], [1.0, 1.0]]
    v = [[-0.5, 0.0], [0.5, 0.0]]
    f = dpd_forces(x, v, BOX, 25.0, 4.5, 0.0, 0.01, random.Random(0))
    # a w - gamma w^2 (e.v) = 12.5 + 4.5 / 4 = 13.625, repulsive on bead 0
    assert f[0] == pytest.approx([13.625, 0.0], abs=1e-12)
    assert f[1] == pytest.approx([-13.625, 0.0], abs=1e-12)
    far = dpd_forces([[0.0, 0.0], [1.0, 0.0]], v, BOX, 25.0, 4.5, 3.0, 0.01, random.Random(0))
    assert far == [[0.0, 0.0], [0.0, 0.0]]


def test_periodic_image_is_used():
    x = [[0.1, 2.0], [3.9, 2.0]]  # distance 0.2 through the boundary
    f = dpd_forces(x, [[0.0, 0.0], [0.0, 0.0]], BOX, 25.0, 0.0, 0.0, 0.01, random.Random(0))
    assert f[0][0] == pytest.approx(25.0 * 0.8, abs=1e-12)
    assert f[1][0] == pytest.approx(-25.0 * 0.8, abs=1e-12)


def test_conservative_force_is_minus_gradient_of_energy():
    rng = random.Random(3)
    x, v = initial_state(12, 2.0, 1.0, rng)
    f = dpd_forces(x, v, 2.0, 25.0, 0.0, 0.0, 0.01, rng)
    eps = 1e-6
    for i in range(len(x)):
        for k in range(2):
            x[i][k] += eps
            up = conservative_energy(x, 2.0, 25.0)
            x[i][k] -= 2 * eps
            down = conservative_energy(x, 2.0, 25.0)
            x[i][k] += eps
            assert -(up - down) / (2 * eps) == pytest.approx(f[i][k], rel=1e-6, abs=1e-6)


def test_total_momentum_is_conserved_to_rounding():
    rng = random.Random(5)
    x, v = initial_state(N, BOX, 1.0, rng)
    f = dpd_forces(x, v, BOX, 25.0, 4.5, 3.0, 0.04, rng)
    for _ in range(200):
        f = dpd_step(x, v, f, BOX, 25.0, 4.5, 3.0, 0.04, rng)
        for k in range(2):
            assert abs(sum(p[k] for p in v)) < 1e-11
            assert abs(sum(q[k] for q in f)) < 1e-10


def max_energy_error(h, time=3.0):
    """Largest |H(t) - H(0)| / N over a run without thermostat (gamma = sigma = 0)."""
    rng = random.Random(6)
    x, v = initial_state(N, BOX, 1.0, rng)
    f = dpd_forces(x, v, BOX, 25.0, 0.0, 0.0, h, rng)

    def energy():
        return conservative_energy(x, BOX, 25.0) + 0.5 * sum(p[0] ** 2 + p[1] ** 2 for p in v)

    e0 = energy()
    worst = 0.0
    for _ in range(round(time / h)):
        f = dpd_step(x, v, f, BOX, 25.0, 0.0, 0.0, h, rng)
        worst = max(worst, abs(energy() - e0) / N)
    return worst


def test_without_thermostat_energy_error_is_second_order():
    coarse, fine = max_energy_error(0.01), max_energy_error(0.005)
    assert coarse < 0.02
    assert coarse / fine > 3.0


def test_temperature_follows_the_fluctuation_dissipation_relation():
    # sigma^2 = 2 gamma kT: sigma = 3 with gamma = 4.5 gives kT = 1, with gamma = 9 gives kT = 1/2.
    for gamma, kt in ((4.5, 1.0), (9.0, 0.5)):
        _, v, temps = run(N, BOX, 25.0, gamma, 3.0, 0.02, 800, seed=1)
        tail = temps[160:]
        mean = sum(tail) / len(tail)
        assert abs(mean - kt) < 0.1 * kt


def test_start_far_from_equilibrium_relaxes_to_kt():
    _, _, temps = run(N, BOX, 25.0, 4.5, 3.0, 0.02, 600, seed=2, kt0=4.0)
    assert temps[0] > 2.0
    tail = temps[200:]
    assert abs(sum(tail) / len(tail) - 1.0) < 0.1


def test_kinetic_temperature_counts_two_n_minus_two_degrees():
    v = [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]
    assert kinetic_temperature(v) == pytest.approx(4.0 / 6.0)
    assert math.isclose(sum(p[0] for p in v), 0.0)
