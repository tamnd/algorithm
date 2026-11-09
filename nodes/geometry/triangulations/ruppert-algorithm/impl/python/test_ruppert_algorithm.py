# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ruppert-algorithm/. The authors are listed in prov/A2ZJPV.jsonl.
import random
from fractions import Fraction

import pytest

from ruppert_algorithm import circumcenter, ruppert


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def incircle(a, b, c, d):
    rows = [(x[0] - d[0], x[1] - d[1]) for x in (a, b, c)]
    (ax, ay), (bx, by), (cx, cy) = rows
    return ((ax * ax + ay * ay) * (bx * cy - cx * by) - (bx * bx + by * by) * (ax * cy - cx * ay)
            + (cx * cx + cy * cy) * (ax * by - bx * ay))


def on_segment(a, b, q):
    return orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) \
        and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])


def proper_cross(a, b, c, d):
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def poly_area2(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def covered(P, subs, a, b):
    """The subsegments on the input segment ab form a chain from a to b."""
    a, b = (Fraction(a[0]), Fraction(a[1])), (Fraction(b[0]), Fraction(b[1]))
    on = [(u, v) for u, v in subs if on_segment(a, b, P[u]) and on_segment(a, b, P[v])]
    length = lambda p: (p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])  # noqa: E731
    pieces = sorted((min(length(P[u]), length(P[v])), max(length(P[u]), length(P[v]))) for u, v in on)
    assert pieces[0][0] == 0 and pieces[-1][1] == length(b)
    assert all(pieces[k][1] == pieces[k + 1][0] for k in range(len(pieces) - 1))
    return len(on)


def check(boundary, segments=(), points=(), B2=2, crossings=True):
    P, tris, subs = ruppert(boundary, segments, points, B2)
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
    # every vertex is used, edges do not cross
    assert {v for t in tris for v in t} == set(range(n))
    if crossings:
        es = [tuple(e) for e in edges]
        for i in range(len(es)):
            for j in range(i + 1, len(es)):
                u, v = es[i]
                x, y = es[j]
                if len({u, v, x, y}) == 4:
                    assert not proper_cross(P[u], P[v], P[x], P[y])
    # Delaunay: no vertex strictly inside any circumcircle
    for a, b, c in tris:
        cc = circumcenter(P[a], P[b], P[c])
        r2 = d2(cc, P[a])
        for k in range(n):
            if k not in (a, b, c):
                assert d2(cc, P[k]) >= r2
                assert incircle(P[a], P[b], P[c], P[k]) <= 0
    # quality: R^2 <= B2 l^2, and every angle has sin^2 >= 1 / (4 B2)
    for a, b, c in tris:
        pa, pb, pc = P[a], P[b], P[c]
        r2 = d2(circumcenter(pa, pb, pc), pa)
        assert r2 <= B2 * min(d2(pa, pb), d2(pb, pc), d2(pc, pa))
        cr = orient(pa, pb, pc) ** 2
        for x, y, z in ((pa, pb, pc), (pb, pc, pa), (pc, pa, pb)):
            assert 4 * B2 * cr >= d2(x, y) * d2(x, z)
    # segments: covered by subsegments that are mesh edges with empty closed diametral disks
    for u, v in subs:
        assert frozenset((u, v)) in edges
        for k in range(n):
            if k not in (u, v):
                assert (P[u][0] - P[k][0]) * (P[v][0] - P[k][0]) + (P[u][1] - P[k][1]) * (P[v][1] - P[k][1]) > 0
    total = sum(covered(P, subs, boundary[i], boundary[(i + 1) % m]) for i in range(m))
    total += sum(covered(P, subs, a, b) for a, b in segments)
    assert total == len(subs)
    for q in points:
        assert (Fraction(q[0]), Fraction(q[1])) in P
    return P, tris, subs


def test_example():
    P, tris, subs = check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(2, 1)])
    assert len(P) == 10 and len(tris) == 10 and len(subs) == 8
    assert (Fraction(39, 10), Fraction(19, 10)) in P


def test_plain_boxes():
    for w, h in ((1, 1), (4, 1), (7, 2), (10, 3)):
        check([(0, 0), (w, 0), (w, h), (0, h)])


def test_convex_polygons_with_obtuse_angles():
    check([(0, 0), (4, 0), (6, 3), (4, 6), (0, 6), (-2, 3)], segments=[((1, 2), (3, 4))])
    check([(0, 0), (4, 0), (5, 3), (2, 5), (-1, 3)], segments=[((1, 1), (3, 1))], points=[(2, 3)])


def test_segments_and_points():
    check([(0, 0), (8, 0), (8, 4), (0, 4)], segments=[((2, 2), (6, 2))])
    check([(0, 0), (8, 0), (8, 3), (0, 3)], segments=[((2, 1), (5, 2))])
    check([(0, 0), (9, 0), (9, 9), (0, 9)], segments=[((1, 1), (8, 2)), ((2, 4), (3, 8))], points=[(6, 6)])


def test_small_features():
    # a point close to the boundary forces small triangles near it
    check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(1, Fraction(1, 5))])
    check([(0, 0), (6, 0), (6, 4), (0, 4)], segments=[((1, 1), (5, Fraction(6, 5)))], crossings=False)


def test_random_domains():
    rng = random.Random(1995)
    done = 0
    while done < 12:
        w, h = rng.randint(3, 12), rng.randint(3, 12)
        segs = []
        for _ in range(rng.randint(0, 2)):
            a = (Fraction(rng.randint(1, 4 * w - 1), 4), Fraction(rng.randint(1, 4 * h - 1), 4))
            b = (Fraction(rng.randint(1, 4 * w - 1), 4), Fraction(rng.randint(1, 4 * h - 1), 4))
            segs.append((a, b))
        pts = [(Fraction(rng.randint(1, 8 * w - 1), 8), Fraction(rng.randint(1, 8 * h - 1), 8))
               for _ in range(rng.randint(0, 2))]
        try:
            P, _, _ = ruppert([(0, 0), (w, 0), (w, h), (0, h)], segs, pts)
        except ValueError:
            continue      # the random input broke a hypothesis
        check([(0, 0), (w, 0), (w, h), (0, h)], segs, pts, crossings=len(P) < 60)
        done += 1


def test_larger_bound():
    # B = 2 is also covered by the theorem, and gives coarser meshes
    check([(0, 0), (6, 0), (6, 4), (0, 4)], points=[(1, Fraction(1, 5))], B2=4)
    check([(0, 0), (9, 0), (9, 9), (0, 9)], segments=[((1, 1), (8, 2))], B2=4)


def test_rejects_inputs_outside_the_hypotheses():
    with pytest.raises(ValueError):
        ruppert([(0, 0), (4, 0), (1, 3)])                  # an acute boundary angle
    with pytest.raises(ValueError):
        ruppert([(0, 0), (4, 0), (4, 4), (0, 4)], B2=Fraction(3, 2))
    with pytest.raises(ValueError):
        ruppert([(0, 0), (4, 0), (4, 4), (0, 4)], segments=[((1, 1), (3, 3)), ((1, 3), (3, 1))])
