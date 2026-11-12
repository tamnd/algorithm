# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/molecular-dynamics/. The authors are listed in prov/CPQSNC.jsonl.
import itertools
import math
import random

import pytest

from molecular_dynamics import (
    harmonic,
    kinetic,
    lennard_jones,
    minimum_image,
    molecular_dynamics,
)

S = 2 ** (1 / 6)


def cube_cluster(rng, spread):
    pos = [[S * i, S * j, S * k] for i in range(2) for j in range(2) for k in range(2)]
    vel = [[rng.gauss(0, spread) for _ in range(3)] for _ in pos]
    cm = [sum(v[c] for v in vel) / len(vel) for c in range(3)]
    vel = [[v[c] - cm[c] for c in range(3)] for v in vel]
    return pos, vel


def lj_pair(r):
    return 4 * (r ** -12 - r ** -6)


def test_harmonic_oscillator_against_exact_solution():
    errors = []
    for h in (0.1, 0.05, 0.025):
        n = round(10 / h)
        x, v, energies = molecular_dynamics([[1.0]], [[0.0]], [1.0], harmonic(1.0), h, n)
        errors.append(abs(x[0][0] - math.cos(10.0)))
        assert abs(v[0][0] + math.sin(10.0)) < 0.01
        # energy error stays O(h^2), with no drift
        assert max(abs(e - 0.5) for e in energies) < 0.13 * h * h
    assert errors[0] == pytest.approx(0.0022766, abs=1e-6)
    # second order: halving h divides the error by about 4
    assert 3.8 < errors[0] / errors[1] < 4.2
    assert 3.8 < errors[1] / errors[2] < 4.2


def test_harmonic_modified_energy_is_exact():
    # velocity Verlet conserves v^2 + w^2 (1 - (h w)^2 / 4) x^2 for x'' = -w^2 x
    k, h = 4.0, 0.2
    w2 = k
    x, v, _ = [[0.3]], [[1.1]], None
    inv0 = v[0][0] ** 2 + w2 * (1 - h * h * w2 / 4) * x[0][0] ** 2
    for _ in range(50):
        x, v, _ = molecular_dynamics(x, v, [1.0], harmonic(k), h, 7)
        inv = v[0][0] ** 2 + w2 * (1 - h * h * w2 / 4) * x[0][0] ** 2
        assert inv == pytest.approx(inv0, rel=1e-12)


def test_forces_are_minus_gradient():
    rng = random.Random(4)
    pos, _ = cube_cluster(rng, 0.0)
    pos = [[c + rng.uniform(-0.1, 0.1) for c in p] for p in pos]
    _, f = lennard_jones(pos)
    eps = 1e-6
    for i in range(len(pos)):
        for a in range(3):
            p1 = [list(p) for p in pos]
            p2 = [list(p) for p in pos]
            p1[i][a] += eps
            p2[i][a] -= eps
            g = (lennard_jones(p1)[0] - lennard_jones(p2)[0]) / (2 * eps)
            assert f[i][a] == pytest.approx(-g, rel=1e-5, abs=1e-6)


def test_energy_against_pair_sum():
    # cube of side 2^(1/6): 12 edges, 12 face and 4 body diagonals
    pos, _ = cube_cluster(random.Random(0), 0.0)
    u, _ = lennard_jones(pos)
    expect = 12 * lj_pair(S) + 12 * lj_pair(S * math.sqrt(2)) + 4 * lj_pair(S * math.sqrt(3))
    assert u == pytest.approx(expect, rel=1e-12)
    assert u == pytest.approx(-15.1033093, abs=1e-6)


def test_minimum_image_against_all_images():
    rng = random.Random(9)
    box = 5.0
    for _ in range(500):
        p = [rng.uniform(0, box) for _ in range(3)]
        q = [rng.uniform(0, box) for _ in range(3)]
        best = min(
            sum((p[a] - q[a] + box * s[a]) ** 2 for a in range(3))
            for s in itertools.product((-1, 0, 1), repeat=3)
        )
        mi = sum(minimum_image(p[a] - q[a], box) ** 2 for a in range(3))
        assert mi == pytest.approx(best, rel=1e-12)


def test_periodic_energy_against_explicit_images():
    rng = random.Random(12)
    box, rc = 6.0, 2.5
    pos = [[rng.uniform(0, box) for _ in range(3)] for _ in range(10)]
    u, _ = lennard_jones(pos, box=box, rc=rc)
    shift = lj_pair(rc)
    expect = 0.0
    for i in range(10):
        for j in range(i + 1, 10):
            for s in itertools.product((-1, 0, 1), repeat=3):
                r = math.sqrt(sum((pos[i][a] - pos[j][a] + box * s[a]) ** 2 for a in range(3)))
                if r < rc:
                    expect += lj_pair(r) - shift
    assert u == pytest.approx(expect, rel=1e-10, abs=1e-10)
    with pytest.raises(ValueError):
        lennard_jones(pos, box=4.0, rc=2.5)


def test_lj_cluster_energy_conservation_and_order():
    pos, vel = cube_cluster(random.Random(1), 0.5)
    m = [1.0] * 8
    assert kinetic(vel, m) + lennard_jones(pos)[0] == pytest.approx(-12.5327297, abs=1e-6)
    drift = []
    for h in (0.005, 0.0025):
        x, v, energies = molecular_dynamics(pos, vel, m, lennard_jones, h, round(2.5 / h))
        drift.append(max(abs(e - energies[0]) for e in energies))
        # Newton's third law: the total momentum stays zero
        for c in range(3):
            assert abs(sum(p[c] for p in v)) < 1e-12
    assert drift[0] < 5e-3
    assert 3.0 < drift[0] / drift[1] < 5.5


def test_dimer_against_rk4_reference():
    # two atoms on a line: reduced to r'' = -2 U'(r) with unit masses
    r0, h, t_end = 1.3, 0.0005, 2.0
    x, v, _ = molecular_dynamics([[0.0], [r0]], [[0.0], [0.0]], [1.0, 1.0], lennard_jones, h, round(t_end / h))
    r_md = x[1][0] - x[0][0]

    def acc(r):
        return 2 * 24 * (2 * r ** -13 - r ** -7)

    r, w, hh = r0, 0.0, 1e-4
    for _ in range(round(t_end / hh)):
        k1r, k1w = w, acc(r)
        k2r, k2w = w + hh / 2 * k1w, acc(r + hh / 2 * k1r)
        k3r, k3w = w + hh / 2 * k2w, acc(r + hh / 2 * k2r)
        k4r, k4w = w + hh * k3w, acc(r + hh * k3r)
        r += hh / 6 * (k1r + 2 * k2r + 2 * k3r + k4r)
        w += hh / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
    assert r_md == pytest.approx(r, abs=1e-5)


def test_time_reversibility():
    pos, vel = cube_cluster(random.Random(3), 0.4)
    m = [1.0] * 8
    x, v, _ = molecular_dynamics(pos, vel, m, lennard_jones, 0.004, 300)
    back, vb, _ = molecular_dynamics(x, [[-c for c in p] for p in v], m, lennard_jones, 0.004, 300)
    for p, q in zip(back, pos):
        for a in range(3):
            assert p[a] == pytest.approx(q[a], abs=1e-8)


def test_edge_cases():
    x, v, e = molecular_dynamics([[1.0, 2.0]], [[0.5, 0.0]], [2.0], harmonic(0.0), 0.1, 10)
    assert x[0] == pytest.approx([1.5, 2.0]) and v[0] == [0.5, 0.0]
    assert e == pytest.approx([0.25] * 11)
    x, v, e = molecular_dynamics([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.1, 0)
    assert x == [[1.0]] and e == [0.5]
    # periodic wrap keeps a free particle in the box
    x, _, _ = molecular_dynamics([[4.9]], [[1.0]], [1.0], harmonic(0.0), 0.5, 1, box=5.0)
    assert x[0][0] == pytest.approx(0.4)
