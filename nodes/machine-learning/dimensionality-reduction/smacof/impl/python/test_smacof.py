# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smacof/. The authors are listed in prov/8BX53A.jsonl.

import math
import random

from smacof import center, guttman_transform, majorizer, raw_stress, smacof


def euclid(points):
    return [[math.dist(p, q) for q in points] for p in points]


def noisy_delta(rng, n, dim, noise):
    pts = [tuple(rng.uniform(0, 5) for _ in range(dim)) for _ in range(n)]
    d = euclid(pts)
    delta = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            delta[i][j] = delta[j][i] = d[i][j] * math.exp(rng.gauss(0, noise))
    return pts, delta


def test_stress_never_increases():
    for seed in range(6):
        rng = random.Random(seed)
        _, delta = noisy_delta(rng, 10, 3, 0.2)
        x0 = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(10)]
        _, hist = smacof(delta, x0, max_iter=200)
        assert all(b <= a + 1e-12 for a, b in zip(hist, hist[1:]))


def test_sandwich_bound_on_step():
    # sigma(Z) - sigma(X+) >= n ||Z - X+||^2 for a centered Z
    rng = random.Random(3)
    _, delta = noisy_delta(rng, 8, 2, 0.3)
    z = center([(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(8)])
    xp = guttman_transform(z, delta)
    gap = raw_stress(z, delta) - raw_stress(xp, delta)
    step = sum((a - b) ** 2 for p, q in zip(z, xp) for a, b in zip(p, q))
    assert gap >= 8 * step - 1e-9


def test_majorizer_touches_and_bounds():
    rng = random.Random(9)
    _, delta = noisy_delta(rng, 7, 2, 0.3)
    z = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(7)]
    assert abs(majorizer(z, z, delta) - raw_stress(z, delta)) < 1e-9
    for _ in range(50):
        x = [(rng.gauss(0, 2), rng.gauss(0, 2)) for _ in range(7)]
        assert raw_stress(x, delta) <= majorizer(x, z, delta) + 1e-9


def test_exact_configuration_is_a_fixed_point():
    rng = random.Random(1)
    pts = center([(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(6)])
    y = guttman_transform(pts, euclid(pts))
    assert max(abs(a - b) for p, q in zip(pts, y) for a, b in zip(p, q)) < 1e-12


def test_converges_to_zero_stress_on_euclidean_input():
    rng = random.Random(5)
    pts = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(8)]
    x0 = [(p[0] + rng.gauss(0, 0.5), p[1] + rng.gauss(0, 0.5)) for p in pts]
    x, hist = smacof(euclid(pts), x0, max_iter=2000)
    assert hist[-1] < 1e-8
    dx = euclid(x)
    d = euclid(pts)
    assert max(abs(dx[i][j] - d[i][j]) for i in range(8) for j in range(8)) < 1e-4
