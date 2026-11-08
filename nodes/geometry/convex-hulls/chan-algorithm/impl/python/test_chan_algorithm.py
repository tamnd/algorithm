# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chan-algorithm/. The authors are listed in prov/9RN5KZ.jsonl.

import random
from fractions import Fraction

from chan_algorithm import chan_algorithm, tangent, upper_chain

Point = tuple[int, int]


def cross(p: Point, q: Point, r: Point) -> int:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def brute_edges(points: list[Point]) -> set[tuple[Point, Point]]:
    """Directed hull edges p -> q by checking every triple: all points on or left of pq,
    and the points on the line pq lie on the closed segment."""
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
    hull = chan_algorithm(points)
    distinct = sorted(set(points))
    if len(distinct) <= 2:
        assert hull == distinct
        return
    edges = brute_edges(points)
    vertices = {v for e in edges for v in e}
    assert set(hull) == vertices and len(hull) == len(vertices)
    assert hull[0] == distinct[0]
    if len(hull) == 2:
        return
    for i in range(len(hull)):
        a, b, c = hull[i], hull[(i + 1) % len(hull)], hull[(i + 2) % len(hull)]
        assert (a, b) in edges and cross(a, b, c) > 0


def test_example() -> None:
    pts = [(0, 0), (6, 1), (3, 3), (9, 4), (1, 6), (5, 7), (8, 8), (2, 2), (4, 5), (7, 3), (3, 9), (6, 5)]
    assert chan_algorithm(pts) == [(0, 0), (6, 1), (9, 4), (8, 8), (3, 9), (1, 6)]
    check(pts)


def test_edges() -> None:
    assert chan_algorithm([]) == []
    assert chan_algorithm([(3, 3), (3, 3)]) == [(3, 3)]
    assert chan_algorithm([(1, 0), (0, 0)]) == [(0, 0), (1, 0)]
    assert chan_algorithm([(0, 0), (1, 1), (2, 2), (5, 5), (3, 3)]) == [(0, 0), (5, 5)]
    assert chan_algorithm([(0, 0), (0, 1), (0, 2)]) == [(0, 0), (0, 2)]
    assert chan_algorithm([(0, 0), (0, 3), (5, 0), (5, 3), (2, 1)]) == [(0, 0), (5, 0), (5, 3), (0, 3)]
    f = Fraction
    assert chan_algorithm([(f(0), f(0)), (f(1, 2), f(1, 2)), (f(1), f(0)), (f(1, 2), f(1, 4))]) == [(f(0), f(0)), (f(1), f(0)), (f(1, 2), f(1, 2))]


def test_tangent_against_scan() -> None:
    rng = random.Random(77)
    for _ in range(600):
        pts = list({(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(rng.randint(1, 12))})
        chain = upper_chain(pts)
        p = (rng.randint(-8, 8), rng.randint(-8, 8))
        cands = [c for c in chain if c > p]
        got = tangent(chain, p)
        if not cands:
            assert got is None
            continue
        best = cands[0]
        for c in cands[1:]:
            o = cross(p, best, c)
            if o > 0 or (o == 0 and (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2 > (best[0] - p[0]) ** 2 + (best[1] - p[1]) ** 2):
                best = c
        assert got == best


def test_random_against_brute_force() -> None:
    rng = random.Random(9031)
    for trial in range(600):
        n = rng.randint(0, 18)
        r = rng.choice([1, 2, 4, 30, 10**6])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        if trial % 9 == 0:
            pts = [(x, 2 * x - 1) for x, _ in pts]
        check(pts)


def test_larger_inputs() -> None:
    rng = random.Random(5)
    for n in (60, 120):
        pts = [(rng.randint(-40, 40), rng.randint(-40, 40)) for _ in range(n)]
        check(pts)
    # many points on a circle-like convex curve: h is about n
    pts = [(x, x * x) for x in range(-30, 31)]
    hull = chan_algorithm(pts)
    assert len(hull) == 61
