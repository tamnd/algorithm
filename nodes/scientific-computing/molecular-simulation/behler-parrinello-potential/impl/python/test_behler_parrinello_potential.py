# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/behler-parrinello-potential/. The authors are listed in prov/JVQRJ5.jsonl.

import math
import random

import pytest

from behler_parrinello_potential import AtomicNetwork, bp_energy_forces, cutoff, g2, symmetry_functions

RC = 4.0
PARAMS = [(0.5, 0.0), (1.0, 1.0), (2.0, 1.5), (0.2, 2.5)]
NET = AtomicNetwork.random(len(PARAMS), 5, seed=11)


def cluster(rng, n, side, dmin):
    out = []
    while len(out) < n:
        p = [rng.uniform(0, side) for _ in range(3)]
        if all(math.dist(p, q) >= dmin for q in out):
            out.append(p)
    return out


def energy(pos):
    return bp_energy_forces(pos, NET, PARAMS, RC)[0]


def rotate(p, axis_angle):
    a, b = axis_angle
    ca, sa, cb, sb = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    x, y, z = p
    x, y = ca * x - sa * y, sa * x + ca * y
    y, z = cb * y - sb * z, sb * y + cb * z
    return [x, y, z]


def test_page_example_g2():
    assert cutoff(1, RC) == pytest.approx(0.853553, abs=1e-6)
    assert cutoff(2, RC) == pytest.approx(0.5)
    assert cutoff(4, RC) == 0.0
    pos = [[0, 0, 0], [1, 0, 0], [0, 2, 0]]
    g = symmetry_functions(pos, 0, [(0.5, 0.0)], RC)[0]
    assert g == pytest.approx(0.585374, abs=1e-6)
    assert g2(1, 0.5, 0, RC) == pytest.approx(0.517706, abs=1e-6)
    assert g2(2, 0.5, 0, RC) == pytest.approx(0.067668, abs=1e-6)
    assert symmetry_functions(pos, 0, [(0.0, 0.0)], RC)[0] == pytest.approx(1.353553, abs=1e-6)


def test_forces_match_finite_differences():
    rng = random.Random(1)
    pos = cluster(rng, 8, 3.5, 0.9)
    _, _, f = bp_energy_forces(pos, NET, PARAMS, RC)
    eps = 1e-6
    for i in range(len(pos)):
        for q in range(3):
            plus = [p[:] for p in pos]
            minus = [p[:] for p in pos]
            plus[i][q] += eps
            minus[i][q] -= eps
            num = -(energy(plus) - energy(minus)) / (2 * eps)
            assert f[i][q] == pytest.approx(num, abs=1e-6)


def test_invariance_translation_rotation_permutation():
    rng = random.Random(2)
    pos = cluster(rng, 9, 3.5, 0.9)
    u0 = energy(pos)
    shifted = [[x + 0.37, y - 1.2, z + 2.5] for x, y, z in pos]
    assert energy(shifted) == pytest.approx(u0, abs=1e-12)
    turned = [rotate(p, (0.7, -1.1)) for p in pos]
    assert energy(turned) == pytest.approx(u0, abs=1e-12)
    perm = pos[:]
    rng.shuffle(perm)
    assert energy(perm) == pytest.approx(u0, abs=1e-12)


def test_total_force_is_zero():
    rng = random.Random(3)
    pos = cluster(rng, 10, 3.5, 0.9)
    _, _, f = bp_energy_forces(pos, NET, PARAMS, RC)
    for q in range(3):
        assert abs(sum(row[q] for row in f)) < 1e-10


def test_atomic_energy_is_local():
    rng = random.Random(4)
    pos = cluster(rng, 6, 3.0, 0.9)
    _, e0, _ = bp_energy_forces(pos, NET, PARAMS, RC)
    i = 0
    c = [sum(p[q] for p in pos) / len(pos) for q in range(3)]
    u = [c[q] - pos[i][q] for q in range(3)]
    norm = math.sqrt(sum(x * x for x in u))
    # a new atom just beyond the cutoff of atom i, past the center of the cluster
    extra = [pos[i][q] + (RC + 0.01) * u[q] / norm for q in range(3)]
    _, e1, _ = bp_energy_forces(pos + [extra], NET, PARAMS, RC)
    assert e1[i] == pytest.approx(e0[i], abs=1e-12)
    close = [k for k, p in enumerate(pos) if math.dist(p, extra) < RC]
    assert close  # some other atom does see it, so the check is not empty
    assert any(abs(e1[k] - e0[k]) > 1e-9 for k in close)


def test_energy_is_extensive():
    rng = random.Random(5)
    pos = cluster(rng, 6, 3.0, 0.9)
    u = energy(pos)
    copy = [[x + 50, y, z] for x, y, z in pos]
    assert energy(pos + copy) == pytest.approx(2 * u, abs=1e-12)


def test_isolated_atom_energy_is_network_at_zero():
    e, _ = NET.energy_and_gradient([0.0] * len(PARAMS))
    assert energy([[0.0, 0.0, 0.0]]) == pytest.approx(e)
