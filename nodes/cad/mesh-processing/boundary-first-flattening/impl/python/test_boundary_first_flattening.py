# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-first-flattening/. The authors are listed in prov/HE01QC.jsonl.

import math
import random

from boundary_first_flattening import bff, curvatures_and_laplacian, dirichlet_to_neumann, neumann_to_dirichlet
from mx2geom import exact_orient2d


def hex_disk(r, rng, bend, jitter=0.15):
    """A hexagonal patch of the triangular lattice, jittered and lifted to z = a x^2 + b y^2 + c x y."""
    pts, index = [], {}
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            if abs(i + j) <= r:
                index[(i, j)] = len(pts)
                pts.append((i + 0.5 * j + rng.uniform(-jitter, jitter), j * math.sqrt(3) / 2 + rng.uniform(-jitter, jitter)))
    a, b, c = [rng.uniform(-bend, bend) for _ in range(3)]
    verts = [(x, y, a * x * x + b * y * y + c * x * y) for x, y in pts]
    faces = []
    for (i, j), v in index.items():
        if (i + 1, j) in index and (i, j + 1) in index:
            faces.append((v, index[(i + 1, j)], index[(i, j + 1)]))
        if (i + 1, j) in index and (i + 1, j - 1) in index:
            faces.append((v, index[(i + 1, j - 1)], index[(i + 1, j)]))
    return verts, faces


def turning_angles(pts, loop):
    """The signed exterior angle of the output polygon at each boundary vertex."""
    m, out = len(loop), []
    for t in range(m):
        p0, p1, p2 = pts[loop[t - 1]], pts[loop[t]], pts[loop[(t + 1) % m]]
        d0 = (p1[0] - p0[0], p1[1] - p0[1])
        d1 = (p2[0] - p1[0], p2[1] - p1[1])
        out.append(math.atan2(d0[0] * d1[1] - d0[1] * d1[0], d0[0] * d1[0] + d0[1] * d1[1]))
    return out


def boundary_lengths(pts, loop):
    return [math.dist(pts[loop[t]], pts[loop[(t + 1) % len(loop)]]) for t in range(len(loop))]


def rectangle_angles(m):
    k = [0.0] * m
    for c in range(4):
        k[(c * m) // 4] = math.pi / 2
    return k


PYRAMID_V = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 0, 1)]
PYRAMID_F = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]


def test_new_turning_angles_add_up_to_two_pi():
    for seed in range(5):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.4)
        a, s, loop = curvatures_and_laplacian(v, f)
        _, k = dirichlet_to_neumann(a, s, loop, [rng.uniform(-0.5, 0.5) for _ in loop])
        assert abs(sum(k) - 2 * math.pi) < 1e-12


def test_dirichlet_and_neumann_maps_are_inverse():
    for seed in range(5):
        rng = random.Random(10 + seed)
        v, f = hex_disk(3, rng, 0.4)
        a, s, loop = curvatures_and_laplacian(v, f)
        u, k = dirichlet_to_neumann(a, s, loop, [rng.uniform(-0.5, 0.5) for _ in loop])
        u2 = neumann_to_dirichlet(a, s, loop, k)
        c = u[loop[0]] - u2[loop[0]]
        assert max(abs(u[x] - u2[x] - c) for x in range(len(v))) < 1e-12


def test_asked_turning_angles_are_met():
    for seed in range(5):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.4)
        _, info = bff(v, f)
        m = len(info["loop"])
        raw = [rng.uniform(0.0, 1.0) for _ in range(m)]
        targets = [rectangle_angles(m), [2 * math.pi * x / sum(raw) for x in raw]]
        for kt in targets:
            pts, info = bff(v, f, k_target=kt)
            got = turning_angles(pts, info["loop"])
            assert max(abs(x - y) for x, y in zip(got, kt)) < 1e-9
            got_len = boundary_lengths(pts, info["loop"])
            assert max(abs(x - y) for x, y in zip(got_len, info["lengths"])) < 1e-9


def test_rectangle_and_length_modes_have_no_flips_on_small_disks():
    for seed in range(5):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.4)
        for kt in (None, rectangle_angles(18)):
            pts, _ = bff(v, f, k_target=kt)
            for x, y, z in f:
                assert exact_orient2d(pts[x], pts[y], pts[z]) > 0


def test_planar_disk_keeps_all_lengths():
    for seed in range(3):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.0)
        pts, info = bff(v, f)
        assert max(abs(x - y) for x, y in zip(info["asked"], info["lengths"])) < 1e-12
        for x, y, z in f:
            for p, q in ((x, y), (y, z), (z, x)):
                assert abs(math.dist(pts[p], pts[q]) - math.dist(v[p], v[q])) < 1e-9


def test_asked_lengths_are_met_up_to_the_smallest_closing_change():
    for seed in range(5):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.4)
        a, s, loop = curvatures_and_laplacian(v, f)
        ub = [rng.uniform(-0.3, 0.3) for _ in loop]
        pts, info = bff(v, f, u_boundary=ub)
        assert max(abs(x - y) for x, y in zip(boundary_lengths(pts, loop), info["lengths"])) < 1e-9
        asked, got, m = info["asked"], info["lengths"], len(loop)
        tang, phi = [], 0.0
        for t in range(m):
            phi += info["k"][t]
            tang.append((math.cos(phi), math.sin(phi)))
        cost = sum((x - y) ** 2 / y for x, y in zip(got, asked))
        # Every other closed polygon with the same directions changes the asked lengths at least as much.
        for _ in range(200):
            d = [rng.gauss(0, 0.05) for _ in range(m)]
            # Project d onto the closing directions: sum d_t T_t = 0.
            g = [[sum(tang[t][r] * tang[t][c] for t in range(m)) for c in range(2)] for r in range(2)]
            h = [sum(d[t] * tang[t][r] for t in range(m)) for r in range(2)]
            det = g[0][0] * g[1][1] - g[0][1] * g[1][0]
            lam = ((g[1][1] * h[0] - g[0][1] * h[1]) / det, (g[0][0] * h[1] - g[1][0] * h[0]) / det)
            d = [d[t] - tang[t][0] * lam[0] - tang[t][1] * lam[1] for t in range(m)]
            other = [x + y for x, y in zip(got, d)]
            assert sum((x - y) ** 2 / y for x, y in zip(other, asked)) >= cost - 1e-15


def test_pyramid_example():
    pts, info = bff(PYRAMID_V, PYRAMID_F)
    assert all(abs(k - math.pi / 2) < 1e-12 for k in info["k"])
    assert abs(info["u"][4] + 0.480602) < 1e-6
    assert max(abs(x - 2) for x in info["lengths"]) < 1e-12
    centre = ((pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2)
    assert math.dist(centre, pts[4]) < 1e-12
    k_t = [math.radians(x) for x in (120, 120, 120, 0)]
    pts, info = bff(PYRAMID_V, PYRAMID_F, k_target=k_t)
    got = turning_angles(pts, info["loop"])
    assert max(abs(x - y) for x, y in zip(got, k_t)) < 1e-12
    assert abs(info["lengths"][0] - 2.031153) < 1e-6
