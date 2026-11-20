# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lennard-jones-potential/. The authors are listed in prov/3RCYBF.jsonl.

import itertools
import math
import random

import pytest

from lennard_jones_potential import (
    energy_forces,
    pair,
    pair_force,
    phi,
    reduced_time_unit,
    tail_energy_per_atom,
    tail_pressure,
)

RMIN = 2 ** (1 / 6)


def test_check_values():
    assert RMIN == pytest.approx(1.122462, abs=1e-6)
    assert phi(RMIN) == pytest.approx(-1.0, abs=1e-14)
    assert pair_force(RMIN) == pytest.approx(0.0, abs=1e-12)
    assert phi(1.0) == 0.0
    assert pair_force(1.0) == pytest.approx(24.0)
    assert phi(2.5) == pytest.approx(-0.016317, abs=5e-7)


def test_scaling_with_eps_and_sigma():
    assert phi(2.0 * 3.4, eps=1.7, sigma=3.4) == pytest.approx(1.7 * phi(2.0))
    assert pair_force(2.0 * 3.4, eps=1.7, sigma=3.4) == pytest.approx(1.7 / 3.4 * pair_force(2.0))


def test_cube_of_eight_atoms():
    pos = [[RMIN * i, RMIN * j, RMIN * k] for i in range(2) for j in range(2) for k in range(2)]
    u, f = energy_forces(pos)
    assert u == pytest.approx(-15.1033, abs=5e-5)
    for fi in f:
        # each corner feels the same force, pointing to the center
        assert math.sqrt(sum(x * x for x in fi)) == pytest.approx(math.sqrt(sum(x * x for x in f[0])))
    assert [sum(fi[a] for fi in f) for a in range(3)] == pytest.approx([0.0, 0.0, 0.0], abs=1e-12)


def test_cutoff_variants():
    rc = 2.5
    assert pair(2.6, rc, "truncated") == (0.0, 0.0)
    assert pair(2.5 - 1e-9, rc, "shifted")[0] == pytest.approx(0.0, abs=1e-9)
    u, f = pair(2.5 - 1e-9, rc, "shifted-force")
    assert u == pytest.approx(0.0, abs=1e-12) and f == pytest.approx(0.0, abs=1e-8)
    assert pair(RMIN, rc, "shifted")[0] == pytest.approx(-1.0 + 0.016316891136)
    assert pair(2.0, rc, "truncated")[0] == pytest.approx(-0.0615234375)
    assert pair(2.0, rc, "shifted")[0] == pytest.approx(-0.045206546364)
    assert pair(2.0, rc, "shifted-force")[0] == pytest.approx(-0.0257068076376)
    # truncation and shifting do not change the force inside the cutoff
    assert pair(1.3, rc, "shifted")[1] == pair(1.3, rc, "truncated")[1] == pytest.approx(pair_force(1.3))


@pytest.mark.parametrize("variant,box", [("full", None), ("truncated", None), ("shifted-force", None), ("shifted", 6.0)])
def test_forces_are_minus_the_gradient(variant, box):
    rng = random.Random(5)
    pos = []
    while len(pos) < 12:
        p = [rng.uniform(0, 6.0) for _ in range(3)]
        if all(math.dist(p, q) > 0.95 for q in pos):
            pos.append(p)
    rc = None if variant == "full" else 2.5
    _, f = energy_forces(pos, rc, variant, box)
    h = 1e-6
    for i in range(0, 12, 3):
        for a in range(3):
            plus = [list(p) for p in pos]
            minus = [list(p) for p in pos]
            plus[i][a] += h
            minus[i][a] -= h
            num = -(energy_forces(plus, rc, variant, box)[0] - energy_forces(minus, rc, variant, box)[0]) / (2 * h)
            assert f[i][a] == pytest.approx(num, rel=1e-6, abs=1e-6)


def simpson(g, a, b, n):
    h = (b - a) / n
    s = g(a) + g(b)
    for k in range(1, n):
        s += (4 if k % 2 else 2) * g(a + k * h)
    return s * h / 3


def test_tail_corrections_against_quadrature():
    rho, rc = 0.8, 2.5
    # U_tail / N = 2 pi rho int_rc^inf r^2 phi(r) dr, with r = rc / t on (0, 1].
    u = 2 * math.pi * rho * simpson(lambda t: 0.0 if t == 0 else (rc / t) ** 2 * phi(rc / t) * rc / t ** 2, 0.0, 1.0, 2000)
    assert tail_energy_per_atom(rho, rc) == pytest.approx(u, rel=1e-8)
    # P_tail = -(2/3) pi rho^2 int_rc^inf r^3 phi'(r) dr.
    p = (2 / 3) * math.pi * rho ** 2 * simpson(lambda t: 0.0 if t == 0 else (rc / t) ** 3 * pair_force(rc / t) * rc / t ** 2, 0.0, 1.0, 2000)
    assert tail_pressure(rho, rc) == pytest.approx(p, rel=1e-8)
    assert tail_energy_per_atom(rho, rc) == pytest.approx(-0.428346, abs=1e-6)
    assert tail_pressure(rho, rc) == pytest.approx(-0.684417, abs=1e-6)


def test_fcc_lattice_sums_and_minimum():
    s6 = s12 = 0.0
    R = 8.0
    for i, j, k in itertools.product(range(-12, 13), repeat=3):
        if (i + j + k) % 2 == 0 and (i, j, k) != (0, 0, 0):
            d2 = (i * i + j * j + k * k) / 2.0
            if d2 <= R * R:
                s6 += d2 ** -3
                s12 += d2 ** -6
    s6 += math.sqrt(2) * 4 * math.pi / (3 * R ** 3)  # the r^-6 sum beyond R, as an integral
    assert s12 == pytest.approx(12.13188, abs=1e-5)
    assert s6 == pytest.approx(14.45392, abs=2e-4)
    rnn = (2 * s12 / s6) ** (1 / 6)
    assert rnn == pytest.approx(1.09017, abs=2e-5)
    assert -s6 * s6 / (2 * s12) == pytest.approx(-8.6102, abs=2e-4)


def test_argon_time_unit():
    m = 39.948 * 1.66053906660e-27
    assert reduced_time_unit(0.3405e-9, 119.8, m) == pytest.approx(2.156e-12, rel=1e-3)
