# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crossing-number-algorithm/. The authors are listed in prov/6ADJ3H.jsonl.

import random
from fractions import Fraction

from crossing_number_algorithm import BOUNDARY, INSIDE, OUTSIDE, crossing_number_algorithm


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_boundary_oracle(poly, q):
    """Independent boundary test: q is a vertex, or collinear with an edge and inside its box."""
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if q == a:
            return True
        if cross(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return False


def quadrant(v, q):
    x, y = v[0] - q[0], v[1] - q[1]
    if x > 0 and y >= 0:
        return 0
    if x <= 0 and y > 0:
        return 1
    if x < 0 and y <= 0:
        return 2
    return 3


def winding_oracle(poly, q):
    """Winding number by summing quarter turns; q must not lie on the boundary."""
    total = 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        d = (quadrant(b, q) - quadrant(a, q)) % 4
        if d == 1:
            total += 1
        elif d == 3:
            total -= 1
        elif d == 2:
            total += 2 if cross(q, a, b) > 0 else -2
    assert total % 4 == 0
    return total // 4


def dedupe(poly):
    out = []
    for p in poly:
        if not out or out[-1] != p:
            out.append(p)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def histogram(rng, m, top):
    """An x-monotone rectilinear polygon with many collinear vertices and horizontal edges."""
    h = [rng.randint(1, top) for _ in range(m)]
    poly = [(0, 0), (m, 0), (m, h[m - 1])]
    for i in range(m - 1, 0, -1):
        poly.append((i, h[i]))
        poly.append((i, h[i - 1]))
    poly.append((0, h[0]))
    return dedupe(poly)


def star_polygon(rng, k, r):
    """A polygon star-shaped around the origin, with vertices sorted by angle."""
    seen = {}
    for _ in range(k):
        p = (rng.randint(-r, r), rng.randint(-r, r))
        if p == (0, 0):
            continue
        half = 0 if p[1] > 0 or (p[1] == 0 and p[0] > 0) else 1
        key = None
        for d in seen:
            if d[0] == half and cross((0, 0), d[1], p) == 0:
                key = d
        if key is None:
            seen[(half, p)] = p
    pts = list(seen.values())
    import functools

    def cmp(a, b):
        ha = 0 if a[1] > 0 or (a[1] == 0 and a[0] > 0) else 1
        hb = 0 if b[1] > 0 or (b[1] == 0 and b[0] > 0) else 1
        if ha != hb:
            return ha - hb
        c = cross((0, 0), a, b)
        return -1 if c > 0 else (1 if c < 0 else 0)

    pts.sort(key=functools.cmp_to_key(cmp))
    n = len(pts)
    if n < 3 or any(cross((0, 0), pts[i], pts[(i + 1) % n]) <= 0 for i in range(n)):
        return None
    return pts


def shear(poly, k):
    return [(x + k * y, y) for x, y in poly]


def queries(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return [(x, y) for x in range(min(xs) - 1, max(xs) + 2) for y in range(min(ys) - 1, max(ys) + 2)]


def check_simple(poly):
    for q in queries(poly):
        got = crossing_number_algorithm(poly, q)
        if on_boundary_oracle(poly, q):
            assert got == BOUNDARY, (poly, q)
        else:
            w = winding_oracle(poly, q)
            assert w in (-1, 0, 1)
            assert got == (INSIDE if w != 0 else OUTSIDE), (poly, q)


def test_example() -> None:
    v = [(0, 0), (10, 0), (10, 8), (7, 4), (5, 4), (4, 8), (2, 4), (0, 8)]
    assert crossing_number_algorithm(v, (1, 4)) == INSIDE
    assert crossing_number_algorithm(v, (6, 6)) == OUTSIDE
    assert crossing_number_algorithm(v, (6, 4)) == BOUNDARY
    assert crossing_number_algorithm(v, (2, 4)) == BOUNDARY
    assert crossing_number_algorithm(v, (3, 4)) == INSIDE
    assert crossing_number_algorithm(v, (11, 4)) == OUTSIDE
    check_simple(v)


def test_small_and_degenerate() -> None:
    assert crossing_number_algorithm([], (0, 0)) == OUTSIDE
    assert crossing_number_algorithm([(1, 1)], (1, 1)) == BOUNDARY
    assert crossing_number_algorithm([(1, 1)], (0, 1)) == OUTSIDE
    seg = [(0, 0), (4, 2)]
    assert crossing_number_algorithm(seg, (2, 1)) == BOUNDARY
    assert crossing_number_algorithm(seg, (1, 1)) == OUTSIDE
    tri = [(0, 0), (4, 0), (0, 4)]
    assert crossing_number_algorithm(tri, (1, 1)) == INSIDE
    assert crossing_number_algorithm(tri, (2, 2)) == BOUNDARY
    assert crossing_number_algorithm(tri, (-1, 0)) == OUTSIDE  # ray along the bottom edge
    assert crossing_number_algorithm(tri, (-1, 4)) == OUTSIDE  # ray through the top vertex
    assert crossing_number_algorithm(tri[::-1], (1, 1)) == INSIDE
    # collinear vertices, and rays along horizontal edges
    sq = [(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2)]
    for q in [(-1, 0), (-1, 2), (-1, 4), (5, 2)]:
        assert crossing_number_algorithm(sq, q) == OUTSIDE
    assert crossing_number_algorithm(sq, (1, 2)) == INSIDE
    assert crossing_number_algorithm(sq, (2, 0)) == BOUNDARY
    # fractions
    assert crossing_number_algorithm(tri, (Fraction(1, 3), Fraction(10, 3))) == INSIDE
    assert crossing_number_algorithm(tri, (Fraction(1, 2), Fraction(7, 2))) == BOUNDARY


def test_random_simple_polygons() -> None:
    rng = random.Random(20261108)
    count = 0
    while count < 250:
        kind = rng.randrange(3)
        if kind == 0:
            poly = histogram(rng, rng.randint(1, 6), 5)
        elif kind == 1:
            poly = star_polygon(rng, rng.randint(3, 9), 4)
            if poly is None:
                continue
        else:
            poly = shear(histogram(rng, rng.randint(1, 5), 4), rng.choice([-1, 1, 2]))
        if rng.random() < 0.5:
            poly = poly[::-1]
        check_simple(poly)
        count += 1


def test_random_self_intersecting_polygons() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randint(3, 8)
        poly = [(rng.randint(0, 5), rng.randint(0, 5)) for _ in range(n)]
        for _ in range(8):
            q = (rng.randint(-1, 6), rng.randint(-1, 6))
            got = crossing_number_algorithm(poly, q)
            if on_boundary_oracle(poly, q):
                assert got == BOUNDARY
            else:
                parity = winding_oracle(poly, q) % 2
                assert got == (INSIDE if parity == 1 else OUTSIDE), (poly, q)
