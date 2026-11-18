# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horizon-based-ambient-occlusion/. The authors are listed in prov/7TY98V.jsonl.

"""HBAO on height fields with known answers."""

import math
import random

from horizon_based_ambient_occlusion import (
    hbao,
    hbao_pixel,
    lookup,
    normal_from_depth,
    tangent_angle,
    wall_reference,
)


def plane(w, h, d0, gx, gy):
    return [[d0 + gx * (i + 0.5) + gy * (j + 0.5) for i in range(w)] for j in range(h)]


def wall(w, h, edge, floor, height):
    return [[floor if i < edge else floor - height for i in range(w)] for _ in range(h)]


def test_planes_are_open() -> None:
    for gx, gy in [(0.0, 0.0), (0.4, 0.0), (-0.3, 0.6), (1.2, 0.5)]:
        D = plane(40, 40, 100.0, gx, gy)
        for falloff in (True, False):
            A = hbao_pixel(D, 20, 20, 8, 12, 1.0, 50.0, falloff=falloff, jitter=0.3, mode="bilinear")
            assert abs(A - 1.0) < 1e-9


def test_one_direction_telescopes_without_falloff() -> None:
    rng = random.Random(71)
    D = [[50.0 + rng.uniform(-3, 3) for _ in range(30)] for _ in range(30)]
    n = normal_from_depth(D, 15, 15)
    for jitter in (0.0, 0.25, 0.6):
        A = hbao_pixel(D, 15, 15, 1, 10, 1.0, 1e9, falloff=False, jitter=jitter, normal=n)
        theta = 2 * math.pi * jitter
        cx, cy = math.cos(theta), math.sin(theta)
        t = tangent_angle(n, cx, cy)
        h = t
        for s in range(1, 11):
            dz = D[15][15] - lookup(D, 15.5 + s * cx, 15.5 + s * cy)
            h = max(h, math.atan2(dz, s))
        assert abs((1 - A) - (math.sin(h) - math.sin(t))) < 1e-12


def test_wall_matches_the_solid_angle_formula() -> None:
    D = wall(200, 200, 100, 200.0, 8.0)
    for i, delta in ((97, 2.5), (95, 4.5), (91, 8.5)):
        A = hbao_pixel(D, i, 100, 64, 360, 0.25, 1e9, falloff=False, jitter=0.5)
        assert abs(A - wall_reference(delta, 8.0)) < 0.02


def test_wall_formula_by_monte_carlo() -> None:
    # Uniform directions over the upper hemisphere, rays against a wall
    # x >= delta of height H: the occluded share is atan(H / delta) / pi.
    rng = random.Random(72)
    delta, H, count, hit = 3.0, 5.0, 40000, 0
    for _ in range(count):
        z = rng.random()
        phi = rng.uniform(0, 2 * math.pi)
        rxy = math.sqrt(1 - z * z)
        ox = rxy * math.cos(phi)
        if ox > 0 and z * (delta / ox) < H:
            hit += 1
    assert abs(hit / count - (1 - wall_reference(delta, H))) < 0.01


def test_falloff_only_removes_occlusion() -> None:
    rng = random.Random(73)
    D = [[60.0 + rng.uniform(-6, 6) for _ in range(32)] for _ in range(32)]
    for _ in range(10):
        i, j = rng.randrange(4, 28), rng.randrange(4, 28)
        hard = hbao_pixel(D, i, j, 8, 8, 1.0, 6.0, falloff=False)
        soft = hbao_pixel(D, i, j, 8, 8, 1.0, 6.0, falloff=True)
        assert 0.0 <= hard <= soft <= 1.0 + 1e-12


def test_whole_image_of_a_plane() -> None:
    # Pixels at least 5 units from the border, so that no sample is clamped.
    D = plane(20, 20, 30.0, 0.2, -0.1)
    A = hbao(D, 4, 4, 1.0, 5.0, mode="bilinear")
    assert all(abs(a - 1.0) < 1e-9 for row in A[5:15] for a in row[5:15])
