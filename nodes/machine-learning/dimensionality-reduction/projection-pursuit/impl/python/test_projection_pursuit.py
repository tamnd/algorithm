# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/projection-pursuit/. The authors are listed in prov/WHZFZK.jsonl.

import math
import random

import pytest

from projection_pursuit import (
    GAUSS_LOGCOSH,
    friedman_tukey_index,
    moment_index,
    negentropy_index,
    projection_pursuit,
    sphere,
)


def bimodal_plane(rng: random.Random, n: int, angle_deg: float) -> list:
    """A bimodal coordinate with small variance and a Gaussian one with large variance, then rotated."""
    c, s = math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))
    out = []
    for _ in range(n):
        a = rng.choice([-1.0, 1.0]) + 0.3 * rng.gauss(0, 1)
        b = 2.0 * rng.gauss(0, 1)
        out.append([c * a - s * b, s * a + c * b])
    return out


def abs_corr(u: list, v: list) -> float:
    n = len(u)
    mu, mv = sum(u) / n, sum(v) / n
    cuv = sum((a - mu) * (b - mv) for a, b in zip(u, v))
    return abs(cuv) / math.sqrt(sum((a - mu) ** 2 for a in u) * sum((b - mv) ** 2 for b in v))


def test_moment_index_exact_values() -> None:
    # Two-point symmetric: k3 = 0, k4 = -2, index 1/12.
    assert moment_index([-1.0, 1.0] * 50) == pytest.approx(1 / 12, abs=1e-12)
    # Uniform on {-1, 0, 1}: k4 = -1.5, index 2.25 / 48.
    assert moment_index([-1.0, 0.0, 1.0] * 40) == pytest.approx(2.25 / 48, abs=1e-12)
    # Bernoulli(1/4): k3^2 = 4/3, k4 = -2/3, index 13/108.
    assert moment_index([0.0, 0.0, 0.0, 1.0] * 30) == pytest.approx(13 / 108, abs=1e-12)


def test_indices_are_affine_invariant() -> None:
    rng = random.Random(1)
    y = [rng.expovariate(1.0) for _ in range(500)]
    for a, b in [(3.0, 1.0), (-0.5, 7.0)]:
        y2 = [a * v + b for v in y]
        assert moment_index(y2) == pytest.approx(moment_index(y), rel=1e-9)
        assert friedman_tukey_index(y2[:200]) == pytest.approx(friedman_tukey_index(y[:200]), rel=1e-9)
    assert negentropy_index([3.0 * v + 1.0 for v in y]) == pytest.approx(negentropy_index(y), rel=1e-9)


def test_gaussian_projections_score_near_zero() -> None:
    assert GAUSS_LOGCOSH == pytest.approx(0.374567, abs=1e-6)
    rng = random.Random(2)
    g = [rng.gauss(0, 1) for _ in range(20000)]
    b = [rng.choice([-1.0, 1.0]) + 0.3 * rng.gauss(0, 1) for _ in range(20000)]
    assert moment_index(g) < 0.002 < moment_index(b)
    assert negentropy_index(g) < 1e-4 < negentropy_index(b)
    assert friedman_tukey_index(g[:300]) < friedman_tukey_index(b[:300])


def test_pursuit_finds_bimodal_axis_and_matches_grid() -> None:
    xs = bimodal_plane(random.Random(3), 600, 30.0)
    dirs, vals = projection_pursuit(xs, 1, random.Random(4))
    z, v = sphere(xs)
    grid = max(moment_index([math.cos(t) * zt[0] + math.sin(t) * zt[1] for zt in z])
               for t in [math.pi * i / 1800 for i in range(1800)])
    assert vals[0] >= grid - 1e-9
    assert vals[0] - grid < 1e-5
    d = dirs[0]
    angle = math.degrees(math.atan2(d[1], d[0])) % 180.0
    assert abs(angle - 30.0) < 3.0


def test_pursuit_beats_pca_on_the_example() -> None:
    xs = bimodal_plane(random.Random(5), 600, 30.0)
    n = len(xs)
    mean = [sum(x[j] for x in xs) / n for j in range(2)]
    proj = lambda w: [sum(a * (x[j] - mean[j]) for j, a in enumerate(w)) for x in xs]
    # PCA's first axis is the Gaussian one at 120 degrees, which scores near 0.
    pc_like = [math.cos(math.radians(120)), math.sin(math.radians(120))]
    dirs, vals = projection_pursuit(xs, 1, random.Random(6))
    assert moment_index(proj(pc_like)) < 0.01 < vals[0]


def test_deflation_in_three_dimensions() -> None:
    rng = random.Random(7)
    srcs, xs = [], []
    a = [[1.0, 0.5, 0.2], [0.3, 1.0, 0.4], [0.2, 0.1, 1.0]]
    for _ in range(800):
        s = [rng.choice([-1.0, 1.0]) + 0.2 * rng.gauss(0, 1), rng.expovariate(1.0), rng.gauss(0, 1)]
        srcs.append(s)
        xs.append([sum(a[i][j] * s[j] for j in range(3)) for i in range(3)])
    dirs, vals = projection_pursuit(xs, 2, random.Random(8), restarts=3)
    assert vals[0] >= vals[1] > 0.05
    n = len(xs)
    mean = [sum(x[j] for x in xs) / n for j in range(3)]
    outs = [[sum(w[j] * (x[j] - mean[j]) for j in range(3)) for x in xs] for w in dirs]
    cols = [[s[j] for s in srcs] for j in range(3)]
    matched = sorted(max(range(3), key=lambda j: abs_corr(o, cols[j])) for o in outs)
    assert matched == [0, 1]  # the two non-Gaussian sources, not the Gaussian one
    assert all(max(abs_corr(o, c) for c in cols) > 0.95 for o in outs)
    assert abs_corr(outs[0], outs[1]) < 1e-8  # orthogonal in the sphered space
