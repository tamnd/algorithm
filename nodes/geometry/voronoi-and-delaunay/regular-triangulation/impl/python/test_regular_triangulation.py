# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regular-triangulation/. The authors are listed in prov/BBD60J.jsonl.

import random
from fractions import Fraction

from regular_triangulation import RegularTriangulation

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


def lower_value(sites, z, p, skip):
    """The height of the lower hull of the lifted sites (other than skip) above p; None outside their hull."""
    best = None
    idx = [k for k in range(len(sites)) if k != skip]
    for a in idx:
        A = sites[a]
        if A == p:
            best = z[a] if best is None else min(best, z[a])
        for b in idx:
            B = sites[b]
            if b <= a:
                continue
            if _orient(A, B, p) == 0:
                dot = (p[0] - A[0]) * (B[0] - A[0]) + (p[1] - A[1]) * (B[1] - A[1])
                ln = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2
                if 0 <= dot <= ln:
                    t = Fraction(dot, ln)
                    v = (1 - t) * z[a] + t * z[b]
                    best = v if best is None else min(best, v)
            for c in idx:
                if c <= b:
                    continue
                C = sites[c]
                det = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
                if det == 0:
                    continue
                la = Fraction((B[0] - p[0]) * (C[1] - p[1]) - (B[1] - p[1]) * (C[0] - p[0]), det)
                lb = Fraction((C[0] - p[0]) * (A[1] - p[1]) - (C[1] - p[1]) * (A[0] - p[0]), det)
                lc = 1 - la - lb
                if min(la, lb, lc) >= 0:
                    v = la * z[a] + lb * z[b] + lc * z[c]
                    best = v if best is None else min(best, v)
    return best


def check(sites) -> RegularTriangulation:
    rt = RegularTriangulation()
    model = {}
    for p, w in sites:
        assert rt.insert(p, w) == (p not in model)
        model.setdefault(p, w)
    rt.check_invariant()
    pts, ws = list(model), list(model.values())
    z = [p[0] ** 2 + p[1] ** 2 - w for p, w in zip(pts, ws)]
    tris = rt.triangles()
    n = len(pts)
    if n < 3 or all(_orient(pts[0], pts[1], p) == 0 for p in pts[2:]):
        assert tris == []
        return rt
    index = {p: i for i, p in enumerate(pts)}
    directed, used, area2 = set(), set(), 0
    for t in tris:
        a, b, c = (index[p] for p in t)
        A, B, C = t
        assert _orient(A, B, C) > 0
        area2 += (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
        for k in range(n):  # no lifted site strictly below the plane of the triangle
            m = [[pts[q][0] - pts[k][0], pts[q][1] - pts[k][1], z[q] - z[k]] for q in (a, b, c)]
            det = (m[0][2] * (m[1][0] * m[2][1] - m[2][0] * m[1][1]) + m[1][2] * (m[2][0] * m[0][1] - m[0][0] * m[2][1])
                   + m[2][2] * (m[0][0] * m[1][1] - m[1][0] * m[0][1]))
            assert det <= 0, "a lifted site is below a triangle"
        for e in ((a, b), (b, c), (c, a)):
            assert e not in directed
            directed.add(e)
        used.update((a, b, c))
    for u, v in directed:
        if (v, u) not in directed:
            assert all(_orient(pts[u], pts[v], q) >= 0 for q in pts), "border edge is not on the hull"
    hull = sorted(set(pts))
    lower, upper = [], []
    for p in hull:
        while len(lower) >= 2 and _orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(hull):
        while len(upper) >= 2 and _orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    poly = lower[:-1] + upper[:-1]
    hull2 = sum(poly[k - 1][0] * poly[k][1] - poly[k][0] * poly[k - 1][1] for k in range(len(poly)))
    assert area2 == hull2, "triangles do not tile the hull"
    for k in range(n):
        lv = lower_value(pts, z, pts[k], k)
        strict_vertex = lv is None or z[k] < lv
        above = lv is not None and z[k] > lv
        if strict_vertex:
            assert k in used, "a non-redundant site is missing"
        if above:
            assert k not in used, "a redundant site is a vertex"
    assert set(rt.vertices()) == {pts[k] for k in used}
    return rt


def test_page_example() -> None:
    sites = [((0, 0), 16), ((6, 0), 9), ((3, 5), 16), ((7, 6), 0), ((3, 2), 0)]
    rt = check(sites)
    assert rt.triangles() == [((0, 0), (6, 0), (3, 5)), ((3, 5), (6, 0), (7, 6))]
    assert rt.vertices() == [(0, 0), (3, 5), (6, 0), (7, 6)]


def test_small_and_degenerate() -> None:
    assert RegularTriangulation().triangles() == []
    check([((1, 1), 5)])
    check([((0, 0), 0), ((4, 0), 3)])
    check([((x, 0), x % 2 * 5) for x in range(6)])
    check([((0, 0), 0), ((2, 0), 9), ((4, 0), 0), ((2, 3), 0)])
    check([((0, 0), 0), ((2, 0), 0), ((4, 0), 9), ((2, 3), 0)])
    check([((0, 0), 0), ((2, 0), 0), ((4, 0), 4), ((2, 3), 0), ((6, 0), 30)])
    for w in range(2, 5):
        for h in range(2, 5):
            check([((x, y), 0) for x in range(w) for y in range(h)])
            check([((x, y), (x * y) % 3) for x in range(w) for y in range(h)])
    check([(p, 0) for p in CIRCLE25])
    check([(p, 0) for p in CIRCLE25] + [((0, 0), 0)])


def test_random_against_brute_force() -> None:
    rng = random.Random(1996)
    for pts in random_inputs(rng, 500):
        pts = pts[:8]
        check([(p, rng.choice((0, 0, rng.randint(0, 20)))) for p in pts])
