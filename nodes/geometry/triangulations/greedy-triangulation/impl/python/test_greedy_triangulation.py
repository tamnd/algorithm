# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-triangulation/. The authors are listed in prov/RBTAEV.jsonl.

import random
from fractions import Fraction

from greedy_triangulation import greedy_triangulation, triangles

Point = tuple[int, int]


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def hull_boundary(points):
    """All input points on the boundary of the convex hull (collinear ones included), and twice the hull area."""
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts, 0

    def chain(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and orient(out[-2], out[-1], p) < 0:
                out.pop()
            out.append(p)
        return out
    hull = chain(pts)[:-1] + chain(pts[::-1])[:-1]
    area2 = sum(hull[i][0] * hull[(i + 1) % len(hull)][1] - hull[(i + 1) % len(hull)][0] * hull[i][1]
                for i in range(len(hull)))
    return hull, area2


def candidates(points):
    n = len(points)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = points[i], points[j]
            if not any(k not in (i, j) and orient(a, b, points[k]) == 0
                       and min(a[0], b[0]) <= points[k][0] <= max(a[0], b[0])
                       and min(a[1], b[1]) <= points[k][1] <= max(a[1], b[1]) for k in range(n)):
                out.append((i, j))
    return out


def proper_cross(points, e, f):
    if set(e) & set(f):
        return False
    a, b = points[e[0]], points[e[1]]
    c, d = points[f[0]], points[f[1]]
    return orient(a, b, c) * orient(a, b, d) < 0 and orient(c, d, a) * orient(c, d, b) < 0


def check_triangulation(points, edges):
    """Brute force: no crossings, maximal, the counts 3n - h - 3 and 2n - h - 2, and the exact area sum."""
    n = len(points)
    cand = candidates(points)
    es = set(edges)
    assert len(es) == len(edges) and es <= set(cand)
    for e in edges:
        for f in edges:
            assert not proper_cross(points, e, f)
    for c in cand:
        if c not in es:
            assert any(proper_cross(points, c, e) for e in edges), c
    hull, area2 = hull_boundary(points)
    h = len(hull)
    tris = triangles(points, edges)
    if area2 == 0:
        assert len(edges) == n - 1 and tris == []
        return
    assert len(edges) == 3 * n - h - 3
    assert len(tris) == 2 * n - h - 2
    assert sum(orient(points[a], points[b], points[c]) for a, b, c in tris) == area2


def all_triangulations(points):
    """Every maximal non-crossing set of candidate segments, by branching include or exclude.
    An excluded segment must be crossed by a chosen one, so a branch dies when no later candidate can do it."""
    cand = candidates(points)
    m = len(cand)
    cross = [[proper_cross(points, cand[a], cand[b]) for b in range(m)] for a in range(m)]
    last = [max([b for b in range(m) if cross[a][b]], default=-1) for a in range(m)]
    out = []
    chosen: list = []
    pending: list = []

    def rec(k):
        for a in pending:
            if last[a] < k and not any(cross[a][b] for b in chosen):
                return
        if k == m:
            out.append([cand[b] for b in chosen])
            return
        if not any(cross[k][b] for b in chosen):
            chosen.append(k)
            rec(k + 1)
            chosen.pop()
            pending.append(k)
            rec(k + 1)
            pending.pop()
        else:
            rec(k + 1)
    rec(0)
    return out


def rank_key(points):
    def key(e):
        a, b = points[e[0]], points[e[1]]
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2, e[0], e[1])
    return key


def test_example():
    pts = [(0, 0), (5, 0), (5, 3), (0, 3), (2, 1)]
    edges = greedy_triangulation(pts)
    assert edges == [(0, 4), (3, 4), (0, 3), (1, 2), (1, 4), (2, 4), (0, 1), (2, 3)]
    check_triangulation(pts, edges)


def test_not_minimum_weight():
    pts = [(0, 4), (1, 8), (3, 0), (1, 7), (6, 0)]
    edges = greedy_triangulation(pts)
    assert edges == [(1, 3), (2, 4), (0, 3), (0, 1), (0, 2), (0, 4), (3, 4), (1, 4)]
    check_triangulation(pts, edges)
    tris = all_triangulations(pts)
    assert len(tris) == 3
    other = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4)}
    assert any(set(t) == other for t in tris)
    # the edges differ in p0p4, p3p4 (squared 52, 74) against p1p2, p2p3 (squared 68, 53);
    # sqrt 52 + sqrt 74 > sqrt 68 + sqrt 53 because both the sums and the products compare that way
    assert 52 + 74 > 68 + 53 and 52 * 74 > 68 * 53


def test_small_and_degenerate():
    assert greedy_triangulation([]) == []
    assert greedy_triangulation([(1, 1)]) == []
    assert greedy_triangulation([(0, 0), (3, 1)]) == [(0, 1)]
    line = [(0, 0), (3, 0), (1, 0), (2, 0)]
    edges = greedy_triangulation(line)
    assert sorted(edges) == [(0, 2), (1, 3), (2, 3)]
    check_triangulation(line, edges)
    grid = [(x, y) for x in range(4) for y in range(3)]
    check_triangulation(grid, greedy_triangulation(grid))
    try:
        greedy_triangulation([(0, 0), (0, 0), (1, 0)])
        assert False
    except ValueError:
        pass


def test_lexicographic_minimum_against_enumeration():
    """The greedy triangulation has the lexicographically smallest sorted edge list among all triangulations."""
    rng = random.Random(1979)
    for trial in range(300):
        n = rng.randint(3, 8)
        r = rng.choice([2, 3, 6])
        pts = list({(rng.randint(0, r), rng.randint(0, r)) for _ in range(n)})
        rng.shuffle(pts)
        edges = greedy_triangulation(pts)
        check_triangulation(pts, edges)
        key = rank_key(pts)
        best = min(sorted(key(e) for e in t) for t in all_triangulations(pts))
        assert sorted(key(e) for e in edges) == best


def test_random_larger():
    rng = random.Random(7)
    for trial in range(40):
        n = rng.randint(8, 22)
        pts = list({(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)})
        check_triangulation(pts, greedy_triangulation(pts))


def test_exact_types():
    pts = [(Fraction(1, 3), Fraction(0)), (Fraction(7, 2), Fraction(1, 5)), (Fraction(2), Fraction(9, 4)),
           (Fraction(0), Fraction(2)), (Fraction(3, 2), Fraction(1))]
    check_triangulation(pts, greedy_triangulation(pts))
    big = 10 ** 30
    pts = [(0, 0), (5 * big, 0), (5 * big, 3 * big), (0, 3 * big), (2 * big, big)]
    assert greedy_triangulation(pts) == [(0, 4), (3, 4), (0, 3), (1, 2), (1, 4), (2, 4), (0, 1), (2, 3)]
