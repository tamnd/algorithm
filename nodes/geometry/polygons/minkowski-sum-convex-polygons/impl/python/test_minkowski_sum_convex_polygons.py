# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minkowski-sum-convex-polygons/. The authors are listed in prov/BG3ZFX.jsonl.

import random
from fractions import Fraction
from math import gcd

import pytest

from minkowski_sum_convex_polygons import minkowski_sum_convex_polygons


def cross3(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def strict_hull(points):
    """Andrew's monotone chain without collinear points; CCW, or 1 or 2 points if degenerate."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def chain(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and cross3(out[-2], out[-1], p) <= 0:
                out.pop()
            out.append(p)
        return out

    lower, upper = chain(pts), chain(pts[::-1])
    hull = lower[:-1] + upper[:-1]
    return hull


def normalize(poly):
    if not poly:
        return poly
    k = min(range(len(poly)), key=lambda i: (poly[i][1], poly[i][0]))
    return poly[k:] + poly[:k]


def oracle(p, q):
    """Brute force: the strict convex hull of all n * m pairwise sums."""
    return normalize(strict_hull([(a[0] + b[0], a[1] + b[1]) for a in p for b in q]))


def twice_area(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def add_collinear(rng, poly):
    """Insert lattice points that lie inside edges, and sometimes repeat a vertex."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        out.append(a)
        if rng.random() < 0.3:
            out.append(a)
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dx), abs(dy))
        for k in range(1, g):
            if rng.random() < 0.5:
                out.append((a[0] + k * dx // g, a[1] + k * dy // g))
    return out


def random_convex(rng):
    kind = rng.randrange(10)
    r = rng.choice([1, 2, 4, 7])
    if kind == 0:
        return [(rng.randint(-r, r), rng.randint(-r, r))]
    if kind == 1:
        a = (rng.randint(-r, r), rng.randint(-r, r))
        b = (rng.randint(-r, r), rng.randint(-r, r))
        if rng.random() < 0.5:
            m = ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2) if (a[0] + b[0]) % 2 == 0 and (a[1] + b[1]) % 2 == 0 else a
            return [a, m, b] if rng.random() < 0.5 else [a, m, b, m]
        return [a, b]
    pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(rng.randint(1, 12))]
    hull = strict_hull(pts)
    if len(hull) >= 3 and rng.random() < 0.5:
        hull = add_collinear(rng, hull)
    k = rng.randrange(len(hull))
    return hull[k:] + hull[:k]


def test_example() -> None:
    p = [(0, 0), (2, 0), (0, 2)]
    q = [(4, 2), (3, 2), (3, 1), (4, 1)]  # a unit square, given from another start vertex
    got = minkowski_sum_convex_polygons(p, q)
    assert got == [(3, 1), (6, 1), (6, 2), (4, 4), (3, 4)]
    assert got == oracle(p, q)


def test_degenerate_inputs() -> None:
    assert minkowski_sum_convex_polygons([(1, 2)], [(3, 4)]) == [(4, 6)]
    assert minkowski_sum_convex_polygons([(0, 0), (2, 1)], [(5, 5)]) == [(5, 5), (7, 6)]
    # two parallel segments give a segment
    assert minkowski_sum_convex_polygons([(0, 0), (2, 2)], [(1, 1), (0, 0)]) == [(0, 0), (3, 3)]
    # two crossing segments give a parallelogram
    assert minkowski_sum_convex_polygons([(0, 0), (2, 0)], [(0, 0), (0, 3)]) == [(0, 0), (2, 0), (2, 3), (0, 3)]
    # collinear and repeated vertices in the input
    sq = [(0, 0), (1, 0), (2, 0), (2, 0), (2, 2), (0, 2), (0, 1)]
    assert minkowski_sum_convex_polygons(sq, [(0, 0)]) == [(0, 0), (2, 0), (2, 2), (0, 2)]
    # fractions
    tri = [(Fraction(0), Fraction(0)), (Fraction(1, 2), Fraction(0)), (Fraction(0), Fraction(1, 3))]
    assert minkowski_sum_convex_polygons(tri, tri) == [(0, 0), (1, 0), (0, Fraction(2, 3))]
    with pytest.raises(ValueError):
        minkowski_sum_convex_polygons([], [(0, 0)])


def test_sum_with_itself_and_reflection() -> None:
    p = [(0, 0), (3, 1), (2, 3)]
    assert minkowski_sum_convex_polygons(p, p) == [(0, 0), (6, 2), (4, 6)]
    neg = [(-x, -y) for x, y in p]
    s = minkowski_sum_convex_polygons(p, neg)
    assert s == oracle(p, neg)
    assert len(s) == 6  # a triangle plus its reflection is a centrally symmetric hexagon


def test_random_pairs() -> None:
    rng = random.Random(20261109)
    for _ in range(1500):
        p, q = random_convex(rng), random_convex(rng)
        got = minkowski_sum_convex_polygons(p, q)
        want = oracle(p, q)
        assert got == want, (p, q, got, want)
        if len(got) >= 3:
            hp, hq = strict_hull(p), strict_hull(q)
            area_p = twice_area(hp) if len(hp) >= 3 else 0
            area_q = twice_area(hq) if len(hq) >= 3 else 0
            assert twice_area(got) >= area_p + area_q  # Brunn-Minkowski in the plane, weak form
        assert minkowski_sum_convex_polygons(q, p) == got  # commutative


def test_linear_size() -> None:
    rng = random.Random(5)
    for _ in range(20):
        p = strict_hull([(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(60)])
        q = strict_hull([(rng.randint(-50, 50), rng.randint(-50, 50)) for _ in range(60)])
        got = minkowski_sum_convex_polygons(p, q)
        assert len(got) <= len(p) + len(q)
        assert got == oracle(p, q)
