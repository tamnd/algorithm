# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplicial-approximation/. The authors are listed in prov/TB95X2.jsonl.

import itertools
import math
import random

from regions import ConvexPolygon, Ellipse, Union, shoelace
from simplicial_approximation import convex_hull, edges, inscribed_disc, simplicial_approximation

TRIANGLE = ConvexPolygon([(0, 0), (6, 0), (0, 6)])
PENTAGON = ConvexPolygon([(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)])
DISC = Ellipse(0, 0, 1, 1)
ELLIPSE = Ellipse(0, 0, 2, 1)
L_SHAPE = Union([ConvexPolygon([(0, 0), (4, 0), (4, 2), (0, 2)]), ConvexPolygon([(0, 0), (2, 0), (2, 4), (0, 4)])], 12.0)


def solve3(a, y):
    det = lambda m: (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det(a)
    if abs(d) < 1e-12:
        return None
    out = []
    for j in range(3):
        m = [row[:] for row in a]
        for i in range(3):
            m[i][j] = y[i]
        out.append(det(m) / d)
    return out


def brute_radius(faces):
    # The LP optimum is at a vertex: try every triple of tight faces.
    best = 0.0
    for f in itertools.combinations(faces, 3):
        x = solve3([[n[0], n[1], 1.0] for _, _, n, _ in f], [b for _, _, _, b in f])
        if x and all(n[0] * x[0] + n[1] * x[1] + x[2] <= b + 1e-9 for _, _, n, b in faces):
            best = max(best, x[2])
    return best


def random_convex_polygon(rng):
    while True:
        hull = convex_hull([(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(rng.randint(3, 9))])
        if len(hull) >= 3 and abs(shoelace(hull)) > 1:
            return hull


def test_convex_hull_contains_all_points():
    rng = random.Random(5)
    for _ in range(100):
        pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(rng.randint(3, 12))]
        hull = convex_hull(pts)
        assert set(hull) <= set(pts)
        assert all(n[0] * p[0] + n[1] * p[1] <= b + 1e-12 for _, _, n, b in edges(hull) for p in pts)


def test_inscribed_disc_lp_against_brute_force():
    rng = random.Random(6)
    for _ in range(150):
        faces = edges(random_convex_polygon(rng))
        hull = [f[0] for f in faces]
        inner = (sum(p[0] for p in hull) / len(hull), sum(p[1] for p in hull) / len(hull))
        centre, radius = inscribed_disc(faces, inner)
        assert math.isclose(radius, brute_radius(faces), rel_tol=1e-9, abs_tol=1e-12)
        assert all(n[0] * centre[0] + n[1] * centre[1] + radius <= b + 1e-9 for _, _, n, b in faces)


def check_run(region, x0, iterations, r_region):
    history = simplicial_approximation(region.exit_point, x0, iterations)
    previous = None
    for rec in history:
        hull, c, r = rec["hull"], rec["centre"], rec["radius"]
        # Every vertex is a point of R, so for convex R the whole hull is in R.
        assert all(region.inside(p) for p in hull)
        assert all(n[0] * c[0] + n[1] * c[1] + r <= b + 1e-9 for _, _, n, b in edges(hull))
        assert r <= r_region + 1e-9
        if previous:
            assert r >= previous["radius"] - 1e-9
            assert all(n[0] * p[0] + n[1] * p[1] <= b + 1e-9 for _, _, n, b in edges(hull) for p in previous["hull"])
        previous = rec
    return history


def test_convex_regions_inside_nested_and_monotone():
    check_run(DISC, (0.3, -0.2), 60, 1.0)
    check_run(ELLIPSE, (0.5, 0.3), 60, 1.0)
    check_run(TRIANGLE, (1.0, 4.0), 60, 6 - 3 * math.sqrt(2))
    check_run(PENTAGON, (1.0, 1.0), 60, brute_radius(edges(PENTAGON.vertices)))


def test_polygon_stops_at_its_inscribed_disc():
    h = check_run(TRIANGLE, (1.0, 4.0), 60, 6 - 3 * math.sqrt(2))
    r = 6 - 3 * math.sqrt(2)
    assert len(h) == 5
    assert math.isclose(h[-1]["radius"], r, rel_tol=1e-9)
    assert math.dist(h[-1]["centre"], (r, r)) < 1e-8
    rng = random.Random(7)
    for _ in range(40):
        region = ConvexPolygon(random_convex_polygon(rng))
        x0 = tuple(sum(p[i] for p in region.vertices) / len(region.vertices) for i in range(2))
        want = brute_radius(edges(region.vertices))
        h = check_run(region, x0, 200, want)
        assert len(h) < 200
        assert math.isclose(h[-1]["radius"], want, rel_tol=1e-7)


def test_measured_area_ratios():
    # Measured, not proved: the tangent rule fills the disc but stalls on the ellipse.
    disc = simplicial_approximation(DISC.exit_point, (0.3, -0.2), 60)
    ratio = [shoelace(rec["hull"]) / DISC.area for rec in disc]
    assert [round(ratio[k], 3) for k in (0, 10, 40, 59)] == [0.595, 0.965, 0.996, 0.998]
    ell = simplicial_approximation(ELLIPSE.exit_point, (0.5, 0.3), 60)
    assert round(shoelace(ell[-1]["hull"]) / ELLIPSE.area, 3) == 0.880
    assert math.isclose(ell[-1]["radius"], 1.0, rel_tol=1e-6)
    longest = simplicial_approximation(ELLIPSE.exit_point, (0.5, 0.3), 60, rule="longest")
    assert shoelace(longest[-1]["hull"]) / ELLIPSE.area > 0.997


def test_nonconvex_region_breaks_the_method():
    h = simplicial_approximation(L_SHAPE.exit_point, (1.0, 1.0), 20)
    first = h[0]
    assert first["hull"] == [(0.0, 1.0), (1.0, 0.0), (4.0, 1.0), (1.0, 4.0)]
    # The hull holds points that are not in R.
    assert not L_SHAPE.inside((2.4, 2.4))
    assert all(n[0] * 2.4 + n[1] * 2.4 <= b for _, _, n, b in edges(first["hull"]))
    # The final disc is larger than any disc in R and pokes out of R.
    last = h[-1]
    c, r = last["centre"], last["radius"]
    best = 2 * math.sqrt(2) / (1 + math.sqrt(2))
    assert r > best + 0.2
    far = (c[0] + r / math.sqrt(2), c[1] + r / math.sqrt(2))
    assert not L_SHAPE.inside(far)
