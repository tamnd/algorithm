# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-interpolation-material-point/. The authors are listed in prov/4J3GZH.jsonl.
import math
import random

import pytest

from generalized_interpolation_material_point import Points, gimp_step, gimp_weights, grid_force, hat, vibrating_bar


def quadrature_weight(i, x, lp, dx, k=2000):
    # oracle: the midpoint rule for the mean of N_i over [x - lp, x + lp]
    a = x - lp
    return sum(hat((a + (j + 0.5) * 2 * lp / k - i * dx) / dx) for j in range(k)) / k


def test_page_example_has_no_interior_force():
    ps = Points([0.3 + 0.6 * k for k in range(8)], [0.0] * 8, [0.6] * 8, [0.6] * 8, [0.3] * 8, stress=[1.0] * 8)
    f = grid_force(ps, 1.0, 7)
    assert f == pytest.approx([1.0, 0.0, 0.0, 0.0, -0.2, -0.8, 0.0], abs=1e-12)
    ws = gimp_weights(0.9, 0.3, 1.0)
    assert [i for i, _, _ in ws] == [0, 1, 2]
    assert [s for _, s, _ in ws] == pytest.approx([2 / 15, 5 / 6, 1 / 30], abs=1e-12)
    assert [g for _, _, g in ws] == pytest.approx([-2 / 3, 1 / 3, 1 / 3], abs=1e-12)


def test_weights_match_quadrature_and_form_a_partition_of_unity():
    rng = random.Random(1)
    for _ in range(60):
        dx = rng.uniform(0.2, 2)
        lp = rng.uniform(0.01, 1) * dx
        x = rng.uniform(2, 10)
        ws = gimp_weights(x, lp, dx)
        for i, s, _ in ws:
            assert s == pytest.approx(quadrature_weight(i, x, lp, dx), abs=1e-6)
        assert sum(s for _, s, _ in ws) == pytest.approx(1, abs=1e-12)
        assert sum(s * i * dx for i, s, _ in ws) == pytest.approx(x, abs=1e-9)
        assert sum(g for _, _, g in ws) == pytest.approx(0, abs=1e-12)
        assert all(s >= 0 for _, s, _ in ws)


def test_gradient_is_the_derivative_of_the_weight():
    rng = random.Random(2)
    for _ in range(200):
        dx, lp = 1.0, rng.uniform(0.05, 0.5)
        x, d = rng.uniform(2, 6), 1e-6
        up = dict((i, s) for i, s, _ in gimp_weights(x + d, lp, dx))
        dn = dict((i, s) for i, s, _ in gimp_weights(x - d, lp, dx))
        for i, _, g in gimp_weights(x, lp, dx):
            assert (up.get(i, 0.0) - dn.get(i, 0.0)) / (2 * d) == pytest.approx(g, abs=1e-5)


def test_gradient_is_continuous_in_the_position():
    # |dS(x + e) - dS(x)| <= e / (lp dx): no jump when a point crosses a node
    rng = random.Random(3)
    for _ in range(300):
        dx, lp, e = 1.0, rng.uniform(0.05, 0.5), 1e-7
        x = rng.choice([3.0, 3.0 + lp, 3.0 - lp, rng.uniform(2, 6)])
        a = dict((i, g) for i, _, g in gimp_weights(x - e, lp, dx))
        b = dict((i, g) for i, _, g in gimp_weights(x + e, lp, dx))
        for i in set(a) | set(b):
            assert abs(a.get(i, 0.0) - b.get(i, 0.0)) <= 2 * e / (lp * dx) + 1e-12


def test_small_domains_give_the_mpm_hat_weights():
    rng = random.Random(4)
    for _ in range(100):
        dx = rng.uniform(0.5, 2)
        x = (rng.randint(2, 8) + rng.uniform(0.1, 0.9)) * dx
        j, w = math.floor(x / dx), x / dx - math.floor(x / dx)
        ws = dict((i, (s, g)) for i, s, g in gimp_weights(x, 1e-6 * dx, dx))
        assert ws[j][0] == pytest.approx(1 - w, abs=1e-9) and ws[j + 1][0] == pytest.approx(w, abs=1e-9)
        assert ws[j][1] == pytest.approx(-1 / dx, abs=1e-9) and ws[j + 1][1] == pytest.approx(1 / dx, abs=1e-9)


def test_any_tiling_with_uniform_stress_has_zero_interior_force():
    rng = random.Random(5)
    for _ in range(30):
        cuts = sorted(rng.uniform(1.0, 7.0) for _ in range(rng.randint(3, 12)))
        lengths = [b - a for a, b in zip(cuts, cuts[1:])]
        xs = [(a + b) / 2 for a, b in zip(cuts, cuts[1:])]
        s = rng.uniform(-2, 2)
        ps = Points(xs, [0.0] * len(xs), [1.0] * len(xs), lengths, [d / 2 for d in lengths], stress=[s] * len(xs))
        f = grid_force(ps, 1.0, 10)
        for i in range(10):
            # only the two ends of the body carry the traction
            assert f[i] == pytest.approx(s * hat(cuts[0] - i) - s * hat(cuts[-1] - i), abs=1e-12)


def test_momentum_is_conserved_and_rigid_translation_is_exact():
    rng = random.Random(6)
    n, dx = 16, 0.5
    xs = [rng.uniform(2, 5) for _ in range(30)]
    ps = Points(xs, [rng.uniform(-1, 1) for _ in xs], [rng.uniform(0.5, 2) for _ in xs], [0.1] * 30, [0.05] * 30,
                stress=[rng.uniform(-1, 1) for _ in xs])
    p0 = sum(m * v for m, v in zip(ps.m, ps.v))
    for _ in range(50):
        ps = gimp_step(ps, dx, n, 10.0, 1e-3)
    assert sum(m * v for m, v in zip(ps.m, ps.v)) == pytest.approx(p0, abs=1e-10)
    xs = [0.5 + 0.25 * k for k in range(10)]
    ps = Points(xs, [0.3] * 10, [1.0] * 10, [0.25] * 10, [0.125] * 10)
    for _ in range(100):
        ps = gimp_step(ps, 0.5, 12, 50.0, 0.01)
    assert ps.v == pytest.approx([0.3] * 10, abs=1e-12)
    assert ps.x == pytest.approx([x + 0.3 for x in xs], abs=1e-9)
    assert ps.stress == pytest.approx([0.0] * 10, abs=1e-12)


def test_vibrating_bar_first_mode():
    young, rho, length, v0 = 100.0, 1.0, 1.0, 0.1
    ps, dx, n = vibrating_bar(20, 2, length, rho, v0)
    c = math.sqrt(young / rho)
    h = 0.1 * dx / c
    w1 = math.pi * c / (2 * length)
    worst = 0.0
    for s in range(1, int(round(0.4 / h)) + 1):
        ps = gimp_step(ps, dx, n, young, h, frozenset([0]))
        vcm = sum(m * v for m, v in zip(ps.m, ps.v)) / sum(ps.m)
        worst = max(worst, abs(vcm - 2 / math.pi * v0 * math.cos(w1 * s * h)))
    assert worst < 0.02 * (2 / math.pi * v0)


def test_stress_stays_smooth_when_points_cross_cells():
    # displacement amplitude v0 / omega_1 = 0.064 > dx = 0.05, so points cross cell boundaries
    young, rho, length, v0 = 100.0, 1.0, 1.0, 1.0
    ps, dx, n = vibrating_bar(20, 2, length, rho, v0)
    h = 0.1 * dx / math.sqrt(young / rho)
    rough = 0.0
    for _ in range(800):
        ps = gimp_step(ps, dx, n + 8, young, h, frozenset([0]))
        st = ps.stress
        rough = max(rough, max(abs(st[k + 1] - 2 * st[k] + st[k - 1]) for k in range(1, len(st) - 1)))
    assert rough < 0.1 * young * v0 / math.sqrt(young / rho)
