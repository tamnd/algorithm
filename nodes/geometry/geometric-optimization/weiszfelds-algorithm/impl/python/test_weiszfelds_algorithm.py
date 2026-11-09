# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiszfelds-algorithm/. The authors are listed in prov/5VREF5.jsonl.

"""Tests for Weiszfeld's algorithm.

The method is numerical. Each test states its tolerance and compares with an
exact closed form, with Kuhn's exact optimality test at a data point, with a
convexity certificate, or with a nested ternary search in the plane.
"""

import math
import random

import pytest

from weiszfelds_algorithm import data_point_is_median, weber_cost, weiszfeld

TOL = 1e-7


def close(p, q, tol=TOL):
    return math.dist(p, q) <= tol


def ternary_reference(points, weights=None, it=100):
    """Minimize the convex cost over a box by nested ternary search."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    lo_y, hi_y = min(ys) - 1.0, max(ys) + 1.0

    def inner(x):
        a, b = lo_y, hi_y
        for _ in range(it):
            m1, m2 = a + (b - a) / 3, b - (b - a) / 3
            if weber_cost(points, (x, m1), weights) < weber_cost(points, (x, m2), weights):
                b = m2
            else:
                a = m1
        return weber_cost(points, (x, (a + b) / 2), weights)

    a, b = min(xs) - 1.0, max(xs) + 1.0
    for _ in range(it):
        m1, m2 = a + (b - a) / 3, b - (b - a) / 3
        if inner(m1) < inner(m2):
            b = m2
        else:
            a = m1
    return inner((a + b) / 2)


def certified_gap(points, y, weights=None):
    """An upper bound on cost(y) - (optimal cost), or None if none is found.

    If the data point nearest to y passes Kuhn's test, the optimum is its cost.
    Otherwise convexity gives cost* >= cost(y) - |grad| * diameter, because y
    and the median both lie in the convex hull of the points.
    """
    if weights is None:
        weights = [1] * len(points)
    k = min(range(len(points)), key=lambda i: math.dist(points[i], y))
    if data_point_is_median(points, k, weights):
        return weber_cost(points, y, weights) - weber_cost(points, points[k], weights)
    if math.dist(points[k], y) == 0.0:
        return None
    d = len(y)
    g = [0.0] * d
    for p, w in zip(points, weights):
        dist = math.dist(p, y)
        for j in range(d):
            g[j] += w * (y[j] - p[j]) / dist
    diam = max(math.dist(p, q) for p in points for q in points)
    return math.sqrt(sum(c * c for c in g)) * diam


def test_single_point_and_copies():
    assert weiszfeld([(3, -2)]) == (3.0, -2.0)
    assert weiszfeld([(1, 1), (1, 1), (1, 1)]) == (1.0, 1.0)


def test_bad_input():
    with pytest.raises(ValueError):
        weiszfeld([])
    with pytest.raises(ValueError):
        weiszfeld([(0, 0), (1, 0)], weights=[1, 0])


def test_page_example_pentagon():
    pent = [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
    y = weiszfeld(pent)
    assert abs(weber_cost(pent, y) - 14.447549153009) < 1e-9
    assert close(y, (2.6413678, 2.6413678), 1e-6)
    assert not any(data_point_is_median(pent, k) for k in range(5))


def test_page_example_first_steps():
    pent = [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
    y1 = weiszfeld(pent, start=(2.4, 2.4), max_iter=1, tol=0)
    assert close(y1, (2.52362, 2.52362), 1e-5)
    assert weber_cost(pent, y1) < weber_cost(pent, (2.4, 2.4))


def test_start_at_a_data_point():
    # Plain Weiszfeld divides by zero here; the Vardi-Zhang step moves away.
    sq = [(0, 0), (4, 0), (4, 4), (0, 4)]
    y1 = weiszfeld(sq, start=(0, 0), max_iter=1, tol=0)
    assert close(y1, (1.47759225, 1.47759225), 1e-7)
    assert close(weiszfeld(sq, start=(0, 0)), (2, 2))


def test_returns_exactly_at_an_optimal_data_point():
    obtuse = [(0, 0), (4, 0), (-1, 1)]
    assert data_point_is_median(obtuse, 0)
    assert weiszfeld(obtuse, start=(0, 0)) == (0.0, 0.0)


def test_obtuse_triangle_converges_to_the_corner():
    obtuse = [(0, 0), (4, 0), (-1, 1)]
    y = weiszfeld(obtuse)
    assert close(y, (0, 0))
    assert abs(weber_cost(obtuse, y) - (4 + math.sqrt(2))) < 1e-9


def test_fermat_point_of_a_triangle():
    tri = [(0, 0), (4, 0), (1, 3)]
    y = weiszfeld(tri)
    assert abs(weber_cost(tri, y) - math.sqrt(22 + 12 * math.sqrt(3))) < 1e-9
    us = [((p[0] - y[0]) / math.dist(p, y), (p[1] - y[1]) / math.dist(p, y)) for p in tri]
    for i in range(3):
        u, v = us[i], us[(i + 1) % 3]
        assert abs(u[0] * v[0] + u[1] * v[1] + 0.5) < 1e-6  # 120 degrees


def test_convex_quadrilateral_meets_at_the_diagonals():
    quad = [(0, 0), (4, 0), (5, 3), (0, 4)]
    y = weiszfeld(quad)
    assert close(y, (2.5, 1.5), 1e-6)
    assert abs(weber_cost(quad, y) - (math.sqrt(34) + 4 * math.sqrt(2))) < 1e-9


def test_point_inside_the_triangle_of_the_others():
    pts = [(0, 0), (6, 0), (0, 6), (1, 1)]
    assert data_point_is_median(pts, 3)
    assert close(weiszfeld(pts), (1, 1), 1e-6)


def test_collinear_points():
    pts = [(0, 0), (1, 1), (5, 5), (9, 9), (10, 10)]
    assert close(weiszfeld(pts), (5, 5), 1e-6)
    pts = [(-3, 0), (0, 0), (2, 0), (7, 0)]
    y = weiszfeld(pts)
    assert abs(y[1]) < 1e-12 and -1e-9 <= y[0] <= 2 + 1e-9
    assert abs(weber_cost(pts, y) - 12) < 1e-9


def test_heavy_weight_wins():
    pts = [(0, 0), (3, 1), (-2, 4), (5, -5)]
    w = [3, 1, 1, 1]
    assert data_point_is_median(pts, 0, w)
    assert close(weiszfeld(pts, w), (0, 0))


def test_duplicates_count_as_weight():
    pts = [(0, 0), (0, 0), (0, 0), (3, 1), (-2, 4), (5, -5)]
    assert close(weiszfeld(pts), (0, 0))
    assert data_point_is_median(pts, 1)


def test_cube_in_three_dimensions():
    cube = [(x, y, z) for x in (0, 2) for y in (0, 2) for z in (0, 2)]
    assert close(weiszfeld(cube, start=(0.1, 1.7, 0.3)), (1, 1, 1))


def test_cost_never_increases():
    rng = random.Random(3)
    for _ in range(200):
        pts = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(rng.randint(2, 7))]
        y = pts[rng.randrange(len(pts))]
        c = weber_cost(pts, y)
        for _ in range(15):
            y = weiszfeld(pts, start=y, max_iter=1, tol=0)
            c2 = weber_cost(pts, y)
            assert c2 <= c + 1e-12
            c = c2


def test_random_inputs_are_certified():
    rng = random.Random(1)
    for _ in range(600):
        n = rng.randint(1, 8)
        pts = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]
        w = None if rng.random() < 0.5 else [rng.randint(1, 4) for _ in range(n)]
        y = weiszfeld(pts, w)
        gap = certified_gap(pts, y, w)
        assert gap is not None and gap <= 1e-6 * (1 + weber_cost(pts, y, w))


def test_random_inputs_against_ternary_search():
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randint(3, 6)
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)]
        y = weiszfeld(pts)
        ref = ternary_reference(pts)
        assert weber_cost(pts, y) <= ref + 1e-9
        assert ref - weber_cost(pts, y) <= 1e-7
