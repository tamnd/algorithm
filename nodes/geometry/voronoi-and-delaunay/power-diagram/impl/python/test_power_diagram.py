# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-diagram/. The authors are listed in prov/N5KV10.jsonl.

import random
from fractions import Fraction

from power_diagram import PowerDiagram, point_in_convex, power

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


def brute_redundant(sites, weights, i):
    """Site i is redundant iff its lifted point (p, |p|^2 - w) lies on or above the lower hull of the others."""
    p = sites[i]
    z = lambda k: sites[k][0] ** 2 + sites[k][1] ** 2 - weights[k]
    others = [k for k in range(len(sites)) if k != i]
    for a in others:
        for b in others:
            for c in others:
                A, B, C = sites[a], sites[b], sites[c]
                det = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])
                if det != 0:
                    lb = Fraction((B[0] - p[0]) * (C[1] - p[1]) - (B[1] - p[1]) * (C[0] - p[0]), det)
                    lc = Fraction((C[0] - p[0]) * (A[1] - p[1]) - (C[1] - p[1]) * (A[0] - p[0]), det)
                    la = 1 - lb - lc
                    if min(lb, lc, la) >= 0 and lb * z(a) + lc * z(b) + la * z(c) <= z(i):
                        return True
                elif a != b and (A[0] - p[0]) * (B[1] - p[1]) - (A[1] - p[1]) * (B[0] - p[0]) == 0:
                    # p on the segment AB
                    dot = (p[0] - A[0]) * (B[0] - A[0]) + (p[1] - A[1]) * (B[1] - A[1])
                    ln = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2
                    if 0 <= dot <= ln:
                        t = Fraction(dot, ln)
                        if (1 - t) * z(a) + t * z(b) <= z(i):
                            return True
    return False


def check(sites, rng) -> None:
    pd = PowerDiagram()
    model = {}
    for p, w in sites:
        assert pd.insert(p, w) == (p not in model)
        model.setdefault(p, w)
    pd.check_invariant()
    pts, ws = list(model), list(model.values())
    cells = pd.cells()
    for i, p in enumerate(pts):
        assert pd.is_redundant(p) == brute_redundant(pts, ws, i)
    x0, y0, x1, y1 = pd.box
    for p, (poly, bounded) in cells.items():
        for v in poly:  # every corner has p among its sites of least power
            assert p in pd.locate(v)
    for _ in range(10):
        q = (Fraction(rng.randint(-60, 60), 3) + Fraction(1, 101), Fraction(rng.randint(-60, 60), 3) + Fraction(1, 103))
        got = pd.locate(q)
        if pts:
            best = min(power(q, p, w) for p, w in model.items())
            assert all(power(q, s, model[s]) == best for s in got)
        if len(got) == 1 and x0 < q[0] < x1 and y0 < q[1] < y1:
            assert point_in_convex(cells[got[0]][0], q) == 1
    for v in pd.vertices():
        assert len(pd.locate(v)) >= 3


def test_page_example() -> None:
    sites = [((0, 0), 16), ((6, 0), 9), ((3, 5), 16), ((7, 6), 0), ((3, 2), 0)]
    pd = PowerDiagram(sites)
    assert pd.is_redundant((3, 2))
    assert sorted(pd.cells()) == [(0, 0), (3, 5), (6, 0), (7, 6)]
    assert pd.vertices() == [(Fraction(43, 12), Fraction(5, 4)), (Fraction(172, 23), Fraction(165, 46))]
    assert pd.locate((3, 2)) == [(3, 5)]  # power -7 at the redundant site, which has power 0 there
    assert pd.locate((Fraction(43, 12), Fraction(5, 4))) == [(0, 0), (6, 0), (3, 5)]
    assert all(not bounded for _, bounded in pd.cells().values())
    check(sites, random.Random(7))


def test_small_and_degenerate() -> None:
    rng = random.Random(8)
    pd = PowerDiagram()
    assert pd.cells() == {} and pd.locate((0, 0)) == []
    check([((1, 1), 5)], rng)
    check([((0, 0), 0), ((4, 0), 0)], rng)
    check([((0, 0), 0), ((4, 0), 20)], rng)
    check([((0, 0), 0), ((4, 0), 16)], rng)
    check([((x, 0), x * x) for x in range(5)], rng)
    check([((x, y), 0) for x in range(3) for y in range(3)], rng)
    check([((x, y), (x + y) % 3) for x in range(3) for y in range(3)], rng)
    check([(p, 0) for p in CIRCLE25], rng)
    check([((0, 0), 1), ((0, 0), 9), ((2, 2), 1)], rng)


def test_random_against_brute_force() -> None:
    rng = random.Random(1987)
    for pts in random_inputs(rng, 500):
        pts = pts[:7]
        check([(p, rng.randint(0, 12)) for p in pts], rng)
