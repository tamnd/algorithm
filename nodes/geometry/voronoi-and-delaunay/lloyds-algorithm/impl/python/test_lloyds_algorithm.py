# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lloyds-algorithm/. The authors are listed in prov/3SPGGR.jsonl.

import random
from fractions import Fraction

from lloyds_algorithm import centroid, energy, lloyd, moments, voronoi_cells

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


def brute_cell_contains(sites, i, q):
    d = [(q[0] - s[0]) ** 2 + (q[1] - s[1]) ** 2 for s in sites]
    return d[i] <= min(d)


def check(points, box, rng, steps=2) -> None:
    sites = [(Fraction(x), Fraction(y)) for x, y in dict.fromkeys(points)]
    x0, y0, x1, y1 = box
    if not sites:
        assert lloyd(points, box, steps) == []
        return
    cells = voronoi_cells(sites, box)
    assert sum(moments(c)[0] for c in cells) == (x1 - x0) * (y1 - y0)
    for _ in range(6):
        q = (Fraction(rng.randint(4 * x0, 4 * x1), 4), Fraction(rng.randint(4 * y0, 4 * y1), 4))
        for i, c in enumerate(cells):
            inside = all((c[k][0] - q[0]) * (c[(k + 1) % len(c)][1] - q[1]) - (c[k][1] - q[1]) * (c[(k + 1) % len(c)][0] - q[0]) >= 0
                         for k in range(len(c)))
            if inside:
                assert brute_cell_contains(sites, i, q)
    prev = energy(sites, box)
    cur = sites
    for _ in range(steps):
        cur = lloyd(cur, box, 1)
        assert all(x0 <= x <= x1 and y0 <= y <= y1 for x, y in cur)
        e = energy(cur, box)
        assert e <= prev
        prev = e
    assert lloyd(points, box, steps) == cur


def test_page_example() -> None:
    sites, box = [(0, 0), (1, 0)], (0, 0, 4, 2)
    assert lloyd(sites, box, 1) == [(Fraction(1, 4), 1), (Fraction(9, 4), 1)]
    out = lloyd(sites, box, 3)
    assert out == [(Fraction(13, 16), 1), (Fraction(45, 16), 1)]
    assert energy(out, box) == Fraction(1051, 192)
    check(sites, box, random.Random(13), steps=4)


def test_fixed_points_and_degenerate() -> None:
    rng = random.Random(14)
    grid = [(2 * x + 1, 2 * y + 1) for x in range(3) for y in range(2)]
    assert lloyd(grid, (0, 0, 6, 4), 2) == [(Fraction(x), Fraction(y)) for x, y in grid]  # a centroidal tessellation
    assert lloyd([(1, 1)], (0, 0, 4, 6), 1) == [(Fraction(2), Fraction(3))]
    assert centroid([(Fraction(0), Fraction(0)), (Fraction(3), Fraction(0)), (Fraction(0), Fraction(3))]) == (1, 1)
    check([], (0, 0, 4, 4), rng)
    check([(x, 0) for x in range(5)], (0, 0, 4, 4), rng)
    check([(x, x) for x in range(5)], (0, 0, 4, 4), rng)
    check([(x, y) for x in range(3) for y in range(3)], (0, 0, 2, 2), rng)
    check([(2, 2), (2, 2), (0, 4)], (0, 0, 4, 4), rng)


def test_random_against_brute_force() -> None:
    rng = random.Random(1957)
    for pts in random_inputs(rng, 500):
        pts = [(x % 9, y % 9) for x, y in pts[:6]]
        check(pts, (0, 0, 8, 8), rng, steps=1 + (len(set(pts)) <= 3))
