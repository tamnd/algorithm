# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arap-parameterization/. The authors are listed in prov/7SBDXS.jsonl.

import math
import random

from arap_parameterization import (
    arap_parameterization,
    closest_rotation,
    energy,
    frames,
    global_matrix,
    global_step,
    jacobian,
)
from mx2geom import cholesky, exact_orient2d


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


PYRAMID_V = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 0, 1)]
PYRAMID_F = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]


def test_closest_rotation_against_angle_search():
    rng = random.Random(1)
    for _ in range(200):
        j = [[rng.uniform(-2, 2), rng.uniform(-2, 2)], [rng.uniform(-2, 2), rng.uniform(-2, 2)]]
        r = closest_rotation(j)
        assert abs(r[0][0] * r[1][1] - r[0][1] * r[1][0] - 1) < 1e-12
        best = sum(j[a][b] * r[a][b] for a in range(2) for b in range(2))
        for k in range(720):
            t = 2 * math.pi * k / 720
            rk = ((math.cos(t), -math.sin(t)), (math.sin(t), math.cos(t)))
            assert sum(j[a][b] * rk[a][b] for a in range(2) for b in range(2)) <= best + 1e-12


def test_energy_equals_cotangent_edge_form():
    rng = random.Random(2)
    v, f = hex_disk(2, rng, 0.5)
    fr = frames(v, f)
    u = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in v]
    rots = []
    for _ in f:
        t = rng.uniform(0, 2 * math.pi)
        rots.append(((math.cos(t), -math.sin(t)), (math.sin(t), math.cos(t))))
    edge_form = 0.0
    for (q, area, cots), tri, r in zip(fr, f, rots):
        for k in range(3):
            ki, kj = (k + 1) % 3, (k + 2) % 3
            e = (q[ki][0] - q[kj][0], q[ki][1] - q[kj][1])
            d = (r[0][0] * e[0] + r[0][1] * e[1], r[1][0] * e[0] + r[1][1] * e[1])
            du = (u[tri[ki]][0] - u[tri[kj]][0], u[tri[ki]][1] - u[tri[kj]][1])
            edge_form += 0.5 * cots[k] * ((du[0] - d[0]) ** 2 + (du[1] - d[1]) ** 2)
    assert abs(edge_form - energy(fr, f, u, rots)) < 1e-9 * edge_form


def test_global_step_beats_random_perturbations():
    rng = random.Random(3)
    v, f = hex_disk(2, rng, 0.5)
    fr = frames(v, f)
    u0, _ = arap_parameterization(v, f, iterations=2)
    rots = [closest_rotation(jacobian(q, area, [u0[x] for x in tri])) for (q, area, _), tri in zip(fr, f)]
    pin = f[0][0]
    a, idx = global_matrix(fr, f, len(v), pin)
    u = global_step(fr, f, len(v), pin, u0[pin], rots, cholesky(a), idx)
    best = energy(fr, f, u, rots)
    for _ in range(300):
        w = [p if k == pin else (p[0] + rng.gauss(0, 0.01), p[1] + rng.gauss(0, 0.01)) for k, p in enumerate(u)]
        assert energy(fr, f, w, rots) >= best - 1e-12


def test_energy_does_not_increase_and_no_flips_on_small_disks():
    for seed in range(8):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.4)
        u, es = arap_parameterization(v, f, iterations=25)
        for k in range(len(es) - 1):
            assert es[k + 1] <= es[k] * (1 + 1e-12) + 1e-15
        assert es[-1] < es[0]
        for a, b, c in f:
            assert exact_orient2d(u[a], u[b], u[c]) > 0


def test_planar_disk_comes_back_isometric():
    for seed in range(3):
        rng = random.Random(seed)
        v, f = hex_disk(3, rng, 0.0)
        u, es = arap_parameterization(v, f, iterations=100)
        assert es[-1] < 1e-20
        for a, b, c in f:
            for x, y in ((a, b), (b, c), (c, a)):
                assert abs(math.dist(u[x], u[y]) - math.dist(v[x], v[y])) < 1e-9


def test_pyramid_example():
    u, es = arap_parameterization(PYRAMID_V, PYRAMID_F, iterations=5, pin=0)
    assert abs(es[0] - 1.899495) < 1e-6
    assert abs(es[1] - 0.323521) < 1e-6
    assert abs(es[-1] - es[1]) < 1e-12
    assert abs(math.dist(u[0], u[1]) - 2.276142) < 1e-6
    assert abs(math.dist(u[0], u[4]) - 1.609476) < 1e-6
