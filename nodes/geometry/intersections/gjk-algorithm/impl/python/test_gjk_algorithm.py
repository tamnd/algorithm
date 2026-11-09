# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gjk-algorithm/. The authors are listed in prov/QSXJNC.jsonl.

import random
from fractions import Fraction

import pytest

from gjk_algorithm import closest_on_simplex, gjk_distance, intersects


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


def inside(h, p):
    """p in the closed convex polygon h (ccw, at least 3 vertices)."""
    return all(cross(h[i], h[(i + 1) % len(h)], p) >= 0 for i in range(len(h)))


def pt_seg2(p, a, b):
    ab = (b[0] - a[0], b[1] - a[1])
    ap = (p[0] - a[0], p[1] - a[1])
    den = ab[0] ** 2 + ab[1] ** 2
    t = Fraction(0) if den == 0 else min(max(Fraction(ap[0] * ab[0] + ap[1] * ab[1], den), Fraction(0)), Fraction(1))
    d = (ap[0] - t * ab[0], ap[1] - t * ab[1])
    return d[0] ** 2 + d[1] ** 2


def on_seg(a, b, p):
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def seg_meet(a, b, c, d):
    d1, d2, d3, d4 = cross(c, d, a), cross(c, d, b), cross(a, b, c), cross(a, b, d)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
        return True
    return on_seg(c, d, a) or on_seg(c, d, b) or on_seg(a, b, c) or on_seg(a, b, d)


def edges(h):
    if len(h) == 1:
        return [(h[0], h[0])]
    if len(h) == 2:
        return [(h[0], h[1])]
    return [(h[i], h[(i + 1) % len(h)]) for i in range(len(h))]


def brute_dist2(p_pts, q_pts):
    hp, hq = hull(p_pts), hull(q_pts)
    if len(hq) >= 3 and any(inside(hq, p) for p in hp):
        return Fraction(0)
    if len(hp) >= 3 and any(inside(hp, q) for q in hq):
        return Fraction(0)
    best = None
    for a, b in edges(hp):
        for c, d in edges(hq):
            if seg_meet(a, b, c, d):
                return Fraction(0)
            for x in (pt_seg2(a, c, d), pt_seg2(b, c, d), pt_seg2(c, a, b), pt_seg2(d, a, b)):
                best = x if best is None else min(best, x)
    return Fraction(best)


def in_minkowski_difference(v, p_pts, q_pts):
    """v in conv(P) - conv(Q), that is conv(P) meets conv(Q) + v."""
    return brute_dist2(p_pts, [(q[0] + v[0], q[1] + v[1]) for q in q_pts]) == 0


def test_example():
    p = [(0, 0), (4, 0), (0, 4)]
    q = [(4, 3), (6, 3), (4, 5)]
    r = gjk_distance(p, q, keep_trace=True)
    assert r.dist2 == Fraction(9, 2) and r.v == (Fraction(-3, 2), Fraction(-3, 2))
    assert r.iterations == 3
    assert [t[0] for t in r.trace] == [(-4, -3), (0, -3), (Fraction(-3, 2), Fraction(-3, 2))]
    assert [t[1] for t in r.trace] == [(0, -3), (-4, 1), (0, -3)]
    assert intersects(p, [(2, 2), (4, 2), (2, 4)])  # touching at (2, 2)
    assert intersects(p, [(1, 1), (3, 1), (1, 3)])


def test_degenerate():
    with pytest.raises(ValueError):
        gjk_distance([], [(0, 0)])
    assert gjk_distance([(0, 0)], [(3, 4)]).dist2 == 25
    assert gjk_distance([(0, 0)], [(0, 0)]).dist2 == 0
    assert gjk_distance([(0, 0), (4, 0)], [(2, 0), (2, 5)]).dist2 == 0  # T junction
    assert gjk_distance([(0, 0), (4, 0)], [(5, 0), (9, 0)]).dist2 == 1  # collinear, apart
    assert gjk_distance([(0, 0), (4, 0)], [(2, 0), (6, 0)]).dist2 == 0  # collinear overlap
    assert gjk_distance([(0, 0), (4, 0), (0, 4)], [(1, 1)]).dist2 == 0  # point inside
    assert gjk_distance([(0, 0), (2, 0), (2, 2), (0, 2)], [(3, 1), (5, 1), (4, 3)]).dist2 == 1
    v, sub = closest_on_simplex([(1, 0), (2, 0), (3, 0)])  # collinear simplex
    assert v == (1, 0) and sub == [(1, 0)]


def test_random():
    rng = random.Random(77)
    worst = 0
    for case in range(1500):
        k = (2, 4, 12)[case % 3]
        np_, nq = rng.randint(1, 7), rng.randint(1, 7)
        p = [(rng.randint(-k, k), rng.randint(-k, k)) for _ in range(np_)]
        off = (rng.randint(-2 * k, 2 * k), rng.randint(-2 * k, 2 * k))
        q = [(rng.randint(-k, k) + off[0], rng.randint(-k, k) + off[1]) for _ in range(nq)]
        if case % 5 == 0:
            q = [(x, 0) for x, _ in q]  # collinear sets
        r = gjk_distance(p, q)
        assert r.dist2 == brute_dist2(p, q)
        assert r.dist2 == r.v[0] ** 2 + r.v[1] ** 2
        if case % 4 == 0:
            assert in_minkowski_difference(r.v, p, q)
        if r.dist2 > 0:  # v is a separating direction: P and Q + v are apart along v
            assert max(-r.v[0] * x - r.v[1] * y for x, y in p) <= min(-r.v[0] * x - r.v[1] * y for x, y in q) - r.dist2
        worst = max(worst, r.iterations)
    assert worst <= 15
