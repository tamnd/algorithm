# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/worley-noise/. The authors are listed in prov/KRW8CM.jsonl.

"""Tests of Worley noise.

The ring search is checked against a brute force search over every feature
point of a large block of cells. The tests also check the ring enumeration,
determinism for a seed, the 1-Lipschitz bound, the mean point count, and
that the 3 x 3 shortcut is not always exact.
"""

import random
from math import dist as euclid

from worley_noise import (
    WorleyNoise,
    cell_points,
    nearest_brute_force,
    ring,
    three_by_three,
    worley,
)


def block_points(seed, density, lo=-8, hi=8):
    pts = []
    for i in range(lo, hi):
        for j in range(lo, hi):
            pts.extend(cell_points(seed, i, j, density))
    return pts


def test_ring_enumerates_each_cell_once():
    for r in range(6):
        cells = list(ring(3, -2, r))
        assert len(cells) == len(set(cells)) == (1 if r == 0 else 8 * r)
        assert all(max(abs(i - 3), abs(j + 2)) == r for i, j in cells)


def test_equals_brute_force():
    rng = random.Random(1)
    for seed, density in ((0, 2.0), (1, 0.7), (2, 4.0)):
        pts = block_points(seed, density)
        for metric in ("euclidean", "manhattan", "chebyshev"):
            for _ in range(150):
                x, y = rng.uniform(-2, 2), rng.uniform(-2, 2)
                k = rng.randint(1, 4)
                want = nearest_brute_force(x, y, pts, k, metric)
                # Points within distance 6 of a query in [-2, 2]^2 lie in the block.
                assert want[-1] < 6
                assert worley(x, y, k, seed, density, metric) == want


def test_deterministic_for_seed():
    a, b, c = WorleyNoise(seed=5), WorleyNoise(seed=5), WorleyNoise(seed=6)
    rng = random.Random(2)
    pts = [(rng.uniform(-50, 50), rng.uniform(-50, 50)) for _ in range(500)]
    va = [a(*p) for p in pts]
    assert va == [b(*p) for p in pts]
    assert va != [c(*p) for p in pts]


def test_order_zero_at_points_and_lipschitz():
    noise = WorleyNoise(seed=3, k=3)
    for (px, py) in noise.points(0, 0) + noise.points(4, -1):
        assert noise(px, py)[0] == 0.0
    rng = random.Random(3)
    for _ in range(500):
        p = (rng.uniform(-20, 20), rng.uniform(-20, 20))
        q = (p[0] + rng.uniform(-0.3, 0.3), p[1] + rng.uniform(-0.3, 0.3))
        fp, fq = noise(*p), noise(*q)
        assert fp == sorted(fp)
        assert noise.f2_minus_f1(*p) >= 0
        # Each F_k is 1-Lipschitz in the Euclidean metric.
        for a, b in zip(fp, fq):
            assert abs(a - b) <= euclid(p, q) + 1e-12


def test_mean_point_count():
    for density in (0.5, 2.0, 5.0):
        counts = [len(cell_points(9, i, j, density)) for i in range(60) for j in range(60)]
        mean = sum(counts) / len(counts)
        assert abs(mean - density) < 0.15 * density + 0.05


def test_three_by_three_shortcut_is_not_always_exact():
    rng = random.Random(4)
    wrong = 0
    for _ in range(1500):
        x, y = rng.uniform(-100, 100), rng.uniform(-100, 100)
        exact = worley(x, y, 1, seed=7, density=0.5)
        if three_by_three(x, y, 1, seed=7, density=0.5) != exact:
            wrong += 1
    # A measurement: with a mean of 0.5 points per cell a few percent of the
    # queries get a wrong F1 from the shortcut.
    assert wrong > 0
