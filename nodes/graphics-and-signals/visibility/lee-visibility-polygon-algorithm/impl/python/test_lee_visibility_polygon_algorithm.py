# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-visibility-polygon-algorithm/. The authors are listed in prov/V14M2Q.jsonl.

import math
import random
from fractions import Fraction as F

from lee_visibility_polygon_algorithm import lee_visibility_polygon, orient, seg_seg


# ---------- exact brute force ----------

def on_segment(p, a, b):
    return orient(a, b, p) == 0 and min(a, b) <= p <= max(a, b)


def in_closed_polygon(p, poly):
    """Exact test: p inside or on the boundary of the simple polygon."""
    n = len(poly)
    for k in range(n):
        if on_segment(p, poly[k], poly[(k + 1) % n]):
            return True
    inside = False
    x, y = p
    for k in range(n):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def sees(z, b, poly):
    """Exact test: the closed segment zb lies in the closed polygon.

    Find every parameter t where zb meets the boundary, sort them, and test
    the midpoint of each piece between two of them.
    """
    ts = {F(0), F(1)}
    dx, dy = b[0] - z[0], b[1] - z[1]

    def param(p):
        return (p[0] - z[0]) / dx if dx != 0 else (p[1] - z[1]) / dy

    n = len(poly)
    for k in range(n):
        hit = seg_seg(z, b, poly[k], poly[(k + 1) % n])
        if hit is None:
            continue
        if hit == "overlap":
            for p in (poly[k], poly[(k + 1) % n]):
                if on_segment(p, z, b):
                    ts.add(param(p))
        else:
            ts.add(param(hit))
    ts = sorted(ts)
    for t0, t1 in zip(ts, ts[1:]):
        t = (t0 + t1) / 2
        if not in_closed_polygon((z[0] + t * dx, z[1] + t * dy), poly):
            return False
    return True


def samples(poly, per_edge):
    n = len(poly)
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        for j in range(per_edge):
            t = F(j, per_edge)
            yield (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def check(poly, z, per_edge=7, interior=40, rng=None):
    poly = [(F(x), F(y)) for x, y in poly]
    z = (F(z[0]), F(z[1]))
    vis = lee_visibility_polygon(poly, z)
    assert len(vis) >= 3
    # Every vertex of the result is a point of P that z sees.
    for p in vis:
        assert sees(z, p, poly), (p, vis)
    # Dense boundary points and all vertices: seen exactly when in the result.
    for b in samples(poly, per_edge):
        assert sees(z, b, poly) == in_closed_polygon(b, vis), (b, poly, z, vis)
    # Random points of the bounding box.
    rng = rng or random.Random(1)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    for _ in range(interior):
        q = (F(rng.randint(0, 997), 997) * (max(xs) - min(xs)) + min(xs),
             F(rng.randint(0, 991), 991) * (max(ys) - min(ys)) + min(ys))
        if q == z or not in_closed_polygon(q, poly):
            continue
        assert sees(z, q, poly) == in_closed_polygon(q, vis), (q, poly, z, vis)
    return vis


# ---------- polygon generators ----------

def is_simple(poly):
    n = len(poly)
    if len(set(poly)) != n:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            hit = seg_seg(a, b, c, d)
            if hit is None:
                continue
            if j == i + 1:
                if hit != b:
                    return False
            elif i == 0 and j == n - 1:
                if hit != a:
                    return False
            else:
                return False
    return True


def random_simple_polygon(rng, n, size=40):
    """Random points, then 2-opt moves until no two edges cross."""
    while True:
        pts = list({(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)})
        if len(pts) < 3:
            continue
        pts = [(F(x), F(y)) for x, y in pts]
        rng.shuffle(pts)
        for _ in range(2000):
            m = len(pts)
            fixed = True
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    a, b, c, d = pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]
                    if seg_seg(a, b, c, d) is not None:
                        pts[i + 1:j + 1] = reversed(pts[i + 1:j + 1])
                        fixed = False
                        break
                if not fixed:
                    break
            if fixed:
                break
        if is_simple(pts) and area2(pts) != 0:
            return pts


def area2(poly):
    return sum(poly[i - 1][0] * poly[i][1] - poly[i][0] * poly[i - 1][1] for i in range(len(poly)))


def interior_point(rng, poly, general=True):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    for _ in range(10000):
        z = (F(rng.randint(1, 10 ** 4 - 1), 10 ** 4) * (max(xs) - min(xs)) + min(xs),
             F(rng.randint(1, 10 ** 4 - 1), 10 ** 4) * (max(ys) - min(ys)) + min(ys))
        if not in_closed_polygon(z, poly):
            continue
        if any(on_segment(z, poly[k], poly[(k + 1) % len(poly)]) for k in range(len(poly))):
            continue
        if general and any(orient(z, a, b) == 0 for a in poly for b in poly if a != b):
            continue
        return z
    return None


def spiral(turns, steps_per_turn=12, width=F(1, 2)):
    """A corridor that winds `turns` times around the origin."""
    outer, inner = [], []
    m = int(turns * steps_per_turn)
    for k in range(m + 1):
        th = 2 * math.pi * k / steps_per_turn
        r = 1 + th / (2 * math.pi)
        c, s = F(round(math.cos(th) * 1000), 1000), F(round(math.sin(th) * 1000), 1000)
        outer.append((F(round(r * 1000), 1000) * c, F(round(r * 1000), 1000) * s))
        rr = F(round(r * 1000), 1000) - width
        inner.append((rr * c, rr * s))
    return outer + inner[::-1]


# ---------- tests ----------

def test_room_with_notch():
    room = [(0, 0), (8, 0), (8, 6), (5, 6), (5, 3), (3, 3), (3, 6), (0, 6)]
    vis = check(room, (7, 1))
    assert set(vis) == {(5, 6), (5, 3), (3, 3), (0, F(9, 2)), (0, 0), (8, 0), (8, 6)}


def test_convex_polygon_sees_everything():
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    vis = check(square, (F(1, 3), F(2, 7)))
    assert set(vis) == {(0, 0), (4, 0), (4, 4), (0, 4)}


def test_clockwise_input():
    room = [(0, 6), (3, 6), (3, 3), (5, 3), (5, 6), (8, 6), (8, 0), (0, 0)]
    check(room, (7, 1))


def test_cases_that_reach_every_scan_state():
    cases = [
        ("SCAND", [(9, 3), (10, 9), (2, 2), (8, 4), (8, 3), (8, 0), (10, 1), (10, 5)], (F(7, 2), F(13, 4))),
        ("SCANB", [(0, 4), (11, 3), (11, 8), (2, 8), (8, 6)], (5, F(19, 4))),
        ("SCANC", [(6, 6), (2, 6), (1, 12), (6, 12), (12, 5), (6, 1), (3, 0), (4, 3), (8, 5), (10, 6), (7, 10)],
         (F(41, 8), F(3921, 1250))),
    ]
    for state, poly, z in cases:
        trace = []
        lee_visibility_polygon(poly, z, trace)
        assert state in {s for s, _, _ in trace}
        check(poly, z, per_edge=12, interior=200)


def test_random_polygons_general_position():
    rng = random.Random(7)
    done = 0
    while done < 40:
        poly = random_simple_polygon(rng, rng.randint(4, 14))
        z = interior_point(rng, poly)
        if z is None:
            continue
        check(poly, z, rng=rng)
        done += 1


def test_random_polygons_many_viewpoints():
    rng = random.Random(11)
    for _ in range(6):
        poly = random_simple_polygon(rng, 24, size=60)
        for _ in range(4):
            z = interior_point(rng, poly)
            if z is not None:
                check(poly, z, per_edge=4, interior=20, rng=rng)


def test_spirals_that_wind_around_the_viewpoint():
    # Lee's original 1983 rules fail when the boundary winds more than a full
    # turn around z (Joe and Simpson 1987). These corridors wind up to 3 times.
    rng = random.Random(5)
    for turns in (F(3, 2), 2, 3):
        poly = spiral(turns)
        assert is_simple(poly)
        for _ in range(3):
            z = interior_point(rng, poly)
            if z is not None:
                check(poly, z, per_edge=3, interior=30, rng=rng)
        for start in (0, 1, 2):
            # viewpoints in the inner end of the corridor
            a, b = poly[start], poly[-1 - start]
            c, d = poly[start + 1], poly[-2 - start]
            z = ((a[0] + b[0] + c[0] + d[0]) / 4, (a[1] + b[1] + c[1] + d[1]) / 4)
            if in_closed_polygon(z, poly):
                check(poly, z, per_edge=3, interior=30, rng=rng)
