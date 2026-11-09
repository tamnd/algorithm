# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/winding-number-algorithm/. The authors are listed in prov/CSD45Q.jsonl.

import math
import random
from fractions import Fraction

from winding_number_algorithm import winding_number, winding_number_algorithm

STAR = [(0, 10), (-6, -8), (10, 3), (-10, 3), (6, -8)]


def cross(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def brute_on_boundary(poly, q):
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if cross(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return False


def angle_winding(poly, q):
    """The winding number as the total turning angle divided by 2 pi, in floating point."""
    total = 0.0
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i][0] - q[0], poly[i][1] - q[1]
        bx, by = poly[(i + 1) % n][0] - q[0], poly[(i + 1) % n][1] - q[1]
        total += math.atan2(float(ax * by - ay * bx), float(ax * bx + ay * by))
    return round(total / (2 * math.pi))


def downward_ray_winding(poly, q):
    """An independent exact count: signed crossings of the downward vertical ray from q."""
    w = 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if a[0] <= q[0] < b[0] and cross(a, b, q) > 0:
            w += 1
        elif b[0] <= q[0] < a[0] and cross(a, b, q) < 0:
            w -= 1
    return w


def crossing_parity(poly, q):
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            x = a[0] + Fraction(q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > q[0]:
                inside = not inside
    return inside


def test_star_example() -> None:
    assert winding_number(STAR, (0, 0)) == 2
    assert winding_number(STAR, (0, 7)) == 1
    assert winding_number(STAR, (12, 0)) == 0
    assert winding_number(STAR, (-12, 3)) == 0
    assert winding_number(STAR, (0, 3)) is None
    assert winding_number(STAR[::-1], (0, 0)) == -2
    assert winding_number_algorithm(STAR, (0, 0)) is True
    assert winding_number_algorithm(STAR, (0, 0), "evenodd") is False
    assert winding_number_algorithm(STAR, (0, 7), "evenodd") is True


def test_vertices_on_the_ray() -> None:
    # The ray from q passes through vertices and along a horizontal edge.
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    diamond = [(2, 0), (4, 2), (2, 4), (0, 2)]
    assert winding_number(square, (-1, 0)) == 0
    assert winding_number(square, (-1, 4)) == 0
    assert winding_number(square, (2, 2)) == 1
    assert winding_number(diamond, (-1, 2)) == 0
    assert winding_number(diamond, (1, 2)) == 1
    assert winding_number(diamond, (2, 2)) == 1
    stairs = [(0, 0), (6, 0), (6, 2), (4, 2), (4, 4), (2, 4), (2, 2), (0, 2)]
    assert winding_number(stairs, (1, 1)) == 1
    assert winding_number(stairs, (-1, 2)) == 0
    assert winding_number(stairs, (3, 3)) == 1
    assert winding_number(stairs, (5, 3)) == 0
    assert winding_number(stairs, (1, 3)) == 0


def test_boundary() -> None:
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    for q in [(0, 0), (4, 4), (2, 0), (4, 1), (0, 3), (Fraction(1, 3), 4)]:
        assert winding_number(square, q) is None
        assert winding_number_algorithm(square, q) is None


def test_small_and_degenerate() -> None:
    assert winding_number([], (0, 0)) == 0
    assert winding_number([(1, 1)], (0, 0)) == 0
    assert winding_number([(1, 1)], (1, 1)) is None
    assert winding_number([(0, 0), (2, 2)], (5, 1)) == 0
    assert winding_number([(0, 0), (2, 2)], (1, 1)) is None
    # A square traced twice, with repeated and collinear vertices.
    sq = [(0, 0), (2, 0), (4, 0), (4, 4), (4, 4), (0, 4)]
    assert winding_number(sq + sq, (1, 1)) == 2


def random_polygon(rng, size, n):
    return [(rng.randint(0, size), rng.randint(0, size)) for _ in range(n)]


def test_random_against_angle_sum_and_other_ray() -> None:
    rng = random.Random(31415)
    checked = 0
    for _ in range(600):
        size = rng.choice([2, 4, 8])
        poly = random_polygon(rng, size, rng.randint(1, 9))
        for _ in range(8):
            q = (rng.randint(-1, size + 1), rng.randint(-1, size + 1))
            w = winding_number(poly, q)
            if brute_on_boundary(poly, q):
                assert w is None
                continue
            assert w is not None
            assert w == downward_ray_winding(poly, q)
            assert w == angle_winding(poly, q)
            checked += 1
        for _ in range(4):
            q = (Fraction(rng.randint(-2, 2 * size + 2), 2), Fraction(rng.randint(-2, 2 * size + 2), 2))
            if not brute_on_boundary(poly, q):
                assert winding_number(poly, q) == downward_ray_winding(poly, q) == angle_winding(poly, q)
                checked += 1
    assert checked > 3000


def test_simple_polygons_agree_with_crossing_parity() -> None:
    rng = random.Random(77)
    for _ in range(400):
        pts = list({(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(rng.randint(3, 10))})
        if len(pts) < 3:
            continue
        cx = Fraction(sum(p[0] for p in pts), len(pts)) + Fraction(1, 13)
        cy = Fraction(sum(p[1] for p in pts), len(pts)) + Fraction(1, 17)
        pts.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
        for _ in range(10):
            q = (Fraction(rng.randint(-2, 20), 2), Fraction(rng.randint(-2, 20), 2))
            w = winding_number(pts, q)
            if w is None:
                continue
            assert w in (-1, 0, 1)
            assert (w != 0) == crossing_parity(pts, q)
