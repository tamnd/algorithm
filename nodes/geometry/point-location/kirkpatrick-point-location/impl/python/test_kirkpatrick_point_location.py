# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kirkpatrick-point-location/. The authors are listed in prov/KVYDDR.jsonl.

import math
import random

import pytest

from kirkpatrick_point_location import KirkpatrickLocator, classify, ear_clip, in_closed, orient


def reference(outer, triangles, q):
    """Linear scan over the input triangles."""
    for i, t in enumerate(triangles):
        a, b, c = t if orient(*t) > 0 else (t[0], t[2], t[1])
        if in_closed((a, b, c), q):
            # a vertex or an edge gets the same answer from every closed triangle that contains it
            return classify((a, b, c), i, q)
    return ("outside",)


def insert_point(tris, p):
    """Insert p into a triangulation (list of ccw triangles) by splitting the triangle or edge."""
    for t in tris:
        if p in t:
            return
    for k, t in enumerate(tris):
        if in_closed(t, p):
            a, b, c = t
            sides = [orient(a, b, p), orient(b, c, p), orient(c, a, p)]
            if all(s > 0 for s in sides):
                tris[k : k + 1] = [(a, b, p), (b, c, p), (c, a, p)]
                return
            j = sides.index(0)  # p is inside the edge (t[j], t[j+1])
            u, w = t[j], t[(j + 1) % 3]
            break
    # split every triangle that has the edge uw
    out = []
    for t in tris:
        if u in t and w in t:
            i = t.index(u)
            if t[(i + 1) % 3] == w:
                x = t[(i + 2) % 3]
                out += [(u, p, x), (p, w, x)]
            else:
                x = t[(i + 1) % 3]
                out += [(u, x, p), (x, w, p)]
        else:
            out.append(t)
    tris[:] = out


def random_flips(tris, rng, count):
    for _ in range(count):
        t = rng.choice(tris)
        k = rng.randrange(3)
        a, b = t[k], t[(k + 1) % 3]
        c = t[(k + 2) % 3]
        other = [s for s in tris if s is not t and a in s and b in s]
        if not other:
            continue
        s = other[0]
        d = next(p for p in s if p != a and p != b)
        # flip ab to cd if the quadrilateral a d b c is strictly convex
        if orient(c, d, a) * orient(c, d, b) < 0 and orient(a, b, c) * orient(a, b, d) < 0:
            tris.remove(t)
            tris.remove(s)
            tris += [(c, a, d), (c, d, b)] if orient(c, a, d) > 0 else [(c, d, a), (c, b, d)]


def random_triangulation(rng, g, m, flips=0):
    outer = ((0, 0), (g, 0), (0, g))
    tris = [outer]
    for _ in range(m):
        x = rng.randint(1, g - 2)
        y = rng.randint(1, g - 1 - x)
        insert_point(tris, (x, y))
    random_flips(tris, rng, flips)
    tris = [t if orient(*t) > 0 else (t[0], t[2], t[1]) for t in tris]
    return outer, tris


def check_triangulation(outer, tris):
    area = sum(orient(*t) for t in tris)
    assert all(orient(*t) > 0 for t in tris)
    assert area == orient(*outer)
    edges = {}
    for t in tris:
        for k in range(3):
            e = (t[k], t[(k + 1) % 3])
            assert e not in edges
            edges[e] = t
    for (a, b) in edges:
        if (b, a) not in edges:
            # a boundary edge lies on the outer triangle
            assert any(orient(outer[k], outer[(k + 1) % 3], a) == 0 and orient(outer[k], outer[(k + 1) % 3], b) == 0 for k in range(3))


def test_generator_makes_triangulations():
    rng = random.Random(3)
    for _ in range(40):
        outer, tris = random_triangulation(rng, rng.randint(4, 14), rng.randint(0, 30), flips=rng.randint(0, 40))
        check_triangulation(outer, tris)


def test_against_linear_scan():
    rng = random.Random(1983)
    for trial in range(150):
        g = rng.randint(3, 12)
        outer, tris = random_triangulation(rng, g, rng.randint(0, 25), flips=rng.randint(0, 30))
        loc = KirkpatrickLocator(outer, tris)
        for x in range(-1, g + 2):
            for y in range(-1, g + 2):
                assert loc.locate((x, y)) == reference(outer, tris, (x, y)), (tris, (x, y))


def test_every_level_is_a_triangulation_and_rounds_remove_enough():
    rng = random.Random(27)
    for _ in range(20):
        outer, tris = random_triangulation(rng, 40, 300, flips=200)
        loc = KirkpatrickLocator(outer, tris)
        sizes = loc.level_sizes
        assert sizes[-1] == 1
        for r, removed in enumerate(loc.removed_per_round):
            vertices = (sizes[r] + 5) // 2  # T = 2N - 5 for a triangulated triangle
            assert 2 * vertices - 5 == sizes[r]
            assert removed >= max(1, (vertices - 3) / 18)
            assert sizes[r + 1] == sizes[r] - 2 * removed
        n = (sizes[0] + 5) // 2
        assert loc.depth() <= math.log(max(n - 3, 1)) / math.log(18 / 17) + 1


def test_query_cost_is_logarithmic_and_size_linear():
    rng = random.Random(5)
    outer, tris = random_triangulation(rng, 200, 1500, flips=500)
    loc = KirkpatrickLocator(outer, tris)
    n = (len(tris) + 5) // 2
    assert loc.size() <= sum(loc.level_sizes)
    assert sum(loc.level_sizes) <= 36 * (n - 3) + loc.depth() + 1
    for _ in range(300):
        q = (rng.randint(-5, 205), rng.randint(-5, 205))
        loc.tests = 0
        loc.locate(q)
        assert loc.tests <= 8 * loc.depth()


def test_high_degree_vertex_and_collinear_points():
    # a fan: many points on one line through the inner vertex (5, 5)
    outer = ((0, 0), (30, 0), (0, 30))
    tris = [outer]
    for p in [(5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (4, 4), (3, 3), (2, 2), (5, 6), (5, 7), (5, 8)]:
        insert_point(tris, p)
    tris = [t if orient(*t) > 0 else (t[0], t[2], t[1]) for t in tris]
    check_triangulation(outer, tris)
    loc = KirkpatrickLocator(outer, tris)
    for x in range(-1, 32):
        for y in range(-1, 32):
            assert loc.locate((x, y)) == reference(outer, tris, (x, y))


def test_small_inputs():
    outer = ((0, 0), (4, 0), (0, 4))
    loc = KirkpatrickLocator(outer, [outer])
    assert loc.depth() == 0
    assert loc.locate((1, 1)) == ("triangle", 0)
    assert loc.locate((2, 2)) == ("edge", ((0, 4), (4, 0)))
    assert loc.locate((5, 5)) == ("outside",)
    assert loc.locate((0, 4)) == ("vertex", (0, 4))


def test_ear_clip_with_collinear_vertices():
    poly = [(0, 0), (2, 0), (4, 0), (4, 2), (2, 1), (0, 2)]
    tris = ear_clip(poly)
    assert len(tris) == len(poly) - 2
    assert sum(orient(*t) for t in tris) == sum(poly[i][0] * poly[(i + 1) % 6][1] - poly[i][1] * poly[(i + 1) % 6][0] for i in range(6))
    with pytest.raises(ValueError):
        KirkpatrickLocator(((0, 0), (1, 1), (2, 2)), [])


def test_worked_example():
    outer = ((0, 0), (12, 0), (0, 12))
    tris = [outer]
    for p in [(3, 3), (6, 2), (2, 6), (4, 4)]:
        insert_point(tris, p)
    tris = [t if orient(*t) > 0 else (t[0], t[2], t[1]) for t in tris]
    loc = KirkpatrickLocator(outer, tris)
    assert tris[1] == ((6, 2), (3, 3), (0, 0)) and tris[2] == ((12, 0), (0, 12), (6, 2))
    assert loc.level_sizes == [9, 5, 3, 1]
    assert loc.removed_per_round == [2, 1, 1]
    assert loc.size() == 17
    loc.tests = 0
    assert loc.locate((4, 2)) == ("triangle", 1)
    assert loc.tests == 2 + 1 + 1
    assert loc.locate((1, 1)) == ("edge", ((0, 0), (3, 3)))
    assert loc.locate((5, 5)) == ("triangle", 2)
