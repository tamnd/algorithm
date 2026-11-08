# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jarvis-march/. The authors are listed in prov/JTX14G.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from jarvis_march import gift_wrapping_3d, jarvis_march, orient3

Point = tuple[int, int]
Point3 = tuple[int, int, int]


def cross(p: Point, q: Point, r: Point) -> int:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def brute_edges(points: list[Point]) -> set[tuple[Point, Point]]:
    """All directed hull edges p -> q, by checking every triple.

    p -> q is an edge when every point is left of or on the line pq, and each point on the line
    lies on the closed segment pq.
    """
    pts = sorted(set(points))
    edges = set()
    for p in pts:
        for q in pts:
            if p == q:
                continue
            ok = True
            for r in pts:
                c = cross(p, q, r)
                if c < 0 or (c == 0 and not (min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]))):
                    ok = False
                    break
            if ok:
                edges.add((p, q))
    return edges


def check(points: list[Point]) -> None:
    hull = jarvis_march(points)
    distinct = sorted(set(points))
    if len(distinct) <= 1:
        assert hull == distinct
        return
    edges = brute_edges(points)
    vertices = {v for e in edges for v in e}
    assert set(hull) == vertices and len(hull) == len(vertices)
    assert hull[0] == distinct[0]
    if len(hull) == 2:  # all points collinear
        assert edges == {(hull[0], hull[1]), (hull[1], hull[0])}
        return
    for i in range(len(hull)):
        a, b, c = hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)]
        assert (a, b) in edges
        assert cross(a, b, c) > 0  # strictly convex, counterclockwise


def test_example() -> None:
    pts = [(0, 0), (4, 0), (2, 1), (5, 3), (2, 2), (3, 5), (0, 4), (1, 2), (2, 4), (4, 4)]
    assert jarvis_march(pts) == [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
    check(pts)


def test_small_and_degenerate() -> None:
    assert jarvis_march([]) == []
    assert jarvis_march([(1, 1)]) == [(1, 1)]
    assert jarvis_march([(1, 1), (1, 1), (1, 1)]) == [(1, 1)]
    assert jarvis_march([(2, 3), (0, 0)]) == [(0, 0), (2, 3)]
    assert jarvis_march([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]
    assert jarvis_march([(0, 2), (0, 0), (0, 1)]) == [(0, 0), (0, 2)]
    assert jarvis_march([(0, 0), (2, 0), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    sq = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 1), (0, 0)]
    assert jarvis_march(sq) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert jarvis_march([(0, 0), (0, 3), (5, 0), (5, 3), (2, 1)]) == [(0, 0), (5, 0), (5, 3), (0, 3)]


def test_fractions_and_large_ints() -> None:
    f = Fraction
    pts = [(f(0), f(0)), (f(1, 3), f(1, 3)), (f(2, 3), f(2, 3)), (f(1), f(0))]
    assert jarvis_march(pts) == [(f(0), f(0)), (f(1), f(0)), (f(2, 3), f(2, 3))]
    big = 10**18
    pts2 = [(0, 0), (big, big + 1), (2 * big, 2 * big + 2), (big, 0)]
    assert jarvis_march(pts2) == [(0, 0), (big, 0), (2 * big, 2 * big + 2)]


def test_random_against_brute_force() -> None:
    rng = random.Random(1973)
    for trial in range(600):
        n = rng.randint(0, 14)
        r = rng.choice([1, 2, 3, 5, 20, 1000])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        if trial % 7 == 0 and n:
            pts += [pts[0]] * 2
        if trial % 11 == 0:
            a, b = rng.randint(-3, 3), rng.randint(-5, 5)
            pts = [(x, a * x + b) for x, _ in pts]  # all collinear
        if trial % 13 == 0:
            pts = [(y, x) for x, y in pts]  # vertical columns
        check(pts)


def brute_facets(pts: list[Point3]) -> set[tuple[int, int, int]]:
    """Facets (i, j, k), counterclockwise from outside, smallest index first, by testing every triple."""
    n = len(pts)
    out = set()
    for i, j, k in combinations(range(n), 3):
        signs = {orient3(pts[i], pts[j], pts[k], pts[r]) > 0 for r in range(n) if r not in (i, j, k)}
        if signs == {False}:
            out.add((i, j, k))
        elif signs == {True}:
            out.add((i, k, j))
    return out


def general_position(pts: list[Point3]) -> bool:
    """No four points coplanar and no three (x, y) projections collinear."""
    if any(orient3(*q) == 0 for q in combinations(pts, 4)):
        return False
    return all(cross(a[:2], b[:2], c[:2]) != 0 for a, b, c in combinations(pts, 3))


def test_3d_examples() -> None:
    tetra = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    assert gift_wrapping_3d(tetra) == brute_facets(tetra) == {(0, 2, 1), (0, 1, 3), (0, 3, 2), (1, 2, 3)}
    # an octahedron, perturbed into general position, with one inner point
    octa = [(10, 1, 0), (-10, 0, 2), (1, 10, 0), (0, -10, 1), (2, 0, 10), (0, 1, -10), (1, 2, 3)]
    assert general_position(octa)
    facets = gift_wrapping_3d(octa)
    assert facets == brute_facets(octa) and len(facets) == 8
    assert 6 not in {i for f in facets for i in f}


def test_3d_random_against_brute_force() -> None:
    rng = random.Random(1970)
    done = 0
    while done < 300:
        n = rng.randint(4, 11)
        r = rng.choice([6, 30, 1000])
        pts = [(rng.randint(-r, r), rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        if not general_position(pts):
            continue
        facets = gift_wrapping_3d(pts)
        assert facets == brute_facets(pts)
        verts = {i for f in facets for i in f}
        assert len(facets) == 2 * len(verts) - 4  # Euler for a simplicial 3-polytope
        done += 1
