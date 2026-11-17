# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-cloud-normal-estimation/. The authors are listed in prov/J9D82K.jsonl.

import math
import random

import pytest

from cvla import svd
from point_cloud_normal_estimation import estimate_normals, k_nearest, plane_normal

EXAMPLE = [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (-1.0, 1.0, 0.0), (1.0, 1.0, 0.0), (0.0, 0.0, 0.5)]


def rotation(rng):
    """A rotation from a random unit quaternion (test only)."""
    w, x, y, z = (rng.gauss(0, 1) for _ in range(4))
    s = math.sqrt(w * w + x * x + y * y + z * z)
    w, x, y, z = w / s, x / s, y / s, z / s
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def apply(r, p):
    return tuple(sum(r[i][j] * p[j] for j in range(3)) for i in range(3))


def parallel(a, b, tol):
    """|a . b| close to 1 for unit vectors."""
    return abs(abs(sum(x * y for x, y in zip(a, b))) - 1.0) <= tol


def test_example() -> None:
    n, var, c = plane_normal(EXAMPLE)
    assert parallel(n, (0.0, 0.0, 1.0), 1e-12)
    assert abs(var - 0.04 / 1.64) < 1e-12
    assert all(abs(a - b) < 1e-15 for a, b in zip(c, (0.0, 0.0, 0.1)))


def test_plane_is_exact() -> None:
    rng = random.Random(21)
    for _ in range(10):
        r = rotation(rng)
        normal = apply(r, (0.0, 0.0, 1.0))
        pts = [apply(r, (rng.uniform(-1, 1), rng.uniform(-1, 1), 0.0)) for _ in range(30)]
        for m, var in estimate_normals(pts, 8):
            assert parallel(m, normal, 1e-9)
            assert var < 1e-12


def test_matches_svd_of_centered_points() -> None:
    rng = random.Random(22)
    for _ in range(20):
        pts = [tuple(rng.gauss(0, s) for s in (1.0, 0.7, 0.2)) for _ in range(rng.randint(3, 15))]
        n, var, c = plane_normal(pts)
        rows = [[q[a] - c[a] for a in range(3)] for q in pts]
        _, s, v = svd(rows)
        assert parallel(n, (v[0][2], v[1][2], v[2][2]), 1e-8)
        # the fitted plane minimizes the sum of squared distances
        cost = sum(sum(n[a] * row[a] for a in range(3)) ** 2 for row in rows)
        assert abs(cost - s[2] ** 2) < 1e-9
        for _ in range(20):
            u = [rng.gauss(0, 1) for _ in range(3)]
            lu = math.sqrt(sum(x * x for x in u))
            other = sum(sum(u[a] / lu * row[a] for a in range(3)) ** 2 for row in rows)
            assert cost <= other + 1e-12
        assert 0.0 <= var <= 1.0 / 3.0 + 1e-12


def test_sphere_normals_are_radial() -> None:
    rng = random.Random(23)
    pts = []
    for _ in range(400):
        u = [rng.gauss(0, 1) for _ in range(3)]
        lu = math.sqrt(sum(x * x for x in u))
        pts.append(tuple(2.0 * x / lu for x in u))
    for p, (m, var) in zip(pts, estimate_normals(pts, 10, viewpoint=(0.0, 0.0, 0.0))):
        radial = tuple(-x / 2.0 for x in p)  # toward the center, the viewpoint
        assert sum(a * b for a, b in zip(m, radial)) > 0.97
        assert var < 0.05


def test_rigid_motion_moves_normals() -> None:
    rng = random.Random(24)
    pts = [(x, y, 0.3 * x * x - 0.2 * y * y + rng.gauss(0, 0.01))
           for x in (-0.4, -0.2, 0.0, 0.2, 0.4) for y in (-0.4, -0.2, 0.0, 0.2, 0.4)]
    r = rotation(rng)
    moved = [tuple(a + b for a, b in zip(apply(r, p), (1.0, -2.0, 0.5))) for p in pts]
    before = estimate_normals(pts, 7)
    after = estimate_normals(moved, 7)
    for (m0, v0), (m1, v1) in zip(before, after):
        assert parallel(apply(r, m0), m1, 1e-8)
        assert abs(v0 - v1) < 1e-9


def test_neighbors_and_errors() -> None:
    pts = [(float(i), 0.0, 0.0) for i in range(6)]
    assert sorted(k_nearest(pts, 0, 3)) == [0, 1, 2]
    assert k_nearest(pts, 3, 1) == [3]
    with pytest.raises(ValueError):
        estimate_normals(pts, 2)
    with pytest.raises(ValueError):
        estimate_normals(pts[:3], 4)
