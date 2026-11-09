# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monotone-polygon-triangulation/. The authors are listed in prov/WF7BGF.jsonl.

import random
from fractions import Fraction

from monotone_polygon_triangulation import _faces, above, make_monotone, triangulate_monotone, triangulate_polygon



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


def is_monotone(pts, piece):
    """y-monotone in the sweep order: one descent and one ascent around the boundary."""
    m = len(piece)
    changes = 0
    for t in range(m):
        a, b, c = pts[piece[t - 1]], pts[piece[t]], pts[piece[(t + 1) % m]]
        if above(b, a) == above(b, c):
            changes += 1
    return changes == 2


def check_pieces(poly):
    n = len(poly)
    pts = poly if twice_area(poly) > 0 else poly[::-1]
    diags = make_monotone(pts)
    for i, j in diags:
        assert (j - i) % n not in (0, 1, n - 1)
        mid = (pts[i][0] + pts[j][0], pts[i][1] + pts[j][1])
        assert point_in_polygon(mid, [(2 * x, 2 * y) for x, y in pts]) == 1
        for k in range(n):
            assert not segments_meet_badly(pts[i], pts[j], pts[k], pts[(k + 1) % n])
    faces = _faces(pts, [(i, (i + 1) % n) for i in range(n)] + diags)
    assert len(faces) == len(diags) + 1
    for f in faces:
        assert is_monotone(pts, f)
    return diags


def run(poly):
    tris = triangulate_polygon(poly)
    check_polygon_triangulation(poly, tris)
    for a, b, c in tris:
        assert orient(poly[a], poly[b], poly[c]) > 0
    if len(poly) >= 3:
        check_pieces(poly)
    return tris


def test_example():
    poly = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    tris = run(poly)
    assert make_monotone(poly) == [(0, 4)]
    assert sorted(tuple(sorted(t)) for t in tris) == [(0, 1, 4), (0, 4, 6), (1, 2, 4), (2, 3, 4), (4, 5, 6)]


def test_small_and_degenerate():
    assert triangulate_polygon([]) == [] and triangulate_polygon([(0, 0), (1, 1)]) == []
    run([(0, 0), (4, 0), (0, 3)])
    run([(0, 0), (0, 3), (4, 0)])
    run([(0, 0), (1, 0), (2, 0), (1, 2)])
    run([(0, 0), (2, 0), (2, 2), (0, 2)])
    run([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)])
    run([(0, 0), (4, 0), (4, 1), (1, 1), (1, 2), (4, 2), (4, 3), (0, 3)])
    try:
        triangulate_polygon([(0, 0), (1, 1), (2, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("a flat polygon must be rejected")


def test_monotone_pieces_directly():
    pts = [(0, 10), (-3, 7), (-1, 5), (-4, 2), (0, 0), (2, 3), (1, 6), (3, 8)]
    tris = triangulate_monotone(pts, list(range(len(pts))))
    check_polygon_triangulation(pts, tris)
    zig = [(0, 20)] + [(-(k % 2) - 1, 20 - 2 * k) for k in range(1, 10)] + [(0, 0)] + [((k % 2) + 1, 2 * k + 1) for k in range(1, 9)]
    assert is_simple(zig) and twice_area(zig) > 0
    check_polygon_triangulation(zig, triangulate_monotone(zig, list(range(len(zig)))))


def test_combs_and_spirals():
    comb = [(0, 0), (20, 0)]
    for k in range(9, -1, -1):
        comb += [(2 * k + 1, 6), (2 * k + 1, 1), (2 * k, 1), (2 * k, 6)] if k else [(1, 6), (1, 1), (0, 1)]
    comb = [p for i, p in enumerate(comb) if p not in comb[:i]]
    assert is_simple(comb)
    run(comb)
    run([(y, -x) for x, y in comb])
    side = [(0, 0), (10, 0), (10, 10), (2, 10), (2, 4), (6, 4), (6, 6), (4, 6), (4, 8), (8, 8), (8, 2), (0, 2)]
    assert is_simple(side)
    run(side)
    run(side[::-1])


def test_random_polygons():
    rng = random.Random(1978)
    for trial in range(300):
        n = rng.randint(3, 24)
        poly = random_simple_polygon(rng, n, rng.choice([3, 4, 6, 20, 1000]))
        run(poly)


def test_fractions_and_big():
    poly = [(Fraction(0), Fraction(0)), (Fraction(5, 2), Fraction(1, 3)), (Fraction(1, 2), Fraction(1, 2)), (Fraction(5, 2), Fraction(7, 3)), (Fraction(0), Fraction(2))]
    assert is_simple(poly)
    run(poly)
    rng = random.Random(5)
    poly = random_simple_polygon(rng, 40, 50)
    big = [(x * 10 ** 18 + 1, y * 10 ** 18 - 5) for x, y in poly]
    run(big)
