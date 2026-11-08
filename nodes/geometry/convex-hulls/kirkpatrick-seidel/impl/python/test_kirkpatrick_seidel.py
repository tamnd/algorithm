# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirkpatrick-seidel/. The authors are listed in prov/TZPPQ8.jsonl.

import random
from fractions import Fraction

from kirkpatrick_seidel import bridge, kirkpatrick_seidel, lower_hull, select

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
    hull = kirkpatrick_seidel(points)
    distinct = set(points)
    if not distinct:
        assert hull == []
        return
    pivot = min(distinct)
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
    assert kirkpatrick_seidel(pts) == [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
    check(pts)


def test_small_and_degenerate() -> None:
    assert kirkpatrick_seidel([]) == []
    assert kirkpatrick_seidel([(1, 1)]) == [(1, 1)]
    assert kirkpatrick_seidel([(1, 1), (1, 1)]) == [(1, 1)]
    assert kirkpatrick_seidel([(2, 3), (0, 0)]) == [(0, 0), (2, 3)]
    assert kirkpatrick_seidel([(3, 3), (1, 1), (0, 0), (2, 2)]) == [(0, 0), (3, 3)]
    assert kirkpatrick_seidel([(0, 2), (0, 0), (0, 1)]) == [(0, 0), (0, 2)]
    assert kirkpatrick_seidel([(0, 0), (2, 0), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    sq = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 1), (1, 1)]
    assert kirkpatrick_seidel(sq) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    # several farthest points on a line parallel to ab
    assert kirkpatrick_seidel([(0, 0), (4, 0), (1, -2), (3, -2), (2, -2), (2, 1)]) == [(0, 0), (1, -2), (3, -2), (4, 0), (2, 1)]
    # vertical sides at both ends
    assert kirkpatrick_seidel([(0, 0), (0, 3), (5, 0), (5, 3), (2, 1)]) == [(0, 0), (5, 0), (5, 3), (0, 3)]


def test_worst_case_parabola() -> None:
    pts = [(2**i, 4**i) for i in range(40)]
    assert kirkpatrick_seidel(pts) == pts  # every point is a vertex of the lower hull


def test_fractions_and_large_ints() -> None:
    f = Fraction
    pts = [(f(0), f(0)), (f(1, 3), f(1, 3)), (f(2, 3), f(2, 3)), (f(1), f(0))]
    assert kirkpatrick_seidel(pts) == [(f(0), f(0)), (f(1), f(0)), (f(2, 3), f(2, 3))]
    big = 10**18
    pts2 = [(0, 0), (big, big + 1), (2 * big, 2 * big + 2), (big, 0)]
    assert kirkpatrick_seidel(pts2) == [(0, 0), (big, 0), (2 * big, 2 * big + 2)]


def test_random_against_brute_force() -> None:
    rng = random.Random(1986)
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


def test_lower_hull_example() -> None:
    pts = [(0, 0), (4, 0), (2, 1), (5, 3), (2, 2), (3, 5), (0, 4), (1, 2), (2, 4), (4, 4)]
    assert lower_hull(pts) == [(0, 0), (4, 0), (5, 3)]
    assert bridge([(0, 0), (1, 2), (2, 1), (3, 5), (4, 0), (5, 3)], 2) == ((0, 0), (4, 0))


def test_select_against_sorted() -> None:
    rng = random.Random(1973)
    for _ in range(500):
        values = [rng.randint(-5, 5) for _ in range(rng.randint(1, 60))]
        k = rng.randrange(len(values))
        assert select(values, k) == sorted(values)[k]


def brute_bridge(pts: list[Point], m: int) -> tuple[Point, Point]:
    """The lower hull edge over x = m, by testing every pair against every point."""
    for l in pts:
        for r in pts:
            if l[0] <= m < r[0] and all(cross(l, r, p) >= 0 for p in pts):
                on = [p for p in pts if cross(l, r, p) == 0]
                if l == min(on) and r == max(on):
                    return l, r
    raise AssertionError("no bridge")


def test_bridge_against_brute_force() -> None:
    rng = random.Random(1986)
    for _ in range(600):
        xs = rng.sample(range(-12, 13), rng.randint(2, 14))
        r = rng.choice([2, 5, 1000])
        pts = [(x, rng.randint(-r, r)) for x in xs]
        if rng.random() < 0.2:
            pts = [(x, 2 * x + 1) for x in xs]  # all on one line
        sx = sorted(xs)
        m = rng.choice(range(sx[0], sx[-1]))
        assert bridge(pts, m) == brute_bridge(pts, m)


def test_larger_random_inputs() -> None:
    rng = random.Random(1987)
    for _ in range(40):
        n = rng.randint(20, 70)
        r = rng.choice([3, 10, 10**6])
        check([(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)])
