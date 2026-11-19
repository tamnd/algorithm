# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-linear-interface-calculation/. The authors are listed in prov/AZM3X0.jsonl.
import math
import random

from piecewise_linear_interface_calculation import (
    area,
    clip,
    disk_fractions,
    l1_error,
    line_constant,
    plic_advect,
    plic_flux,
    smeared_cells,
    strip_flux,
    total_volume,
    youngs_normal,
)

SQUARE = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


def band(n, x0, x1, along_x=True):
    dx = 1.0 / n
    prof = [max(0.0, min((i + 1) * dx, x1) - max(i * dx, x0)) / dx for i in range(n)]
    return [[prof[i] if along_x else prof[j] for j in range(n)] for i in range(n)]


def test_line_constant_hand_values():
    assert abs(line_constant(1.0, 1.0, 0.125) - 0.5) < 1e-15  # triangle x + y <= 1/2
    assert abs(line_constant(1.0, 2.0, 0.3) - 1.1) < 1e-15  # middle case, a = 0.36667
    assert abs(line_constant(1.0, 0.0, 0.3) - 0.3) < 1e-15  # vertical line x = 0.3
    assert abs(line_constant(-1.0, 0.0, 0.3) - (-0.7)) < 1e-15  # fluid on the right: x >= 0.7
    assert abs(strip_flux(1.0, 1.0, 0.5, 0.6, True) - 0.005) < 1e-15
    assert strip_flux(1.0, 1.0, 0.5, 0.3, True) == 0.0


def test_reconstruction_keeps_the_volume():
    rng = random.Random(3)
    for _ in range(3000):
        nx, ny, f = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.random()
        if rng.random() < 0.1:
            nx = 0.0
        b = line_constant(nx, ny, f)
        assert abs(area(clip(SQUARE, nx, ny, b)) - f) < 1e-14


def test_youngs_normal_directions():
    F = band(8, 0.2, 0.55)  # fluid on the left of x = 0.55 in cell 4
    nx, ny = youngs_normal(F, 4, 3)
    assert nx > 0 and ny == 0.0
    n = 8
    H = [[1.0 if i + j < n else (0.5 if i + j == n else 0.0) for j in range(n)] for i in range(n)]
    nx, ny = youngs_normal(H, 4, 4)
    assert nx > 0 and abs(nx - ny) < 1e-15  # the 45 degree normal is found exactly


def test_flux_bounds():
    rng = random.Random(5)
    n = 6
    for _ in range(300):
        F = [[rng.random() for _ in range(n)] for _ in range(n)]
        c = rng.random()
        d, j = rng.randrange(n), rng.randrange(n)
        for fwd in (True, False):
            for ax in (True, False):
                f = F[d][j] if ax else F[j][d]
                q = plic_flux(F, d, j, c, fwd, ax)
                assert max(0.0, c - (1.0 - f)) <= q <= min(c, f)


def test_band_translation_is_exact():
    n = 20
    dt = 0.3 / n
    for ax in (True, False):
        for s in (1.0, -1.0):
            u = (lambda y: s) if ax else (lambda y: 0.0)
            v = (lambda x: 0.0) if ax else (lambda x: s)
            F = plic_advect(band(n, 0.21, 0.52, ax), dt, 9, u, v)
            E = band(n, 0.21 + 9 * s * dt, 0.52 + 9 * s * dt, ax)
            assert max(abs(a - b) for ra, rb in zip(F, E) for a, b in zip(ra, rb)) < 1e-13


def test_rotation_is_sharp_and_conservative():
    n = 32
    w = 2 * math.pi
    F0 = disk_fractions(n, 0.5, 0.75, 0.15)
    steps = 201
    F = plic_advect(F0, 1.0 / steps, steps, lambda y: -w * (y - 0.5), lambda x: w * (x - 0.5))
    assert abs(total_volume(F) - total_volume(F0)) < 1e-14
    assert min(min(r) for r in F) >= 0.0 and max(max(r) for r in F) <= 1.0
    rel = l1_error(F, F0) / total_volume(F0)
    assert abs(rel - 0.0184) < 5e-4  # donor-acceptor gives 0.2378 on the same run
    assert smeared_cells(F) == smeared_cells(F0) == 36


def test_bad_input():
    for args in ((0.0, 0.0, 0.5), (1.0, 0.0, 1.5), (1.0, 0.0, -0.1)):
        try:
            line_constant(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    for dt, steps in ((0.2, 1), (0.0, 1), (0.1, -1)):
        try:
            plic_advect(band(8, 0.2, 0.5), dt, steps, lambda y: 1.0, lambda x: 0.0)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
