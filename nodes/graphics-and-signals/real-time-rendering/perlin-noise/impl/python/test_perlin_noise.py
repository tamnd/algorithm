# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perlin-noise/. The authors are listed in prov/QWP9HR.jsonl.

"""Tests of improved Perlin noise.

The nested lerps of the implementation are checked against a direct sum of
the 8 corner terms with tensor product weights, exactly on rational points.
The tests also check the zeros at the lattice points, the gradient there,
the fade conditions, the period 256, determinism for a seed and the bound 2.
"""

import random
from fractions import Fraction
from math import floor

from perlin_noise import GRADIENTS, PerlinNoise, corner_gradient, fade, grad, noise


def reference(x, y, z, perm):
    """Sum over the 8 corners of w_a(x) w_b(y) w_c(z) g . (p - corner)."""
    fx, fy, fz = floor(x), floor(y), floor(z)
    tx, ty, tz = x - fx, y - fy, z - fz
    total = 0
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                g = corner_gradient(fx + a, fy + b, fz + c, perm)
                d = (tx - a, ty - b, tz - c)
                wx = fade(tx) if a else 1 - fade(tx)
                wy = fade(ty) if b else 1 - fade(ty)
                wz = fade(tz) if c else 1 - fade(tz)
                total += wx * wy * wz * (g[0] * d[0] + g[1] * d[1] + g[2] * d[2])
    return total


def rand_point(rng, lo=-20, hi=20):
    return tuple(Fraction(rng.randint(lo * 64, hi * 64), 64) for _ in range(3))


def test_grad_matches_table():
    rng = random.Random(1)
    for h in range(256):
        x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)
        g = GRADIENTS[h & 15]
        assert abs(grad(h, x, y, z) - (g[0] * x + g[1] * y + g[2] * z)) < 1e-15
    assert sorted(set(GRADIENTS)) == sorted(
        {v for v in GRADIENTS if sum(abs(c) for c in v) == 2})
    assert len(set(GRADIENTS)) == 12


def test_against_direct_sum_exact():
    n = PerlinNoise(seed=7)
    rng = random.Random(2)
    for _ in range(300):
        x, y, z = rand_point(rng)
        assert noise(x, y, z, n.perm) == reference(x, y, z, n.perm)


def test_zero_at_lattice_points():
    n = PerlinNoise(seed=3)
    rng = random.Random(3)
    for _ in range(300):
        i, j, k = rng.randint(-600, 600), rng.randint(-600, 600), rng.randint(-600, 600)
        assert n(i, j, k) == 0
        assert n(float(i), float(j), float(k)) == 0.0


def test_fade_conditions():
    f = fade
    assert f(Fraction(0)) == 0 and f(Fraction(1)) == 1
    # f'(t) = 30 t^2 (t - 1)^2 and f''(t) = 60 t (t - 1) (2t - 1), so both
    # vanish at 0 and 1. Check them by exact finite differences of the polynomial.
    e = Fraction(1, 10 ** 6)
    for t in (Fraction(0), Fraction(1)):
        d1 = (f(t + e) - f(t - e)) / (2 * e)
        d2 = (f(t + e) - 2 * f(t) + f(t - e)) / (e * e)
        assert abs(d1) < Fraction(1, 10 ** 10) and abs(d2) < Fraction(1, 10 ** 4)
    rng = random.Random(4)
    for _ in range(100):
        t = Fraction(rng.randint(0, 1000), 1000)
        assert f(t) == 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3
        assert 0 <= f(t) <= 1


def test_gradient_at_lattice_point_is_corner_gradient():
    n = PerlinNoise(seed=5)
    rng = random.Random(5)
    h = 1e-6
    for _ in range(50):
        i, j, k = rng.randint(-50, 50), rng.randint(-50, 50), rng.randint(-50, 50)
        g = corner_gradient(i, j, k, n.perm)
        num = (
            (n(i + h, j, k) - n(i - h, j, k)) / (2 * h),
            (n(i, j + h, k) - n(i, j - h, k)) / (2 * h),
            (n(i, j, k + h) - n(i, j, k - h)) / (2 * h),
        )
        for a, b in zip(num, g):
            assert abs(a - b) < 1e-6


def test_period_256_and_continuity():
    n = PerlinNoise(seed=6)
    rng = random.Random(6)
    for _ in range(200):
        x, y, z = rng.uniform(-10, 10), rng.uniform(-10, 10), rng.uniform(-10, 10)
        assert abs(n(x, y, z) - n(x + 256, y - 512, z + 256)) < 1e-9
    for _ in range(200):
        k = rng.randint(-20, 20)
        y, z = rng.uniform(-5, 5), rng.uniform(-5, 5)
        assert abs(n(k - 1e-9, y, z) - n(k + 1e-9, y, z)) < 1e-7


def test_deterministic_for_seed_and_bounded():
    a, b, c = PerlinNoise(seed=11), PerlinNoise(seed=11), PerlinNoise(seed=12)
    rng = random.Random(8)
    pts = [(rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(-30, 30)) for _ in range(2000)]
    va = [a(*p) for p in pts]
    assert va == [b(*p) for p in pts]
    assert va != [c(*p) for p in pts]
    # Each corner term is at most |d_i| + |d_j| <= 2, and the weights are convex.
    assert max(abs(v) for v in va) <= 2
    assert abs(sum(va) / len(va)) < 0.05
