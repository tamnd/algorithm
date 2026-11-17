# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voxel-grid-downsampling/. The authors are listed in prov/S76VBE.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from voxel_grid_downsampling import voxel_grid_downsample, voxel_index

EXAMPLE = [(0.2, 0.1, 0.0), (0.6, 0.3, 0.0), (1.5, 0.2, 0.0), (1.8, 0.9, 0.0),
           (1.2, 0.4, 0.0), (0.3, 1.7, 0.0)]


def brute_force(points, size, origin=(0, 0, 0)):
    """Group by comparing every pair of points: same voxel when the three
    floors agree. Quadratic, independent of any dict."""
    groups = []
    for p in points:
        for g in groups:
            q = g[0]
            if all(math.floor((p[a] - origin[a]) / size) == math.floor((q[a] - origin[a]) / size)
                   for a in range(3)):
                g.append(p)
                break
        else:
            groups.append([p])
    return [tuple(sum(p[a] for p in g) / len(g) for a in range(3)) for g in groups]


def test_example() -> None:
    pts = [tuple(F(str(v)) for v in p) for p in EXAMPLE]
    out = voxel_grid_downsample(pts, F(1))
    assert out == [(F("0.4"), F("0.2"), 0), (F("1.5"), F("0.5"), 0), (F("0.3"), F("1.7"), 0)]


def test_matches_brute_force_exact() -> None:
    rng = random.Random(1)
    for trial in range(40):
        n = rng.randint(0, 60)
        size = F(rng.randint(1, 8), rng.randint(1, 4))
        origin = tuple(F(rng.randint(-5, 5), 3) for _ in range(3))
        pts = [tuple(F(rng.randint(-40, 40), 7) for _ in range(3)) for _ in range(n)]
        assert voxel_grid_downsample(pts, size, origin) == brute_force(pts, size, origin)


def test_centroid_stays_in_its_voxel_and_counts() -> None:
    rng = random.Random(2)
    pts = [(rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-1, 1)) for _ in range(300)]
    size = 0.7
    out = voxel_grid_downsample(pts, size)
    keys = {voxel_index(p, size) for p in pts}
    assert len(out) == len(keys)
    out_keys = {voxel_index(c, size) for c in out}
    assert out_keys == keys


def test_order_does_not_change_the_set() -> None:
    rng = random.Random(3)
    pts = [tuple(F(rng.randint(-30, 30), 4) for _ in range(3)) for _ in range(80)]
    a = voxel_grid_downsample(pts, F(3, 2))
    shuffled = pts[:]
    rng.shuffle(shuffled)
    b = voxel_grid_downsample(shuffled, F(3, 2))
    assert sorted(a) == sorted(b)


def test_edges() -> None:
    assert voxel_grid_downsample([], 1.0) == []
    assert voxel_grid_downsample([(1.0, 2.0, 3.0)], 0.5) == [(1.0, 2.0, 3.0)]
    # A point on a voxel face goes to the voxel above (half-open boxes).
    assert voxel_index((1.0, -1.0, 0.0), 1.0) == (1, -1, 0)
    assert voxel_index((-0.5, 0.0, 0.0), 1.0) == (-1, 0, 0)
    with pytest.raises(ValueError):
        voxel_grid_downsample([(0.0, 0.0, 0.0)], 0.0)
