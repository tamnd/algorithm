# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/height-field-water/. The authors are listed in prov/CH9SFZ.jsonl.

import math
import random
from fractions import Fraction

import height_field_water as hw


def gauss_solve(a, b):
    """Gaussian elimination with exact Fraction arithmetic and row pivoting."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def test_thomas_matches_gaussian_elimination() -> None:
    rng = random.Random(1)
    for n in (1, 2, 3, 7):
        sub = [Fraction(rng.randint(-5, 5), rng.randint(1, 5)) for _ in range(n)]
        sup = [Fraction(rng.randint(-5, 5), rng.randint(1, 5)) for _ in range(n)]
        diag = [abs(sub[i]) + abs(sup[i]) + Fraction(rng.randint(1, 9), rng.randint(1, 3)) for i in range(n)]
        rhs = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        a = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            a[i][i] = diag[i]
            if i > 0:
                a[i][i - 1] = sub[i]
            if i < n - 1:
                a[i][i + 1] = sup[i]
        assert hw.thomas(sub, diag, sup, rhs) == gauss_solve(a, rhs)


def test_volume_is_kept_exactly() -> None:
    rng = random.Random(2)
    nx, ny = 4, 3
    h = [[Fraction(rng.randint(8, 12), 10) for _ in range(ny)] for _ in range(nx)]
    h_prev = [[x + Fraction(rng.randint(-2, 2), 100) for x in col] for col in h]
    shift = (sum(map(sum, h)) - sum(map(sum, h_prev))) / (nx * ny)
    h_prev = [[x + shift for x in col] for col in h_prev]
    depth = [[Fraction(rng.randint(0, 10), 10) for _ in range(ny)] for _ in range(nx)]
    dx, dt = Fraction(1, 10), Fraction(1, 50)
    v0 = hw.volume(h, dx)
    assert hw.volume(h_prev, dx) == v0
    for _ in range(2):
        h, h_prev = hw.step(h, h_prev, depth, dt, dx, Fraction(981, 100), Fraction(1, 10))
        assert hw.volume(h, dx) == v0


def bump(nx, ny, dx):
    return [[1.0 + 0.05 * math.exp(-(((i - 0.4 * nx) ** 2 + (j - 0.5 * ny) ** 2) * dx * dx / 0.06))
             for j in range(ny)] for i in range(nx)]


def test_energy_does_not_increase_for_a_constant_depth() -> None:
    nx = ny = 12
    dx, dt = 0.1, 0.03
    h = bump(nx, ny, dx)
    h_prev = [list(col) for col in h]
    depth = [[1.0] * ny for _ in range(nx)]
    e = hw.discrete_energy(h, h_prev, depth, dt, dx)
    e0 = e
    for _ in range(25):
        h_new, h_prev = hw.step(h, h_prev, depth, dt, dx)
        h = h_new
        e_new = hw.discrete_energy(h, h_prev, depth, dt, dx)
        assert e_new <= e * (1.0 + 1e-12)
        e = e_new
    assert e < e0


def test_wave_speed_is_close_to_the_shallow_water_speed() -> None:
    # A measurement: a bump in a channel of depth 1 m splits into two waves with speed (g d)^(1/2) = 3.13209 m/s.
    nx, dx, dt = 400, 0.025, 0.01
    xs = [(i + 0.5) * dx for i in range(nx)]
    h = [[1.0 + 0.01 * math.exp(-((x - 5.0) / 0.2) ** 2)] for x in xs]
    h_prev = [list(col) for col in h]
    depth = [[1.0] for _ in xs]
    for _ in range(100):
        h, h_prev = hw.step(h, h_prev, depth, dt, dx)
    peak = max((h[i][0], xs[i]) for i in range(nx) if xs[i] > 5.0)[1]
    assert abs(math.sqrt(9.81 * 1.0) - 3.13209) < 1e-5
    assert abs((peak - 5.0) - 3.13209) < 0.03 * 3.13209


def test_flat_lake_over_rough_ground_stays_flat() -> None:
    rng = random.Random(3)
    nx, ny, dx = 8, 6, 0.1
    ground = [[rng.uniform(0.0, 1.5) for _ in range(ny)] for _ in range(nx)]
    h = [[max(1.0, ground[i][j]) for j in range(ny)] for i in range(nx)]
    out = hw.simulate(h, ground, 0.02, dx, 10)
    assert max(abs(out[i][j] - h[i][j]) for i in range(nx) for j in range(ny)) < 1e-12


def test_simulate_keeps_the_volume_with_a_changing_depth() -> None:
    rng = random.Random(4)
    nx, ny, dx = 10, 8, 0.1
    ground = [[rng.uniform(0.0, 0.5) for _ in range(ny)] for _ in range(nx)]
    h = bump(nx, ny, dx)
    out = hw.simulate(h, ground, 0.02, dx, 20, damping=0.05)
    assert abs(hw.volume(out, dx) - hw.volume(h, dx)) < 1e-12
