# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-layer-mesh-generation/. The authors are listed in prov/H3T7WW.jsonl.

import math
import random
from fractions import Fraction as F

from boundary_layer_mesh_generation import area2, collapse_height, grow_layers, is_simple_polygon, layer_heights
from mg3geom import boundary_edges, exact, is_valid_planar_mesh, orient2d, twice_area

U = [(0.0, 0.0), (3.0, 0.0), (3.0, 2.0), (2.0, 2.0), (2.0, 1.0), (1.0, 1.0), (1.0, 2.0), (0.0, 2.0)]
HORSESHOE = [(0.0, 0.0), (4.0, 0.0), (4.0, 3.0), (2.2, 3.0), (2.2, 2.5), (3.5, 2.5), (3.5, 0.5), (0.5, 0.5),
             (0.5, 2.5), (1.8, 2.5), (1.8, 3.0), (0.0, 3.0)]


def convex_polygon(rng, n):
    """A convex polygon with n vertices on an ellipse, counterclockwise."""
    angles = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
    a, b = rng.uniform(1, 3), rng.uniform(1, 3)
    return [(a * math.cos(t), b * math.sin(t)) for t in angles]


def line_distance(p, a, b):
    return abs((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])) / math.dist(a, b)


def inside_quad(q, x):
    return all(orient2d(q[s], q[(s + 1) % 4], x) > 0 for s in range(4))


def test_heights_follow_the_growth_ratio_exactly():
    d = layer_heights(F(1, 100), F(6, 5), 12)
    assert d[0] == 0 and d[1] == F(1, 100)
    for k in range(1, 12):
        assert (d[k + 1] - d[k]) / (d[k] - d[k - 1]) == F(6, 5)
        assert d[k] == F(1, 100) * (F(6, 5) ** k - 1) / (F(6, 5) - 1)


def test_layer_vertices_sit_at_the_layer_height_from_both_wall_edges():
    rng = random.Random(1)
    wall = convex_polygon(rng, 9)
    n = len(wall)
    pts, quads, k, why = grow_layers(wall, 0.01, 1.25, 10)
    d = layer_heights(0.01, 1.25, 10)
    assert k == 10 and why is None
    for layer in range(1, 11):
        for i in range(n):
            p = pts[layer * n + i]
            for a, b in ((wall[i - 1], wall[i]), (wall[i], wall[(i + 1) % n])):
                assert abs(line_distance(p, a, b) - d[layer]) < 1e-9 * (1 + d[layer])


def test_convex_walls_never_stop_and_the_quads_tile_the_layers():
    rng = random.Random(2)
    for _ in range(8):
        wall = convex_polygon(rng, rng.randint(3, 12))
        if min(math.dist(wall[i], wall[i - 1]) for i in range(len(wall))) < 1e-3:
            continue
        n = len(wall)
        pts, quads, k, why = grow_layers(wall, 0.02, 1.3, 12)
        assert k == 12 and why is None
        E = [exact(p) for p in pts]
        assert is_valid_planar_mesh(E, quads)                      # no inverted quad, conforming
        outer = E[12 * n:]
        assert area2(pts, quads) == twice_area(outer) - twice_area(E[:n])
        bnd = set(boundary_edges(quads))
        assert bnd == {(i, (i - 1) % n) for i in range(n)} | {(12 * n + i, 12 * n + (i + 1) % n) for i in range(n)}


def test_concave_corners_stop_at_the_collapse_height():
    d = layer_heights(0.05, 1.2, 10)
    h = min(collapse_height(U, i) for i in range(len(U)))
    assert abs(h - 0.5) < 1e-12
    expected = max(k for k in range(11) if d[k] < h)
    pts, quads, k, why = grow_layers(U, 0.05, 1.2, 10)
    assert k == expected == 6 and "not strictly convex" in why
    E = [exact(p) for p in pts]
    assert is_valid_planar_mesh(E, quads)
    # brute force: no point lies inside two quads
    rng = random.Random(3)
    for _ in range(3000):
        x = (F(rng.randint(-2000, 5000), 1000), F(rng.randint(-2000, 4000), 1000))
        assert sum(inside_quad([E[i] for i in q], x) for q in quads) <= 1


def test_colliding_fronts_stop_on_the_simplicity_test():
    pts, quads, k, why = grow_layers(HORSESHOE, 0.05, 1.2, 10)
    d = layer_heights(0.05, 1.2, 10)
    # the two tips face each other across a gap of 0.4, so the fronts meet at height 0.2
    assert d[3] < 0.2 < d[4]
    assert k == 3 and "not simple" in why
    assert min(collapse_height(HORSESHOE, i) for i in range(len(HORSESHOE))) > d[4]
    n = len(HORSESHOE)
    E = [exact(p) for p in pts]
    assert is_valid_planar_mesh(E, quads) and is_simple_polygon(E[3 * n:])
    assert area2(pts, quads) == twice_area(E[3 * n:]) - twice_area(E[:n])
