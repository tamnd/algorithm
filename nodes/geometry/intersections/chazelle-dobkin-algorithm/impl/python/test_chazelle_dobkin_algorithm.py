# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-dobkin-algorithm/. The authors are listed in prov/FCMSRJ.jsonl.

import math
import random

import pytest

from chazelle_dobkin_algorithm import Counter, chains, convex_polygons_intersect, gap_nonnegative


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def on_segment(p, a, b):
    return (cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def segments_meet(a, b, c, d):
    d1, d2, d3, d4 = cross(c, d, a), cross(c, d, b), cross(a, b, c), cross(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return on_segment(a, c, d) or on_segment(b, c, d) or on_segment(c, a, b) or on_segment(d, a, b)


def inside(p, h):
    if len(h) == 1:
        return p == h[0]
    if len(h) == 2:
        return on_segment(p, h[0], h[1])
    return all(cross(h[i], h[(i + 1) % len(h)], p) >= 0 for i in range(len(h)))


def edges(h):
    if len(h) <= 2:
        return [(h[0], h[-1])]
    return [(h[i], h[(i + 1) % len(h)]) for i in range(len(h))]


def brute(p_pts, q_pts):
    hp, hq = hull(p_pts), hull(q_pts)
    if any(inside(p, hq) for p in hp) or any(inside(q, hp) for q in hq):
        return True
    return any(segments_meet(a, b, c, d) for a, b in edges(hp) for c, d in edges(hq))


P = [(0, 0), (2, 3), (4, 4), (6, 4), (8, 3), (10, 0), (5, -2)]
Q = [(1, 8), (3, 6), (5, 5), (7, 5), (9, 7), (5, 10)]


def test_chains_of_example():
    assert chains(P) == ([(0, 0), (2, 3), (4, 4), (6, 4), (8, 3), (10, 0)], [(0, 0), (5, -2), (10, 0)])
    assert chains(Q) == ([(1, 8), (5, 10), (9, 7)], [(1, 8), (3, 6), (5, 5), (7, 5), (9, 7)])


def test_example_disjoint_then_touching():
    cp = chains(P)
    assert not convex_polygons_intersect(cp, chains(Q))
    q_down = [(x, y - 1) for x, y in Q]
    assert convex_polygons_intersect(cp, chains(q_down))
    assert gap_nonnegative(cp[0], chains(q_down)[1])
    q_down2 = [(x, y - 2) for x, y in Q]
    assert convex_polygons_intersect(cp, chains(q_down2))


def test_degenerate_shapes():
    pt = chains([(2, 2)])
    seg = chains([(0, 0), (4, 4)])
    vert = chains([(2, -1), (2, 5)])
    assert convex_polygons_intersect(pt, seg)
    assert convex_polygons_intersect(pt, vert)
    assert convex_polygons_intersect(seg, vert)
    assert not convex_polygons_intersect(chains([(3, 2)]), seg)
    assert not convex_polygons_intersect(chains([(5, 0), (5, 9)]), seg)
    square = chains([(0, 0), (2, 0), (2, 2), (0, 2)])
    assert convex_polygons_intersect(square, chains([(2, 2), (4, 4)]))
    assert convex_polygons_intersect(square, chains([(2, 1), (3, 1), (3, 5)]))
    assert not convex_polygons_intersect(square, chains([(3, 0), (3, 2), (5, 1)]))


def test_x_ranges_disjoint():
    assert not convex_polygons_intersect(chains([(0, 0), (1, 5), (1, -5)]), chains([(2, 0), (3, 1), (3, -1)]))


def random_polygon(rng, r):
    k = rng.randint(1, 9)
    ox, oy = rng.randint(-r, r), rng.randint(-r, r)
    return [(ox + rng.randint(-r, r), oy + rng.randint(-r, r)) for _ in range(k)]


def test_random_against_brute_force():
    rng = random.Random(20261109)
    hits = 0
    for _ in range(4000):
        r = rng.choice([1, 2, 3, 5, 10])
        p_pts, q_pts = random_polygon(rng, r), random_polygon(rng, r)
        want = brute(p_pts, q_pts)
        hits += want
        assert convex_polygons_intersect(chains(p_pts), chains(q_pts)) == want, (p_pts, q_pts)
        assert convex_polygons_intersect(chains(q_pts), chains(p_pts)) == want
    assert 500 < hits < 3500


def test_random_translates_touch_often():
    rng = random.Random(7)
    for _ in range(600):
        p_pts = random_polygon(rng, 4)
        hp = hull(p_pts)
        dx, dy = rng.randint(-8, 8), rng.randint(-8, 8)
        q_pts = [(x + dx, y + dy) for x, y in hp]
        assert convex_polygons_intersect(chains(p_pts), chains(q_pts)) == brute(p_pts, q_pts)


def circle_points(n, scale):
    return [(round(scale * math.cos(2 * math.pi * i / n)), round(scale * math.sin(2 * math.pi * i / n)))
            for i in range(n)]


@pytest.mark.parametrize("n", [16, 256, 4096])
def test_logarithmic_number_of_steps(n):
    big = circle_points(n, 1000 * n)
    cp = chains(big)
    for shift in range(-5, 6):
        other = chains([(x + shift * 500 * n, y + 7) for x, y in big])
        cnt = Counter()
        got = convex_polygons_intersect(cp, other, cnt)
        assert got == (abs(shift) <= 3)
        assert cnt.steps <= 40 * math.log2(n)
