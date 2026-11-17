# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shot-descriptor/. The authors are listed in prov/KZZVS0.jsonl.

import math
import random

import pytest

from shot_descriptor import (
    LENGTH,
    cosine_bin,
    disambiguate,
    local_reference_frame,
    neighbors,
    shot,
    volume_index,
)


def unit(v):
    length = math.sqrt(sum(x * x for x in v))
    return [x / length for x in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rotation(rng):
    w, x, y, z = unit([rng.gauss(0, 1) for _ in range(4)])
    return (
        (1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)),
        (2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)),
        (2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)),
    )


def apply(R, v, t=(0.0, 0.0, 0.0)):
    return [sum(R[r][c] * v[c] for c in range(3)) + t[r] for r in range(3)]


def surface(rng, n, a=0.3, b=0.1, c=0.05):
    """Points on z = a x^2 + b y^2 + c x y^2 (no symmetry), with normals."""
    pts, nrm = [], []
    for _ in range(n):
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        pts.append([x, y, a * x * x + b * y * y + c * x * y * y])
        nrm.append(unit([-(2 * a * x + c * y * y), -(2 * b * y + 2 * c * x * y), 1.0]))
    return pts, nrm


def example():
    xy = [(1, 0), (-0.5, 0), (0, 0.8), (0, -0.4), (0.6, 0.6)]
    pts = [[x, y, 0.2 * x * x + 0.1 * y * y] for x, y in xy]
    nrm = [unit([-0.4 * x, -0.2 * y, 1.0]) for x, y in xy]
    return pts, nrm


def test_example() -> None:
    pts, nrm = example()
    x, y, z = local_reference_frame(pts, (0, 0, 0), 2.0)
    assert all(abs(a - b) < 1e-4 for a, b in zip(x, (0.8239, 0.5517, 0.1293)))
    assert all(abs(a - b) < 1e-4 for a, b in zip(z, (-0.1201, -0.0531, 0.9913)))
    h = shot(pts, nrm, (0, 0, 0), 2.0)
    nonzero = [i for i, v in enumerate(h) if v]
    assert nonzero == [32, 76, 164, 252, 351]
    assert all(abs(h[i] - 1 / math.sqrt(5)) < 1e-12 for i in nonzero)


def test_frame_is_orthonormal_and_right_handed() -> None:
    rng = random.Random(61)
    pts, _ = surface(rng, 200)
    for p in pts[:20]:
        x, y, z = local_reference_frame(pts, p, 0.6)
        for a in (x, y, z):
            assert abs(dot(a, a) - 1) < 1e-12
        assert abs(dot(x, y)) < 1e-12 and abs(dot(y, z)) < 1e-12 and abs(dot(x, z)) < 1e-12
        cz = [x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]]
        assert all(abs(a - b) < 1e-12 for a, b in zip(cz, z))


def test_frame_moves_with_the_cloud() -> None:
    rng = random.Random(62)
    pts, _ = surface(rng, 200)
    R = rotation(rng)
    t = (2.0, -3.0, 0.5)
    moved = [apply(R, p, t) for p in pts]
    for i in range(15):
        f = local_reference_frame(pts, pts[i], 0.6)
        g = local_reference_frame(moved, moved[i], 0.6)
        for a, b in zip(f, g):
            assert all(abs(u - v) < 1e-8 for u, v in zip(apply(R, a), b))


def test_descriptor_is_rigid_invariant_and_unit() -> None:
    rng = random.Random(63)
    pts, nrm = surface(rng, 300)
    R = rotation(rng)
    t = (-1.0, 4.0, 2.0)
    mp = [apply(R, p, t) for p in pts]
    mn = [apply(R, m) for m in nrm]
    for i in range(10):
        a = shot(pts, nrm, pts[i], 0.7)
        b = shot(mp, mn, mp[i], 0.7)
        assert len(a) == LENGTH
        assert abs(sum(v * v for v in a) - 1) < 1e-12
        assert max(abs(u - v) for u, v in zip(a, b)) < 1e-12


def oracle(points, normals, p, radius):
    """Spherical coordinates by acos, binned without the helper functions."""
    x, y, z = local_reference_frame(points, p, radius)
    h = [0] * 352
    for q, n in zip(points, normals):
        o = [q[k] - p[k] for k in range(3)]
        d = math.sqrt(dot(o, o))
        if not 0 < d < radius:
            continue
        a, b, c = dot(o, x), dot(o, y), dot(o, z)
        az = math.degrees(math.atan2(b, a)) % 360
        sector = int(az // 45)
        half = int(c >= 0)
        shell = int(d >= radius / 2)
        cos_t = dot(n, z)
        k = min(10, int((cos_t + 1) * 5.5))
        h[((sector * 2 + half) * 2 + shell) * 11 + k] += 1
    s = math.sqrt(sum(v * v for v in h))
    return [v / s for v in h]


def test_matches_oracle() -> None:
    rng = random.Random(64)
    pts, nrm = surface(rng, 250)
    for i in range(10):
        a, b = shot(pts, nrm, pts[i], 0.8), oracle(pts, nrm, pts[i], 0.8)
        assert max(abs(u - v) for u, v in zip(a, b)) < 1e-12


def test_disambiguation() -> None:
    offs = [[1, 0, 0], [2, 0, 0], [-1, 0, 0]]
    assert disambiguate([1, 0, 0], offs) == [1, 0, 0]
    assert disambiguate([-1, 0, 0], offs) == [1, 0, 0]
    # A tie in the counts goes by the sum of the projections.
    assert disambiguate([-1, 0, 0], [[3, 0, 0], [-1, 0, 0]]) == [1, 0, 0]


def test_bins() -> None:
    assert cosine_bin(-1.0) == 0 and cosine_bin(1.0) == 10 and cosine_bin(0.0) == 5
    assert volume_index((1.0, 0.0, 0.1), 2.0) == 3
    assert volume_index((0.1, 0.0, -0.1), 2.0) == 0
    assert volume_index((0.0, -0.1, 0.1), 2.0) == (6 * 2 + 1) * 2
    assert {volume_index((math.cos(t), math.sin(t), s), 3.0)
            for t in [math.radians(22.5 + 45 * j) for j in range(8)] for s in (-0.1, 0.1)} == set(range(0, 32, 2))


def test_edges() -> None:
    assert shot([[0, 0, 0], [1, 0, 0]], [[0, 0, 1]] * 2, (0, 0, 0), 2.0) is None
    assert neighbors([[0, 0, 0], [1, 0, 0], [3, 0, 0]], (0, 0, 0), 2.0) == [1]
    with pytest.raises(TypeError):
        shot(None, None, (0, 0, 0), 1.0)
