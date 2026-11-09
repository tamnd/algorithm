# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polygon-simplicity-test/. The authors are listed in prov/HSYKXN.jsonl.

import math
import random
from fractions import Fraction

from polygon_simplicity_test import find_violation, is_simple


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_seg(a, b, q):
    return orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])


def meet(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return on_seg(a, b, c) or on_seg(a, b, d) or on_seg(c, d, a) or on_seg(c, d, b)


def common_points_besides(a, b, shared):
    """Do the segments a-shared and shared-b (sharing the end point shared) meet elsewhere?"""
    return (on_seg(shared, b, a) and a != shared) or (on_seg(shared, a, b) and b != shared)


def brute_simple(poly):
    """The definition, edge pair by edge pair, in O(n^2)."""
    n = len(poly)
    if n < 3 or len(set(poly)) < n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            a, b = poly[i], poly[(i + 1) % n]
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1:
                if common_points_besides(a, d, b):
                    return False
            elif i == 0 and j == n - 1:
                if common_points_besides(c, b, a):
                    return False
            elif meet(a, b, c, d):
                return False
    return True


def witness_is_valid(poly, w):
    kind, i, j = w
    n = len(poly)
    if kind == "too few vertices":
        return n < 3
    if kind == "repeated vertex":
        return i != j and poly[i] == poly[j]
    edge = lambda k: (poly[k], poly[(k + 1) % n])
    if kind == "fold":
        (a, b), (c, d) = edge(i), edge(j)
        return (j - i) % n == 1 and common_points_besides(a, d, b)
    if kind == "meet":
        return (i - j) % n not in (1, n - 1) and i != j and meet(*edge(i), *edge(j))
    return False


def check(poly):
    w = find_violation(poly)
    assert (w is None) == brute_simple(poly), poly
    if w is not None:
        assert witness_is_valid(poly, w), (poly, w)


def test_small_cases() -> None:
    assert not is_simple([])
    assert not is_simple([(0, 0)])
    assert not is_simple([(0, 0), (1, 0)])
    assert not is_simple([(0, 0), (1, 0), (2, 0)])
    assert is_simple([(0, 0), (1, 0), (0, 1)])
    assert is_simple([(0, 0), (2, 0), (4, 0), (4, 4), (0, 4)])
    assert find_violation([(0, 0), (4, 0), (4, 4), (0, 0), (0, 4)])[0] == "repeated vertex"
    assert find_violation([(0, 0), (4, 0), (2, 0), (2, 3)])[0] == "fold"
    assert find_violation([(0, 0), (2, 2), (2, 0), (0, 2)]) == ("meet", 0, 2)


def test_degenerate_contacts() -> None:
    # A vertex on a non-adjacent edge, collinear overlaps, vertical edges, a touching notch.
    cases = [
        [(0, 0), (4, 0), (4, 4), (2, 0), (0, 4)],
        [(0, 0), (6, 0), (6, 2), (4, 2), (4, 0), (5, 0), (5, 1), (2, 1), (2, 3), (0, 3)],
        [(0, 0), (0, 4), (2, 4), (2, 2), (0, 2), (1, 1)],
        [(0, 0), (3, 0), (3, 3), (0, 3), (0, 2), (1, 2), (1, 1), (0, 1)],
        [(0, 0), (3, 0), (3, 3), (0, 3), (0, 2), (1, 2), (1, 1), (0, 1), (0, 0)],
        [(0, 0), (4, 0), (4, 1), (1, 1), (1, 2), (4, 2), (4, 3), (0, 3)],
        [(0, 0), (4, 0), (4, 4), (2, 4), (2, 0), (1, 4), (0, 4)],
        [(Fraction(1, 2), 0), (3, 0), (3, 3), (Fraction(1, 2), 3)],
    ]
    for poly in cases:
        check(poly)
        check(poly[::-1])


def random_star(rng, size, k):
    pts = list({(rng.randint(0, size), rng.randint(0, size)) for _ in range(k)})
    cx = Fraction(sum(p[0] for p in pts), len(pts)) + Fraction(1, 7)
    cy = Fraction(sum(p[1] for p in pts), len(pts)) + Fraction(1, 11)
    pts.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    return pts


def test_random_against_all_pairs() -> None:
    rng = random.Random(1976)
    simple = 0
    for trial in range(6000):
        size = rng.choice([2, 3, 4, 6])
        if trial % 3 == 0:
            poly = random_star(rng, size, rng.randint(3, 9))
        else:
            poly = [(rng.randint(0, size), rng.randint(0, size)) for _ in range(rng.randint(0, 8))]
        check(poly)
        simple += brute_simple(poly)
    assert simple > 800


def test_random_rectilinear_walks() -> None:
    # Axis-parallel walks produce many vertical edges, collinear overlaps and touching corners.
    rng = random.Random(42)
    for _ in range(3000):
        x, y = 0, 0
        poly = [(x, y)]
        for _ in range(rng.randint(2, 7)):
            if len(poly) % 2:
                x = rng.randint(0, 4)
            else:
                y = rng.randint(0, 4)
            poly.append((x, y))
        poly.append((0, y))
        check(poly)
