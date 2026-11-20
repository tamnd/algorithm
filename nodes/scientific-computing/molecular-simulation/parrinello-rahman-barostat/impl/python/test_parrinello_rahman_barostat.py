# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parrinello-rahman-barostat/. The authors are listed in prov/A5VK4X.jsonl.
import math
import random

import pytest

from parrinello_rahman_barostat import (
    det2,
    lj_force_shifted,
    pair_forces,
    parrinello_rahman,
    triangular_lattice,
)

PHI = lj_force_shifted(1.8)
ZERO = [[0.0, 0.0], [0.0, 0.0]]


def lattice(seed, spread=0.3):
    pos, cell = triangular_lattice(4, 6, 1.12)
    rng = random.Random(seed)
    vel = [[rng.gauss(0.0, spread), rng.gauss(0.0, spread)] for _ in pos]
    cm = [sum(v[a] for v in vel) / len(vel) for a in range(2)]
    return pos, [[v[0] - cm[0], v[1] - cm[1]] for v in vel], cell


def test_enthalpy_is_conserved_with_second_order_error():
    pos, vel, cell = lattice(3)
    m = [1.0] * len(pos)
    spreads = []
    for h in (0.01, 0.005, 0.0025):
        out = parrinello_rahman(pos, vel, m, cell, ZERO, PHI, h, round(0.5 / h), 1.0, 5.0)[4]
        es = [o[0] for o in out]
        spreads.append(max(es) - min(es))
    assert spreads[0] / spreads[1] == pytest.approx(4.0, rel=0.15)
    assert spreads[1] / spreads[2] == pytest.approx(4.0, rel=0.15)


def test_time_reversible():
    pos, vel, cell = lattice(4)
    m = [1.0] * len(pos)
    cv = [[0.01, 0.002], [-0.003, -0.02]]
    r, v, c, cd, _ = parrinello_rahman(pos, vel, m, cell, cv, PHI, 0.005, 150, 1.0, 5.0)
    neg = [[-x for x in row] for row in v]
    r, v, c, cd, _ = parrinello_rahman(r, neg, m, c, [[-x for x in row] for row in cd], PHI, 0.005, 150, 1.0, 5.0)
    for a, b in zip(r, pos):
        assert a == pytest.approx(b, abs=1e-9)
    for a, b in zip(v, vel):
        assert [-x for x in a] == pytest.approx(b, abs=1e-9)
    for a, b in zip(c, cell):
        assert a == pytest.approx(b, abs=1e-9)


def velocity_verlet_fixed_cell(pos, vel, cell, h, steps):
    """Reference: plain velocity Verlet in the fixed rectangular cell."""
    lx, ly = cell[0][0], cell[1][1]
    r = [list(p) for p in pos]
    v = [list(p) for p in vel]

    def forces():
        f = [[0.0, 0.0] for _ in r]
        for i in range(len(r)):
            for j in range(i + 1, len(r)):
                dx = r[i][0] - r[j][0]
                dy = r[i][1] - r[j][1]
                dx -= lx * round(dx / lx)
                dy -= ly * round(dy / ly)
                d = math.hypot(dx, dy)
                if d < PHI.rc:
                    _, mag = PHI(d)
                    f[i][0] += mag * dx / d
                    f[i][1] += mag * dy / d
                    f[j][0] -= mag * dx / d
                    f[j][1] -= mag * dy / d
        return f
    f = forces()
    for _ in range(steps):
        for i in range(len(r)):
            for a in range(2):
                v[i][a] += 0.5 * h * f[i][a]
                r[i][a] += h * v[i][a]
        f = forces()
        for i in range(len(r)):
            for a in range(2):
                v[i][a] += 0.5 * h * f[i][a]
    return r, v


def test_heavy_cell_reduces_to_constant_volume_dynamics():
    pos, vel, cell = lattice(5)
    m = [1.0] * len(pos)
    r, v, c, _, out = parrinello_rahman(pos, vel, m, cell, ZERO, PHI, 0.01, 100, 1.0, 1e14)
    r_ref, v_ref = velocity_verlet_fixed_cell(pos, vel, cell, 0.01, 100)
    for a, b in zip(r, r_ref):
        assert a == pytest.approx(b, abs=1e-7)
    for a, b in zip(v, v_ref):
        assert a == pytest.approx(b, abs=1e-7)
    assert out[-1][1] == pytest.approx(det2(cell), rel=1e-9)


def test_cell_shrinks_under_high_pressure_and_grows_under_low_pressure():
    pos, vel, cell = lattice(6)
    m = [1.0] * len(pos)
    v0 = det2(cell)
    high = parrinello_rahman(pos, vel, m, cell, ZERO, PHI, 0.01, 60, 4.0, 5.0)[4]
    low = parrinello_rahman(pos, vel, m, cell, ZERO, PHI, 0.01, 60, -1.0, 5.0)[4]
    assert high[-1][1] < v0 < low[-1][1]


def test_internal_pressure_averages_to_the_external_pressure():
    # W d^2H/dt^2 = det(H) (Pi - P) H^-T, and dH/dt stays bounded, so the
    # time average of the internal pressure tends to P.
    pos, vel, cell = lattice(3)
    m = [1.0] * len(pos)
    for pressure in (0.5, 1.5):
        out = parrinello_rahman(pos, vel, m, cell, ZERO, PHI, 0.01, 400, pressure, 2.0)[4]
        p = [0.5 * (o[2][0][0] + o[2][1][1]) for o in out]
        assert sum(p) / len(p) == pytest.approx(pressure, abs=0.05)


def test_virial_matches_finite_difference_of_energy_under_strain():
    # dU/dH = -sum f_ij s_ij^T: compare with a central difference.
    pos, _, cell = lattice(7)
    rng = random.Random(7)
    pos = [[x + rng.uniform(-0.05, 0.05), y + rng.uniform(-0.05, 0.05)] for x, y in pos]
    inv = [[1 / cell[0][0], 0.0], [0.0, 1 / cell[1][1]]]
    s = [[inv[0][0] * x, inv[1][1] * y] for x, y in pos]
    _, _, fs, _ = pair_forces(s, cell, PHI)
    eps = 1e-6
    for a in range(2):
        for b in range(2):
            up = [list(row) for row in cell]
            dn = [list(row) for row in cell]
            up[a][b] += eps
            dn[a][b] -= eps
            du = (pair_forces(s, up, PHI)[0] - pair_forces(s, dn, PHI)[0]) / (2 * eps)
            assert -du == pytest.approx(fs[a][b], abs=1e-5)


def test_cutoff_larger_than_half_the_cell_raises():
    pos, _, cell = lattice(1)
    with pytest.raises(ValueError):
        pair_forces([[0.0, 0.0], [0.5, 0.5]], [[3.0, 0.0], [0.0, 3.0]], PHI)
