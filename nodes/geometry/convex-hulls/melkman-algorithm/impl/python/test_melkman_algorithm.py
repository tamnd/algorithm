# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/melkman-algorithm/. The authors are listed in prov/ACJQR7.jsonl.

import random

from melkman_algorithm import MelkmanHull, melkman_algorithm

Point = tuple[int, int]


def cross(p: Point, q: Point, r: Point) -> int:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_segment(p: Point, q: Point, r: Point) -> bool:
    """True when r lies on the closed segment pq."""
    return cross(p, q, r) == 0 and min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def segments_meet(a: Point, b: Point, c: Point, d: Point) -> bool:
    """True when the closed segments ab and cd have a common point."""
    d1, d2, d3, d4 = cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)


def can_extend(path: list[Point], v: Point) -> bool:
    """True when path followed by v is still a simple polyline."""
    if not path:
        return True
    u = path[-1]
    if v == u:
        return False
    if len(path) >= 2:
        w = path[-2]
        # the new segment uv may touch the previous segment wu only at u
        if cross(w, u, v) == 0 and (v[0] - u[0]) * (w[0] - u[0]) + (v[1] - u[1]) * (w[1] - u[1]) > 0:
            return False
    for i in range(len(path) - 2):
        if segments_meet(path[i], path[i + 1], u, v):
            return False
    return True


def random_simple_polyline(rng: random.Random, n: int, size: int) -> list[Point]:
    path: list[Point] = []
    tries = 0
    while len(path) < n and tries < 40 * n:
        tries += 1
        v = (rng.randint(0, size), rng.randint(0, size))
        if can_extend(path, v):
            path.append(v)
    return path


def brute_edges(points: list[Point]) -> set[tuple[Point, Point]]:
    """All directed hull edges p -> q, by checking every triple."""
    pts = sorted(set(points))
    edges = set()
    for p in pts:
        for q in pts:
            if p != q and all(cross(p, q, r) > 0 or (cross(p, q, r) == 0 and on_segment(p, q, r)) for r in pts):
                edges.add((p, q))
    return edges


def check_hull(points: list[Point], hull: list[Point]) -> None:
    distinct = set(points)
    if not distinct:
        assert hull == []
        return
    assert hull[0] == min(distinct)
    if len(distinct) == 1:
        assert hull == [min(distinct)]
        return
    edges = brute_edges(points)
    vertices = {v for e in edges for v in e}
    assert set(hull) == vertices and len(hull) == len(vertices)
    if len(hull) == 2:
        assert edges == {(hull[0], hull[1]), (hull[1], hull[0])}
        return
    for i in range(len(hull)):
        a, b, c = hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)]
        assert (a, b) in edges
        assert cross(a, b, c) > 0


def test_example() -> None:
    v = [(0, 0), (6, 0), (3, 2), (2, 1), (1, 3), (5, 5), (-1, 4), (0, 2)]
    assert can_extend(v[:-1], v[-1]) and all(can_extend(v[:i], v[i]) for i in range(len(v)))
    m = MelkmanHull()
    states = []
    for p in v:
        m.add(p)
        states.append(list(m.d))
    assert states[2] == [(3, 2), (0, 0), (6, 0), (3, 2)]
    assert states[3] == states[2]  # (2, 1) is inside
    assert states[4] == [(1, 3), (0, 0), (6, 0), (3, 2), (1, 3)]
    assert states[5] == [(5, 5), (1, 3), (0, 0), (6, 0), (5, 5)]
    assert states[6] == [(-1, 4), (0, 0), (6, 0), (5, 5), (-1, 4)]
    assert states[7] == states[6]  # (0, 2) is inside a pocket
    assert melkman_algorithm(v) == [(-1, 4), (0, 0), (6, 0), (5, 5)]
    check_hull(v, melkman_algorithm(v))


def test_small_and_degenerate() -> None:
    assert melkman_algorithm([]) == []
    assert melkman_algorithm([(2, 3)]) == [(2, 3)]
    assert melkman_algorithm([(2, 3), (2, 3)]) == [(2, 3)]
    assert melkman_algorithm([(3, 3), (0, 0)]) == [(0, 0), (3, 3)]
    assert melkman_algorithm([(0, 0), (1, 1), (2, 2), (5, 5)]) == [(0, 0), (5, 5)]
    assert melkman_algorithm([(0, 2), (0, 1), (0, 0)]) == [(0, 0), (0, 2)]
    assert melkman_algorithm([(0, 0), (1, 0), (2, 0), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    assert melkman_algorithm([(0, 0), (2, 0), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    assert melkman_algorithm([(0, 0), (1, 1), (2, 0)]) == [(0, 0), (2, 0), (1, 1)]
    # repeated consecutive vertices are ignored
    assert melkman_algorithm([(0, 0), (0, 0), (2, 0), (2, 0), (1, 1), (1, 1)]) == [(0, 0), (2, 0), (1, 1)]
    # a point on a hull edge is not a vertex
    assert melkman_algorithm([(0, 0), (4, 0), (4, 4), (2, 4), (0, 4)]) == [(0, 0), (4, 0), (4, 4), (0, 4)]
    # a simple polygon given once around, clockwise
    assert melkman_algorithm([(0, 0), (0, 4), (2, 2), (4, 4), (4, 0)]) == [(0, 0), (4, 0), (4, 4), (0, 4)]


def test_spiral() -> None:
    # a square spiral winding inward: every new vertex is inside the hull of the first ones
    s = [(0, 0), (10, 0), (10, 10), (1, 10), (1, 1), (9, 1), (9, 9), (2, 9), (2, 2), (8, 2)]
    assert all(can_extend(s[:i], s[i]) for i in range(len(s)))
    assert melkman_algorithm(s) == [(0, 0), (10, 0), (10, 10), (1, 10)]
    # winding outward: every new vertex is a new hull vertex
    out = list(reversed(s))
    check_hull(out, melkman_algorithm(out))


def test_self_intersecting_input_breaks_it() -> None:
    # the last segment crosses the first one, so the precondition fails and the hull is wrong
    bad = [(0, 0), (10, 0), (5, 10), (5, 1), (5, -5)]
    assert (5, -5) not in melkman_algorithm(bad)


def test_random_polylines_against_brute_force() -> None:
    rng = random.Random(1987)
    for case in range(700):
        size = rng.choice([3, 5, 8, 20, 1000])
        n = rng.randint(1, 14)
        v = random_simple_polyline(rng, n, size)
        check_hull(v, melkman_algorithm(v))


def test_online_prefixes() -> None:
    rng = random.Random(1988)
    for case in range(250):
        size = rng.choice([4, 6, 30])
        v = random_simple_polyline(rng, rng.randint(1, 12), size)
        m = MelkmanHull()
        for i, p in enumerate(v):
            m.add(p)
            check_hull(v[: i + 1], m.hull())


def test_random_star_polygons() -> None:
    # vertices sorted by angle around an interior point form a simple polygon
    rng = random.Random(1989)
    checked = 0
    for case in range(200):
        pts = {(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(rng.randint(3, 40))}
        pts.discard((0, 0))
        quad = lambda p: (0 if p[1] > 0 or (p[1] == 0 and p[0] > 0) else 1)
        best: dict[tuple[int, int, int], Point] = {}
        for p in pts:
            from math import gcd

            g = gcd(abs(p[0]), abs(p[1]))
            best.setdefault((quad(p), p[0] // g, p[1] // g), p)
        from functools import cmp_to_key

        def by_angle(a: Point, b: Point) -> int:
            if quad(a) != quad(b):
                return quad(a) - quad(b)
            return -cross((0, 0), a, b)

        poly = sorted(best.values(), key=cmp_to_key(by_angle))
        if len(poly) < 3:
            continue
        start = rng.randrange(len(poly))
        poly = poly[start:] + poly[:start]
        if rng.random() < 0.5:
            poly.reverse()
        if not all(can_extend(poly[:i], poly[i]) for i in range(len(poly))):
            continue
        checked += 1
        check_hull(poly, melkman_algorithm(poly))
    assert checked >= 150
