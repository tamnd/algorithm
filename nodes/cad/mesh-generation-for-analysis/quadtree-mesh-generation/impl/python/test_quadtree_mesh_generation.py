# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadtree-mesh-generation/. The authors are listed in prov/C1TYAG.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F

import pytest

from mg2geom import orient2d, triangle_angles_deg
from quadtree_mesh_generation import Quadtree, aspect, quadtree_mesh


def random_points(seed, n, size=40):
    r = random.Random(seed)
    pts = set()
    while len(pts) < n:
        pts.add((r.randint(0, size), r.randint(0, size)))
    return sorted(pts)


def leaf_square(t, b):
    k, i, j = b
    x0, y0 = t.corner(k, i, j)
    return x0, y0, t.width(k)


def side_contact(s, u):
    """Length of the common boundary of two closed squares with disjoint interiors (brute force)."""
    ax, ay, aw = s
    bx, by, bw = u
    if ax + aw == bx or bx + bw == ax:  # vertical contact
        return max(0, min(ay + aw, by + bw) - max(ay, by))
    if ay + aw == by or by + bw == ay:  # horizontal contact
        return max(0, min(ax + aw, bx + bw) - max(ax, bx))
    return 0


CASES = [random_points(seed, n) for seed, n in [(1, 2), (2, 3), (3, 5), (4, 8), (5, 11), (6, 12), (7, 4)]]
CASES.append([(0, 0), (8, 0), (8, 1)])  # a close pair far from a third point
CASES.append([(F(1, 3), F(2, 7)), (F(5, 2), F(-1, 9)), (F(3, 4), F(9, 5))])  # rational input


@pytest.mark.parametrize("pts", CASES)
def test_tree_is_balanced_by_brute_force(pts):
    t, _, _ = quadtree_mesh(pts)
    sq = [leaf_square(t, b) for b in t.leaves]
    for a in range(len(sq)):
        for b in range(a + 1, len(sq)):
            if side_contact(sq[a], sq[b]) > 0:
                ratio = sq[a][2] / sq[b][2]
                assert ratio in (F(1, 2), 1, 2), (sq[a], sq[b])


@pytest.mark.parametrize("pts", CASES)
def test_point_leaves_are_surrounded_by_eight_equal_leaves(pts):
    t, _, _ = quadtree_mesh(pts)
    sq = {leaf_square(t, b) for b in t.leaves}
    for p in t.points:
        holders = [s for s in sq if s[0] <= p[0] < s[0] + s[2] and s[1] <= p[1] < s[1] + s[2]]
        assert len(holders) == 1
        x0, y0, w = holders[0]
        assert sum(1 for s in sq if s[0] <= p[0] < s[0] + s[2] and s[1] <= p[1] < s[1] + s[2]) == 1
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di or dj:
                    assert (x0 + di * w, y0 + dj * w, w) in sq
        others = [q for q in t.points if q != p]
        assert min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in others) >= 8 * w * w


@pytest.mark.parametrize("pts", CASES)
def test_triangles_tile_the_root_square(pts):
    t, v, tris = quadtree_mesh(pts)
    assert all(orient2d(v[a], v[b], v[c]) > 0 for a, b, c in tris)
    assert sum(orient2d(v[a], v[b], v[c]) for a, b, c in tris) == 2 * t.side ** 2
    edges = Counter()
    for a, b, c in tris:
        for e in ((a, b), (b, c), (c, a)):
            edges[e] += 1
    x0, y0, s = t.origin[0], t.origin[1], t.side
    for (a, b), m in edges.items():
        assert m == 1
        if (b, a) not in edges:  # a boundary edge lies on the root boundary
            pa, pb = v[a], v[b]
            assert (pa[0] == pb[0] and pa[0] in (x0, x0 + s)) or (pa[1] == pb[1] and pa[1] in (y0, y0 + s))
    # Every inner edge has its twin, so no vertex hangs in the middle of an edge,
    # and with positive areas that sum to the square this is a triangulation.
    assert set(t.points) <= set(v)


@pytest.mark.parametrize("pts", CASES)
def test_aspect_ratio_at_most_4_and_angle_bound(pts):
    _, v, tris = quadtree_mesh(pts)
    bound = math.degrees(math.asin(0.25))  # 14.4775..., from A <= 4 and 1/sin(theta) <= A
    for a, b, c in tris:
        assert aspect(v[a], v[b], v[c]) <= 4
        assert min(triangle_angles_deg(v[a], v[b], v[c])) >= bound - 1e-9


def test_many_random_inputs_keep_the_bound():
    worst = 0
    for seed in range(100, 115):
        _, v, tris = quadtree_mesh(random_points(seed, 2 + seed % 9, 60))
        worst = max(worst, max(aspect(v[a], v[b], v[c]) for a, b, c in tris))
    assert worst <= 4


def test_three_by_three_block_lets_a_warped_box_have_a_split_side():
    # With the 3 by 3 block of the paper, a box that shares the warped corner can
    # have a split side. The 5 by 5 block of this page rules it out.
    pts = [(11, 19), (12, 9), (19, 5)]
    with pytest.raises(AssertionError):
        quadtree_mesh(pts, reach=1)
    quadtree_mesh(pts, reach=2)


def test_trace_of_the_three_point_example():
    t = Quadtree([(0, 0), (4, 0), (1, 3)])
    trace = []
    t.build(trace)
    assert [r for r, _ in trace] == ["crowded"] * 4 + ["neighbor"] * 2 + ["balance"]
    assert Counter(t.width(b[0]) for b in t.leaves) == {1: 68, 2: 39, 4: 2}
    _, v, tris = quadtree_mesh([(0, 0), (4, 0), (1, 3)])
    assert (len(v), len(tris)) == (232, 434)
    assert max(aspect(v[a], v[b], v[c]) for a, b, c in tris) == F(5, 2)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        quadtree_mesh([(1, 1)])
    with pytest.raises(ValueError):
        quadtree_mesh([(1, 1), (1, 1)])
