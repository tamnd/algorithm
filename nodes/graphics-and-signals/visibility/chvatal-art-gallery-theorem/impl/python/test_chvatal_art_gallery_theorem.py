# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chvatal-art-gallery-theorem/. The authors are listed in prov/9V33Q8.jsonl.

import itertools
import random
from fractions import Fraction as F

from chvatal_art_gallery_theorem import chvatal_guards, fan_partition, orient


# ---------- the fan partition on its own ----------

def random_triangulation(labels, rng):
    """A random triangulation of the convex polygon with these labels."""
    if len(labels) == 3:
        return [frozenset(labels)]
    n = len(labels)
    i = rng.randrange(1, n - 1)  # the apex of the triangle on the edge labels[0] labels[-1]
    out = [frozenset((labels[0], labels[i], labels[-1]))]
    if i >= 2:
        out += random_triangulation(labels[:i + 1], rng)
    if i <= n - 3:
        out += random_triangulation(labels[i:], rng)
    return out


def check_fans(n, tris, fans):
    seen = []
    for c, ts in fans:
        assert ts
        for t in ts:
            assert c in t
        seen += ts
    assert sorted(map(sorted, seen)) == sorted(map(sorted, tris))
    assert len(fans) <= n // 3


def test_every_case_of_the_proof():
    # The centers of small fans are picked at random, so that the rare
    # cases (a fan of the rest centered at a given vertex of T) also occur.
    rng = random.Random(3)
    want = {"1", "2a", "2b.1", "2b.2", "3a", "3b.1", "3b.2", "3d.1", "3d.2", "3d.3"}
    cases = set()
    for _ in range(20000):
        n = rng.randint(6, 14)
        tris = random_triangulation(list(range(n)), rng)
        trace = []
        fans = fan_partition(list(range(n)), tris, trace, rng.choice)
        check_fans(n, tris, fans)
        cases.update(trace)
        if cases == want:
            break
    assert cases == want


def test_all_triangulations_of_small_polygons():
    def all_triangulations(labels):
        if len(labels) < 3:
            yield []
            return
        for i in range(1, len(labels) - 1):
            for left in all_triangulations(labels[:i + 1]):
                for right in all_triangulations(labels[i:]):
                    yield [frozenset((labels[0], labels[i], labels[-1]))] + left + right

    for n in range(3, 11):
        for tris in all_triangulations(list(range(n))):
            check_fans(n, tris, fan_partition(list(range(n)), tris))


# ---------- exact visibility in a polygon ----------

def seg_cross(a, b, c, d):
    """Do the closed segments ab and cd meet?"""
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True

    def on(p, q, r):
        return orient(p, q, r) == 0 and min(p, q) <= r <= max(p, q)
    return on(a, b, c) or on(a, b, d) or on(c, d, a) or on(c, d, b)


def in_closed(p, poly):
    n = len(poly)
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        if orient(a, b, p) == 0 and min(a, b) <= p <= max(a, b):
            return True
    inside = False
    for k in range(n):
        (x1, y1), (x2, y2) = poly[k], poly[(k + 1) % n]
        if (y1 > p[1]) != (y2 > p[1]) and x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1) > p[0]:
            inside = not inside
    return inside


def sees(g, q, poly):
    """The closed segment gq lies in the polygon: test it between all its boundary contacts."""
    ts = {F(0), F(1)}
    n = len(poly)
    dx, dy = q[0] - g[0], q[1] - g[1]
    for k in range(n):
        a, b = poly[k], poly[(k + 1) % n]
        for p in (a, b):
            if orient(g, q, p) == 0 and min(g, q) <= p <= max(g, q):
                ts.add((p[0] - g[0]) / dx if dx else (p[1] - g[1]) / dy)
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = dx * ey - dy * ex
        if den != 0:
            t = ((a[0] - g[0]) * ey - (a[1] - g[1]) * ex) / den
            s = ((a[0] - g[0]) * dy - (a[1] - g[1]) * dx) / den
            if 0 <= t <= 1 and 0 <= s <= 1:
                ts.add(t)
    ts = sorted(ts)
    return all(in_closed((g[0] + (t0 + t1) / 2 * dx, g[1] + (t0 + t1) / 2 * dy), poly)
               for t0, t1 in zip(ts, ts[1:]))


def random_polygon(rng, n, size=30):
    """A random simple counterclockwise polygon with no three vertices on a line."""
    while True:
        pts = list({(F(rng.randint(0, size)), F(rng.randint(0, size))) for _ in range(n)})
        if any(orient(a, b, c) == 0 for a, b, c in itertools.combinations(pts, 3)):
            continue
        rng.shuffle(pts)
        for _ in range(500):
            m = len(pts)
            moved = False
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    if seg_cross(pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]):
                        pts[i + 1:j + 1] = reversed(pts[i + 1:j + 1])
                        moved = True
            if not moved:
                break
        else:
            continue
        area = sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                   for k in range(len(pts)))
        return pts if area > 0 else pts[::-1]


def sample_points(poly, tris, rng, per_triangle=3):
    out = []
    for t in tris:
        a, b, c = (poly[i] for i in t)
        for _ in range(per_triangle):
            u, v = F(rng.randint(1, 50)), F(rng.randint(1, 50))
            w = F(rng.randint(1, 50))
            s = u + v + w
            out.append(((u * a[0] + v * b[0] + w * c[0]) / s, (u * a[1] + v * b[1] + w * c[1]) / s))
    return out


def test_guards_see_random_polygons():
    rng = random.Random(11)
    for _ in range(25):
        poly = random_polygon(rng, rng.randint(6, 12))
        guards, fans, tris = chvatal_guards(poly)
        check_fans(len(poly), tris, fans)
        assert len(guards) <= len(poly) // 3
        for q in sample_points(poly, tris, rng):
            assert any(sees(poly[g], q, poly) for g in guards)


def min_vertex_guards(poly, points):
    """Brute force over vertex subsets: the fewest vertices that see all the points."""
    seen_by = [{j for j, q in enumerate(points) if sees(v, q, poly)} for v in poly]
    everything = set(range(len(points)))
    for size in range(1, len(poly) + 1):
        for subset in itertools.combinations(range(len(poly)), size):
            if set().union(*(seen_by[i] for i in subset)) == everything:
                return size
    raise AssertionError("the vertices do not see all points")


def test_brute_force_minimum_is_not_more_than_chvatal():
    rng = random.Random(5)
    for _ in range(10):
        poly = random_polygon(rng, rng.randint(6, 9))
        guards, fans, tris = chvatal_guards(poly)
        pts = sample_points(poly, tris, rng, per_triangle=2)
        assert min_vertex_guards(poly, pts) <= len(guards) <= len(poly) // 3


def test_comb_needs_n_over_3():
    # A comb with k prongs and 3k vertices.
    # Prong p has its apex at (3p + 1, 4) and its base from (3p, 1) to
    # (3p + 2, 1); the outer bases of the first and last prong are the two
    # bottom corners (0, 0) and (3k - 1, 0).
    for k in (2, 3, 4):
        poly = [(F(0), F(0)), (F(3 * k - 1), F(0))]
        for p in range(k - 1, -1, -1):
            poly.append((F(3 * p + 1), F(4)))
            if p > 0:
                poly += [(F(3 * p), F(1)), (F(3 * p - 1), F(1))]
        assert len(poly) == 3 * k
        guards, fans, tris = chvatal_guards(poly)
        tips = [(F(3 * p + 1), F(4) - F(1, 10)) for p in range(k)]
        assert min_vertex_guards(poly, tips) == k == len(guards)
