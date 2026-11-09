# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polygon-triangulation-dp/. The authors are listed in prov/2ZMWQH.jsonl.

import random
from fractions import Fraction
from math import comb

from polygon_triangulation_dp import count_triangulations, optimal_triangulation



def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_closed_segment(p, a, b):
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet_badly(a, b, c, d):
    """True when segments ab and cd share a point that is not a common endpoint."""
    shared = {a, b} & {c, d}
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    for p, s, t in ((c, a, b), (d, a, b), (a, c, d), (b, c, d)):
        if p not in shared and on_closed_segment(p, s, t):
            return True
    if len(shared) == 1 and o1 == 0 and o2 == 0:  # collinear and sharing one endpoint: overlap?
        s = shared.pop()
        u = b if a == s else a
        w = d if c == s else c
        if (u[0] - s[0]) * (w[0] - s[0]) + (u[1] - s[1]) * (w[1] - s[1]) > 0:
            return True
    return False


def twice_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def is_simple(poly):
    n = len(poly)
    if n < 3 or len(set(poly)) != n:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if segments_meet_badly(a, b, c, d):
                return False
    return twice_area(poly) != 0


def point_in_polygon(p, poly):
    """1 strictly inside, 0 on the boundary, -1 outside. Exact (crossing number)."""
    n = len(poly)
    inside = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_closed_segment(p, a, b):
            return 0
        if (a[1] > p[1]) != (b[1] > p[1]):
            # x of the crossing compared with p[0], without division
            o = orient(a, b, p)
            if (o > 0) == (b[1] > a[1]):
                inside = not inside
    return 1 if inside else -1


def check_polygon_triangulation(poly, tris):
    """tris are index triples into poly. Checks the count, orientation, area, no crossings, inside."""
    n = len(poly)
    if n < 3:
        assert tris == []
        return
    assert len(tris) == n - 2
    sign = 1 if twice_area(poly) > 0 else -1
    tot = 0
    edges = set()
    for t in tris:
        assert len(set(t)) == 3
        a, b, c = (poly[i] for i in t)
        o = orient(a, b, c)
        assert o != 0
        tot += abs(o)
        for i, j in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges.add((min(i, j), max(i, j)))
        for k in range(n):
            if k not in t:
                p = poly[k]
                o1, o2, o3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
                assert not ((o1 > 0 and o2 > 0 and o3 > 0) or (o1 < 0 and o2 < 0 and o3 < 0))
    assert tot == abs(twice_area(poly))
    assert len({tuple(sorted(t)) for t in tris}) == len(tris)
    el = sorted(edges)
    assert len(el) == 2 * n - 3
    for x in range(len(el)):
        i, j = el[x]
        for y in range(x + 1, len(el)):
            k, m = el[y]
            assert not segments_meet_badly(poly[i], poly[j], poly[k], poly[m])
        if (j - i) % n not in (1, n - 1):  # a diagonal: its midpoint must be strictly inside
            mid = (poly[i][0] + poly[j][0], poly[i][1] + poly[j][1])
            assert point_in_polygon(mid, [(2 * x0, 2 * y0) for x0, y0 in poly]) == 1
            for k in range(n):
                a, b = poly[k], poly[(k + 1) % n]
                assert not segments_meet_badly(poly[i], poly[j], a, b)
    _ = sign


def random_simple_polygon(rng, n, r):
    """Grow a simple polygon from a triangle by replacing an edge ab with a, p, b."""
    while True:
        tri = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(3)]
        if orient(*tri) != 0:
            break
    poly = tri if orient(*tri) > 0 else tri[::-1]
    tries = 0
    while len(poly) < n and tries < 60 * n:
        tries += 1
        p = (rng.randint(-r, r), rng.randint(-r, r))
        if p in poly:
            continue
        i = rng.randrange(len(poly))
        cand = poly[: i + 1] + [p] + poly[i + 1:]
        if is_simple(cand):
            poly = cand
    if rng.random() < 0.5:
        poly = poly[::-1]
    k = rng.randrange(len(poly))
    return poly[k:] + poly[:k]


def all_triangulations(poly):
    """Brute force: every set of n - 3 pairwise non-crossing diagonals, as triangle lists."""
    n = len(poly)
    big = [(2 * x, 2 * y) for x, y in poly]
    diags = []
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            if any(segments_meet_badly(poly[i], poly[j], poly[k], poly[(k + 1) % n]) for k in range(n)):
                continue
            mid = (poly[i][0] + poly[j][0], poly[i][1] + poly[j][1])
            if point_in_polygon(mid, big) == 1:
                diags.append((i, j))
    out = []

    def rec(start, chosen):
        if len(chosen) == n - 3:
            edges = {(i, (i + 1) % n) for i in range(n)} | set(chosen)
            edges = {(min(e), max(e)) for e in edges}
            tris = []
            for a in range(n):
                for b in range(a + 1, n):
                    for c in range(b + 1, n):
                        if (a, b) in edges and (b, c) in edges and (a, c) in edges:
                            tris.append((a, b, c))
            out.append(tris)
            return
        for t in range(start, len(diags)):
            d = diags[t]
            if all(not segments_meet_badly(poly[d[0]], poly[d[1]], poly[e[0]], poly[e[1]]) for e in chosen):
                chosen.append(d)
                rec(t + 1, chosen)
                chosen.pop()

    rec(0, [])
    return out


def random_weight(rng):
    table = {}

    def w(a, b, c):
        key = tuple(sorted((a, b, c)))
        if key not in table:
            table[key] = rng.randint(0, 50)
        return table[key]
    return w


def sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def perimeter_sq(poly):
    return lambda a, b, c: sq(poly[a], poly[b]) + sq(poly[b], poly[c]) + sq(poly[c], poly[a])


def check_result(poly, weight, cost, tris):
    check_polygon_triangulation(poly, tris)
    for a, b, c in tris:
        assert orient(poly[a], poly[b], poly[c]) > 0
    assert cost == sum(weight(*t) for t in tris)


def test_example():
    poly = [(0, 0), (6, 0), (6, 4), (4, 4), (3, 1), (2, 4), (0, 4)]
    w = perimeter_sq(poly)
    cost, tris = optimal_triangulation(poly, w)
    check_result(poly, w, cost, tris)
    assert count_triangulations(poly) == 4
    assert cost == 2 * 56 + 96  # twice the squared diagonal lengths plus the squared side lengths
    assert sorted(tuple(sorted(t)) for t in tris) == [(0, 1, 4), (0, 4, 6), (1, 2, 4), (2, 3, 4), (4, 5, 6)]


def test_small_cases():
    assert optimal_triangulation([(0, 0), (1, 0)], perimeter_sq([(0, 0), (1, 0)])) == (0, [])
    tri = [(0, 0), (4, 0), (0, 3)]
    assert optimal_triangulation(tri, perimeter_sq(tri)) == (16 + 25 + 9, [(0, 1, 2)])
    assert count_triangulations(tri) == 1
    cw = tri[::-1]
    cost, tris = optimal_triangulation(cw, perimeter_sq(cw))
    assert cost == 50 and len(tris) == 1
    flat = [(0, 0), (1, 0), (2, 0), (1, 2)]
    assert count_triangulations(flat) == 1
    cost, tris = optimal_triangulation(flat, perimeter_sq(flat))
    check_result(flat, perimeter_sq(flat), cost, tris)
    try:
        optimal_triangulation([(0, 0), (1, 1), (2, 2)], perimeter_sq([(0, 0), (1, 1), (2, 2)]))
    except ValueError:
        pass
    else:
        raise AssertionError("a flat polygon must be rejected")


def test_convex_catalan():
    for n in range(3, 13):
        poly = [(0, 0)] + [(k, k * k) for k in range(1, n)]
        poly = [poly[0]] + sorted(poly[1:], key=lambda p: -p[0])
        poly = [(x, y) for x, y in poly]
        poly = list(reversed(poly)) if twice_area(poly) < 0 else poly
        assert count_triangulations(poly) == comb(2 * n - 4, n - 2) // (n - 1)


def test_against_enumeration():
    rng = random.Random(1979)
    checked = 0
    for trial in range(300):
        n = rng.randint(3, 9)
        poly = random_simple_polygon(rng, n, rng.choice([3, 5, 12]))
        n = len(poly)
        alls = all_triangulations(poly)
        assert len(alls) == count_triangulations(poly)
        for w in (random_weight(rng), perimeter_sq(poly)):
            cost, tris = optimal_triangulation(poly, w)
            check_result(poly, w, cost, tris)
            assert cost == min(sum(w(*t) for t in ts) for ts in alls)
        checked += 1
    assert checked == 300


def test_fractions_and_large():
    poly = [(Fraction(0), Fraction(0)), (Fraction(5, 2), Fraction(0)), (Fraction(5, 2), Fraction(7, 3)), (Fraction(1, 3), Fraction(1, 2)), (Fraction(0), Fraction(2))]
    w = perimeter_sq(poly)
    cost, tris = optimal_triangulation(poly, w)
    check_result(poly, w, cost, tris)
    rng = random.Random(7)
    poly = random_simple_polygon(rng, 30, 40)
    w = perimeter_sq(poly)
    cost, tris = optimal_triangulation(poly, w)
    check_result(poly, w, cost, tris)
    big = [(x * 10 ** 15 + 3, y * 10 ** 15 - 7) for x, y in poly]
    w2 = perimeter_sq(big)
    cost2, tris2 = optimal_triangulation(big, w2)
    check_result(big, w2, cost2, tris2)
