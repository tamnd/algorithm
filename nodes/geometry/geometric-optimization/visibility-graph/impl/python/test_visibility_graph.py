# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/visibility-graph/. The authors are listed in prov/KH2F9W.jsonl.

"""Tests for the visibility graph, against an independent clipping oracle."""

import math
import random
from fractions import Fraction

import pytest

from visibility_graph import VisibilityGraph, orient, strictly_inside, visible


def clip_visible(p, q, obstacles):
    """Oracle: cut pq at every parameter where it meets an obstacle edge.

    For each edge ab, solve p + t (q - p) = a + u (b - a) exactly. A crossing
    or touching point adds its t; a collinear overlap adds the parameters of
    its ends. Between consecutive cuts the open piece misses every edge, so
    its midpoint decides whether it lies in an interior.
    """
    if p == q:
        return not any(strictly_inside(p, poly) for poly in obstacles)
    dx, dy = q[0] - p[0], q[1] - p[1]
    cuts = {Fraction(0), Fraction(1)}
    for poly in obstacles:
        n = len(poly)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            ex, ey = b[0] - a[0], b[1] - a[1]
            den = dx * ey - dy * ex
            if den != 0:
                t = Fraction((a[0] - p[0]) * ey - (a[1] - p[1]) * ex, den)
                u = Fraction((a[0] - p[0]) * dy - (a[1] - p[1]) * dx, den)
                if 0 <= t <= 1 and 0 <= u <= 1:
                    cuts.add(t)
            elif (a[0] - p[0]) * dy - (a[1] - p[1]) * dx == 0:
                for v in (a, b):
                    t = Fraction(dx * (v[0] - p[0]) + dy * (v[1] - p[1]), dx * dx + dy * dy)
                    if 0 <= t <= 1:
                        cuts.add(t)
    cuts = sorted(cuts)
    for s, t in zip(cuts, cuts[1:]):
        m = (s + t) / 2
        mid = (p[0] + m * dx, p[1] + m * dy)
        if any(strictly_inside(mid, poly) for poly in obstacles):
            return False
    return True


def random_polygon(rng, cx, cy, rad):
    """A random simple polygon, star-shaped around (cx, cy), with integer vertices."""
    while True:
        k = rng.randint(3, 6)
        angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(k))
        pts = []
        for a in angles:
            r = rng.uniform(1, rad)
            v = (cx + round(r * math.cos(a)), cy + round(r * math.sin(a)))
            if v not in pts:
                pts.append(v)
        if len(pts) >= 3 and is_simple(pts) and orient_sum(pts) != 0:
            return pts


def orient_sum(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def is_simple(poly):
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if orient(poly[i - 1], a, b) == 0 and (b[0] - a[0]) * (a[0] - poly[i - 1][0]) + (b[1] - a[1]) * (a[1] - poly[i - 1][1]) <= 0:
            return False  # a spike that folds back
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                continue
            if segments_meet(a, b, c, d):
                return False
    return True


def segments_meet(a, b, c, d):
    def on(p, s, t):
        return orient(s, t, p) == 0 and min(s[0], t[0]) <= p[0] <= max(s[0], t[0]) and min(s[1], t[1]) <= p[1] <= max(s[1], t[1])
    d1, d2 = orient(a, b, c), orient(a, b, d)
    d3, d4 = orient(c, d, a), orient(c, d, b)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
        return True
    return on(c, a, b) or on(d, a, b) or on(a, c, d) or on(b, c, d)


def random_scene(rng):
    cells = [(x, y) for x in range(3) for y in range(3)]
    rng.shuffle(cells)
    obstacles = [random_polygon(rng, 10 * x + 5, 10 * y + 5, 4) for x, y in cells[: rng.randint(1, 3)]]
    return obstacles


SQUARE = [(3, -2), (7, -2), (7, 2), (3, 2)]


def test_no_obstacles():
    g = VisibilityGraph([], [(0, 0), (1, 5), (-2, 3)])
    assert g.edges() == {(0, 1), (0, 2), (1, 2)}
    assert g.shortest_path((0, 0), (3, 4))[0] == 5.0


def test_square_sides_but_not_diagonals():
    g = VisibilityGraph([SQUARE])
    assert g.edges() == {(0, 1), (1, 2), (2, 3), (0, 3)}
    g.check_invariant()


def test_path_around_a_square():
    g = VisibilityGraph([SQUARE])
    length, path = g.shortest_path((0, 0), (10, 0))
    assert abs(length - (4 + 2 * math.sqrt(13))) < 1e-12
    assert path[0] == (0, 0) and path[-1] == (10, 0) and len(path) == 4


def test_grazing_and_passing_through_vertices():
    a = [(0, 0), (2, 0), (2, 2), (0, 2)]
    b = [(4, 0), (6, 0), (6, 2), (4, 2)]
    assert visible((0, 2), (6, 2), [a, b])          # along the top edges
    assert visible((0, 0), (6, 0), [a, b])          # along the bottom edges
    assert visible((2, 2), (4, 0), [a, b])          # in the gap
    assert not visible((0, 0), (6, 2), [a, b])      # through both interiors
    assert not visible((-1, -1), (3, 3), [a])       # along the diagonal of a square
    assert visible((-1, -1), (3, 3), [[(0, 0), (2, 0), (2, 2)]])  # along the hypotenuse of a triangle


def test_diagonal_through_a_corner_only():
    tri = [(0, 0), (4, 0), (0, 4)]
    assert visible((-1, 5), (5, -1), [tri])         # touches the hypotenuse along its length
    assert not visible((-1, -1), (2, 2), [tri])     # enters the interior at (0, 0)
    assert visible((5, 0), (0, 5), [tri])           # parallel to the hypotenuse, outside


def test_pocket_of_a_nonconvex_obstacle():
    u = [(0, 0), (6, 0), (6, 6), (4, 6), (4, 2), (2, 2), (2, 6), (0, 6)]
    g = VisibilityGraph([u])
    idx = {v: i for i, v in enumerate(g.nodes)}
    e = {frozenset((g.nodes[i], g.nodes[j])) for i, j in g.edges()}
    assert frozenset([(2, 6), (4, 6)]) in e         # across the mouth of the pocket
    assert frozenset([(2, 2), (4, 6)]) in e         # inside the pocket
    assert frozenset([(0, 0), (6, 6)]) not in e
    assert len(idx) == 8
    g.check_invariant()


def test_many_collinear_vertices_against_the_oracle():
    comb = [(0, 0), (6, 0), (6, 3), (5, 3), (5, 1), (4, 1), (4, 3), (3, 3), (3, 1),
            (2, 1), (2, 3), (1, 3), (1, 1), (0, 1)]
    flat = [(8, 0), (10, 0), (12, 0), (12, 2), (10, 2), (8, 2)]   # straight angles
    for obstacles in ([comb], [flat], [comb, flat], [comb[::-1], flat[::-1]]):
        pts = [(x, y) for x in range(-1, 14) for y in range(-1, 5)
               if not any(strictly_inside((x, y), poly) for poly in obstacles)]
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                assert visible(pts[i], pts[j], obstacles) == clip_visible(pts[i], pts[j], obstacles)


def test_point_inside_is_rejected():
    with pytest.raises(ValueError):
        VisibilityGraph([SQUARE], [(5, 0)])
    with pytest.raises(ValueError):
        VisibilityGraph([SQUARE]).shortest_path((5, 0), (10, 10))


def test_page_example():
    tri = [(2, 1), (5, 0), (4, 4)]
    rect = [(6, 2), (8, 2), (8, 6), (6, 6)]
    g = VisibilityGraph([tri, rect])
    assert g.edge_count() == 12
    length, path = g.shortest_path((0, 0), (10, 4))
    assert path == [(0, 0), (5, 0), (8, 2), (10, 4)]
    assert abs(length - (5 + math.sqrt(13) + math.sqrt(8))) < 1e-12


def test_random_scenes_against_the_oracle():
    rng = random.Random(7)
    for _ in range(200):
        obstacles = random_scene(rng)
        extra = []
        while len(extra) < 4:
            v = (rng.randint(-2, 32), rng.randint(-2, 32))
            if not any(strictly_inside(v, poly) for poly in obstacles):
                extra.append(v)
        g = VisibilityGraph(obstacles, extra)
        n = len(g.nodes)
        linked = g.edges()
        for i in range(n):
            for j in range(i + 1, n):
                expect = clip_visible(g.nodes[i], g.nodes[j], obstacles)
                assert ((i, j) in linked) == expect, (obstacles, g.nodes[i], g.nodes[j])


def test_random_paths_are_valid_and_short():
    rng = random.Random(8)
    for _ in range(120):
        obstacles = random_scene(rng)
        ends = []
        while len(ends) < 2:
            v = (rng.randint(-2, 32), rng.randint(-2, 32))
            if not any(strictly_inside(v, poly) for poly in obstacles):
                ends.append(v)
        g = VisibilityGraph(obstacles)
        length, path = g.shortest_path(*ends)
        assert path[0] == ends[0] and path[-1] == ends[1]
        assert abs(sum(math.dist(a, b) for a, b in zip(path, path[1:])) - length) < 1e-9
        for a, b in zip(path, path[1:]):
            assert clip_visible(a, b, obstacles)
        assert length >= math.dist(*ends) - 1e-12
        if clip_visible(ends[0], ends[1], obstacles):
            assert abs(length - math.dist(*ends)) < 1e-12
        # the inner vertices of a shortest path are obstacle vertices
        corners = {v for poly in obstacles for v in poly}
        assert all(v in corners for v in path[1:-1])
