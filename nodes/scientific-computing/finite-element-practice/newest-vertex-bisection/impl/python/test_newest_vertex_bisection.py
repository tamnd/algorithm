# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newest-vertex-bisection/. The authors are listed in prov/GGH2BB.jsonl.

import random

from newest_vertex_bisection import (area, hanging_nodes, is_conforming, refine,
                                     refine_by_hanging_nodes, shape_key)


def l_shape():
    coords = [(-1.0, -1.0), (0.0, -1.0), (-1.0, 0.0), (0.0, 0.0),
              (1.0, 0.0), (-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)]
    elements = [[0, 3, 1], [3, 0, 2], [3, 5, 2], [5, 3, 6], [3, 7, 4], [7, 3, 6]]
    boundary = [[0, 1], [1, 3], [3, 4], [4, 7], [7, 6], [6, 5], [5, 2], [2, 0]]
    return coords, elements, boundary


def canon(coords, elements):
    return sorted(tuple(sorted(coords[v] for v in z)) for z in elements)


def total_area(coords, elements):
    return sum(area(coords, z) for z in elements)


def test_single_triangle_hand_example():
    c, e, b = refine([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)], [[0, 1, 2]],
                     [[0, 1], [1, 2], [2, 0]], [0])
    assert c[3] == (0.5, 0.0)
    assert e == [[2, 0, 3], [1, 2, 3]]
    assert sorted(tuple(x) for x in b) == [(0, 3), (1, 2), (2, 0), (3, 1)]
    assert all(z[2] == 3 for z in e)


def test_closure_on_two_triangles():
    coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    elements = [[0, 2, 1], [2, 0, 3]]
    boundary = [[0, 1], [1, 2], [2, 3], [3, 0]]
    c, e, b = refine(coords, elements, boundary, [0])
    assert len(e) == 4
    assert is_conforming(c, e, b)
    c2, e2, b2 = refine(c, e, b, [0])
    assert is_conforming(c2, e2, b2)
    assert len(e2) == 5  # the refinement edge of element 0 is on the boundary
    c3, e3, b3 = refine(c2, e2, b2, [t for t in range(len(e2)) if 4 in e2[t][:2]])
    assert is_conforming(c3, e3, b3)
    assert abs(sum(abs(area(c3, z)) for z in e3) - 1.0) < 1e-12


def test_matches_hanging_node_oracle_and_conforms():
    rng = random.Random(7)
    coords, elements, boundary = l_shape()
    signed = total_area(coords, elements)
    for _ in range(9):
        marked = [t for t in range(len(elements)) if rng.random() < 0.15] or [0]
        parents = [tuple(sorted(coords[v] for v in elements[t])) for t in marked]
        c1, e1, b1 = refine(coords, elements, boundary, marked)
        c2, e2, _ = refine_by_hanging_nodes(coords, elements, boundary, marked)
        assert canon(c1, e1) == canon(c2, e2)
        assert is_conforming(c1, e1, b1)
        assert not hanging_nodes(c1, e1)
        assert abs(sum(abs(area(c1, z)) for z in e1) - 3.0) < 1e-12
        assert abs(total_area(c1, e1) - signed) < 1e-12  # bisection keeps the orientation
        assert all(abs(area(c1, z)) > 0 for z in e1)
        children = set(canon(c1, e1))
        assert all(p not in children for p in parents)
        coords, elements, boundary = c1, e1, b1


def test_uniform_bisection_of_one_triangle_doubles():
    coords = [(0.0, 0.0), (1.0, 0.0), (0.3, 0.7)]
    elements = [[0, 1, 2]]
    boundary = [[0, 1], [1, 2], [2, 0]]
    for k in range(1, 9):
        coords, elements, boundary = refine(coords, elements, boundary, list(range(len(elements))))
        assert len(elements) == 2 ** k
        assert abs(total_area(coords, elements) - 0.35) < 1e-12
        assert is_conforming(coords, elements, boundary)


def test_at_most_four_similarity_classes():
    rng = random.Random(3)
    base = [(0.0, 0.0), (1.0, 0.0), (0.3, 0.7)]
    for rot in range(3):
        coords = list(base)
        elements = [[rot % 3, (rot + 1) % 3, (rot + 2) % 3]]
        boundary = [[0, 1], [1, 2], [2, 0]]
        for _ in range(12):
            marked = [t for t in range(len(elements)) if rng.random() < 0.3] or [0]
            coords, elements, boundary = refine(coords, elements, boundary, marked)
        assert is_conforming(coords, elements, boundary)
        assert len({shape_key(coords, z) for z in elements}) <= 4


def test_unmarked_mesh_is_unchanged():
    coords, elements, boundary = l_shape()
    c, e, b = refine(coords, elements, boundary, [])
    assert c == coords and e == elements and b == boundary
