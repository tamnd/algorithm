# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-mesh-generation/. The authors are listed in prov/YMYTYF.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache

import pytest

from mg2geom import dihedral_angles_deg, orient3d, radius_edge2
from octree_mesh_generation import (
    ball_values,
    build_tree,
    cut_by_sign,
    fill_leaves,
    meets_sphere,
    octree_mesh,
    split_prism,
)

DIH_MIN = math.degrees(math.atan(1 / math.sqrt(2)))  # 35.26 degrees
DIH_MAX = 90 + DIH_MIN  # 125.26 degrees


def random_ball(seed):
    r = random.Random(seed)
    center = tuple(F(r.randint(12, 20), 2) for _ in range(3))
    r2 = F(r.randint(6, 80), 3)  # never a quarter-integer, so never zero at a vertex
    return center, r2


CASES = [
    ((8, 8, 8), F(91, 3)),  # the example of the page
    ((F(15, 2), 8, F(17, 2)), F(91, 3)),  # off center
    ((7, 9, 8), F(10, 3)),  # a small ball: the tree is graded
    random_ball(1),
    random_ball(2),
]
DEPTH = 3


@lru_cache(maxsize=None)
def stages(i):
    center, r2 = CASES[i]
    center = tuple(F(c) for c in center)
    t = build_tree(center, r2, DEPTH)
    verts, tets = fill_leaves(t)
    f = ball_values(verts, center, r2)
    inside = cut_by_sign(verts, tets, f)
    outside = cut_by_sign(verts, tets, [-x for x in f])
    return t, verts, tets, inside, outside


def box(t, b):
    w = t.width(b[0])
    return tuple((x, x + w) for x in t.lower(b))


def contact_dim(p, q):
    """Dimension of the intersection of two closed boxes, or -1 if they are apart (brute force)."""
    dim = 0
    for (a0, a1), (b0, b1) in zip(p, q):
        lo, hi = max(a0, b0), min(a1, b1)
        if lo > hi:
            return -1
        dim += lo < hi
    return dim


def faces(tets):
    c = Counter()
    for a, b, cc, d in tets:
        # outward oriented faces of a positive tetrahedron, as sorted triple plus parity
        for tri in ((b, cc, d), (a, d, cc), (a, b, d), (a, cc, b)):
            c[tri_key(tri)] += 1
    return c


def tri_key(tri):
    """A rotation-invariant key that keeps the orientation of the triangle."""
    i = tri.index(min(tri))
    return tri[i:] + tri[:i]


def check_face_pairs(verts, tets, on_boundary):
    c = faces(tets)
    for tri, m in c.items():
        assert m == 1, tri
        twin = (tri[0], tri[2], tri[1])
        if twin not in c:
            assert on_boundary([verts[v] for v in tri]), tri


@pytest.mark.parametrize("i", range(len(CASES)))
def test_tree_is_balanced_by_brute_force(i):
    t = stages(i)[0]
    leaves = sorted(t.leaves)
    boxes = [box(t, b) for b in leaves]
    for a in range(len(leaves)):
        for b in range(a + 1, len(leaves)):
            if contact_dim(boxes[a], boxes[b]) >= 1:
                assert abs(leaves[a][0] - leaves[b][0]) <= 1, (leaves[a], leaves[b])


@pytest.mark.parametrize("i", range(len(CASES)))
def test_leaves_at_the_surface_have_the_finest_size(i):
    t = stages(i)[0]
    center, r2 = CASES[i]
    for b in t.leaves:
        if meets_sphere(t.lower(b), t.width(b[0]), tuple(F(c) for c in center), F(r2)):
            assert b[0] == DEPTH


@pytest.mark.parametrize("i", range(len(CASES)))
def test_template_mesh_is_a_conforming_mesh_of_the_cube(i):
    t, verts, tets = stages(i)[:3]
    vols = [orient3d(*[verts[v] for v in tet]) for tet in tets]
    assert all(v > 0 for v in vols)
    assert sum(vols) == 6 * t.side**3

    def on_cube_face(ps):
        return any(all(p[a] == s for p in ps) for a in range(3) for s in (0, t.side))

    check_face_pairs(verts, tets, on_cube_face)


@pytest.mark.parametrize("i", range(len(CASES)))
def test_template_tetrahedra_have_the_proved_quality(i):
    verts, tets = stages(i)[1:3]
    for tet in tets:
        p = [verts[v] for v in tet]
        assert radius_edge2(*p) <= F(5, 2)
        d = dihedral_angles_deg(*p)
        assert DIH_MIN - 1e-9 <= min(d) and max(d) <= DIH_MAX + 1e-9


def test_template_list_by_enumeration():
    # Every template tetrahedron is (cell center, square center, two ring neighbors).
    # Up to the symmetries of the cube, the square is the bottom face of [0, 8]^3 or a
    # quarter of it; a whole face may carry any of its four edge midpoints; a quarter
    # carries none (balance). This lists all 112 shapes and finds the exact extremes.
    cc = (4, 4, 4)
    shapes = []
    for u0, v0, h in [(0, 0, 8), (0, 0, 4), (4, 0, 4), (0, 4, 4), (4, 4, 4)]:
        cs = [(u0, v0), (u0 + h, v0), (u0 + h, v0 + h), (u0, v0 + h)]
        for mask in range(16 if h == 8 else 1):
            ring = []
            for s in range(4):
                ring.append(cs[s] + (0,))
                if mask >> s & 1:
                    a, b = cs[s], cs[(s + 1) % 4]
                    ring.append(((a[0] + b[0]) // 2, (a[1] + b[1]) // 2, 0))
            sc = (u0 + h // 2, v0 + h // 2, 0)
            shapes += [(cc, sc, ring[s], ring[(s + 1) % len(ring)]) for s in range(len(ring))]
    assert len(shapes) == 112
    assert max(radius_edge2(*s) for s in shapes) == F(5, 2)
    d = [a for s in shapes for a in dihedral_angles_deg(*s)]
    assert min(d) == pytest.approx(DIH_MIN) and max(d) == pytest.approx(DIH_MAX)


@pytest.mark.parametrize("i", range(len(CASES)))
def test_cut_mesh_is_conforming_and_matches_the_outside(i):
    t, verts, tets, inside, outside = stages(i)
    center, r2 = CASES[i]
    center = tuple(F(c) for c in center)
    template = set(verts)
    vi, ti = inside
    vo, to = outside
    vol_in = [orient3d(*[vi[v] for v in tet]) for tet in ti]
    vol_out = [orient3d(*[vo[v] for v in tet]) for tet in to]
    assert all(v > 0 for v in vol_in + vol_out)
    # the two parts fill the cube exactly
    assert sum(vol_in) + sum(vol_out) == 6 * t.side**3
    # every boundary face of the inside lies on the cut surface: its vertices are cut points
    check_face_pairs(vi, ti, lambda ps: not any(p in template for p in ps))
    # the cut triangles of the inside are the cut triangles of the outside, reversed
    cut_in = {tuple(vi[v] for v in tri) for tri in faces(ti) if not any(vi[v] in template for v in tri)}
    cut_out = {tuple(vo[v] for v in tri) for tri in faces(to) if not any(vo[v] in template for v in tri)}
    cut_in = {tri for tri in cut_in if (tri[0], tri[2], tri[1]) not in cut_in}
    rev = set()
    for tri in cut_out:
        r = (tri[0], tri[2], tri[1])
        i0 = r.index(min(r))
        rev.add(r[i0:] + r[:i0])
    norm = set()
    for tri in cut_in:
        i0 = tri.index(min(tri))
        norm.add(tri[i0:] + tri[:i0])
    assert norm == rev
    # every vertex of the inside lies in the closed ball (f is concave, so f >= 0 on the cut points)
    assert all(v >= 0 for v in ball_values(vi, center, r2))
    # A leaf that misses the sphere is kept whole or dropped whole, so the kept volume
    # and the ball differ only inside the leaves that meet the sphere.
    ball = 4 / 3 * math.pi * float(r2) ** 1.5
    band = sum(t.width(b[0]) ** 3 for b in t.leaves if meets_sphere(t.lower(b), t.width(b[0]), center, F(r2)))
    assert abs(sum(vol_in) / 6 - ball) <= band


def test_cutting_gives_no_shape_guarantee():
    # The template bound does not survive the cut: thin pieces appear where the
    # sphere passes close to a vertex.
    vi, ti = stages(1)[3]
    worst = min(min(dihedral_angles_deg(*[vi[v] for v in tet])) for tet in ti)
    assert worst < 1.0


def test_split_prism_gives_three_positive_tetrahedra_and_the_min_vertex_diagonals():
    r = random.Random(7)
    pts = [(0, 0, 0), (4, 0, 0), (0, 4, 0), (1, 1, 5), (5, 1, 5), (1, 5, 5)]  # a slanted prism
    for _ in range(30):
        order = list(range(6))
        r.shuffle(order)
        rank = {v: order[v] for v in range(6)}
        out = split_prism((0, 1, 2), (3, 4, 5), key=lambda v: rank[v])
        vols = []
        for tet in out:
            o = orient3d(*[pts[v] for v in tet])
            assert o != 0
            vols.append(abs(o))
        # the three pieces fill the prism: six times its volume is 6 * area 8 * height 5
        assert sum(vols) == 240
        edges = {frozenset((a, b)) for tet in out for a in tet for b in tet if a != b}
        for q in [(0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]:
            m = min(q, key=lambda v: rank[v])
            j = q.index(m)
            assert frozenset((m, q[(j + 2) % 4])) in edges
            assert frozenset((q[(j + 1) % 4], q[(j + 3) % 4])) not in edges


def test_example_counts():
    t, verts, tets, inside, _ = stages(0)
    assert Counter(b[0] for b in t.leaves) == {3: 256, 2: 32}
    assert (len(verts), len(tets)) == (1777, 7680)
    assert (len(inside[0]), len(inside[1])) == (1395, 4656)
    f = ball_values(verts, (8, 8, 8), F(91, 3))
    assert Counter(sum(1 for v in tet if f[v] > 0) for tet in tets) == {0: 4848, 1: 576, 2: 384, 3: 528, 4: 1344}
    vi, ti = inside
    worst = min(min(dihedral_angles_deg(*[vi[v] for v in tet])) for tet in ti)
    assert worst == pytest.approx(1.8923, abs=1e-4)
    assert sum(orient3d(*[vi[v] for v in tet]) for tet in ti) / 6 == pytest.approx(673.5244, abs=1e-4)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        octree_mesh((8, 8, 8), 36, 3)  # the sphere passes through the vertex (14, 8, 8)
    with pytest.raises(ValueError):
        octree_mesh((2, 8, 8), F(91, 3), 3)  # the ball leaves the root cube
    with pytest.raises(ValueError):
        octree_mesh((8, 8, 8), 5, 0)
