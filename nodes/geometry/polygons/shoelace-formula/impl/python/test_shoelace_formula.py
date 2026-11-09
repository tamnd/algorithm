# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shoelace-formula/. The authors are listed in prov/1ARC5T.jsonl.

import math
import random
from fractions import Fraction

from shoelace_formula import polygon_area, shoelace_formula, twice_signed_area, twice_signed_area_shifted


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def on_segment(p, a, b):
    return orient(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_meet(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if ((o1 > 0 and o2 < 0) or (o1 < 0 and o2 > 0)) and ((o3 > 0 and o4 < 0) or (o3 < 0 and o4 > 0)):
        return True
    return on_segment(c, a, b) or on_segment(d, a, b) or on_segment(a, c, d) or on_segment(b, c, d)


def is_simple(poly):
    """All-pairs test: edges meet only at the shared vertex of consecutive edges."""
    n = len(poly)
    if n < 3 or len(set(poly)) < n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            a, b = poly[i], poly[(i + 1) % n]
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                shared = b if j == i + 1 else a
                other1 = a if shared == b else b
                other2 = d if shared == c else c
                if orient(other1, shared, other2) == 0 and (other1[0] - shared[0]) * (other2[0] - shared[0]) + (other1[1] - shared[1]) * (other2[1] - shared[1]) > 0:
                    return False
            elif segments_meet(a, b, c, d):
                return False
    return True


def strictly_inside(q, poly):
    """Crossing parity for a lattice point q that is not on the boundary."""
    n = len(poly)
    c = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            if (orient(a, b, q) > 0) == (b[1] > a[1]):
                c = not c
    return c


def pick_area(poly):
    """Area by Pick's theorem, A = I + B/2 - 1, with I and B counted by brute force."""
    n = len(poly)
    b = sum(math.gcd(abs(poly[(i + 1) % n][0] - poly[i][0]), abs(poly[(i + 1) % n][1] - poly[i][1])) for i in range(n))
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    inner = 0
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            q = (x, y)
            if any(on_segment(q, poly[i], poly[(i + 1) % n]) for i in range(n)):
                continue
            inner += strictly_inside(q, poly)
    return Fraction(inner) + Fraction(b, 2) - 1


def random_star_polygon(rng, size, k):
    """A simple polygon on the grid, made by sorting random points by angle around a center."""
    while True:
        pts = list({(rng.randint(0, size), rng.randint(0, size)) for _ in range(k)})
        cx = Fraction(sum(p[0] for p in pts), len(pts)) + Fraction(1, 7)
        cy = Fraction(sum(p[1] for p in pts), len(pts)) + Fraction(1, 11)
        pts.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
        if len(pts) >= 3 and is_simple(pts) and twice_signed_area(pts) != 0:
            return pts


def test_worked_example() -> None:
    poly = [(1, 0), (4, 1), (5, 4), (2, 5), (3, 2), (0, 3)]
    assert twice_signed_area(poly) == 24
    assert shoelace_formula(poly) == 12
    assert pick_area(poly) == 12 and is_simple(poly)
    assert shoelace_formula(poly[::-1]) == -12


def test_small_inputs() -> None:
    assert twice_signed_area([]) == 0
    assert twice_signed_area([(1, 2)]) == 0
    assert twice_signed_area([(1, 2), (3, 4)]) == 0
    assert twice_signed_area([(0, 0), (1, 0), (0, 1)]) == 1
    assert twice_signed_area([(0, 0), (1, 1), (2, 2)]) == 0


def test_unit_shapes() -> None:
    assert shoelace_formula([(0, 0), (1, 0), (1, 1), (0, 1)]) == 1
    assert shoelace_formula([(0, 0), (0, 1), (1, 1), (1, 0)]) == -1
    rect = [(0, 0), (4, 0), (4, 3), (0, 3)]
    assert polygon_area(rect) == 12
    with_flat = [(0, 0), (2, 0), (4, 0), (4, 3), (2, 3), (0, 3)]
    assert polygon_area(with_flat) == 12


def test_self_intersecting() -> None:
    bowtie = [(0, 0), (2, 2), (2, 0), (0, 2)]
    assert twice_signed_area(bowtie) == 0
    # A square traced twice has winding number 2 inside, so the signed area doubles.
    sq = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert shoelace_formula(sq + sq) == 2
    # Figure eight with unequal loops: +1 on the right loop, -1 on the left loop.
    fig8 = [(0, 0), (4, 2), (4, 0), (0, 2)]
    assert twice_signed_area(fig8) == 0
    # The edges (0,0)-(6,3) and (6,0)-(0,2) cross at x = (12/5, 6/5). The signed area is the
    # sum of the signed areas of the two loops, one clockwise and one counterclockwise.
    fig8b = [(0, 0), (6, 3), (6, 0), (0, 2)]
    x = (Fraction(12, 5), Fraction(6, 5))
    right = shoelace_formula([x, (6, 3), (6, 0)])
    left = shoelace_formula([(0, 0), x, (0, 2)])
    assert right < 0 < left
    assert shoelace_formula(fig8b) == right + left == -3


def test_fractions_and_translation() -> None:
    rng = random.Random(17)
    for _ in range(200):
        poly = random_star_polygon(rng, 8, rng.randint(3, 9))
        a = shoelace_formula(poly)
        dx, dy = Fraction(rng.randint(-50, 50), 7), Fraction(rng.randint(-50, 50), 3)
        moved = [(x + dx, y + dy) for x, y in poly]
        assert shoelace_formula(moved) == a
        big = [(x + 10**15, y - 10**15) for x, y in poly]
        assert shoelace_formula(big) == a
        assert twice_signed_area_shifted(poly) == twice_signed_area(poly)
        rot = poly[3 % len(poly):] + poly[: 3 % len(poly)]
        assert shoelace_formula(rot) == a
        assert shoelace_formula(poly[::-1]) == -a


def test_against_pick() -> None:
    rng = random.Random(2024)
    for _ in range(500):
        poly = random_star_polygon(rng, rng.choice([3, 5, 8]), rng.randint(3, 10))
        assert polygon_area(poly) == pick_area(poly)


def test_triangle_fan_on_convex() -> None:
    rng = random.Random(5)
    for _ in range(300):
        pts = list({(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(12)})
        pts.sort()
        lower, upper = [], []
        for p in pts:
            while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
                lower.pop()
            lower.append(p)
        for p in reversed(pts):
            while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
                upper.pop()
            upper.append(p)
        hull = lower[:-1] + upper[:-1]
        if len(hull) < 3:
            continue
        fan = sum(orient(hull[0], hull[i], hull[i + 1]) for i in range(1, len(hull) - 1))
        assert twice_signed_area(hull) == fan > 0
