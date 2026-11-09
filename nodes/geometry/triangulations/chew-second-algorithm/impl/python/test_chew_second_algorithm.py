# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chew-second-algorithm/. The authors are listed in prov/R64BJ4.jsonl.
import random
from fractions import Fraction

import pytest

from chew_second_algorithm import chew, circumcenter


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def on_segment(a, b, q):
    return orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) \
        and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])


def proper_cross(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def blocked(x, w, P, subs):
    """Does a subsegment meet the open segment from the point x to the vertex w?"""
    for u, v in subs:
        a, b = P[u], P[v]
        if proper_cross(x, w, a, b):
            return True
        for e in (a, b):
            if e != w and e != x and on_segment(x, w, e):
                return True
    return False


def poly_area2(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def chain(P, subs, a, b):
    """The subsegments on the input segment ab form a chain from a to b."""
    a, b = (Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))
    on = [(u, v) for u, v in subs if on_segment(a, b, P[u]) and on_segment(a, b, P[v])]
    pos = lambda p: (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])  # noqa: E731
    pieces = sorted((min(pos(P[u]), pos(P[v])), max(pos(P[u]), pos(P[v]))) for u, v in on)
    assert pieces[0][0] == 0 and pieces[-1][1] == pos(b)
    assert all(pieces[k][1] == pieces[k + 1][0] for k in range(len(pieces) - 1))
    return len(on)


def check(boundary, segments=(), points=(), B2=Fraction(5, 4), crossings=True):
    P, tris, subs = chew(boundary, segments, points, B2)
    n = len(P)
    assert len(set(P)) == n
    # area and orientation
    assert all(orient(P[a], P[b], P[c]) > 0 for a, b, c in tris)
    assert sum(orient(P[a], P[b], P[c]) for a, b, c in tris) == poly_area2(boundary)
    # counts: h vertices lie on the boundary
    m = len(boundary)
    h = sum(1 for p in P if any(on_segment(boundary[i], boundary[(i + 1) % m], p) for i in range(m)))
    edges = {frozenset(e) for a, b, c in tris for e in ((a, b), (b, c), (c, a))}
    assert len(tris) == 2 * n - h - 2
    assert len(edges) == 3 * n - h - 3
    assert {v for t in tris for v in t} == set(range(n))
    if crossings:
        es = [tuple(e) for e in edges]
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                u, v = es[i]
                x, y = es[j]
                if len({u, v, x, y}) == 4:
                    assert not proper_cross(P[u], P[v], P[x], P[y])
    # segments: chains of subsegments, each one a mesh edge
    for u, v in subs:
        assert frozenset((u, v)) in edges
    total = sum(chain(P, subs, boundary[i], boundary[(i + 1) % m]) for i in range(m))
    total += sum(chain(P, subs, a, b) for a, b in segments)
    assert total == len(subs)
    for q in points:
        assert (Fraction(q[0]), Fraction(q[1])) in P
    # constrained Delaunay: no vertex visible from the centroid lies strictly inside a circumcircle
    sub_set = {frozenset(s) for s in subs}
    for a, b, c in tris:
        cc = circumcenter(P[a], P[b], P[c])
        r2 = d2(cc, P[a])
        x = ((P[a][0] + P[b][0] + P[c][0]) / 3, (P[a][1] + P[b][1] + P[c][1]) / 3)
        for k in range(n):
            if k not in (a, b, c) and d2(cc, P[k]) < r2:
                assert blocked(x, P[k], P, subs)
    # and every edge that is not a subsegment is locally Delaunay
    apex = {}
    for a, b, c in tris:
        apex[(a, b)], apex[(b, c)], apex[(c, a)] = c, a, b
    for (u, v), w in apex.items():
        x = apex.get((v, u))
        if x is not None and frozenset((u, v)) not in sub_set:
            cc = circumcenter(P[u], P[v], P[w])
            assert d2(cc, P[x]) >= d2(cc, P[u])
    # quality: R^2 <= B2 l^2, and every angle has sin^2 >= 1 / (4 B2)
    for a, b, c in tris:
        pa, pb, pc = P[a], P[b], P[c]
        r2 = d2(circumcenter(pa, pb, pc), pa)
        assert r2 <= B2 * min(d2(pa, pb), d2(pb, pc), d2(pc, pa))
        cr = orient(pa, pb, pc) ** 2
        for x, y, z in ((pa, pb, pc), (pb, pc, pa), (pc, pa, pb)):
            assert 4 * B2 * cr >= d2(x, y) * d2(x, z)
    return P, tris, subs


def test_example():
    trace = []
    P, tris, subs = chew([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(2, 1)], trace=trace)
    check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(2, 1)])
    assert len(P) == 8 and len(tris) == 8
    assert sum(len(step[4]) for step in trace if step[0] == "split") == 1


def test_plain_domains():
    for w, h in ((1, 1), (4, 1), (7, 2), (10, 3)):
        check([(0, 0), (w, 0), (w, h), (0, h)])
    check([(0, 0), (4, 0), (5, 2), (1, 2)])                         # angles of about 63.4 degrees
    check([(0, 0), (6, 0), (7, 2), (3, 6), (-1, 2)])


def test_acute_corners_with_features():
    # corners between 60 and 90 degrees, where neighboring boundary edges come close
    check([(0, 0), (8, 0), (10, 4), (2, 4)], segments=[((3, 1), (6, 3))])
    check([(0, 0), (8, 0), (10, 4), (2, 4)], points=[(Fraction(3, 2), Fraction(1, 2))])
    check([(0, 0), (6, 0), (7, 2), (3, 6), (-1, 2)], segments=[((1, 1), (5, 2))], points=[(3, 4)])


def test_segments_and_points():
    check([(0, 0), (12, 0), (12, 3), (0, 3)], segments=[((1, 1), (11, 2))])
    check([(0, 0), (8, 0), (8, 4), (0, 4)], segments=[((2, 2), (6, 2))])
    check([(0, 0), (9, 0), (9, 9), (0, 9)], segments=[((1, 1), (8, 2)), ((2, 4), (3, 8))], points=[(6, 6)])


def test_small_features():
    check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(1, Fraction(1, 5))])
    check([(0, 0), (6, 0), (6, 4), (0, 4)], segments=[((1, 1), (5, Fraction(6, 5)))], crossings=False)


def test_not_always_delaunay():
    # the output is only constrained Delaunay: a long segment hides vertices behind it
    P, tris, subs = check([(0, 0), (10, 0), (10, 4), (0, 4)], [((1, 2), (9, 2))])
    assert len(P) == 8
    bad = 0
    for a, b, c in tris:
        cc = circumcenter(P[a], P[b], P[c])
        bad += any(k not in (a, b, c) and d2(cc, P[k]) < d2(cc, P[a]) for k in range(len(P)))
    assert bad == 2


def test_random_domains():
    rng = random.Random(1993)
    done = 0
    while done < 8:
        w, h = rng.randint(3, 10), rng.randint(3, 10)
        k = rng.randint(0, 2)
        box = [(0, 0), (w, 0), (w + k, h), (k, h)]          # a parallelogram, angles at least 60 degrees
        segs = []
        for _ in range(rng.randint(0, 2)):
            a = (Fraction(rng.randint(1, 4 * w - 1), 4) + Fraction(k, 2), Fraction(rng.randint(1, 4 * h - 1), 4))
            b = (Fraction(rng.randint(1, 4 * w - 1), 4) + Fraction(k, 2), Fraction(rng.randint(1, 4 * h - 1), 4))
            segs.append((a, b))
        pts = [(Fraction(rng.randint(1, 8 * w - 1), 8) + Fraction(k, 2), Fraction(rng.randint(1, 8 * h - 1), 8))
               for _ in range(rng.randint(0, 2))]
        try:
            P, _, _ = chew(box, segs, pts)
        except ValueError:
            continue      # the random input broke a hypothesis
        check(box, segs, pts, crossings=len(P) < 40)
        done += 1


def test_larger_bound():
    check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(1, Fraction(1, 5))], B2=2)
    check([(0, 0), (9, 0), (9, 9), (0, 9)], segments=[((1, 1), (8, 2))], B2=2)


def test_rejects_inputs_outside_the_hypotheses():
    with pytest.raises(ValueError):
        chew([(0, 0), (4, 0), (5, 1)])                    # an angle below 60 degrees
    with pytest.raises(ValueError):
        chew([(0, 0), (4, 0), (4, 4), (0, 4)], B2=Fraction(6, 5))
    with pytest.raises(ValueError):
        chew([(0, 0), (4, 0), (4, 4), (0, 4)], segments=[((1, 1), (3, 3)), ((1, 3), (3, 1))])
    with pytest.raises(ValueError):
        chew([(0, 0), (4, 0), (4, 4), (0, 4)], segments=[((1, 1), (3, 3))], points=[(2, 2)])
