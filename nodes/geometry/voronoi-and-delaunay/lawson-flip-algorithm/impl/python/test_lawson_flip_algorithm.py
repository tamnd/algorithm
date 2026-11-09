# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lawson-flip-algorithm/. The authors are listed in prov/024GPG.jsonl.

import random

from lawson_flip_algorithm import lawson_flip, sweep_triangulation

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


def test_page_example() -> None:
    pts = [(1, 2), (0, 6), (2, 0), (8, 5), (8, 1), (4, 0)]
    start = sweep_triangulation(pts)
    assert sorted(tuple(pts[i] for i in t) for t in start) == [
        ((0, 6), (1, 2), (2, 0)), ((0, 6), (2, 0), (4, 0)), ((0, 6), (4, 0), (8, 1)), ((0, 6), (8, 1), (8, 5))]
    tris = lawson_flip(pts)
    assert tris == [((0, 6), (1, 2), (8, 5)), ((1, 2), (2, 0), (4, 0)), ((1, 2), (4, 0), (8, 5)), ((4, 0), (8, 1), (8, 5))]
    check_delaunay(pts, tris)
    old = [(0, 0), (4, 0), (8, 0), (2, 3), (6, 3), (4, 6)]
    check_delaunay(old, lawson_flip(old))


def test_sweep_triangulation_is_a_triangulation() -> None:
    rng = random.Random(77)
    for pts in random_inputs(rng, 200):
        d = list(dict.fromkeys(pts))
        tris = sweep_triangulation(d)
        if len(d) < 3 or all(_orient(d[0], d[1], p) == 0 for p in d[2:]):
            assert tris == []
            continue
        hull = brute_hull_edges(d)
        assert len(tris) == 2 * len(d) - 2 - len(hull)
        directed = set()
        for a, b, c in tris:
            assert _orient(d[a], d[b], d[c]) > 0
            directed |= {(a, b), (b, c), (c, a)}
        assert len(directed) == 3 * len(tris)
        assert {(u, v) for u, v in directed if (v, u) not in directed} == hull


def test_small_and_degenerate() -> None:
    assert lawson_flip([]) == []
    assert lawson_flip([(0, 0), (0, 0)]) == []
    assert lawson_flip([(0, 0), (1, 1), (2, 2)]) == []
    assert lawson_flip([(0, 0), (0, 3), (0, 1), (0, 2)]) == []
    for w in range(1, 5):
        for h in range(1, 5):
            grid = [(x, y) for x in range(w) for y in range(h)]
            check_delaunay(grid, lawson_flip(grid))


def test_random_against_brute_force() -> None:
    rng = random.Random(1977)
    for pts in random_inputs(rng, 600):
        check_delaunay(pts, lawson_flip(pts))
