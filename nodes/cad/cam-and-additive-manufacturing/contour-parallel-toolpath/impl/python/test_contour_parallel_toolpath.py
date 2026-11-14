# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contour-parallel-toolpath/. The authors are listed in prov/DWDHQ8.jsonl.

import random
from fractions import Fraction as F

import pytest

from contour_parallel_toolpath import (
    clip,
    contour_parallel,
    cross,
    depth,
    half_planes,
    loop_lengths,
    loop_segments,
    offset,
)


def unit_vectors():
    """Rational points on the unit circle from small Pythagorean triples."""
    base = {(F(1), F(0))}
    for m in range(2, 5):
        for n in range(1, m):
            k = m * m + n * n
            base.add((F(m * m - n * n, k), F(2 * m * n, k)))
    out = set()
    for a, b in base:
        for x, y in ((a, b), (b, a)):
            for sx in (1, -1):
                for sy in (1, -1):
                    out.add((sx * x, sy * y))
    return sorted(out)


UNITS = unit_vectors()


def random_convex(rng: random.Random):
    """A random convex polygon whose edges have rational unit normals."""
    while True:
        k = rng.randrange(3, 8)
        normals = rng.sample(UNITS, k)
        box = [(F(-500), F(-500)), (F(500), F(-500)), (F(500), F(500)), (F(-500), F(500))]
        poly = box
        for a, b in normals:
            poly = clip(poly, a, b, F(rng.randrange(3, 20)))
        if len(poly) < 3 or any(abs(x) == 500 or abs(y) == 500 for x, y in poly):
            continue
        n = len(poly)
        poly = [poly[i] for i in range(n) if cross(poly[i - 1], poly[i], poly[(i + 1) % n]) != 0]
        if len(poly) >= 3:
            return poly


def seg_dist2(p, a, b):
    """Exact squared distance from point p to segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    px, py = p[0] - a[0], p[1] - a[1]
    l2 = dx * dx + dy * dy
    t = F(0) if l2 == 0 else max(F(0), min(F(1), (px * dx + py * dy) / l2))
    ex, ey = px - t * dx, py - t * dy
    return ex * ex + ey * ey


def inside_convex(poly, p):
    if len(poly) == 1:
        return p == poly[0]
    if len(poly) == 2:
        return cross(poly[0], poly[1], p) == 0 and seg_dist2(p, poly[0], poly[1]) == 0
    return all(cross(poly[i], poly[(i + 1) % len(poly)], p) >= 0 for i in range(len(poly)))


def boundary_dist2(poly, p):
    """Squared distance from p to the boundary of a polygon, by a scan of all edges."""
    return min(seg_dist2(p, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))


def dist2_to_convex(poly, p):
    if not poly:
        return None
    if inside_convex(poly, p):
        return F(0)
    return min(seg_dist2(p, a, b) for a, b in loop_segments(poly))


def path_dist2(loops, p):
    return min(seg_dist2(p, a, b) for _, q in loops for a, b in loop_segments(q))


def grid(poly, steps):
    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for i in range(steps + 1):
        for j in range(steps + 1):
            yield (x0 + (x1 - x0) * F(2 * i + 1, 2 * steps + 2), y0 + (y1 - y0) * F(2 * j + 1, 2 * steps + 2))


def same_cycle(a, b):
    if len(a) != len(b):
        return False
    if not a:
        return True
    k = a.index(b[0]) if b[0] in a else -1
    return k >= 0 and a[k:] + a[:k] == b


TRIANGLE = [(0, 0), (12, 0), (0, 9)]


def test_example_triangle():
    loops = contour_parallel(TRIANGLE, 1, 1)
    assert [d for d, _ in loops] == [1, 2, 3]
    assert same_cycle(loops[0][1], [(1, 1), (9, 1), (1, 7)])
    assert same_cycle(loops[1][1], [(2, 2), (6, 2), (2, 5)])
    assert loops[2][1] == [(3, 3)]
    assert loop_lengths(loops) == [24, 12, 0]


def test_rectangle_ends_in_a_segment():
    loops = contour_parallel([(0, 0), (8, 0), (8, 4), (0, 4)], 1, 1)
    assert [d for d, _ in loops] == [1, 2]
    assert sorted(loops[1][1]) == [(2, 2), (6, 2)]
    assert loop_lengths(loops) == [16, 8]


def test_offset_against_distance_to_boundary():
    rng = random.Random(7)
    for _ in range(25):
        poly = random_convex(rng)
        planes = half_planes(poly)
        for _ in range(3):
            d = F(rng.randrange(0, 12), rng.randrange(1, 4))
            q = offset(poly, d)
            for p in grid(poly, 7):
                inside_p = inside_convex(poly, p)
                want = inside_p and boundary_dist2(poly, p) >= d * d
                assert (bool(q) and inside_convex(q, p)) == want
                if inside_p:
                    assert depth(planes, p) ** 2 == boundary_dist2(poly, p)


def test_cut_region_is_the_opening_when_step_at_most_radius():
    rng = random.Random(11)
    for _ in range(12):
        poly = random_convex(rng)
        r = F(rng.randrange(1, 4), 2)
        s = r * F(rng.randrange(1, 5), 4)
        loops = contour_parallel(poly, r, s)
        if not loops:
            continue
        core = offset(poly, r)
        for p in grid(poly, 9):
            in_opening = dist2_to_convex(core, p) <= r * r
            assert (path_dist2(loops, p) <= r * r) == in_opening


def test_tool_stays_in_pocket():
    rng = random.Random(3)
    for _ in range(30):
        poly = random_convex(rng)
        planes = half_planes(poly)
        r = F(rng.randrange(1, 6), 2)
        for d, q in contour_parallel(poly, r, F(1)):
            assert d >= r
            for v in q:
                assert depth(planes, v) >= d


def test_large_step_leaves_material_in_a_corner():
    loops = contour_parallel(TRIANGLE, 1, 2)
    assert [d for d, _ in loops] == [1, 3]
    p = (F(21, 10), F(21, 10))
    assert inside_convex(offset(TRIANGLE, 1), p)
    assert path_dist2(loops, p) > 1


def test_square_corner_threshold():
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    p = (F(41, 20), F(41, 20))
    loops = contour_parallel(square, 1, F(9, 5))
    assert inside_convex(offset(square, 1), p) and path_dist2(loops, p) > 1
    loops = contour_parallel(square, 1, F(17, 10))
    core = offset(square, 1)
    for q in grid(square, 24):
        if dist2_to_convex(core, q) <= 1:
            assert path_dist2(loops, q) <= 1


def test_bad_input():
    with pytest.raises(ValueError):
        contour_parallel([(0, 0), (1, 0), (0, 1)], 1, 1)  # hypotenuse sqrt(2)
    with pytest.raises(ValueError):
        contour_parallel([(0, 0), (0, 4), (4, 0)], 1, 1)  # clockwise
    with pytest.raises(ValueError):
        contour_parallel(TRIANGLE, 0, 1)
