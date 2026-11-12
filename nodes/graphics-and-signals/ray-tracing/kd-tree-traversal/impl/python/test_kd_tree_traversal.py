# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-tree-traversal/. The authors are listed in prov/AK1SG3.jsonl.

import math
import random
from fractions import Fraction

from kd_tree_traversal import any_hit, box_interval, build, closest_hit, hit_triangle, leaf_cells, tri_box, visited_leaves

P = ((0, 0, 0), (16, 2, 0), (16, 0, 2))  # in the plane x = 8 (y + z), box [0, 16] x [0, 2] x [0, 2]
Q = ((10, 0, 0), (10, 2, 0), (10, 0, 2))  # in the plane x = 10


def test_example_and_the_cell_check() -> None:
    tris = [P, Q]
    tree = build(tris, max_leaf=1, max_depth=1)
    root = tree.nodes[0]
    assert (root.axis, root.split) == (0, 8)
    assert tree.nodes[root.left].tris == [0] and tree.nodes[root.right].tris == [0, 1]
    o, d = (-1, Fraction(7, 8), Fraction(7, 8)), (1, 0, 0)
    assert hit_triangle(P, o, d) == 15 and hit_triangle(Q, o, d) == 11
    assert visited_leaves(tree, o, d) == [(root.left, 1, 9), (root.right, 9, 17)]
    assert closest_hit(tree, tris, o, d) == (11, 1)
    assert closest_hit(tree, tris, o, d, check_cell=False) == (15, 0)  # the hit of P lies beyond the near cell
    o, d = (20, Fraction(7, 8), Fraction(7, 8)), (-1, 0, 0)
    assert visited_leaves(tree, o, d) == [(root.right, 4, 12), (root.left, 12, 20)]
    assert closest_hit(tree, tris, o, d) == (6, 0)  # found in the first leaf, at t = 6 <= 12


def random_ray(rng, tris):
    o = [rng.randint(-4, 20) for _ in range(3)]
    if rng.random() < 0.5:
        a, b, c = rng.choice(tris)
        d = [a[i] + b[i] + c[i] - 3 * o[i] for i in range(3)]
    else:
        d = [rng.randint(-3, 3) for _ in range(3)]
    if rng.random() < 0.3:
        d[rng.randrange(3)] = 0
    if rng.random() < 0.3:
        k = rng.randrange(3)
        o[k] = rng.choice(rng.choice(tris))[k]
    if all(x == 0 for x in d):
        d = [0, 0, 1]
    return tuple(o), tuple(d)


def overlaps(box, cell):
    return all(box[0][a] <= cell[1][a] and cell[0][a] <= box[1][a] for a in range(3))


def random_scene(rng, n, small):
    if small:
        out = []
        for _ in range(n):
            b = [rng.randint(0, 14) for _ in range(3)]
            out.append(tuple(tuple(b[a] + rng.randint(0, 2) for a in range(3)) for _ in range(3)))
        return out
    return [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]


def test_random_scenes() -> None:
    rng = random.Random(6)
    wrong_without_check = 0
    for trial in range(150):
        n = rng.randint(1, 25)
        tris = random_scene(rng, n, trial % 2 == 0)
        tree = build(tris, max_leaf=rng.choice([1, 2, 3]), max_depth=rng.choice([3, 6, 10]))
        cells = leaf_cells(tree)
        for i, cell in cells:  # a leaf holds exactly the triangles whose box meets its closed cell
            assert sorted(tree.nodes[i].tris) == [r for r in range(n) if overlaps(tri_box(tris[r]), cell)]
        cell_of = dict(cells)
        for _ in range(8):
            o, d = random_ray(rng, tris)
            walk = visited_leaves(tree, o, d)
            span = box_interval(tree.lo, tree.hi, o, d, math.inf)
            if walk:  # the leaf intervals follow each other along the ray, and each is the ray in its cell
                assert span is not None and walk[0][1] == span[0] and walk[-1][2] == span[1]
                for (_, _, tf), (_, tn, _) in zip(walk, walk[1:]):
                    assert tf == tn
                for i, tn, tf in walk:
                    assert box_interval(*cell_of[i], o, d, math.inf) == (tn, tf)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
            got = closest_hit(tree, tris, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            bad = closest_hit(tree, tris, o, d, check_cell=False)
            wrong_without_check += (bad[0] if bad else None) != (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            got = closest_hit(tree, tris, o, d, tmax)
            near = [t for t in ts if t <= tmax]
            assert (got[0] if got else None) == (min(near) if near else None)
            assert any_hit(tree, tris, o, d, tmax) == bool(near)
    assert wrong_without_check > 0


def test_ray_in_a_split_plane() -> None:
    tris = [((8, 0, 0), (8, 4, 0), (8, 0, 4)), ((0, 1, 1), (4, 1, 1), (0, 3, 3)), ((12, 0, 1), (16, 4, 1), (12, 4, 3))]
    tree = build(tris, max_leaf=1)
    assert tree.nodes[0].axis == 0 and tree.nodes[0].split == 8
    for o, d in (((8, 1, -2), (0, 0, 1)), ((8, 1, 1), (0, 1, 0)), ((8, 1, 1), (1, 0, 0)), ((8, 1, 1), (-1, 0, 0))):
        ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
        got = closest_hit(tree, tris, o, d)
        assert (got[0] if got else None) == (min(ts) if ts else None)
