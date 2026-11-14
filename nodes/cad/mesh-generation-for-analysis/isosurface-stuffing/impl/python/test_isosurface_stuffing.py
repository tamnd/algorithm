# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isosurface-stuffing/. The authors are listed in prov/B7WM22.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache

import pytest

from isosurface_stuffing import (
    DIHEDRAL_MAX,
    DIHEDRAL_MIN,
    Stuffing,
    bcc_tetrahedra,
    is_black,
    isosurface_stuffing,
    split_prism,
)
from mg2geom import circumcenter3, dihedral_angles_deg, dist2, insphere, orient3d, radius_edge2


def random_ball(seed):
    r = random.Random(seed)
    center = tuple(F(r.randint(-500, 500), 1000) for _ in range(3))
    r2 = F(r.randint(300, 1500), 1000)
    h = F(1, r.randint(3, 5))
    return center, r2, h


CASES = [
    ((F(3, 100), F(-2, 100), F(1, 100)), F(1), F(1, 4)),  # the example of the page
    ((0, 0, 0), F(1), F(1, 4)),  # lattice points lie exactly on the sphere
    random_ball(1),
    random_ball(2),
]


@lru_cache(maxsize=None)
def run(i):
    center, r2, h = CASES[i]
    return isosurface_stuffing(center, r2, h)


def lattice(lo, hi):
    return {(i, j, k) for i in range(lo, hi + 1) for j in range(lo, hi + 1) for k in range(lo, hi + 1) if i % 2 == j % 2 == k % 2}


# The BCC tetrahedron, in doubled coordinates: black edges (0,0,0)-(2,0,0) and (1,1,1)-(1,-1,1).
BCC = ((0, 0, 0), (2, 0, 0), (1, 1, 1), (1, -1, 1))


def test_bcc_tetrahedron_shape():
    d = dihedral_angles_deg(*BCC)
    # pairs in the order 01, 02, 03, 12, 13, 23; the black edges are 01 and 23
    assert d[0] == pytest.approx(90) and d[5] == pytest.approx(90)
    assert all(x == pytest.approx(60) for x in d[1:5])
    # six times the volume is 4 in doubled units, so the volume is 4 / 6 / 8 = 1/12 of h^3
    assert orient3d(*BCC) == 4
    assert F(orient3d(*BCC), 6 * 8) == F(1, 12)
    # circumcenter (1/2, 0, 1/4) h, R^2 = 5/16 h^2, shortest edge sqrt(3)/2 h
    cc = circumcenter3(*BCC)
    assert tuple(x / 2 for x in cc) == (F(1, 2), 0, F(1, 4))
    assert dist2(cc, BCC[0]) / 4 == F(5, 16)
    assert radius_edge2(*BCC) == F(5, 12)


def test_bcc_circumsphere_is_strictly_empty():
    others = lattice(-6, 8) - set(BCC)
    worst = max(insphere(*BCC, p) for p in others)
    assert worst < 0  # no other lattice point is inside or on the sphere
    assert worst == -8  # -1/4 for h = 1; doubling the coordinates multiplies it by 2^5
    # the same fact as a margin: the nearest other lattice point is at squared distance
    # 13/16 h^2 from the circumcenter, against R^2 = 5/16 h^2
    cc = circumcenter3(*BCC)
    assert min(dist2(p, cc) for p in others) / 4 == F(13, 16)


def test_bcc_tetrahedra_tile_space():
    pts = lattice(-2, 10)
    tets = bcc_tetrahedra(pts)
    # every cubic lattice point away from the border starts 3 black edges with 4 tetrahedra each
    per_point = Counter(t[0] for t in tets)
    assert all(per_point[p] == 12 for p in lattice(0, 6) if p[0] % 2 == 0)
    # 12 tetrahedra of volume 1/12 per unit cell: the volume is right; now check no overlap
    # and no gap by locating random points (brute force over all tetrahedra)
    r = random.Random(3)
    boxes = []
    for t in tets:
        lo = tuple(min(p[a] for p in t) for a in range(3))
        hi = tuple(max(p[a] for p in t) for a in range(3))
        boxes.append((lo, hi, t if orient3d(*t) > 0 else (t[1], t[0], t[2], t[3])))
    for _ in range(150):
        x = tuple(F(r.randint(3000, 5000), 1000) + F(1, 7919) for _ in range(3))
        hits = 0
        for lo, hi, (a, b, c, d) in boxes:
            if all(lo[k] <= x[k] <= hi[k] for k in range(3)):
                if orient3d(x, b, c, d) > 0 and orient3d(a, x, c, d) > 0 and orient3d(a, b, x, d) > 0 and orient3d(a, b, c, x) > 0:
                    hits += 1
        assert hits == 1, x


def test_parity_rule_is_the_same_from_both_sides():
    s = Stuffing((0, 0, 0), 1, 1)
    pts = lattice(-2, 4)
    n = 0
    for a in pts:
        for b in pts:
            if not (a < b and dist2(a, b) in (3, 4)):
                continue
            for x in pts:
                if dist2(a, x) in (3, 4) and dist2(b, x) in (3, 4) and x not in (a, b):
                    # a BCC triangle: one black edge and two red edges
                    assert sum(is_black(p, q) for p, q in ((a, b), (a, x), (b, x))) == 1
                    assert s.quad_diagonal(a, b, x) == s.quad_diagonal(b, a, x)
                    n += 1
    assert n > 1000


def test_split_prism():
    pts = {"b0": (0, 0, 0), "b1": (6, 0, 0), "b2": (0, 6, 0), "t0": (1, 1, 5), "t1": (7, 1, 5), "t2": (1, 7, 5)}
    bottom, top = ("b0", "b1", "b2"), ("t0", "t1", "t2")
    quads = [(bottom[i], bottom[(i + 1) % 3], top[(i + 1) % 3], top[i]) for i in range(3)]
    for mask in range(8):
        diags = [frozenset((q[0], q[2])) if mask >> i & 1 else frozenset((q[1], q[3])) for i, q in enumerate(quads)]
        deg = Counter(v for g in diags for v in g)
        if max(deg.values()) < 2:
            with pytest.raises(ValueError):
                split_prism(bottom, top, diags)
            continue
        out = split_prism(bottom, top, diags)
        assert sum(abs(orient3d(*[pts[v] for v in t])) for t in out) == 6 * 18 * 5
        edges = {frozenset((a, b)) for t in out for a in t for b in t if a != b}
        for g, q in zip(diags, quads):
            assert g in edges and frozenset(set(q) - g) not in edges


def faces(tets):
    c = Counter()
    for a, b, cc, d in tets:
        for tri in ((b, cc, d), (a, d, cc), (a, b, d), (a, cc, b)):
            i = tri.index(min(tri))
            c[tri[i:] + tri[:i]] += 1
    return c


@pytest.mark.parametrize("i", range(len(CASES)))
def test_mesh_of_a_ball(i):
    state, verts, tets = run(i)
    center, r2, h = CASES[i]
    f = state.f
    # every tetrahedron has positive volume in the warped (final) geometry, by an exact test
    vols = [orient3d(*[verts[v] for v in t]) for t in tets]
    assert all(v > 0 for v in vols)
    # the stated dihedral bounds of Table 1 hold on every tetrahedron
    for t in tets:
        d = dihedral_angles_deg(*[verts[v] for v in t])
        assert DIHEDRAL_MIN <= min(d) and max(d) <= DIHEDRAL_MAX
    # face to face: every face is used once in each orientation, or once on the boundary
    c = faces(tets)
    tol = 1e-12 * float(r2)
    for tri, m in c.items():
        assert m == 1
        if (tri[0], tri[2], tri[1]) not in c:
            assert all(abs(float(f(verts[v]))) <= tol for v in tri)
    # no vertex leaves the closed ball, so no tetrahedron does
    assert all(float(f(p)) >= -tol for p in verts)
    # a lattice point deeper than the largest warp distance stays where it is, and the
    # BCC tetrahedra of such points are kept whole, so the mesh contains the ball of
    # radius r - 1.5 h; it lies in the ball of radius r
    r = math.sqrt(r2)
    vol = sum(vols) / 6
    assert 4 / 3 * math.pi * (r - 1.5 * float(h)) ** 3 < vol < 4 / 3 * math.pi * r**3


@pytest.mark.parametrize("i", range(len(CASES)))
def test_no_violation_is_left_after_warping(i):
    state = run(i)[0]
    for q in state.points:
        if q in state.warped:
            assert state.value[q] == 0
            assert abs(float(state.f(state.pos[q]))) <= 1e-12
            # it moved to a cut point on one of its own edges, within the alpha fraction
            r = state.warped[q]
            assert state.cut_param(q, r) < state.alpha[is_black(q, r)]
            continue
        assert state.pos[q] == state.orig[q]
        for r in state.neighbors(q):
            if state.has_cut(q, r):
                assert state.cut_param(q, r) >= state.alpha[is_black(q, r)]


def test_warping_is_what_removes_the_slivers():
    center, r2, h = CASES[0]
    _, verts, tets = isosurface_stuffing(center, r2, h, alpha_long=0, alpha_short=0)
    worst = min(min(dihedral_angles_deg(*[verts[v] for v in t])) for t in tets)
    assert worst < 1  # cutting the lattice without warping leaves a 0.17 degree sliver


def test_example_counts():
    state, verts, tets = run(0)
    assert len(state.points) == 3456
    assert sum(1 for p in state.points if state.f(state.orig[p]) > 0) == 544
    assert len(state.warped) == 242
    assert sum(is_black(q, r) for q, r in state.warped.items()) == 84
    assert (len(verts), len(tets)) == (834, 3546)
    d = [a for t in tets for a in dihedral_angles_deg(*[verts[v] for v in t])]
    assert min(d) == pytest.approx(19.0757, abs=1e-4)
    assert max(d) == pytest.approx(135.6767, abs=1e-4)
    vol = sum(orient3d(*[verts[v] for v in t]) for t in tets) / 6
    assert float(vol) == pytest.approx(4.1222, abs=1e-4)
    # the radius-edge ratio is not what the method bounds; it reaches about 2.2 here
    assert max(radius_edge2(*[verts[v] for v in t]) for t in tets) == pytest.approx(4.8936, abs=1e-4)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        isosurface_stuffing((0, 0, 0), 0, F(1, 4))
    with pytest.raises(ValueError):
        isosurface_stuffing((0, 0, 0), 1, 0)
