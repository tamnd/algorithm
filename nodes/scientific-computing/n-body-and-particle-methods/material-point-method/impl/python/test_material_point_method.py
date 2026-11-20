# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/material-point-method/. The authors are listed in prov/AX0ZM2.jsonl.
import math
import random

import pytest

from material_point_method import Particles, grid_force, hat_weights, mpm_step, vibrating_bar


def test_page_example_cell_crossing_force():
    # 8 points 0.6 dx apart with V_p = 0.6 and a uniform stress 1: cells hold 2, 1, 2, 2, 1 points
    ps = Particles([0.3 + 0.6 * k for k in range(8)], [0.0] * 8, [0.6] * 8, [0.6] * 8, stress=[1.0] * 8)
    f = grid_force(ps, 1.0, 7)
    assert f[1:5] == pytest.approx([-0.6, 0.6, 0.0, -0.6], abs=1e-12)


def test_uniform_points_give_zero_interior_force():
    rng = random.Random(1)
    for _ in range(20):
        ppc = rng.randint(1, 4)
        dx = rng.uniform(0.1, 2)
        cells = 6
        xs = [(c + (k + 0.5) / ppc) * dx for c in range(cells) for k in range(ppc)]
        s = rng.uniform(-3, 3)
        ps = Particles(xs, [0.0] * len(xs), [1.0] * len(xs), [dx / ppc] * len(xs), stress=[s] * len(xs))
        f = grid_force(ps, dx, cells + 2)
        assert f[1:cells] == pytest.approx([0.0] * (cells - 1), abs=1e-12)
        # the boundary nodes get the traction of the stress, -s at the left end and +s at the right end
        assert f[0] == pytest.approx(s, abs=1e-12) and f[cells] == pytest.approx(-s, abs=1e-12)


def test_weights_form_a_partition_of_unity():
    rng = random.Random(2)
    for _ in range(500):
        dx = rng.uniform(0.1, 3)
        x = rng.uniform(0, 20)
        ws = hat_weights(x, dx)
        assert sum(w for _, w, _ in ws) == pytest.approx(1, abs=1e-12)
        assert sum(w * i * dx for i, w, _ in ws) == pytest.approx(x, abs=1e-9)
        assert sum(dn for _, _, dn in ws) == pytest.approx(0, abs=1e-12)
        assert all(w >= 0 for _, w, _ in ws)


def test_mass_and_momentum_are_conserved_without_supports():
    rng = random.Random(3)
    n, dx = 14, 0.5
    xs = [rng.uniform(2, 4.5) for _ in range(30)]
    ps = Particles(xs, [rng.uniform(-1, 1) for _ in xs], [rng.uniform(0.5, 2) for _ in xs], [0.1] * 30,
                   stress=[rng.uniform(-1, 1) for _ in xs])
    p0 = sum(m * v for m, v in zip(ps.m, ps.v))
    for _ in range(50):
        ps = mpm_step(ps, dx, n, 10.0, 1e-3)
    assert sum(m * v for m, v in zip(ps.m, ps.v)) == pytest.approx(p0, abs=1e-10)
    assert min(ps.x) > 0 and max(ps.x) < (n - 2) * dx


def test_rigid_translation_is_exact():
    xs = [0.5 + 0.25 * k for k in range(10)]
    ps = Particles(xs, [0.3] * 10, [1.0] * 10, [0.25] * 10)
    for _ in range(100):
        ps = mpm_step(ps, 0.5, 12, 50.0, 0.01)
    assert ps.v == pytest.approx([0.3] * 10, abs=1e-12)
    assert ps.x == pytest.approx([x + 0.3 for x in xs], abs=1e-9)
    assert ps.stress == pytest.approx([0.0] * 10, abs=1e-12)
    assert ps.F == pytest.approx([1.0] * 10, abs=1e-12)


def test_vibrating_bar_first_mode():
    # fixed at x = 0, free at x = 1; c = sqrt(E / rho) = 10, omega_1 = pi c / 2, period 0.4
    young, rho, length, v0 = 100.0, 1.0, 1.0, 0.1
    ps, dx, n = vibrating_bar(20, 2, length, young, rho, v0, 0.0)
    c = math.sqrt(young / rho)
    h = 0.1 * dx / c
    w1 = math.pi * c / (2 * length)
    worst = 0.0
    for s in range(1, int(round(0.4 / h)) + 1):
        ps = mpm_step(ps, dx, n, young, h, frozenset([0]))
        vcm = sum(m * v for m, v in zip(ps.m, ps.v)) / sum(ps.m)
        worst = max(worst, abs(vcm - 2 / math.pi * v0 * math.cos(w1 * s * h)))
    assert worst < 0.02 * (2 / math.pi * v0)
