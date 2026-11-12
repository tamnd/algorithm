# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-curves/. The authors are listed in prov/RXEEKH.jsonl.

import math
import random

from principal_curves import first_principal_direction, local_linear, principal_curve, project_to_polyline


def dist_to_segment(p, a, b):
    ab = [y - x for x, y in zip(a, b)]
    t = max(0.0, min(1.0, sum((pi - ai) * d for pi, ai, d in zip(p, a, ab)) / sum(d * d for d in ab)))
    return math.sqrt(sum((pi - ai - t * d) ** 2 for pi, ai, d in zip(p, a, ab)))


def test_points_on_a_segment_give_the_segment():
    a, b = [1.0, 2.0, -1.0], [4.0, 6.0, 1.0]
    pts = [[a[k] + t / 19 * (b[k] - a[k]) for k in range(3)] for t in range(20)]
    random.Random(0).shuffle(pts)
    vertices, lams, history = principal_curve(pts)
    assert history[-1] < 1e-20
    assert all(dist_to_segment(v, a, b) < 1e-9 for v in vertices)
    ends = sorted([vertices[0], vertices[-1]])
    assert all(abs(u - w) < 1e-9 for u, w in zip(ends[0] + ends[1], a + b))
    length = math.sqrt(sum((y - x) ** 2 for x, y in zip(a, b)))
    assert abs(max(lams) - min(lams) - length) < 1e-9


def test_noisy_segment_stays_near_the_segment():
    r = random.Random(1)
    ts = [r.uniform(0.0, 4.0) for _ in range(100)]
    pts = [[t + r.gauss(0.0, 0.05), 0.5 * t + r.gauss(0.0, 0.05)] for t in ts]
    vertices, _, history = principal_curve(pts)
    assert history[-1] <= history[0]
    assert max(abs(v[1] - 0.5 * v[0]) / math.sqrt(1.25) for v in vertices) < 0.05


def test_arc_is_followed():
    r = random.Random(2)
    th = [r.uniform(0.0, math.pi) for _ in range(100)]
    pts = [[math.cos(s) + r.gauss(0.0, 0.05), math.sin(s) + r.gauss(0.0, 0.05)] for s in th]
    vertices, _, history = principal_curve(pts, span=0.2)
    assert history[-1] < 0.05 * history[0]  # far better than the first principal component line
    assert sum(abs(math.hypot(*v) - 1.0) for v in vertices) / len(vertices) < 0.03


def test_projection_matches_brute_force():
    rng = random.Random(3)
    poly = [[rng.uniform(-2, 2), rng.uniform(-2, 2)] for _ in range(6)]
    samples = []
    for a, b in zip(poly, poly[1:]):
        samples += [[a[0] + t / 400 * (b[0] - a[0]), a[1] + t / 400 * (b[1] - a[1])] for t in range(401)]
    for _ in range(50):
        x = [rng.uniform(-3, 3), rng.uniform(-3, 3)]
        lam, p, d2 = project_to_polyline(x, poly)
        brute = min((x[0] - s[0]) ** 2 + (x[1] - s[1]) ** 2 for s in samples)
        assert d2 <= brute + 1e-12
        assert brute - d2 < 1e-3
        assert abs((x[0] - p[0]) ** 2 + (x[1] - p[1]) ** 2 - d2) < 1e-12


def test_local_linear_reproduces_lines():
    r = random.Random(4)
    lams = sorted(r.uniform(-1, 1) for _ in range(30))
    xs = [[2.0 + 3.0 * t, -1.0 + 0.5 * t] for t in lams]
    for at in (lams[0], lams[7], 0.123, lams[-1]):
        f = local_linear(lams, xs, at, 0.2)
        assert abs(f[0] - (2.0 + 3.0 * at)) < 1e-12 and abs(f[1] - (-1.0 + 0.5 * at)) < 1e-12


def test_start_line_direction_is_an_eigenvector():
    r = random.Random(5)
    pts = [[r.gauss(0, 3), r.gauss(0, 1), r.gauss(0, 0.5)] for _ in range(200)]
    pts = [[x + 0.5 * y, y - 0.3 * z, z] for x, y, z in pts]
    mean, v = first_principal_direction(pts)
    n = len(pts)
    cov = [[sum((p[a] - mean[a]) * (p[b] - mean[b]) for p in pts) / n for b in range(3)] for a in range(3)]
    cv = [sum(cov[a][b] * v[b] for b in range(3)) for a in range(3)]
    lam = sum(c * w for c, w in zip(cv, v))
    assert all(abs(c - lam * w) < 1e-9 for c, w in zip(cv, v))
