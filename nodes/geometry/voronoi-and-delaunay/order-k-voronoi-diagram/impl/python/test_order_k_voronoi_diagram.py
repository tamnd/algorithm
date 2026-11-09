# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/order-k-voronoi-diagram/. The authors are listed in prov/93B6PD.jsonl.

import random
from fractions import Fraction

from order_k_voronoi_diagram import OrderKVoronoiDiagram

def _sign(v) -> int:
    return (v > 0) - (v < 0)


def _orient(a, b, c) -> int:
    return _sign((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def _incircle_any(a, b, c, d) -> int:
    """1 if d is strictly inside the circle through a, b, c (any orientation), 0 on it, -1 outside."""
    m = [[p[0] - d[0], p[1] - d[1]] for p in (a, b, c)]
    for r in m:
        r.append(r[0] * r[0] + r[1] * r[1])
    det = (m[0][0] * (m[1][1] * m[2][2] - m[2][1] * m[1][2])
           - m[0][1] * (m[1][0] * m[2][2] - m[2][0] * m[1][2])
           + m[0][2] * (m[1][0] * m[2][1] - m[2][0] * m[1][1]))
    return _sign(det) * _orient(a, b, c)


def brute_delaunay_triples(pts) -> set:
    """All index triples with an empty open circumdisc: the union of all Delaunay triangulations."""
    n = len(pts)
    out = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if _orient(pts[i], pts[j], pts[k]) == 0:
                    continue
                if all(_incircle_any(pts[i], pts[j], pts[k], pts[m]) <= 0 for m in range(n) if m not in (i, j, k)):
                    out.add(frozenset((i, j, k)))
    return out


def brute_hull_edges(pts) -> set:
    """Directed counterclockwise hull boundary edges, keeping every input point on the boundary."""
    out = set()
    for i, a in enumerate(pts):
        for j, b in enumerate(pts):
            if i == j:
                continue
            ok = True
            for k, c in enumerate(pts):
                if k in (i, j):
                    continue
                o = _orient(a, b, c)
                if o < 0 or (o == 0 and (c[0] - a[0]) * (c[0] - b[0]) + (c[1] - a[1]) * (c[1] - b[1]) < 0):
                    ok = False
                    break
            if ok:
                out.add((i, j))
    return out


def check_delaunay(points, triangles) -> None:
    """Assert that triangles (triples of points) is a Delaunay triangulation of the distinct input points."""
    pts = list(dict.fromkeys(points))
    index = {p: i for i, p in enumerate(pts)}
    n = len(pts)
    if n < 3 or all(_orient(pts[0], pts[1], p) == 0 for p in pts[2:]):
        assert list(triangles) == []
        return
    brute = brute_delaunay_triples(pts)
    directed = set()
    used = set()
    for t in triangles:
        a, b, c = (index[p] for p in t)
        assert _orient(pts[a], pts[b], pts[c]) > 0, "triangle not counterclockwise"
        assert frozenset((a, b, c)) in brute, "a point is inside a circumcircle"
        for e in ((a, b), (b, c), (c, a)):
            assert e not in directed, "directed edge used twice"
            directed.add(e)
        used.update((a, b, c))
    assert used == set(range(n)), "a point is not a vertex"
    hull = brute_hull_edges(pts)
    assert {(u, v) for (u, v) in directed if (v, u) not in directed} == hull, "border is not the hull"
    assert len(triangles) == 2 * n - 2 - len(hull)
    general = all(_incircle_any(pts[a], pts[b], pts[c], pts[d]) != 0
                  for a in range(n) for b in range(a + 1, n) for c in range(b + 1, n) for d in range(c + 1, n)
                  if _orient(pts[a], pts[b], pts[c]) != 0) if n <= 9 else False
    if general:
        assert {frozenset(index[p] for p in t) for t in triangles} == brute


CIRCLE25 = [(5, 0), (4, 3), (3, 4), (0, 5), (-3, 4), (-4, 3), (-5, 0), (-4, -3), (-3, -4), (0, -5), (3, -4), (4, -3)]


def random_inputs(rng, count: int):
    """Small point lists: random, grids (many cocircular points), collinear, duplicates, circles."""
    for trial in range(count):
        kind = trial % 8
        if kind == 0:
            w, h = rng.randint(1, 4), rng.randint(1, 3)
            s = rng.randint(1, 3)
            pts = [(s * x, s * y) for x in range(w) for y in range(h)]
            rng.shuffle(pts)
        elif kind == 1:
            a, b = rng.randint(-3, 3), rng.randint(-4, 4)
            pts = [(x, a * x + b) for x in (rng.randint(-6, 6) for _ in range(rng.randint(0, 7)))]
        elif kind == 2:
            pts = rng.sample(CIRCLE25, rng.randint(3, 8))
            if rng.random() < 0.5:
                pts.append((rng.randint(-2, 2), rng.randint(-2, 2)))
        else:
            r = rng.choice([1, 2, 3, 5, 40])
            pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(rng.randint(0, 10))]
        if trial % 3 == 0 and pts:
            pts += [rng.choice(pts) for _ in range(2)]
        if trial % 5 == 0:
            pts = [(y, x) for x, y in pts]
        yield pts


def k_nearest(sites, q, k):
    d = sorted(((s[0] - q[0]) ** 2 + (s[1] - q[1]) ** 2, s) for s in sites)
    unique = k == len(d) or d[k - 1][0] < d[k][0]
    return frozenset(s for _, s in d[:k]), unique


def check(points, k, box, rng) -> None:
    vd = OrderKVoronoiDiagram(k, box)
    model = []
    for p in points:
        assert vd.insert(p) == (p not in model)
        if p not in model:
            model.append(p)
    vd.check_invariant()
    cells = vd.cells()
    if len(model) < k:
        assert cells == {}
        return
    if k == len(model):
        assert list(cells) == [frozenset(model)]
    x0, y0, x1, y1 = box
    for _ in range(12):
        q = (Fraction(rng.randint(4 * x0, 4 * x1), 4) + Fraction(1, 97), Fraction(rng.randint(4 * y0, 4 * y1), 4) + Fraction(1, 89))
        if not (x0 <= q[0] <= x1 and y0 <= q[1] <= y1):
            continue
        want, unique = k_nearest(model, q, k)
        got = vd.locate(q)
        if unique:
            assert got == [want]
        else:
            assert got and all(len(g) == k for g in got)


def test_page_example() -> None:
    pts = [(0, 0), (6, 0), (3, 5), (8, 6), (1, 7)]
    vd = OrderKVoronoiDiagram(2, (-10, -10, 20, 20), pts)
    vd.check_invariant()
    assert vd.locate((Fraction(3, 1), Fraction(1, 1))) == [frozenset([(0, 0), (6, 0)])]
    check(pts, 2, (-10, -10, 20, 20), random.Random(5))
    big = (-10 ** 4, -10 ** 4, 10 ** 4, 10 ** 4)  # holds every vertex of every order for these sites
    assert [len(OrderKVoronoiDiagram(k, big, pts).cells()) for k in range(1, 6)] == [5, 8, 7, 4, 1]
    cells = OrderKVoronoiDiagram(2, big, pts).cells()
    assert frozenset([(0, 0), (8, 6)]) not in cells and frozenset([(6, 0), (1, 7)]) not in cells
    F = Fraction
    assert cells[frozenset([(3, 5), (6, 0)])] == [(3, F(8, 5)), (F(74, 11), F(-7, 11)), (F(83, 14), F(47, 14)),
                                                  (F(91, 22), F(87, 22)), (3, F(22, 7))]
    assert sorted(cells[frozenset([(0, 0), (3, 5)])]) == sorted([(F(-21, 2), F(-13, 2)), (3, F(8, 5)), (3, F(22, 7)),
                                                                 (F(-3, 8), F(29, 8))])


def test_small_and_degenerate() -> None:
    rng = random.Random(6)
    box = (-4, -4, 8, 8)
    check([], 1, box, rng)
    check([(1, 1)], 2, box, rng)
    check([(1, 1)], 1, box, rng)
    for k in (1, 2, 3):
        check([(x, 0) for x in range(4)], k, box, rng)
        check([(x, y) for x in range(3) for y in range(3)], k, box, rng)
        check([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1), (1, 1)], k, box, rng)


def test_random_against_brute_force() -> None:
    rng = random.Random(1982)
    count = 0
    for pts in random_inputs(rng, 500):
        pts = pts[:7]
        k = rng.randint(1, 3)
        check(pts, k, (-8, -8, 8, 8), rng)
        count += 1
    assert count == 500
