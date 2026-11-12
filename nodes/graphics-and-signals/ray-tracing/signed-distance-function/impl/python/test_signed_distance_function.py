# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signed-distance-function/. The authors are listed in prov/4489K1.jsonl.

import math
import random

from signed_distance_function import (
    gradient,
    length,
    sd_box,
    sd_intersection,
    sd_plane,
    sd_sphere,
    sd_subtraction,
    sd_torus,
    sd_union,
)

EPS = 1e-9


def sphere_samples(c, r, nt, nph):
    """Latitude-longitude samples of a sphere, with the covering radius of the grid.

    Each surface point lies in a grid cell, and its nearest corner is at most half the cell
    diagonal away along the surface, so at most that far in space."""
    pts = []
    dt, dp = math.pi / nt, 2 * math.pi / nph
    for i in range(nt + 1):
        t = i * dt
        for j in range(nph):
            ph = j * dp
            pts.append((c[0] + r * math.sin(t) * math.cos(ph), c[1] + r * math.cos(t), c[2] + r * math.sin(t) * math.sin(ph)))
    return pts, r * math.hypot(dt, dp) / 2


def box_samples(b, k):
    """Grid samples of the six faces of the box with half extents b."""
    pts = []
    cover = 0.0
    for axis in range(3):
        u, v = [a for a in range(3) if a != axis]
        su, sv = 2 * b[u] / k, 2 * b[v] / k
        cover = max(cover, math.hypot(su, sv) / 2)
        for sign in (-1.0, 1.0):
            for i in range(k + 1):
                for j in range(k + 1):
                    p = [0.0, 0.0, 0.0]
                    p[axis] = sign * b[axis]
                    p[u] = -b[u] + i * su
                    p[v] = -b[v] + j * sv
                    pts.append(tuple(p))
    return pts, cover


def torus_samples(big_r, small_r, nu, nv):
    pts = []
    du, dv = 2 * math.pi / nu, 2 * math.pi / nv
    for i in range(nu):
        u = i * du
        for j in range(nv):
            v = j * dv
            w = big_r + small_r * math.cos(v)
            pts.append((w * math.cos(u), small_r * math.sin(v), w * math.sin(u)))
    return pts, math.hypot((big_r + small_r) * du, small_r * dv) / 2


def brute(p, pts):
    return min(length((p[0] - q[0], p[1] - q[1], p[2] - q[2])) for q in pts)


def random_point(rng, s):
    return (rng.uniform(-s, s), rng.uniform(-s, s), rng.uniform(-s, s))


def check_exact(f, pts, cover, inside, rng, n=40, s=3.0):
    for _ in range(n):
        p = random_point(rng, s)
        d = f(p)
        bd = brute(p, pts)
        assert abs(d) <= bd + EPS
        assert bd <= abs(d) + cover + EPS
        if abs(d) > 1e-6:
            assert (d < 0) == inside(p)


def test_sphere_against_dense_samples():
    rng = random.Random(1)
    c, r = (0.3, -0.2, 0.1), 1.2
    pts, cover = sphere_samples(c, r, 60, 120)
    check_exact(lambda p: sd_sphere(p, c, r), pts, cover, lambda p: length((p[0] - c[0], p[1] - c[1], p[2] - c[2])) < r, rng)


def test_box_against_dense_samples():
    rng = random.Random(2)
    b = (1.0, 0.6, 0.4)
    pts, cover = box_samples(b, 40)
    check_exact(lambda p: sd_box(p, b), pts, cover, lambda p: all(abs(p[i]) < b[i] for i in range(3)), rng, s=1.6)


def test_torus_against_dense_samples():
    rng = random.Random(3)
    pts, cover = torus_samples(1.0, 0.35, 120, 36)

    def inside(p):
        return math.hypot(math.hypot(p[0], p[2]) - 1.0, p[1]) < 0.35

    check_exact(lambda p: sd_torus(p, 1.0, 0.35), pts, cover, inside, rng, s=1.8)


def test_plane_is_signed_projection():
    rng = random.Random(4)
    n = (2 / 3, -1 / 3, 2 / 3)
    for _ in range(50):
        p = random_point(rng, 5.0)
        d = sd_plane(p, n, 0.5)
        foot = (p[0] - d * n[0], p[1] - d * n[1], p[2] - d * n[2])
        assert abs(sd_plane(foot, n, 0.5)) < 1e-12
        assert abs(length((p[0] - foot[0], p[1] - foot[1], p[2] - foot[2])) - abs(d)) < 1e-12


def union_surface(ca, cb, r, nt, nph, nseam):
    """Samples of the boundary of the union of two equal spheres: the part of each sphere that
    is outside the other, plus samples of the seam circle where they meet."""
    pa, cover = sphere_samples(ca, r, nt, nph)
    pb, _ = sphere_samples(cb, r, nt, nph)
    pts = [p for p in pa if sd_sphere(p, cb, r) >= 0] + [p for p in pb if sd_sphere(p, ca, r) >= 0]
    half = length((cb[0] - ca[0], cb[1] - ca[1], cb[2] - ca[2])) / 2
    rho = math.sqrt(r * r - half * half)
    mid = ((ca[0] + cb[0]) / 2, (ca[1] + cb[1]) / 2, (ca[2] + cb[2]) / 2)
    for k in range(nseam):
        a = 2 * math.pi * k / nseam
        pts.append((mid[0], mid[1] + rho * math.cos(a), mid[2] + rho * math.sin(a)))
    # A trimmed cell near the seam can lose its corners, so allow one full cell diagonal plus
    # half the seam spacing.
    return pts, 2 * cover + math.pi * rho / nseam


def test_union_exact_outside_bound_inside():
    rng = random.Random(5)
    ca, cb, r = (-0.75, 0.0, 0.0), (0.75, 0.0, 0.0), 1.0
    pts, cover = union_surface(ca, cb, r, 60, 120, 400)

    def f(p):
        return sd_union(sd_sphere(p, ca, r), sd_sphere(p, cb, r))

    for _ in range(40):
        p = random_point(rng, 2.5)
        d = f(p)
        bd = brute(p, pts)
        if d >= 0:
            assert abs(bd - d) <= cover + EPS
        else:
            assert -d <= bd + EPS
    origin = (0.0, 0.0, 0.0)
    assert abs(f(origin) + 0.25) < 1e-12
    assert abs(brute(origin, pts) - math.sqrt(1 - 0.75 ** 2)) <= cover


def test_intersection_exact_inside_bound_outside():
    rng = random.Random(6)
    ca, cb, r = (-0.5, 0.0, 0.0), (0.5, 0.0, 0.0), 1.0
    pa, cover = sphere_samples(ca, r, 60, 120)
    pb, _ = sphere_samples(cb, r, 60, 120)
    pts = [p for p in pa if sd_sphere(p, cb, r) <= 0] + [p for p in pb if sd_sphere(p, ca, r) <= 0]
    rho = math.sqrt(r * r - 0.25)
    pts += [(0.0, rho * math.cos(2 * math.pi * k / 400), rho * math.sin(2 * math.pi * k / 400)) for k in range(400)]
    cover = 2 * cover + math.pi * rho / 400
    for _ in range(40):
        p = random_point(rng, 2.5)
        d = sd_intersection(sd_sphere(p, ca, r), sd_sphere(p, cb, r))
        bd = brute(p, pts)
        if d <= 0:
            assert abs(bd + d) <= cover + EPS
        else:
            assert d <= bd + EPS


def test_lipschitz_one_for_all_combinations():
    rng = random.Random(7)
    shapes = [
        lambda p: sd_sphere(p, (0.0, 0.0, 0.0), 1.0),
        lambda p: sd_box(p, (1.0, 0.5, 0.25)),
        lambda p: sd_torus(p, 1.0, 0.3),
        lambda p: sd_union(sd_box(p, (1.0, 0.2, 0.2)), sd_sphere(p, (1.0, 0.0, 0.0), 0.5)),
        lambda p: sd_subtraction(sd_box(p, (1.0, 1.0, 1.0)), sd_sphere(p, (0.0, 0.0, 0.0), 1.2)),
    ]
    for f in shapes:
        for _ in range(300):
            p, q = random_point(rng, 3.0), random_point(rng, 3.0)
            assert abs(f(p) - f(q)) <= length((p[0] - q[0], p[1] - q[1], p[2] - q[2])) + 1e-12


def test_gradient_norm_one_away_from_ties():
    rng = random.Random(8)
    b = (1.0, 0.6, 0.4)
    count = 0
    while count < 200:
        p = random_point(rng, 2.0)
        q = sorted((abs(p[i]) - b[i], i) for i in range(3))
        if q[2][0] < 0 and (q[2][0] - q[1][0] < 1e-3 or abs(p[q[2][1]]) < 1e-3):
            continue  # near the medial set of the box, where the gradient jumps
        g = gradient(lambda x: sd_box(x, b), p)
        assert abs(length(g) - 1.0) < 1e-6
        count += 1


def test_worked_values():
    assert abs(sd_box((2.0, 3.0, 0.5), (1.0, 1.0, 1.0)) - math.sqrt(5)) < 1e-12
    assert abs(sd_box((0.5, 0.2, 0.0), (1.0, 1.0, 1.0)) + 0.5) < 1e-12
    assert abs(sd_sphere((3.0, 4.0, 0.0), (0.0, 0.0, 0.0), 2.0) - 3.0) < 1e-12
