# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimization-based-mesh-smoothing/. The authors are listed in prov/9DFJ45.jsonl.

import math
import random

from mg3geom import exact, orient2d
from optimization_based_mesh_smoothing import (laplacian_target, min_norm_point, min_quality, quality,
                                               quality_gradient, smooth_mesh, smooth_vertex, star_link, valid)


def ring(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n)]


def random_star(rng):
    """A link polygon that is star-shaped about the origin, with 4 to 8 corners."""
    k = rng.randint(4, 8)
    while True:
        angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(k))
        gaps = [(angles[(i + 1) % k] - angles[i]) % (2 * math.pi) for i in range(k)]
        if max(gaps) < 0.9 * math.pi:
            break
    poly = [(round(r * math.cos(t), 3), round(r * math.sin(t), 3)) for t, r in ((t, rng.uniform(1, 4)) for t in angles)]
    return ring(poly)


def start_point(rng, link):
    while True:
        x = (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3))
        if valid(x, link):
            return x


def grid_search(link, n=40):
    """Best smallest quality over valid points of a grid on the bounding box,
    then over a finer grid around the best point (the reference method)."""
    xs = [a[0] for a, _ in link]
    ys = [a[1] for a, _ in link]
    lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
    best_q, best = -1.0, None
    for level in range(3):
        hx, hy = (hi_x - lo_x) / n, (hi_y - lo_y) / n
        for i in range(n + 1):
            for j in range(n + 1):
                y = (lo_x + i * hx, lo_y + j * hy)
                if valid(y, link):
                    q = min_quality(y, link)
                    if q > best_q:
                        best_q, best = q, y
        lo_x, hi_x = best[0] - 3 * hx, best[0] + 3 * hx
        lo_y, hi_y = best[1] - 3 * hy, best[1] + 3 * hy
    return best_q, best


def test_quality_values():
    s = math.sqrt(3) / 2
    assert abs(quality((0.0, 0.0), (1.0, 0.0), (0.5, s)) - 1.0) < 1e-12
    assert quality((0.0, 0.0), (1.0, 0.0), (2.0, 0.0)) == 0.0
    assert quality((0.0, 0.0), (0.5, s), (1.0, 0.0)) < 0


def test_gradient_against_finite_differences():
    rng = random.Random(1)
    for _ in range(200):
        x, a, b = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(3)]
        g = quality_gradient(x, a, b)
        h = 1e-6
        fx = (quality((x[0] + h, x[1]), a, b) - quality((x[0] - h, x[1]), a, b)) / (2 * h)
        fy = (quality((x[0], x[1] + h), a, b) - quality((x[0], x[1] - h), a, b)) / (2 * h)
        assert abs(fx - g[0]) < 1e-4 * (1 + abs(g[0]))
        assert abs(fy - g[1]) < 1e-4 * (1 + abs(g[1]))


def test_min_norm_point_against_optimality_conditions():
    # p is the least-norm point of the hull iff p is in the hull and
    # g . p >= |p|^2 for every generator g; the origin is in the hull iff
    # no direction u has g . u < 0 for all g (checked on 3600 directions)
    rng = random.Random(2)
    zeros = 0
    for _ in range(400):
        gs = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(rng.randint(1, 5))]
        p = min_norm_point(gs)
        pp = p[0] ** 2 + p[1] ** 2
        if pp == 0:
            zeros += 1
            for k in range(3600):
                u = (math.cos(k * math.pi / 1800), math.sin(k * math.pi / 1800))
                assert max(g[0] * u[0] + g[1] * u[1] for g in gs) >= -1e-9
        else:
            assert all(g[0] * p[0] + g[1] * p[1] >= pp - 1e-9 for g in gs)
            u = (-p[0] / math.sqrt(pp), -p[1] / math.sqrt(pp))
            assert max(g[0] * u[0] + g[1] * u[1] for g in gs) < 0   # the origin is outside
    assert zeros > 20


def test_min_quality_never_decreases_and_stays_valid():
    rng = random.Random(3)
    for _ in range(60):
        link = random_star(rng)
        x0 = start_point(rng, link)
        x, hist = smooth_vertex(x0, link)
        assert all(h1 > h0 for h0, h1 in zip(hist, hist[1:]))
        assert valid(x, link)
        # the exact orientation of every triangle of the result is positive
        assert all(orient2d(exact(x), exact(a), exact(b)) > 0 for a, b in link)


def test_matches_grid_search():
    # min q is quasi-concave on the kernel, so a stationary point is a global
    # maximum; the grid search must not find anything clearly better
    rng = random.Random(4)
    for _ in range(12):
        link = random_star(rng)
        x0 = start_point(rng, link)
        x, hist = smooth_vertex(x0, link)
        gq, _ = grid_search(link)
        assert hist[-1] >= gq - 1e-4
        assert hist[-1] <= gq + 2e-3   # the fine grid gets close to the optimum


def test_laplacian_inverts_where_max_min_does_not():
    link = ring([(-2.0, 0.0), (0.0, -2.0), (6.0, -1.0), (1.0, 0.0), (6.0, 1.0), (0.0, 2.0)])
    x0 = (0.0, 0.0)
    assert valid(x0, link)
    lap = laplacian_target(link)
    assert lap == (11 / 6, 0.0)
    assert not valid(lap, link)
    assert min(quality(lap, a, b) for a, b in link) < 0
    x, hist = smooth_vertex(x0, link)
    assert valid(x, link)
    assert abs(hist[0] - 0.0541) < 1e-4 and abs(hist[-1] - 0.1011) < 1e-4


def test_tangled_start_is_rejected():
    link = ring([(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)])
    try:
        smooth_vertex((3.0, 0.0), link)
    except ValueError:
        return
    assert False, "a tangled star must be rejected"


def test_mesh_sweep_raises_worst_quality():
    rng = random.Random(5)
    n = 5
    pts = []
    for j in range(n + 1):
        for i in range(n + 1):
            inner = 0 < i < n and 0 < j < n
            pts.append((i + (rng.uniform(-0.35, 0.35) if inner else 0.0), j + (rng.uniform(-0.35, 0.35) if inner else 0.0)))
    tris = []
    for j in range(n):
        for i in range(n):
            v = j * (n + 1) + i
            tris += [(v, v + 1, v + n + 2), (v, v + n + 2, v + n + 1)]
    assert all(orient2d(exact(pts[a]), exact(pts[b]), exact(pts[c])) > 0 for a, b, c in tris)
    free = [j * (n + 1) + i for j in range(1, n) for i in range(1, n)]
    before = min(quality(pts[a], pts[b], pts[c]) for a, b, c in tris)
    out = smooth_mesh(pts, tris, free)
    after = min(quality(out[a], out[b], out[c]) for a, b, c in tris)
    assert after >= before
    assert all(orient2d(exact(out[a]), exact(out[b]), exact(out[c])) > 0 for a, b, c in tris)
    assert len(star_link(tris, free[0])) == 6
