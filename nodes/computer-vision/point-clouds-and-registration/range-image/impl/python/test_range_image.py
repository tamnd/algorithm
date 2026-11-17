# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-image/. The authors are listed in prov/M707AA.jsonl.

import math
import random

import pytest

from range_image import RangeImage

EXAMPLE = [(0.0, -0.5, 2.0), (0.0, -1.0, 4.0), (-1.0, 0.5, 2.0), (1.0, 0.25, 1.0), (0.2, 0.0, -1.0)]


def test_example() -> None:
    img = RangeImage.from_points(EXAMPLE, 3, 2, 2.0, 2.0, 1.0, 0.5)
    assert img.depth == [[None, 2.0, None], [2.0, None, None]]
    assert img.point(1, 0) == (0.0, -0.5, 2.0)
    assert img.point(0, 1) == (-1.0, 0.5, 2.0)
    assert img.point(2, 1) is None
    assert abs(img.range_at(1, 0) - 2.0 * math.sqrt(1.0625)) < 1e-15
    assert [(u, v) for u, v, _ in img.to_point_cloud()] == [(1, 0), (0, 1)]


def brute_force_zbuffer(points, W, H, fx, fy, cx, cy):
    """For each pixel, scan all points and keep the least depth among those
    whose projection lies in the pixel square [u - 1/2, u + 1/2) x [v - 1/2, v + 1/2)."""
    out = [[None] * W for _ in range(H)]
    for v in range(H):
        for u in range(W):
            best = None
            for X, Y, Z in points:
                if Z <= 0:
                    continue
                x, y = fx * X / Z + cx, fy * Y / Z + cy
                if u - 0.5 <= x < u + 0.5 and v - 0.5 <= y < v + 0.5:
                    if best is None or Z < best:
                        best = Z
            out[v][u] = best
    return out


def test_zbuffer_matches_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(15):
        W, H = rng.randint(1, 8), rng.randint(1, 6)
        fx, fy = rng.uniform(2, 6), rng.uniform(2, 6)
        cx, cy = (W - 1) / 2, (H - 1) / 2
        pts = [(rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-0.5, 4)) for _ in range(60)]
        img = RangeImage.from_points(pts, W, H, fx, fy, cx, cy)
        assert img.depth == brute_force_zbuffer(pts, W, H, fx, fy, cx, cy)


def test_round_trip_and_range() -> None:
    rng = random.Random(12)
    W, H = 9, 7
    img = RangeImage(W, H, 5.0, 4.0, 4.0, 3.0)
    for v in range(H):
        for u in range(W):
            img.depth[v][u] = None if rng.random() < 0.2 else rng.uniform(0.5, 5.0)
    cloud = img.to_point_cloud()
    again = RangeImage.from_points([p for _, _, p in cloud], W, H, 5.0, 4.0, 4.0, 3.0)
    for v in range(H):
        for u in range(W):
            a, b = img.depth[v][u], again.depth[v][u]
            assert (a is None and b is None) or abs(a - b) <= 1e-12
    for u, v, p in cloud:
        assert abs(img.range_at(u, v) - math.sqrt(sum(c * c for c in p))) <= 1e-12


def test_neighbors_stop_at_depth_jumps() -> None:
    img = RangeImage(4, 3, 2.0, 2.0, 1.5, 1.0)
    for v in range(3):
        for u in range(4):
            img.depth[v][u] = 1.0 if u < 2 else 3.0
    img.depth[0][0] = None
    assert sorted(img.neighbors(1, 1, 0.5)) == [(0, 1), (1, 0), (1, 2)]
    assert sorted(img.neighbors(2, 1, 0.5)) == [(2, 0), (2, 2), (3, 1)]
    assert sorted(img.neighbors(1, 1, 5.0)) == [(0, 1), (1, 0), (1, 2), (2, 1)]
    assert img.neighbors(0, 0, 5.0) == []
    assert img.normal(1, 1, 0.5) is not None  # one-sided difference to the left
    img.depth[1][0] = None
    assert img.normal(1, 1, 0.5) is None  # no valid horizontal neighbor


def test_normal_of_a_plane() -> None:
    rng = random.Random(13)
    for _ in range(10):
        n = [rng.gauss(0, 0.3), rng.gauss(0, 0.3), -1.0]
        ln = math.sqrt(sum(c * c for c in n))
        n = [c / ln for c in n]
        d = -rng.uniform(1.0, 3.0) * abs(n[2])  # plane n . X = d, in front of the camera
        W, H, fx, fy, cx, cy = 6, 5, 4.0, 4.0, 2.5, 2.0
        img = RangeImage(W, H, fx, fy, cx, cy)
        for v in range(H):
            for u in range(W):
                a, b, c = img.ray(u, v)
                img.depth[v][u] = d / (n[0] * a + n[1] * b + n[2] * c)
        for v in range(H):
            for u in range(W):
                m = img.normal(u, v, 100.0)
                assert m is not None
                assert all(abs(m[i] - n[i]) < 1e-9 for i in range(3))  # n faces the camera
                p = img.point(u, v)
                assert m[0] * p[0] + m[1] * p[1] + m[2] * p[2] < 0


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        RangeImage(0, 3, 1.0, 1.0, 0.0, 0.0)
