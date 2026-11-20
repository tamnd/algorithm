# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/embedded-atom-method/. The authors are listed in prov/4CFCM8.jsonl.

import math
import random

import pytest

from embedded_atom_method import eam_energy_forces, fcc_lattice

# The page example: F(rho) = -sqrt(rho), f(r) = ((rc - r) / (rc - 1))^2 with f(1) = 1, no pair term.
RC = 1.2


def sqrt_embed(x):
    return -math.sqrt(x)


def sqrt_dembed(x):
    return -0.5 / math.sqrt(x) if x > 0 else 0.0


def step_density(r):
    return ((RC - r) / (RC - 1)) ** 2 if r < RC else 0.0


def step_ddensity(r):
    return -2 * (RC - r) / (RC - 1) ** 2 if r < RC else 0.0


def zero(r):
    return 0.0


def page_model(positions, box=None):
    return eam_energy_forces(positions, sqrt_embed, sqrt_dembed, step_density, step_ddensity, zero, zero, RC, box)


# A smooth model for the derivative tests.
RC2 = 2.5


def s_embed(x):
    return -math.sqrt(x + 0.1) + 0.05 * x * x


def s_dembed(x):
    return -0.5 / math.sqrt(x + 0.1) + 0.1 * x


def s_density(r):
    return (RC2 - r) ** 3 if r < RC2 else 0.0


def s_ddensity(r):
    return -3 * (RC2 - r) ** 2 if r < RC2 else 0.0


def s_pair(r):
    return (RC2 - r) ** 3 / r ** 2 if r < RC2 else 0.0


def s_dpair(r):
    return (-3 * (RC2 - r) ** 2 / r ** 2 - 2 * (RC2 - r) ** 3 / r ** 3) if r < RC2 else 0.0


def smooth_model(positions, box=None, k=0.0):
    """The smooth model after the gauge change F + k rho, phi - 2 k f, which leaves U unchanged."""
    return eam_energy_forces(
        positions,
        lambda x: s_embed(x) + k * x,
        lambda x: s_dembed(x) + k,
        s_density,
        s_ddensity,
        lambda r: s_pair(r) - 2 * k * s_density(r),
        lambda r: s_dpair(r) - 2 * k * s_ddensity(r),
        RC2,
        box,
    )


def random_cluster(rng, n, side, dmin):
    out = []
    while len(out) < n:
        p = [rng.uniform(0, side) for _ in range(3)]
        if all(math.dist(p, q) >= dmin for q in out):
            out.append(p)
    return out


def numeric_forces(model, positions, eps=1e-6, **kw):
    out = []
    for i in range(len(positions)):
        row = []
        for q in range(3):
            plus = [p[:] for p in positions]
            minus = [p[:] for p in positions]
            plus[i][q] += eps
            minus[i][q] -= eps
            row.append(-(model(plus, **kw)[0] - model(minus, **kw)[0]) / (2 * eps))
        out.append(row)
    return out


def test_dimer_and_trimer():
    u, rho, _ = page_model([[0, 0, 0], [1, 0, 0]])
    assert rho == [pytest.approx(1), pytest.approx(1)]
    assert u == pytest.approx(-2)
    tri = [[0, 0, 0], [1, 0, 0], [0.5, math.sqrt(3) / 2, 0]]
    u, rho, f = page_model(tri)
    assert u == pytest.approx(-3 * math.sqrt(2))
    assert u / 3 == pytest.approx(-1.41421, abs=1e-5)  # energy per bond falls from 2 to 1.414


def test_fcc_cohesive_and_vacancy_energy():
    a = math.sqrt(2)  # nearest-neighbor distance 1
    pos = fcc_lattice(3, a)
    box = 3 * a
    n = len(pos)
    u, rho, f = page_model(pos, box)
    assert all(x == pytest.approx(12) for x in rho)
    assert u / n == pytest.approx(-math.sqrt(12))
    assert max(abs(c) for row in f for c in row) < 1e-9
    uv, _, _ = page_model(pos[1:], box)
    ev = uv - (n - 1) / n * u
    assert ev == pytest.approx(12 * (math.sqrt(12) - math.sqrt(11)))
    assert ev == pytest.approx(1.7698, abs=1e-4)
    assert ev / math.sqrt(12) == pytest.approx(0.5109, abs=1e-4)


def test_forces_match_finite_differences_free_cluster():
    rng = random.Random(1)
    pos = random_cluster(rng, 7, 2.5, 0.8)
    _, _, f = smooth_model(pos)
    num = numeric_forces(smooth_model, pos)
    for row, nrow in zip(f, num):
        for c, nc in zip(row, nrow):
            assert c == pytest.approx(nc, abs=1e-5)


def test_forces_match_finite_differences_periodic():
    rng = random.Random(2)
    box = 5.2
    pos = random_cluster(rng, 12, box, 0.8)
    _, _, f = smooth_model(pos, box=box)
    num = numeric_forces(smooth_model, pos, box=box)
    for row, nrow in zip(f, num):
        for c, nc in zip(row, nrow):
            assert c == pytest.approx(nc, abs=1e-5)


def test_total_force_is_zero():
    rng = random.Random(3)
    pos = random_cluster(rng, 10, 3.0, 0.8)
    _, _, f = smooth_model(pos)
    for q in range(3):
        assert abs(sum(row[q] for row in f)) < 1e-10


def test_gauge_change_leaves_energy_and_forces():
    rng = random.Random(4)
    pos = random_cluster(rng, 9, 3.0, 0.8)
    u0, _, f0 = smooth_model(pos)
    for k in (0.7, -1.3):
        u1, _, f1 = smooth_model(pos, k=k)
        assert u1 == pytest.approx(u0, abs=1e-10)
        for row0, row1 in zip(f0, f1):
            for c0, c1 in zip(row0, row1):
                assert c1 == pytest.approx(c0, abs=1e-10)


def test_linear_embedding_is_a_pair_potential():
    rng = random.Random(5)
    pos = random_cluster(rng, 8, 3.0, 0.8)
    c = 0.4
    u, _, _ = eam_energy_forces(pos, lambda x: c * x, lambda x: c, s_density, s_ddensity, s_pair, s_dpair, RC2)
    pair_sum = 0.0
    for i in range(len(pos)):
        for j in range(i + 1, len(pos)):
            r = math.dist(pos[i], pos[j])
            pair_sum += s_pair(r) + 2 * c * s_density(r)
    assert u == pytest.approx(pair_sum)


def test_rejects_long_cutoff_in_small_box():
    with pytest.raises(ValueError):
        page_model([[0, 0, 0], [1, 0, 0]], box=2.0)
