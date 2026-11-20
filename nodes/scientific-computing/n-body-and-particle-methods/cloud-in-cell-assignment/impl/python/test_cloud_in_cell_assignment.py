# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cloud-in-cell-assignment/. The authors are listed in prov/JDCYVP.jsonl.
import random
from fractions import Fraction as Fr

import pytest

from cloud_in_cell_assignment import (
    cic_deposit,
    cic_deposit_2d,
    cic_interpolate,
    cic_interpolate_2d,
)


def brute_deposit(xs, qs, m, length):
    """Oracle: rho_j = sum_i q_i W(x_i - x_j) / dx with the hat W, summed over periodic images."""
    dx = length / m
    rho = []
    for j in range(m):
        s = 0.0
        for x, q in zip(xs, qs):
            for k in range(-4, 5):
                d = abs(x - j * dx - k * length)
                s += q * max(0.0, 1 - d / dx) / dx
        rho.append(s)
    return rho


def field_from_density(rho, length):
    """Periodic 1D field with dE/dx = rho - mean(rho) and zero mean.

    E at the half points is a running sum; E at grid point j is the mean of the
    two half points around it. This is minus the centred difference of the
    potential of the 3-point Laplacian, so its kernel is antisymmetric.
    """
    m = len(rho)
    dx = length / m
    mean = sum(rho) / m
    half, acc = [], 0 * dx
    for r in rho:
        acc += dx * (r - mean)
        half.append(acc)
    shift = sum(half) / m
    half = [h - shift for h in half]
    return [(half[j] + half[j - 1]) / 2 for j in range(m)]


def test_page_example():
    rho = cic_deposit([0.25, 1.5, 3.75], [1, 2, 1], 4, 4.0)
    assert rho == [1.5, 1.25, 1.0, 0.25]
    e = cic_interpolate([1.0, 0.0, -1.0, 0.0], [0.25, 1.5, 3.75], 4.0)
    assert e == [0.75, -0.5, 0.75]


def test_matches_brute_force():
    rng = random.Random(11)
    for _ in range(500):
        m = rng.randint(1, 9)
        length = rng.uniform(0.5, 5.0)
        n = rng.randint(0, 6)
        xs = [rng.uniform(-length, 2 * length) for _ in range(n)]
        qs = [rng.uniform(-2, 2) for _ in range(n)]
        got = cic_deposit(xs, qs, m, length)
        want = brute_deposit(xs, qs, m, length)
        assert got == pytest.approx(want, abs=1e-9)


def test_charge_conserved_exactly():
    rng = random.Random(5)
    for _ in range(200):
        m = rng.randint(1, 12)
        length = Fr(rng.randint(1, 30), rng.randint(1, 7))
        n = rng.randint(0, 8)
        xs = [Fr(rng.randint(-500, 500), rng.randint(1, 50)) for _ in range(n)]
        qs = [Fr(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        rho = cic_deposit(xs, qs, m, length)
        assert sum(rho) * (length / m) == sum(qs)


def test_particle_on_grid_point():
    rho = cic_deposit([Fr(3)], [Fr(2)], 8, Fr(8))
    assert rho == [0, 0, 0, 2, 0, 0, 0, 0]
    assert cic_deposit([], [], 3, 1.0) == [0.0, 0.0, 0.0]


def test_interpolation_reproduces_linear_fields():
    # Away from the periodic seam, CIC interpolation is exact for a + b x.
    m, length = 10, Fr(10)
    field = [Fr(3) - Fr(1, 2) * j for j in range(m)]
    rng = random.Random(2)
    xs = [Fr(rng.randint(0, 899), 100) for _ in range(100)]
    got = cic_interpolate(field, xs, length)
    assert got == [Fr(3) - Fr(1, 2) * x for x in xs]


def test_no_self_force_and_momentum_conserved_exactly():
    rng = random.Random(7)
    length, m = Fr(16), 16
    # one particle: its own field gives it no force, wherever it is
    for _ in range(50):
        x = Fr(rng.randint(0, 1599), 100)
        rho = cic_deposit([x], [Fr(1)], m, length)
        e = cic_interpolate(field_from_density(rho, length), [x], length)
        assert e == [0]
    # many particles: the forces sum to zero exactly
    for _ in range(30):
        n = rng.randint(2, 10)
        xs = [Fr(rng.randint(0, 1599), 100) for _ in range(n)]
        qs = [Fr(rng.randint(-5, 5)) for _ in range(n)]
        rho = cic_deposit(xs, qs, m, length)
        e = cic_interpolate(field_from_density(rho, length), xs, length)
        assert sum(q * ei for q, ei in zip(qs, e)) == 0


def test_2d_conservation_and_bilinear_reproduction():
    rng = random.Random(3)
    nx, ny, lx, ly = 4, 6, Fr(2), Fr(3)
    ps = [(Fr(rng.randint(0, 199), 100), Fr(rng.randint(0, 299), 100)) for _ in range(20)]
    qs = [Fr(rng.randint(1, 4)) for _ in ps]
    rho = cic_deposit_2d(ps, qs, nx, ny, lx, ly)
    assert sum(map(sum, rho)) * (lx / nx) * (ly / ny) == sum(qs)
    # a bilinear field a + b x + c y + d x y is reproduced inside one period
    dx, dy = lx / nx, ly / ny
    f = lambda x, y: 1 + 2 * x - 3 * y + x * y
    field = [[f(i * dx, j * dy) for j in range(ny)] for i in range(nx)]
    inside = [(x, y) for x, y in ps if x < lx - dx and y < ly - dy]
    got = cic_interpolate_2d(field, inside, lx, ly)
    assert got == [f(x, y) for x, y in inside]


def test_2d_matches_product_of_1d_weights():
    rng = random.Random(9)
    for _ in range(100):
        x, y = rng.uniform(0, 3), rng.uniform(0, 2)
        rho = cic_deposit_2d([(x, y)], [1.0], 3, 2, 3.0, 2.0)
        rx = cic_deposit([x], [1.0], 3, 3.0)
        ry = cic_deposit([y], [1.0], 2, 2.0)
        for i in range(3):
            for j in range(2):
                assert rho[i][j] == pytest.approx(rx[i] * ry[j], abs=1e-12)
