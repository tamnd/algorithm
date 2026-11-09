# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fortunes-algorithm/. The authors are listed in prov/A89AWB.jsonl.

import random
from fractions import Fraction

from fortunes_algorithm import Event, breakpoint_side, fortune, sign_plus_root

def bisector_interval(pts, i, j):
    """Points c(t) = m + t d of the bisector of pts[i] and pts[j] (m the midpoint, d = (pts[i] - pts[j]) turned
    by 90 degrees) that no site is strictly closer to: a closed interval (lo, hi), None for an infinite end,
    or None if it is empty. Exact, with Fraction."""
    p, q = pts[i], pts[j]
    mx, my = Fraction(p[0] + q[0], 2), Fraction(p[1] + q[1], 2)
    dx, dy = -(p[1] - q[1]), p[0] - q[0]
    lo = hi = None
    for k, r in enumerate(pts):
        if k in (i, j):
            continue
        ax, ay = r[0] - p[0], r[1] - p[1]
        coef = 2 * (dx * ax + dy * ay)
        rhs = (r[0] ** 2 + r[1] ** 2 - p[0] ** 2 - p[1] ** 2) - 2 * (mx * ax + my * ay)
        if coef == 0:
            if rhs < 0:
                return None
        elif coef > 0:
            hi = rhs / coef if hi is None else min(hi, rhs / coef)
        else:
            lo = rhs / coef if lo is None else max(lo, rhs / coef)
    if lo is not None and hi is not None and lo > hi:
        return None
    return (lo, hi)


def bisector_point(pts, i, j, t):
    p, q = pts[i], pts[j]
    return (Fraction(p[0] + q[0], 2) - t * (p[1] - q[1]), Fraction(p[1] + q[1], 2) + t * (p[0] - q[0]))


def brute_voronoi(points):
    """Vertices (sorted list of exact points) and edges {frozenset({p, q}): sorted pair of ends, None = infinity}
    of the Voronoi diagram, from the definition: an edge for each pair whose bisector part has positive length,
    a vertex for each point equidistant from three or more sites with no site closer."""
    pts = list(dict.fromkeys(points))
    n = len(pts)
    edges = {}
    for i in range(n):
        for j in range(i + 1, n):
            iv = bisector_interval(pts, i, j)
            if iv is None or (iv[0] is not None and iv[0] == iv[1]):
                continue
            ends = [None if t is None else bisector_point(pts, i, j, t) for t in iv]
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
                if all((v[0] - s[0]) ** 2 + (v[1] - s[1]) ** 2 >= r2 for s in pts):
                    verts.add(v)
    return sorted(verts), edges

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


def same_as_brute(pts) -> None:
    assert fortune(pts) == brute_voronoi(pts)


def test_page_example() -> None:
    pts = [(2, 8), (6, 7), (0, 4), (4, 5), (8, 3), (3, 0)]
    vertices, edges = fortune(pts)
    same_as_brute(pts)
    F = Fraction
    assert vertices == [(F(12, 7), F(79, 14)), (F(93, 38), F(103, 38)), (F(39, 10), F(71, 10)),
                        (F(56, 11), F(24, 11)), (F(19, 3), F(14, 3))]
    assert len(edges) == 10 and edges[frozenset([(2, 8), (6, 7)])] == ((F(39, 10), F(71, 10)), None)
    same_as_brute([(2, 8), (6, 7), (0, 4), (4, 4), (8, 3), (3, 0)])


def test_exact_helpers() -> None:
    assert sign_plus_root(-3, 1, 9) == 0 and sign_plus_root(-3, 1, 10) == 1 and sign_plus_root(3, -1, 8) == 1
    assert sign_plus_root(0, -2, 5) == -1 and sign_plus_root(-1, 0, 7) == -1
    # p = (0, 2), q = (4, 1), sweep at y = 0: the breakpoint is 8 - 34^(1/2), about 2.17
    assert breakpoint_side(2, (0, 2), (4, 1), 0) == -1 and breakpoint_side(3, (0, 2), (4, 1), 0) == 1
    # with q on the left the breakpoint is 8 + 34^(1/2), about 13.83
    assert breakpoint_side(13, (4, 1), (0, 2), 0) == -1 and breakpoint_side(14, (4, 1), (0, 2), 0) == 1
    # a circle event at y = 3 - 2 = 1 comes before a site at y = 0 and after a site at y = 2
    e = Event(Fraction(3), Fraction(4), Fraction(0), 0, 0)
    assert e < Event(0, 0, 0, 1, 1) and Event(2, 0, 0, 1, 2) < e


def test_small_and_degenerate() -> None:
    assert fortune([]) == ([], {})
    assert fortune([(1, 1), (1, 1)]) == ([], {})
    v, e = fortune([(0, 0), (2, 0)])
    assert v == [] and e == {frozenset([(0, 0), (2, 0)]): (None, None)}
    for pts in ([(x, 0) for x in range(5)], [(0, y) for y in range(5)], [(x, x) for x in range(5)],
                [(0, 0), (2, 0), (1, 1)], [(0, 0), (2, 0), (1, 5), (1, -5)]):
        same_as_brute(pts)
    for w in range(1, 5):
        for h in range(1, 5):
            same_as_brute([(x, y) for x in range(w) for y in range(h)])
    same_as_brute(CIRCLE25)
    same_as_brute(CIRCLE25 + [(0, 0)])


def test_random_against_brute_force() -> None:
    rng = random.Random(1987)
    for pts in random_inputs(rng, 600):
        same_as_brute(pts)
