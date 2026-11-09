# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ear-clipping/. The authors are listed in prov/7DYMFT.jsonl.

import random
from fractions import Fraction

from ear_clipping import ear_clipping

def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_closed_segment(p, a, b):
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet_badly(a, b, c, d):
    """True when segments ab and cd share a point that is not a common endpoint."""
    shared = {a, b} & {c, d}
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    for p, s, t in ((c, a, b), (d, a, b), (a, c, d), (b, c, d)):
        if p not in shared and on_closed_segment(p, s, t):
            return True
    if len(shared) == 1 and o1 == 0 and o2 == 0:  # collinear and sharing one endpoint: overlap?
        s = shared.pop()
        u = b if a == s else a
        w = d if c == s else c
        if (u[0] - s[0]) * (w[0] - s[0]) + (u[1] - s[1]) * (w[1] - s[1]) > 0:
            return True
    return False


def twice_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def is_simple(poly):
    n = len(poly)
    if n < 3 or len(set(poly)) != n:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if segments_meet_badly(a, b, c, d):
                return False
    return twice_area(poly) != 0


def point_in_polygon(p, poly):
    """1 strictly inside, 0 on the boundary, -1 outside. Exact (crossing number)."""
    n = len(poly)
    inside = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_closed_segment(p, a, b):
            return 0
        if (a[1] > p[1]) != (b[1] > p[1]):
            # x of the crossing compared with p[0], without division
            o = orient(a, b, p)
            if (o > 0) == (b[1] > a[1]):
                inside = not inside
    return 1 if inside else -1


def check_polygon_triangulation(poly, tris):
    """tris are index triples into poly. Checks the count, orientation, area, no crossings, inside."""
    n = len(poly)
    if n < 3:
        assert tris == []
        return
    assert len(tris) == n - 2
    sign = 1 if twice_area(poly) > 0 else -1
    tot = 0
    edges = set()
    for t in tris:
        assert len(set(t)) == 3
        a, b, c = (poly[i] for i in t)
        o = orient(a, b, c)
        assert o != 0
        tot += abs(o)
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges.add((min(i, j), max(i, j)))
        for k in range(n):
            if k not in t:
                p = poly[k]
                o1, o2, o3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
                assert not ((o1 > 0 and o2 > 0 and o3 > 0) or (o1 < 0 and o2 < 0 and o3 < 0))
    assert tot == abs(twice_area(poly))
    assert len({tuple(sorted(t)) for t in tris}) == len(tris)
    el = sorted(edges)
    assert len(el) == 2 * n - 3
    for x in range(len(el)):
        i, j = el[x]
        for y in range(x + 1, len(el)):
            k, m = el[y]
            assert not segments_meet_badly(poly[i], poly[j], poly[k], poly[m])
        if (j - i) % n not in (1, n - 1):  # a diagonal: its midpoint must be strictly inside
            mid = (poly[i][0] + poly[j][0], poly[i][1] + poly[j][1])
            assert point_in_polygon(mid, [(2 * x0, 2 * y0) for x0, y0 in poly]) == 1
            for k in range(n):
                a, b = poly[k], poly[(k + 1) % n]
                assert not segments_meet_badly(poly[i], poly[j], a, b)
    _ = sign


def random_simple_polygon(rng, n, r):
    """Grow a simple polygon from a triangle by replacing an edge ab with a, p, b."""
    while True:
        tri = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(3)]
        if orient(*tri) != 0:
            break
    poly = tri if orient(*tri) > 0 else tri[::-1]
    tries = 0
    while len(poly) < n and tries < 60 * n:
        tries += 1
        p = (rng.randint(-r, r), rng.randint(-r, r))
        if p in poly:
            continue
        i = rng.randrange(len(poly))
        cand = poly[: i + 1] + [p] + poly[i + 1:]
        if is_simple(cand):
            poly = cand
    if rng.random() < 0.5:
        poly = poly[::-1]
    k = rng.randrange(len(poly))
    return poly[k:] + poly[:k]


def test_example() -> None:
    poly = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    tris = ear_clipping(poly)
    check_polygon_triangulation(poly, tris)
    assert len(tris) == 5


def test_small_and_degenerate() -> None:
    assert ear_clipping([]) == []
    assert ear_clipping([(0, 0)]) == []
    assert ear_clipping([(0, 0), (1, 0)]) == []
    assert sorted(ear_clipping([(0, 0), (1, 0), (0, 1)])[0]) == [0, 1, 2]
    try:
        ear_clipping([(0, 0), (1, 0), (2, 0)])
        raise AssertionError('a flat polygon must be rejected')
    except ValueError:
        pass
    for poly in (
        [(0, 0), (1, 0), (0, 1)],
        [(0, 1), (1, 0), (0, 0)],  # clockwise
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)],  # collinear vertices
        [(0, 0), (4, 0), (4, 1), (1, 1), (1, 2), (4, 2), (4, 3), (0, 3)],  # a C shape
        [(0, 0), (3, 0), (3, 3), (2, 3), (2, 1), (1, 1), (1, 3), (0, 3)],  # a U with a narrow gap
        [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (1, 2)],  # no reflex vertex, but (1, 0) blocks the apex
        [(0, 0), (10, 0), (10, 1), (9, 1), (8, 5), (7, 1), (6, 1), (5, 5), (4, 1), (3, 1), (2, 5), (1, 1), (0, 1)],  # a comb
    ):
        check_polygon_triangulation(poly, ear_clipping(poly))


def test_convex_and_fractions() -> None:
    f = Fraction
    poly = [(f(0), f(0)), (f(1, 2), f(-1, 3)), (f(1), f(0)), (f(1), f(1)), (f(1, 3), f(2, 3))]
    tris = ear_clipping(poly)
    assert len(tris) == 3
    big = 10**15
    check_polygon_triangulation([(0, 0), (big, 1), (big + 1, big), (1, big + 1)], ear_clipping([(0, 0), (big, 1), (big + 1, big), (1, big + 1)]))


def test_spiral() -> None:
    poly = [(0, 0), (6, 0), (6, 6), (1, 6), (1, 2), (4, 2), (4, 4), (3, 4), (3, 3), (2, 3), (2, 5), (5, 5), (5, 1), (0, 1)]
    assert is_simple(poly)
    check_polygon_triangulation(poly, ear_clipping(poly))


def test_random_against_brute_force() -> None:
    rng = random.Random(1975)
    for trial in range(250):
        n = rng.randint(3, 16)
        r = rng.choice([2, 3, 4, 6, 50])
        poly = random_simple_polygon(rng, n, r)
        check_polygon_triangulation(poly, ear_clipping(poly))
