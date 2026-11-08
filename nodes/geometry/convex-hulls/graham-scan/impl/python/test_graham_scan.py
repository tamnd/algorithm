# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graham-scan/. The authors are listed in prov/YMCTB9.jsonl.

import random
from fractions import Fraction

from graham_scan import graham_scan

Point = tuple[int, int]


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
    hull = graham_scan(points)
    distinct = set(points)
    if not distinct:
        assert hull == []
        return
    pivot = min(distinct, key=lambda p: (p[1], p[0]))
    assert hull[0] == pivot
    if len(distinct) == 1:
        assert hull == [pivot]
        return
    edges = brute_edges(points)
    vertices = {v for e in edges for v in e}
    assert set(hull) == vertices and len(hull) == len(vertices)
    if len(hull) == 2:  # all points collinear
        assert edges == {(hull[0], hull[1]), (hull[1], hull[0])}
        return
    for i in range(len(hull)):
        a, b, c = hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)]
        assert (a, b) in edges
        assert cross(a, b, c) > 0  # strictly convex, counterclockwise


def test_example() -> None:
    pts = [(0, 0), (4, 0), (2, 1), (5, 3), (2, 2), (3, 5), (0, 4), (1, 2), (2, 4), (4, 4)]
    assert graham_scan(pts) == [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
    check(pts)


def test_small_and_degenerate() -> None:
    assert graham_scan([]) == []
    assert graham_scan([(1, 1)]) == [(1, 1)]
    assert graham_scan([(1, 1), (1, 1)]) == [(1, 1)]
    assert graham_scan([(2, 3), (0, 0)]) == [(0, 0), (2, 3)]
    assert graham_scan([(3, 3), (1, 1), (0, 0), (2, 2)]) == [(0, 0), (3, 3)]
    assert graham_scan([(0, 2), (0, 0), (0, 1)]) == [(0, 0), (0, 2)]
    assert graham_scan([(3, 0), (1, 0), (2, 0)]) == [(1, 0), (3, 0)]
    assert graham_scan([(0, 0), (2, 0), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    # the pivot must be the leftmost of the lowest points
    assert graham_scan([(5, 0), (0, 0), (3, 0), (2, 4)]) == [(0, 0), (5, 0), (2, 4)]
    # collinear points on the first and on the last ray from the pivot
    sq = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 1), (1, 1)]
    assert graham_scan(sq) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert graham_scan([(0, 0), (1, 1), (2, 2), (2, 0), (0, 2)]) == [(0, 0), (2, 0), (2, 2), (0, 2)]


def test_fractions_and_large_ints() -> None:
    f = Fraction
    pts = [(f(0), f(0)), (f(1, 3), f(1, 3)), (f(2, 3), f(2, 3)), (f(1), f(0))]
    assert graham_scan(pts) == [(f(0), f(0)), (f(1), f(0)), (f(2, 3), f(2, 3))]
    big = 10**18
    pts2 = [(0, 0), (big, big + 1), (2 * big, 2 * big + 2), (big, 0)]
    assert graham_scan(pts2) == [(0, 0), (big, 0), (2 * big, 2 * big + 2)]


def test_random_against_brute_force() -> None:
    rng = random.Random(1972)
    for trial in range(700):
        n = rng.randint(0, 14)
        r = rng.choice([1, 2, 3, 5, 20, 1000])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        if trial % 7 == 0 and n:
            pts += [pts[0]] * 2
        if trial % 11 == 0:
            a, b = rng.randint(-3, 3), rng.randint(-5, 5)
            pts = [(x, a * x + b) for x, _ in pts]  # all collinear
        if trial % 13 == 0:
            pts = [(y, x) for x, y in pts]  # vertical lines and columns
        check(pts)
