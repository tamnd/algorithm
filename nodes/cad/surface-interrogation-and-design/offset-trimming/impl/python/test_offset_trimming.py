# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/offset-trimming/. The authors are listed in prov/MJFVD0.jsonl.

import math
import random
from fractions import Fraction

from offset_trimming import (
    curve_derivative,
    curve_point,
    offset_point,
    offset_trimming,
    polyline_crossings,
)

DUMBBELL = [(-3, -1.5), (-1, -0.4), (1, -0.4), (3, -1.5), (3, 1.5), (1, 0.4), (-1, 0.4), (-3, 1.5)]


def basis_point(points, t):
    """Reference: the uniform cubic B-spline basis functions on span floor(t)."""
    n = len(points)
    i = int(math.floor(t)) % n
    u = t - math.floor(t)
    b = ((1 - u) ** 3 / 6, (3 * u**3 - 6 * u**2 + 4) / 6, (-3 * u**3 + 3 * u**2 + 3 * u + 1) / 6, u**3 / 6)
    ctrl = [points[(i - 3 + k) % n] for k in range(4)]
    return (sum(b[k] * ctrl[k][0] for k in range(4)), sum(b[k] * ctrl[k][1] for k in range(4)))


def brute_meet(a, b, c, e):
    """Independent exact test: solve a + s (b - a) = c + u (e - c) in fractions.

    Return True, False, or None for parallel segments that overlap on a line.
    """
    a, b, c, e = [(Fraction(p[0]), Fraction(p[1])) for p in (a, b, c, e)]
    if a == b or c == e:
        p, (s0, s1) = (a, (c, e)) if a == b else (c, (a, b))
        if s0 == s1:
            return p == s0
        on_line = (s1[0] - s0[0]) * (p[1] - s0[1]) == (s1[1] - s0[1]) * (p[0] - s0[0])
        return on_line and min(s0[0], s1[0]) <= p[0] <= max(s0[0], s1[0]) and min(s0[1], s1[1]) <= p[1] <= max(s0[1], s1[1])
    rx, ry = b[0] - a[0], b[1] - a[1]
    sx, sy = e[0] - c[0], e[1] - c[1]
    wx, wy = c[0] - a[0], c[1] - a[1]
    det = rx * sy - ry * sx
    if det == 0:
        if rx * wy - ry * wx != 0:
            return False  # parallel lines
        # Collinear: compare projections on the common direction.
        k = 0 if (rx != 0 or sx != 0) else 1
        lo1, hi1 = sorted((a[k], b[k]))
        lo2, hi2 = sorted((c[k], e[k]))
        return None if lo1 <= hi2 and lo2 <= hi1 else False
    s = (wx * sy - wy * sx) / det
    u = (wx * ry - wy * rx) / det
    return 0 <= s <= 1 and 0 <= u <= 1


def boxes_meet(a, b, c, e):
    return (min(a[0], b[0]) <= max(c[0], e[0]) and min(c[0], e[0]) <= max(a[0], b[0])
            and min(a[1], b[1]) <= max(c[1], e[1]) and min(c[1], e[1]) <= max(a[1], b[1]))


def brute_crossings(q):
    """All pairs of non-adjacent segments, each tested; the box test only skips pairs that cannot meet."""
    m = len(q)
    out, overlap = [], False
    for i in range(m):
        for j in range(i + 1, m):
            if (j - i) % m in (1, m - 1):
                continue
            if not boxes_meet(q[i], q[(i + 1) % m], q[j], q[(j + 1) % m]):
                continue
            r = brute_meet(q[i], q[(i + 1) % m], q[j], q[(j + 1) % m])
            if r is None:
                overlap = True
            elif r:
                out.append((i, j))
    return out, overlap


def dense_curve(points, per_span=300):
    n = len(points)
    return [curve_point(points, k / per_span) for k in range(n * per_span)]


def dist_point_segment(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = vx * vx + vy * vy
    s = 0.0 if L == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L))
    return math.hypot(p[0] - a[0] - s * vx, p[1] - a[1] - s * vy)


def brute_distance(poly, p):
    """Distance from p to the dense closed polyline of C, a lower bound up to the chord error."""
    return min(dist_point_segment(p, poly[k], poly[(k + 1) % len(poly)]) for k in range(len(poly)))


def proper(a, b, c, e):
    def o(p, q, r):
        v = (Fraction(q[0]) - Fraction(p[0])) * (Fraction(r[1]) - Fraction(p[1])) - (Fraction(q[1]) - Fraction(p[1])) * (Fraction(r[0]) - Fraction(p[0]))
        return (v > 0) - (v < 0)

    return o(a, b, c) * o(a, b, e) < 0 and o(c, e, a) * o(c, e, b) < 0


def test_de_boor_matches_basis_functions_and_derivative():
    rng = random.Random(3)
    for n in (4, 5, 8, 11):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)]
        for _ in range(50):
            t = rng.uniform(0, n)
            a, b = curve_point(pts, t), basis_point(pts, t)
            assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12
            h = 1e-6
            p, m = curve_point(pts, t + h), curve_point(pts, t - h)
            d = curve_derivative(pts, t)
            assert abs(d[0] - (p[0] - m[0]) / (2 * h)) < 1e-6 and abs(d[1] - (p[1] - m[1]) / (2 * h)) < 1e-6


def test_sweep_equals_brute_force_on_random_polylines():
    rng = random.Random(11)
    for _ in range(60):
        m = rng.randint(4, 40)
        q = [(rng.uniform(-10, 10), rng.uniform(-10, 10)) for _ in range(m)]
        expected, overlap = brute_crossings(q)
        assert not overlap
        assert polyline_crossings(q) == expected


def test_sweep_on_integer_grids_with_touching_and_collinear_cases():
    rng = random.Random(12)
    raised = equal = 0
    for _ in range(300):
        m = rng.randint(4, 14)
        q = [(float(rng.randint(0, 4)), float(rng.randint(0, 4))) for _ in range(m)]
        expected, overlap = brute_crossings(q)
        if overlap:
            try:
                polyline_crossings(q)
            except ValueError:
                raised += 1
                continue
            raise AssertionError("a collinear overlap must be reported as degenerate input")
        assert polyline_crossings(q) == expected
        equal += 1
    assert raised > 0 and equal > 0


def test_sweep_equals_brute_force_on_offsets():
    for d, m in ((0.5, 400), (0.6, 300), (-0.5, 200), (0.3, 250)):
        q = [offset_point(DUMBBELL, k * len(DUMBBELL) / m, d) for k in range(m)]
        expected, overlap = brute_crossings(q)
        assert not overlap
        assert polyline_crossings(q) == expected


def test_dumbbell_example():
    q, crossings, pieces = offset_trimming(DUMBBELL, 0.5, 400)
    assert len(crossings) == 6
    assert len(pieces) == 12
    kept = [p for p in pieces if p.kept]
    assert len(kept) == 6
    for p in pieces:
        if p.kept:
            assert abs(p.distance - 0.5) < 1e-9
        else:
            assert p.distance < 0.5 - 1e-3


def test_kept_points_are_at_distance_d_and_removed_points_closer():
    poly = dense_curve(DUMBBELL)
    for d, m in ((0.5, 400), (0.6, 400)):
        q, crossings, pieces = offset_trimming(DUMBBELL, d, m)
        cut_points = [p.polyline[0] for p in pieces]
        for p in pieces:
            for v in p.polyline[1:-1]:
                if min(math.dist(v, c) for c in cut_points) < 0.02:
                    continue
                bd = brute_distance(poly, v)
                if p.kept:
                    assert bd >= abs(d) - 1e-4
                else:
                    assert bd < abs(d) - 1e-4


def test_kept_pieces_do_not_cross_and_close_up():
    rng = random.Random(5)
    shapes = [DUMBBELL]
    for _ in range(3):
        n = 9
        pts = []
        for k in range(n):
            ang = 2 * math.pi * k / n
            r = rng.uniform(1.0, 3.0)
            pts.append((r * math.cos(ang), r * math.sin(ang)))
        shapes.append(pts)
    for pts in shapes:
        for d in (0.4, 0.7, -0.4):
            _, _, pieces = offset_trimming(pts, d, 300)
            kept = [p.polyline for p in pieces if p.kept]
            segs = [(pl[k], pl[k + 1]) for pl in kept for k in range(len(pl) - 1)]
            for i in range(len(segs)):
                for j in range(i + 1, len(segs)):
                    if boxes_meet(*segs[i], *segs[j]):
                        assert not proper(*segs[i], *segs[j])
            starts = sorted(pl[0] for pl in kept)
            ends = sorted(pl[-1] for pl in kept)
            assert starts == ends


def test_outward_offset_of_convex_curve_keeps_everything():
    n = 8
    pts = [(2 * math.cos(2 * math.pi * k / n), 2 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    _, crossings, pieces = offset_trimming(pts, -1.0, 200)
    assert crossings == [] and len(pieces) == 1 and pieces[0].kept


def test_inward_offset_beyond_every_radius_of_curvature_removes_everything():
    n = 8
    pts = [(2 * math.cos(2 * math.pi * k / n), 2 * math.sin(2 * math.pi * k / n)) for k in range(n)]
    # The curve is close to a circle of radius about 1.80, so d = 2.5 exceeds every radius of curvature.
    _, _, pieces = offset_trimming(pts, 2.5, 200)
    assert pieces and not any(p.kept for p in pieces)
