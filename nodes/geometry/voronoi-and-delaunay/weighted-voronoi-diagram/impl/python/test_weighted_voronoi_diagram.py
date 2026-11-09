# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-voronoi-diagram/. The authors are listed in prov/25RNN7.jsonl.

import random
from decimal import Decimal, getcontext
from fractions import Fraction

from weighted_voronoi_diagram import WeightedVoronoiDiagram, sign_root_diff

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

getcontext().prec = 80


def dec_dist(mode, q, p, w):
    d = ((Decimal(q[0].numerator) / q[0].denominator - p[0]) ** 2
         + (Decimal(q[1].numerator) / q[1].denominator - p[1]) ** 2).sqrt()
    return d - w if mode == "additive" else d / w


def check(mode, sites, rng) -> None:
    vd = WeightedVoronoiDiagram(mode)
    model = {}
    for p, w in sites:
        assert vd.insert(p, w) == (p not in model)
        model.setdefault(p, w)
    if not model:
        assert vd.nearest((0, 0)) == []
        return
    queries = [(Fraction(p[0]), Fraction(p[1])) for p in model]
    queries += [(Fraction(rng.randint(-60, 60), rng.randint(1, 4)), Fraction(rng.randint(-60, 60), rng.randint(1, 4)))
                for _ in range(8)]
    for q in queries:
        got = vd.nearest(q)
        d = {p: dec_dist(mode, q, p, w) for p, w in model.items()}
        best = min(d.values())
        near = {p for p, v in d.items() if v - best < Decimal(10) ** -60}
        assert set(got) <= near and got
        if len(near) == 1:
            assert got == list(near)
            if mode == "additive":
                assert vd.has_cell(got[0])
    for p in model:
        assert vd.has_cell(p) == (vd.nearest(p) == [p])
    items = list(model.items())
    for (p, wp), (r, wr) in zip(items, items[1:]):
        b = vd.bisector(p, r)
        i, j = vd.sites.index(p), vd.sites.index(r)
        if b[0] == "line":
            assert wp == wr
            mid = (Fraction(p[0] + r[0], 2), Fraction(p[1] + r[1], 2))
            assert vd.compare(mid, i, j) == 0
        elif b[0] == "circle":
            c, r2 = b[1], b[2]
            for q in ((Fraction(wr * p[0] + wp * r[0], wp + wr), Fraction(wr * p[1] + wp * r[1], wp + wr)),
                      (Fraction(wr * p[0] - wp * r[0], wr - wp), Fraction(wr * p[1] - wp * r[1], wr - wp))):
                assert vd.compare(q, i, j) == 0
                assert (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2 == r2
            light = p if wp < wr else r
            assert (light[0] - c[0]) ** 2 + (light[1] - c[1]) ** 2 < r2  # the lighter site is inside
        elif b[0] == "ray":
            start, end = b[1], b[2]
            for t in (0, 1, 3):
                q = (start[0] + t * (start[0] - end[0]), start[1] + t * (start[1] - end[1]))
                assert vd.compare(q, i, j) == 0
        elif b[0] == "empty":
            heavy = i if wp > wr else j
            assert not vd.has_cell(vd.sites[i + j - heavy])


def test_page_example() -> None:
    sites = [((0, 0), 3), ((8, 0), 1), ((4, 6), 2), ((1, 1), 0)]
    vd = WeightedVoronoiDiagram("additive", sites)
    assert not vd.has_cell((1, 1))
    assert vd.nearest((4, 0)) == [(0, 0)] and vd.nearest((5, 0)) == [(0, 0), (8, 0)]
    m = WeightedVoronoiDiagram("multiplicative", [((0, 0), 1), ((6, 0), 2)])
    assert m.bisector((0, 0), (6, 0)) == ("circle", (Fraction(-2), Fraction(0)), Fraction(16))
    check("additive", sites, random.Random(9))


def test_exact_roots() -> None:
    for a in range(0, 30):
        for b in range(0, 30):
            for c in range(-8, 9):
                want = (Decimal(a).sqrt() - Decimal(b).sqrt() - c)
                s = sign_root_diff(a, b, c)
                if abs(want) > Decimal(10) ** -50:
                    assert s == (1 if want > 0 else -1)
                else:
                    assert s == 0
    vd = WeightedVoronoiDiagram("additive", [((0, 0), 2), ((10, 0), 5)])
    k = 2 - 5
    assert vd.bisector((0, 0), (10, 0)) == ("hyperbola", (0, 0), (10, 0), k)
    assert vd.compare((Fraction(10 + k, 2), 0), 0, 1) == 0
    vd = WeightedVoronoiDiagram("additive", [((0, 0), 5), ((3, 0), 2)])
    assert vd.bisector((0, 0), (3, 0)) == ("ray", (3, 0), (0, 0))


def test_small_and_degenerate() -> None:
    rng = random.Random(10)
    for mode in ("additive", "multiplicative"):
        check(mode, [], rng)
        check(mode, [((1, 1), 2)], rng)
        check(mode, [((x, 0), 1 + x % 2) for x in range(5)], rng)
        check(mode, [((x, y), 1) for x in range(3) for y in range(3)], rng)
        check(mode, [((x, y), 1 + (x + y) % 3) for x in range(3) for y in range(3)], rng)
        check(mode, [(p, 2) for p in CIRCLE25] + [((0, 0), 2)], rng)
        check(mode, [((0, 0), 4), ((4, 0), 1), ((0, 0), 1)], rng)


def test_random_against_brute_force() -> None:
    rng = random.Random(1979)
    for pts in random_inputs(rng, 500):
        mode = rng.choice(("additive", "multiplicative"))
        lo = 0 if mode == "additive" else 1
        check(mode, [(p, rng.randint(lo, 6)) for p in pts[:8]], rng)
