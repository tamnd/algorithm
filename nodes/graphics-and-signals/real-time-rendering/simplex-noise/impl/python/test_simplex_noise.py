# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-noise/. The authors are listed in prov/PWY9S0.jsonl.

"""Tests of simplex noise.

The 2D case is checked against a direct copy of the structure of Gustavson's
2D code. In 2, 3 and 4 dimensions the sum over the n + 1 corners is checked
against a brute force sum over every lattice point near the point, which is
the claim of the proof. The tests also check that the point lies in the
chosen simplex, the zeros at the lattice points, continuity, determinism for
a seed, and that a radius above 0.5 breaks the corner sum.
"""

import random
from itertools import product
from math import floor, sqrt

from simplex_noise import (
    GRAD3,
    SimplexNoise,
    corner_term,
    simplex_corners,
    skew_constants,
    unskew,
)


def gustavson_2d(xin, yin, perm):
    """The 2D noise written as in Gustavson's paper, with r^2 = 0.5 and scale 70."""
    F2 = 0.5 * (sqrt(3.0) - 1.0)
    G2 = (3.0 - sqrt(3.0)) / 6.0
    s = (xin + yin) * F2
    i, j = floor(xin + s), floor(yin + s)
    t = (i + j) * G2
    x0, y0 = xin - (i - t), yin - (j - t)
    i1, j1 = (1, 0) if x0 > y0 else (0, 1)
    x1, y1 = x0 - i1 + G2, y0 - j1 + G2
    x2, y2 = x0 - 1.0 + 2.0 * G2, y0 - 1.0 + 2.0 * G2
    ii, jj = i & 255, j & 255
    gi = (
        perm[ii + perm[jj]] % 12,
        perm[ii + i1 + perm[jj + j1]] % 12,
        perm[ii + 1 + perm[jj + 1]] % 12,
    )
    total = 0.0
    for g, (dx, dy) in zip(gi, ((x0, y0), (x1, y1), (x2, y2))):
        t = 0.5 - dx * dx - dy * dy
        if t > 0:
            t *= t
            total += t * t * (GRAD3[g][0] * dx + GRAD3[g][1] * dy)
    return 70.0 * total


def brute_force(noise, x, reach=2):
    """Sum the corner term of every lattice point whose skewed cell is near x."""
    n = len(x)
    F, _ = skew_constants(n)
    s = sum(x) * F
    base = [floor(c + s) for c in x]
    total = 0.0
    for off in product(range(-reach, reach + 1), repeat=n):
        k = tuple(b + o for b, o in zip(base, off))
        total += corner_term(x, k, noise.perm, noise.grads, noise.r2)
    return noise.scale * total


def test_matches_gustavson_2d():
    noise = SimplexNoise(n=2, seed=1)
    rng = random.Random(1)
    for _ in range(3000):
        x, y = rng.uniform(-300, 300), rng.uniform(-300, 300)
        assert abs(noise(x, y) - gustavson_2d(x, y, noise.perm)) < 1e-12


def test_skew_constants():
    F2, G2 = skew_constants(2)
    assert abs(F2 - (sqrt(3) - 1) / 2) < 1e-15
    assert abs(G2 - (3 - sqrt(3)) / 6) < 1e-15
    for n in range(1, 8):
        F, G = skew_constants(n)
        # The unskew undoes the skew: (1 + nF)(1 - nG) = 1.
        assert abs((1 + n * F) * (1 - n * G) - 1) < 1e-14


def test_point_lies_in_chosen_simplex():
    rng = random.Random(2)
    for n in (2, 3, 4, 5):
        F, _ = skew_constants(n)
        for _ in range(300):
            x = [rng.uniform(-50, 50) for _ in range(n)]
            y = [c + sum(x) * F for c in x]
            cs = simplex_corners(x)
            assert len(set(cs)) == n + 1
            # Barycentric weights in skewed space: differences of the sorted
            # fractional parts. They are nonnegative and rebuild the point.
            k = cs[0]
            f = sorted((a - b for a, b in zip(y, k)), reverse=True)
            lam = [1 - f[0]] + [f[m] - f[m + 1] for m in range(n - 1)] + [f[-1]]
            assert min(lam) >= -1e-12 and abs(sum(lam) - 1) < 1e-12
            rebuilt = [sum(lam[m] * cs[m][a] for m in range(n + 1)) for a in range(n)]
            assert max(abs(a - b) for a, b in zip(rebuilt, y)) < 1e-9


def test_corner_sum_equals_brute_force():
    rng = random.Random(3)
    for n, count in ((2, 400), (3, 200), (4, 40)):
        noise = SimplexNoise(n=n, seed=n)
        for _ in range(count):
            x = [rng.uniform(-40, 40) for _ in range(n)]
            assert abs(noise(*x) - brute_force(noise, x)) < 1e-12


def test_larger_radius_breaks_corner_sum():
    noise = SimplexNoise(n=3, seed=4, r2=0.6)
    rng = random.Random(4)
    worst = 0.0
    for _ in range(300):
        x = [rng.uniform(-20, 20) for _ in range(3)]
        worst = max(worst, abs(noise(*x) - brute_force(noise, x)))
    # With r2 = 0.5 the difference is below 1e-12 (the test above).
    assert worst > 1e-6


def test_zero_at_lattice_points():
    rng = random.Random(5)
    for n in (2, 3, 4):
        noise = SimplexNoise(n=n, seed=5)
        for _ in range(200):
            k = tuple(rng.randint(-300, 300) for _ in range(n))
            assert abs(noise(*unskew(k))) < 1e-9


def test_continuity():
    rng = random.Random(6)
    for n in (2, 3, 4):
        noise = SimplexNoise(n=n, seed=6)
        for _ in range(300):
            x = [rng.uniform(-20, 20) for _ in range(n)]
            e = [rng.uniform(-1e-7, 1e-7) for _ in range(n)]
            y = [a + b for a, b in zip(x, e)]
            assert abs(noise(*x) - noise(*y)) < 1e-4


def test_deterministic_for_seed():
    a, b, c = SimplexNoise(2, seed=9), SimplexNoise(2, seed=9), SimplexNoise(2, seed=10)
    rng = random.Random(7)
    pts = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(2000)]
    va = [a(*p) for p in pts]
    assert va == [b(*p) for p in pts]
    assert va != [c(*p) for p in pts]
    assert max(abs(v) for v in va) <= 1.0
