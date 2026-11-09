# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farthest-point-voronoi-diagram/. The authors are listed in prov/0J56YS.jsonl.

import random
from fractions import Fraction

from farthest_point_voronoi_diagram import FarthestPointVoronoiDiagram, incircle

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


def far_interval(pts, i, j):
    """Points c(t) = m + t d of the bisector of pts[i], pts[j] with no site strictly farther than pts[i]."""
    p, q = pts[i], pts[j]
    mx, my = Fraction(p[0] + q[0], 2), Fraction(p[1] + q[1], 2)
    dx, dy = -(p[1] - q[1]), p[0] - q[0]
    lo = hi = None
    for k, r in enumerate(pts):
        if k in (i, j):
            continue
        # |c - p|^2 >= |c - r|^2  <=>  2 c.(r - p) >= |r|^2 - |p|^2
        ax, ay = r[0] - p[0], r[1] - p[1]
        coef = 2 * (dx * ax + dy * ay)
        rhs = (r[0] ** 2 + r[1] ** 2 - p[0] ** 2 - p[1] ** 2) - 2 * (mx * ax + my * ay)
        if coef == 0:
            if rhs > 0:
                return None
        elif coef > 0:
            lo = rhs / coef if lo is None else max(lo, rhs / coef)
        else:
            hi = rhs / coef if hi is None else min(hi, rhs / coef)
    if lo is not None and hi is not None and lo > hi:
        return None
    return (lo, hi)


def brute_farthest(points):
    pts = list(dict.fromkeys(points))
    n = len(pts)
    edges = {}
    for i in range(n):
        for j in range(i + 1, n):
            iv = far_interval(pts, i, j)
            if iv is None or (iv[0] is not None and iv[0] == iv[1]):
                continue
            ends = [None if t is None else (Fraction(pts[i][0] + pts[j][0], 2) - t * (pts[i][1] - pts[j][1]),
                                            Fraction(pts[i][1] + pts[j][1], 2) + t * (pts[i][0] - pts[j][0]))
                    for t in iv]
            edges[frozenset((pts[i], pts[j]))] = tuple(sorted(ends, key=lambda e: (e is None, e)))
    verts = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                a, b, c = pts[i], pts[j], pts[k]
                d = 2 * ((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))
                if d == 0:
                    continue
                bx, by, cx, cy = b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1]
                v = (a[0] + Fraction(cy * (bx * bx + by * by) - by * (cx * cx + cy * cy), d),
                     a[1] + Fraction(bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by), d))
                r2 = (v[0] - a[0]) ** 2 + (v[1] - a[1]) ** 2
                if all((v[0] - s[0]) ** 2 + (v[1] - s[1]) ** 2 <= r2 for s in pts):
                    verts.add(v)
    return sorted(verts), edges


def check(pts, rng) -> None:
    fd = FarthestPointVoronoiDiagram(pts)
    verts, edges = brute_farthest(pts)
    assert fd.vertices() == verts
    assert fd.edges() == edges
    hull = fd.sites_with_cells()
    if len(hull) >= 3:
        # a tree: h cells, h - 2 vertices in general position, 2h - 3 edges
        assert len(edges) <= 2 * len(hull) - 3 and len(verts) <= len(hull) - 2
    model = list(dict.fromkeys(pts))
    for _ in range(4):
        q = (rng.randint(-30, 30), rng.randint(-30, 30))
        if model:
            best = max((s[0] - q[0]) ** 2 + (s[1] - q[1]) ** 2 for s in model)
            s = fd.farthest(q)
            assert (s[0] - q[0]) ** 2 + (s[1] - q[1]) ** 2 == best


def test_page_example() -> None:
    pts = [(0, 0), (6, 0), (6, 4), (0, 6), (3, 2)]
    fd = FarthestPointVoronoiDiagram(pts)
    assert fd.sites_with_cells() == [(0, 0), (6, 0), (6, 4), (0, 6)]
    # the fan triangle (0,0), (6,0), (6,4) has (0,6) strictly outside its circle, so the diagonal is flipped
    assert incircle((0, 0), (6, 0), (6, 4), (0, 6)) < 0
    assert fd.vertices() == [(2, 2), (3, 3)]
    assert fd.edges() == {
        frozenset({(0, 0), (6, 0)}): ((3, 3), None),
        frozenset({(0, 0), (0, 6)}): ((3, 3), None),
        frozenset({(6, 0), (6, 4)}): ((2, 2), None),
        frozenset({(6, 4), (0, 6)}): ((2, 2), None),
        frozenset({(0, 6), (6, 0)}): ((2, 2), (3, 3)),
    }
    assert fd.farthest((10, 10)) == (0, 0)
    assert fd.farthest((3, 2)) == (0, 6)
    check(pts, random.Random(3))


def test_small_and_degenerate() -> None:
    rng = random.Random(4)
    assert FarthestPointVoronoiDiagram().edges() == {}
    for pts in ([(1, 1)], [(0, 0), (4, 2)], [(x, 0) for x in range(5)], [(0, 0), (2, 0), (2, 2), (0, 2)],
                [(x, y) for x in range(4) for y in range(4)], CIRCLE25):
        check(pts, rng)


def test_random_against_brute_force() -> None:
    rng = random.Random(1975)
    for pts in random_inputs(rng, 600):
        check(pts, rng)
