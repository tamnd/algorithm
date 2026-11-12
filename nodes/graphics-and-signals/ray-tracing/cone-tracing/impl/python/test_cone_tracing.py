# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cone-tracing/. The authors are listed in prov/7SNYXJ.jsonl.

import math
import random

from cone_tracing import (
    LIST_SIZE,
    Cone,
    axis_coordinates,
    cone_meets_sphere,
    disk_fraction_below,
    dot,
    lens_area,
    norm,
    pixel_cone,
    plane_coverage,
    scale,
    sphere_coverage,
    sub,
    trace_cone,
    unit,
)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def basis(d):
    e1 = unit(cross(d, (1.0, 0.0, 0.0) if abs(d[0]) < 0.9 else (0.0, 1.0, 0.0)))
    return e1, cross(d, e1)


def disk_grid(n):
    """Midpoints of an n by n grid that lie in the unit disk."""
    pts = []
    for i in range(n):
        for j in range(n):
            x, y = 2 * (i + 0.5) / n - 1, 2 * (j + 0.5) / n - 1
            if x * x + y * y <= 1:
                pts.append((x, y))
    return pts


def ray_dir(cone, x, y, e1, e2):
    """The ray of the cone through the point (x, y) of its unit cross-section."""
    k = cone.tan_a
    return unit(tuple(cone.d[m] + k * (x * e1[m] + y * e2[m]) for m in range(3)))


def ray_hits_sphere(o, v, c, r):
    w = sub(c, o)
    t = dot(w, v)
    return t > 0 and dot(w, w) - t * t < r * r


def first_hit(o, v, spheres, planes):
    best = (math.inf, None)
    for c, r, color in spheres:
        w = sub(c, o)
        t = dot(w, v)
        q = dot(w, w) - t * t
        if q < r * r and t - math.sqrt(r * r - q) > 0:
            best = min(best, (t - math.sqrt(r * r - q), color))
    for p, n, color in planes:
        vn = dot(v, n)
        if vn < 0:
            best = min(best, (dot(sub(p, o), n) / vn, color))
    return best[1]


def random_cone(rng):
    apex = tuple(rng.uniform(-1, 1) for _ in range(3))
    axis = tuple(rng.gauss(0, 1) for _ in range(3))
    return Cone(apex, axis, math.radians(rng.uniform(2, 40)))


def test_fast_test_matches_dense_distance_to_the_cone():
    rng = random.Random(1)
    yes = no = 0
    while yes + no < 300:
        cone = random_cone(rng)
        t0 = rng.uniform(-2, 8)
        c = tuple(cone.o[m] + t0 * cone.d[m] + rng.uniform(-3, 3) for m in range(3))
        r = rng.uniform(0.1, 3)
        t, sep = axis_coordinates(cone, c)
        # dense samples of the cone's boundary in the half-plane through the axis and c
        h = 1e-3
        dist = min(math.hypot(t - x, sep - x * cone.tan_a) for x in (k * h for k in range(int(15 / h))))
        if t >= 0 and sep <= t * cone.tan_a:
            dist = 0.0
        if abs(dist - r) < 2 * h:
            continue
        assert cone_meets_sphere(cone, c, r) == (dist < r)
        yes += dist < r
        no += dist >= r
    assert yes > 100 and no > 100


def test_fast_test_agrees_with_rays_of_the_cone():
    rng = random.Random(2)
    pts = disk_grid(24) + [(math.cos(2 * math.pi * k / 400), math.sin(2 * math.pi * k / 400)) for k in range(400)]
    for _ in range(80):
        cone = random_cone(rng)
        e1, e2 = basis(cone.d)
        c = tuple(cone.o[m] + 6 * cone.d[m] + rng.uniform(-3, 3) for m in range(3))
        r = rng.uniform(0.2, 1.5)
        hit = any(ray_hits_sphere(cone.o, ray_dir(cone, x, y, e1, e2), c, r) for x, y in pts)
        if hit:  # some ray of the cone meets the ball
            assert cone_meets_sphere(cone, c, r)
        hit_grown = any(ray_hits_sphere(cone.o, ray_dir(cone, x, y, e1, e2), c, 1.05 * r) for x, y in pts)
        if not hit_grown:
            assert not cone_meets_sphere(cone, c, 0.95 * r)


def test_lens_area_matches_grid_sampling():
    rng = random.Random(3)
    pts = disk_grid(200)
    for _ in range(12):
        r1, r2 = rng.uniform(0.5, 2), rng.uniform(0.2, 2.5)
        s = rng.uniform(0, r1 + r2 + 0.3)
        count = sum((r1 * x - s) ** 2 + (r1 * y) ** 2 < r2 * r2 for x, y in pts)
        assert abs(lens_area(r1, r2, s) / (math.pi * r1 * r1) - count / len(pts)) < 0.01


def test_disk_fraction_matches_grid_sampling():
    pts = disk_grid(300)
    for h in (-1.2, -0.9, -0.5, -0.1, 0.0, 0.3, 0.77, 1.0, 1.5):
        count = sum(x < h for x, _ in pts)
        assert abs(disk_fraction_below(h) - count / len(pts)) < 0.005


def test_plane_coverage_matches_rays_of_the_cone():
    rng = random.Random(4)
    pts = disk_grid(120)
    for _ in range(12):
        cone = Cone((0.0, rng.uniform(0.5, 3), 0.0), (rng.gauss(0, 1), rng.uniform(-0.6, 0.2), rng.gauss(0, 1)), math.radians(rng.uniform(3, 30)))
        e1, e2 = basis(cone.d)
        n = (0.0, 1.0, 0.0)
        f, depth = plane_coverage(cone, (0.0, 0.0, 0.0), n)
        count = sum(dot(ray_dir(cone, x, y, e1, e2), n) < 0 for x, y in pts)
        assert abs(f - count / len(pts)) < 0.01
        if cone.d[1] < 0:
            assert math.isclose(depth, cone.o[1] / -cone.d[1])


def test_sphere_coverage_never_exceeds_the_rays_that_hit():
    rng = random.Random(5)
    pts = disk_grid(120)
    for _ in range(15):
        cone = random_cone(rng)
        e1, e2 = basis(cone.d)
        c = tuple(cone.o[m] + 8 * cone.d[m] + rng.uniform(-2, 2) for m in range(3))
        r = rng.uniform(0.3, 1.5)
        t, sep = axis_coordinates(cone, c)
        if t <= r:
            continue
        rc = t * cone.tan_a
        cp = tuple(cone.o[m] + t * cone.d[m] for m in range(3))
        in_lens = in_rays = 0
        for x, y in pts:
            q = tuple(cp[m] + rc * (x * e1[m] + y * e2[m]) for m in range(3))
            lens = norm(sub(q, c)) < r
            ray = ray_hits_sphere(cone.o, unit(sub(q, cone.o)), c, r)
            assert ray or not lens  # a point of the great circle's disk is hit by its ray
            in_lens += lens
            in_rays += ray
        f, _ = sphere_coverage(cone, c, r)
        assert abs(f - in_lens / len(pts)) < 0.015
        assert in_lens <= in_rays


def test_pixel_row_across_a_silhouette():
    c, r, w = (0.0, 0.0, 10.0), 2.0, 0.02
    got = [round(sphere_coverage(pixel_cone((0.0, 0.0, 0.0), (k * w, 0.0, 1.0), w), c, r)[0], 3) for k in range(8, 13)]
    assert got == [1.0, 1.0, 0.618, 0.058, 0.0]
    assert not cone_meets_sphere(pixel_cone((0.0, 0.0, 0.0), (12 * w, 0.0, 1.0), w), c, r)


def test_sphere_in_front_of_the_floor_matches_supersampling():
    rng = random.Random(6)
    pts = disk_grid(100)
    floor = [((0.0, -3.0, 0.0), (0.0, 1.0, 0.0), 0.25)]
    for _ in range(6):
        sphere = [((rng.uniform(-0.6, 0.6), -1.2, 8.0), 0.5, 1.0)]
        cone = Cone((0.0, 0.0, 0.0), (0.0, -0.15, 1.0), math.radians(5))
        assert plane_coverage(cone, *floor[0][:2])[0] == 1.0
        e1, e2 = basis(cone.d)
        color, hits = trace_cone(cone, sphere, floor, 0.0)
        f = sphere_coverage(cone, *sphere[0][:2])[0]
        assert math.isclose(color, f * 1.0 + (1 - f) * 0.25)
        exact = sum(first_hit(cone.o, ray_dir(cone, x, y, e1, e2), sphere, floor) for x, y in pts) / len(pts)
        assert abs(color - exact) < 0.02


def test_abutting_objects_are_mixed_as_if_they_overlapped():
    cone = Cone((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), math.atan(0.2))
    spheres = [((1.0, 0.0, 10.0), 0.8, 1.0), ((-1.0, 0.0, 10.0), 0.8, 1.0)]
    color, hits = trace_cone(cone, spheres, [], 0.0)
    assert [round(f, 6) for _, _, f, _ in hits] == [0.16, 0.16]
    assert math.isclose(color, 0.16 + 0.84 * 0.16)  # 0.2944, while the two disks cover 0.32
    e1, e2 = basis(cone.d)
    pts = disk_grid(150)
    exact = sum(first_hit(cone.o, ray_dir(cone, x, y, e1, e2), spheres, []) or 0.0 for x, y in pts) / len(pts)
    assert abs(exact - 0.32) < 0.01


def test_keeps_the_eight_nearest_objects():
    cone = Cone((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), math.atan(0.2))
    spheres = [((0.3, 0.0, z), 0.2, z / 100) for z in (12.0, 3.0, 7.0, 9.0, 4.0, 11.0, 5.0, 8.0, 6.0, 10.0)]
    color, hits = trace_cone(cone, spheres, [], 0.5)
    assert len(hits) == LIST_SIZE
    assert [round(c * 100) for _, _, _, c in hits] == [3, 4, 5, 6, 7, 8, 9, 10]
    expect, left = 0.0, 1.0
    for z in (3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0):
        f = sphere_coverage(cone, (0.3, 0.0, z), 0.2)[0]
        expect += left * f * z / 100
        left *= 1 - f
    assert math.isclose(color, expect + left * 0.5)


def test_horizon():
    for y, want in ((-0.05, 1.0), (0.0, 0.5), (0.05, 0.0)):
        f, _ = plane_coverage(Cone((0.0, 0.0, 0.0), (0.0, y, 1.0), math.atan(0.05)), (0.0, -1.5, 0.0), (0.0, 1.0, 0.0))
        assert math.isclose(f, want, abs_tol=1e-12)
    assert scale(2, (1, 2, 3)) == (2, 4, 6)
