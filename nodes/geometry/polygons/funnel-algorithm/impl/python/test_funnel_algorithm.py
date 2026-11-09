# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/funnel-algorithm/. The authors are listed in prov/GH08T5.jsonl.

import heapq
import random
from fractions import Fraction
from math import gcd, hypot, isclose

import pytest

from funnel_algorithm import ear_clipping, funnel, path_length, shortest_path, sleeve


def cross3(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area2(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def on_seg(a, b, p):
    return cross3(a, b, p) == 0 and (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1]) <= 0


def seg_meet(a, b, c, d):
    """Closed segments ab and cd share a point."""
    d1, d2, d3, d4 = cross3(c, d, a), cross3(c, d, b), cross3(a, b, c), cross3(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return on_seg(c, d, a) or on_seg(c, d, b) or on_seg(a, b, c) or on_seg(a, b, d)


def is_simple(poly):
    n = len(poly)
    if len(set(poly)) != n or n < 3:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                s, o1, o2 = (b, a, d) if j == i + 1 else (a, b, c)
                if cross3(s, o1, o2) == 0 and (o1[0] - s[0]) * (o2[0] - s[0]) + (o1[1] - s[1]) * (o2[1] - s[1]) > 0:
                    return False
            elif seg_meet(a, b, c, d):
                return False
    return True


def in_closed_polygon(poly, p):
    """Exact test by the crossing rule, with the boundary counted as inside."""
    n = len(poly)
    inside = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_seg(a, b, p):
            return True
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fraction(p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                inside = not inside
    return inside


def segment_inside(poly, p, q):
    """Exact test that the closed segment pq lies in the closed polygon.

    Cut pq at every point where it meets the boundary; between two cuts the open piece either lies
    on the boundary or misses it, so testing its midpoint decides it.
    """
    if p == q:
        return in_closed_polygon(poly, p)
    n = len(poly)
    cuts = {Fraction(0), Fraction(1)}
    dx, dy = q[0] - p[0], q[1] - p[1]
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for v in (a, b):
            if on_seg(p, q, v):
                cuts.add(Fraction((v[0] - p[0]) * dx + (v[1] - p[1]) * dy, dx * dx + dy * dy))
        den = dx * (b[1] - a[1]) - dy * (b[0] - a[0])
        if den != 0:
            tn = (a[0] - p[0]) * (b[1] - a[1]) - (a[1] - p[1]) * (b[0] - a[0])
            un = (a[0] - p[0]) * dy - (a[1] - p[1]) * dx
            tt, uu = Fraction(tn, den), Fraction(un, den)
            if 0 <= tt <= 1 and 0 <= uu <= 1:
                cuts.add(tt)
    cuts = sorted(cuts)
    for lo, hi in zip(cuts, cuts[1:]):
        m = (lo + hi) / 2
        if not in_closed_polygon(poly, (p[0] + m * dx, p[1] + m * dy)):
            return False
    return True


def oracle_length(poly, s, t):
    """Dijkstra on the visibility graph of s, t and the polygon vertices, with exact visibility."""
    nodes = [s, t] + [v for v in poly if v not in (s, t)]
    m = len(nodes)
    dist = [float("inf")] * m
    dist[0] = 0.0
    heap = [(0.0, 0)]
    done = [False] * m
    while heap:
        d, i = heapq.heappop(heap)
        if done[i]:
            continue
        done[i] = True
        if i == 1:
            return d
        for j in range(m):
            if not done[j] and segment_inside(poly, nodes[i], nodes[j]):
                nd = d + hypot(nodes[j][0] - nodes[i][0], nodes[j][1] - nodes[i][1])
                if nd < dist[j]:
                    dist[j] = nd
                    heapq.heappush(heap, (nd, j))
    raise AssertionError("t not reachable")


def check(poly, tris, s, t):
    path = shortest_path(poly, tris, s, t)
    assert path[0] == s and path[-1] == t
    vertices = set(poly)
    for p in path[1:-1]:
        assert p in vertices
    for a, b, c in zip(path, path[1:], path[2:]):
        assert cross3(a, b, c) != 0, (poly, s, t, path)  # every inner point is a real bend
    for a, b in zip(path, path[1:]):
        assert a != b
        assert segment_inside(poly, a, b), (poly, s, t, path)
    want = oracle_length(poly, s, t)
    assert isclose(path_length(path), want, rel_tol=1e-9, abs_tol=1e-9), (poly, s, t, path, want)
    return path


def add_collinear(rng, poly):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        out.append(a)
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dx), abs(dy))
        for k in range(1, g):
            if rng.random() < 0.3:
                out.append((a[0] + k * dx // g, a[1] + k * dy // g))
    return out


def random_simple(rng, n, g):
    """A random simple polygon: a random order of grid points, untangled by 2-opt moves."""
    for _ in range(50):
        pts = list({(rng.randint(0, g), rng.randint(0, g)) for _ in range(n)})
        if len(pts) < 3:
            continue
        rng.shuffle(pts)
        for _ in range(200):
            m = len(pts)
            bad = None
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    if seg_meet(pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]):
                        bad = (i, j)
                        break
                if bad:
                    break
            if not bad:
                break
            i, j = bad
            pts[i + 1:j + 1] = pts[i + 1:j + 1][::-1]
        if is_simple(pts) and area2(pts) != 0:
            return pts if area2(pts) > 0 else pts[::-1]
    return None


def random_point(rng, poly):
    """A lattice point of the closed polygon: a vertex, a point of an edge, or any point of the box."""
    r = rng.random()
    if r < 0.2:
        return rng.choice(poly)
    if r < 0.35:
        i = rng.randrange(len(poly))
        a, b = poly[i], poly[(i + 1) % len(poly)]
        g = gcd(abs(b[0] - a[0]), abs(b[1] - a[1]))
        k = rng.randint(0, g)
        return (a[0] + k * (b[0] - a[0]) // g, a[1] + k * (b[1] - a[1]) // g)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    while True:
        p = (rng.randint(min(xs), max(xs)), rng.randint(min(ys), max(ys)))
        if in_closed_polygon(poly, p):
            return p


SPIRAL = [(0, 0), (10, 0), (10, 10), (2, 10), (2, 4), (6, 4), (6, 6), (4, 6), (4, 8), (8, 8), (8, 2), (0, 2)]
COMB = [(0, 0), (5, 0), (5, 3), (4, 3), (4, 1), (3, 1), (3, 3), (2, 3), (2, 1), (1, 1), (1, 3), (0, 3)]
EXAMPLE = [(0, 0), (8, 0), (8, 6), (5, 6), (5, 2), (3, 2), (3, 6), (0, 6)]


def test_example() -> None:
    tris = ear_clipping(EXAMPLE)
    assert shortest_path(EXAMPLE, tris, (1, 5), (7, 5)) == [(1, 5), (3, 2), (5, 2), (7, 5)]
    check(EXAMPLE, tris, (1, 5), (7, 5))


def test_straight_line_when_visible() -> None:
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    tris = ear_clipping(square)
    assert shortest_path(square, tris, (0, 0), (4, 4)) == [(0, 0), (4, 4)]
    assert shortest_path(square, tris, (1, 3), (1, 3)) == [(1, 3)]
    assert shortest_path(square, tris, (0, 1), (4, 1)) == [(0, 1), (4, 1)]


def test_fixed_shapes() -> None:
    tris = ear_clipping(SPIRAL)
    path = check(SPIRAL, tris, (1, 1), (5, 5))
    assert len(path) > 3
    tris = ear_clipping(COMB)
    assert shortest_path(COMB, tris, (0, 3), (5, 3)) == [(0, 3), (1, 1), (4, 1), (5, 3)]
    check(COMB, tris, (0, 3), (5, 3))
    check(COMB, tris, (1, 3), (4, 3))


def test_path_along_collinear_boundary() -> None:
    # an L-shape with extra vertices on its edges; the path bends at the reflex corner (2, 2)
    poly = [(0, 0), (2, 0), (4, 0), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (0, 4), (0, 2)]
    tris = ear_clipping(poly)
    assert shortest_path(poly, tris, (4, 1), (1, 4)) == [(4, 1), (2, 2), (1, 4)]
    assert shortest_path(poly, tris, (4, 2), (2, 4)) == [(4, 2), (2, 2), (2, 4)]
    # the segment from (4, 0) to (0, 4) touches the boundary only at the reflex corner (2, 2)
    assert shortest_path(poly, tris, (4, 0), (0, 4)) == [(4, 0), (0, 4)]
    assert shortest_path(poly, tris, (4, 2), (0, 4)) == [(4, 2), (2, 2), (0, 4)]
    check(poly, tris, (4, 0), (0, 4))
    check(poly, tris, (3, 2), (2, 3))


def test_no_straight_points_in_output() -> None:
    poly = [(0, 0), (2, 2), (0, 2), (0, 1)]
    assert shortest_path(poly, ear_clipping(poly), (0, 0), (0, 2)) == [(0, 0), (0, 2)]


def test_any_triangulation_works() -> None:
    # a fan from the kernel vertex (3, 0) of a star-shaped polygon
    poly = [(3, 0), (6, 1), (5, 3), (6, 6), (3, 4), (0, 6), (1, 3), (0, 1)]
    fan = [(0, i, i + 1) for i in range(1, len(poly) - 1)]
    for s, t in [((6, 6), (0, 6)), ((5, 3), (1, 3)), ((6, 1), (0, 6)), ((3, 4), (3, 0))]:
        assert path_length(shortest_path(poly, fan, s, t)) == pytest.approx(
            path_length(shortest_path(poly, ear_clipping(poly), s, t)))
        check(poly, fan, s, t)


def test_bad_input() -> None:
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    with pytest.raises(ValueError):
        shortest_path(square, ear_clipping(square), (0, 0), (5, 5))
    with pytest.raises(ValueError):
        ear_clipping(square[::-1])
    with pytest.raises(ValueError):
        funnel(square, [(0, 1), (0, 1)], (1, 1), (2, 2))


def test_random_polygons() -> None:
    rng = random.Random(20261109)
    done = 0
    while done < 600:
        poly = random_simple(rng, rng.randint(3, 12), rng.choice([5, 8, 12]))
        if poly is None:
            continue
        if rng.random() < 0.4:
            poly = add_collinear(rng, poly)
        tris = ear_clipping(poly)
        if rng.random() < 0.3:
            # the same polygon, triangulated from another starting vertex
            k = rng.randrange(len(poly))
            rot = poly[k:] + poly[:k]
            tris = [tuple((i + k) % len(poly) for i in tri) for tri in ear_clipping(rot)]
        s, t = random_point(rng, poly), random_point(rng, poly)
        check(poly, tris, s, t)
        portals = sleeve(poly, tris, s, t)
        assert len(portals) <= len(poly) - 3
        done += 1


def test_portals_are_chained() -> None:
    rng = random.Random(5)
    for _ in range(100):
        poly = random_simple(rng, rng.randint(5, 12), 10)
        if poly is None:
            continue
        tris = ear_clipping(poly)
        s, t = random_point(rng, poly), random_point(rng, poly)
        portals = sleeve(poly, tris, s, t)
        for (l1, r1), (l2, r2) in zip(portals, portals[1:]):
            assert (l1 == l2) != (r1 == r2)
        diagonals = {frozenset(p) for p in portals}
        assert len(diagonals) == len(portals)
        n = len(poly)
        for left, right in portals:
            assert (left - right) % n not in (1, n - 1)  # a portal is a diagonal, not a polygon edge
