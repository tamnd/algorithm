# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smagorinsky-model/. The authors are listed in prov/XS6424.jsonl.

import math
import random

import pytest

from smagorinsky_model import (
    dissipation_2d,
    eddy_viscosity_from_gradient,
    lilly_constant,
    smagorinsky_2d,
    strain_magnitude_from_gradient,
    taylor_green,
)


def test_lilly_constant():
    assert lilly_constant(1.5) == pytest.approx(0.17327, abs=1e-5)
    assert lilly_constant(1.6) == pytest.approx(0.16508, abs=1e-5)


def test_pointwise_cases():
    # pure shear dU/dy = g gives |S| = g
    assert strain_magnitude_from_gradient([[0.0, 3.0], [0.0, 0.0]]) == pytest.approx(3.0)
    # solid-body rotation has no strain
    assert strain_magnitude_from_gradient([[0.0, -2.0], [2.0, 0.0]]) == 0.0
    # plane strain du/dx = a, dv/dy = -a gives |S| = 2a
    assert strain_magnitude_from_gradient([[1.5, 0.0], [0.0, -1.5]]) == pytest.approx(3.0)
    # SI example: Delta = 1 cm, |S| = 50 1/s, C_s = 0.1
    assert eddy_viscosity_from_gradient([[0.0, 50.0], [0.0, 0.0]], 0.1, 0.01) == pytest.approx(5e-5)
    # 3D gradient: rotation about z plus shear in x-z
    g = [[0.0, -1.0, 4.0], [1.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    assert strain_magnitude_from_gradient(g) == pytest.approx(4.0)


def test_taylor_green_exact_discrete_factor():
    n = 32
    u, v, h = taylor_green(n)
    cs = 0.17
    nut, mag = smagorinsky_2d(u, v, h, h, cs, h)
    factor = math.sin(h) / h
    assert factor == pytest.approx(0.993587, abs=1e-6)
    for i in range(n):
        for j in range(n):
            exact = 2 * abs(math.sin(i * h) * math.sin(j * h))
            assert mag[i][j] == pytest.approx(factor * exact, abs=1e-12)
    # at x = y = pi/2 (i = j = 8)
    assert nut[8][8] == pytest.approx((cs * h) ** 2 * 2 * factor, rel=1e-12)
    assert nut[8][8] == pytest.approx(2.2141e-3, abs=1e-7)


def test_second_order_convergence():
    errs = []
    for n in (16, 32, 64):
        u, v, h = taylor_green(n)
        _, mag = smagorinsky_2d(u, v, h, h, 0.17, 1.0)
        i = j = n // 4
        errs.append(abs(mag[i][j] - 2.0))
    for a, b in zip(errs, errs[1:]):
        assert math.log2(a / b) == pytest.approx(2.0, abs=0.05)


def random_field(n, rng):
    h = 2 * math.pi / n
    u = [[0.0] * n for _ in range(n)]
    v = [[0.0] * n for _ in range(n)]
    for _ in range(6):
        kx, ky = rng.randint(1, 4), rng.randint(1, 4)
        a, ph = rng.uniform(-1, 1), rng.uniform(0, 2 * math.pi)
        # stream function a sin(kx x + ky y + ph) gives a divergence-free field
        for i in range(n):
            for j in range(n):
                c = a * math.cos(kx * i * h + ky * j * h + ph)
                u[i][j] += ky * c
                v[i][j] -= kx * c
    return u, v, h


def test_nonnegative_and_galilean_invariant():
    rng = random.Random(2024)
    u, v, h = random_field(24, rng)
    diss = dissipation_2d(u, v, h, h, 0.17, h)
    assert min(min(row) for row in diss) >= 0.0
    nut, _ = smagorinsky_2d(u, v, h, h, 0.17, h)
    shifted = [[x + 3.7 for x in row] for row in u]
    nut2, _ = smagorinsky_2d(shifted, v, h, h, 0.17, h)
    for a, b in zip(nut, nut2):
        for x, y in zip(a, b):
            assert x == pytest.approx(y, abs=1e-12)
