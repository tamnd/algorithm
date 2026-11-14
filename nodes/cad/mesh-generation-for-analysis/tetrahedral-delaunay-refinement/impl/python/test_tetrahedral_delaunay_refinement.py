# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetrahedral-delaunay-refinement/. The authors are listed in prov/VNAEW7.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache

import pytest

from mg2geom import dihedral_angles_deg, dist2, dot, insphere, orient3d, radius_edge2, sub, tri_circumcenter3
from tetrahedral_delaunay_refinement import SCALE, delaunay_refine

SIDES = (4, 3, 2)
EXAMPLE = ((1, 1, F(1, 2)), (F(5, 2), 2, 1))


def random_inner(seed, n):
    r = random.Random(seed)
    pts = set()
    while len(pts) < n:
        pts.add(tuple(F(r.randint(1, 4 * s - 1), 4) for s in SIDES))
    return tuple(sorted(pts))


CASES = [
    (SIDES, (), 2),
    (SIDES, EXAMPLE[:1], 2),
    ((3, 3, 3), ((1, 1, 1),), 2),
    (SIDES, EXAMPLE, 2),
    (SIDES, EXAMPLE, F(6, 5)),  # below the proved threshold: no guarantee, but it stops here
    (SIDES, random_inner(1, 4), 2),
    (SIDES, random_inner(2, 4), 2),
    (SIDES, random_inner(3, 3), 2),
]


@lru_cache(maxsize=None)
def run(i):
    sides, inner, B = CASES[i]
    return delaunay_refine(sides, inner, B)


def edges(tets):
    return {tuple(sorted((t[i], t[j]))) for t in tets for i in range(4) for j in range(i + 1, 4)}


def face_count(tets):
    return Counter(tuple(sorted(t[:k] + t[k + 1 :])) for t in tets for k in range(4))


def on_box(P, f, L):
    return any(all(P[v][k] == s for v in f) for k in range(3) for s in (0, L[k]))


def d_min(sides, inner):
    """The smallest distance between two input features that do not meet.

    For the box these are opposite faces (distance = side), an inner vertex and a
    face, or two inner vertices. Any ball that meets two such features has diameter
    at least this distance, so the local feature size is at least d_min / 2 everywhere.
    """
    d = [float(s) for s in sides]
    for p in inner:
        d += [float(min(F(p[k]), sides[k] - F(p[k]))) for k in range(3)]
        d += [math.sqrt(dist2(p, q)) for q in inner if q != p]
    return min(d)


@pytest.mark.parametrize("i", range(len(CASES)))
def test_delaunay_by_brute_force_and_radius_edge_bound(i):
    R = run(i)
    P = R.pts
    for t in R.tets:
        T = [P[v] for v in t]
        # empty circumsphere: no vertex of the mesh lies strictly inside, by the exact insphere test
        assert all(insphere(*T, p) <= 0 for p in P)
        # the quality goal: radius-edge ratio at most B, compared exactly as squares
        assert radius_edge2(*T) <= R.B2


@pytest.mark.parametrize("i", range(len(CASES)))
def test_conforming_mesh_of_the_box(i):
    R = run(i)
    P, L = R.pts, R.L
    vols = [orient3d(*[P[v] for v in t]) for t in R.tets]
    assert all(v > 0 for v in vols)
    assert sum(vols) == 6 * L[0] * L[1] * L[2]
    # face to face: an interior face lies in two tetrahedra, a boundary face in one, on the box
    for f, m in face_count(R.tets).items():
        assert m in (1, 2)
        assert (m == 1) == on_box(P, f, L)
    # every input vertex is a mesh vertex
    sides, inner, _ = CASES[i]
    for p in inner:
        assert tuple(int(F(x) * SCALE) for x in p) in P
    # the subsegments are mesh edges and cover the 12 box edges exactly
    E = edges(R.tets)
    assert set(R.subsegs) <= E
    length = Counter()
    for a, b in R.subsegs:
        d = sub(P[b], P[a])
        k = [j for j in range(3) if d[j] != 0]
        assert len(k) == 1
        length[k[0]] += abs(d[k[0]])
    assert [length[k] for k in range(3)] == [4 * L[k] for k in range(3)]


@pytest.mark.parametrize("i", range(len(CASES)))
def test_nothing_is_encroached_at_the_end(i):
    R = run(i)
    P, L = R.pts, R.L
    for a, b in R.subsegs:
        # closed diametral sphere: (p - a).(p - b) <= 0 means p is inside or on it
        assert all(dot(sub(p, P[a]), sub(p, P[b])) > 0 for p in P if p not in (P[a], P[b]))
    for f, m in face_count(R.tets).items():
        if m != 1:
            continue
        cc = tri_circumcenter3(*[P[v] for v in f])
        R2 = dist2(cc, P[f[0]])
        k = [k for k in range(3) if P[f[0]][k] == P[f[1]][k] == P[f[2]][k]][0]
        # closed equatorial sphere; vertices in the facet plane do not count
        assert all(dist2(p, cc) > R2 for p in P if p[k] != P[f[0]][k])


@pytest.mark.parametrize("i", [k for k in range(len(CASES)) if CASES[k][2] >= 2])
def test_edges_are_not_shorter_than_the_proved_bound(i):
    # For B = 2 every insertion radius is at least lfs_min / 2 >= d_min / 4.
    # Rounding to the 1/SCALE grid can cost at most a few grid units.
    R = run(i)
    sides, inner, _ = CASES[i]
    bound = d_min(sides, inner) / 4 * SCALE - 2
    for v, r2 in enumerate(R.r2):
        if r2 is not None:
            assert math.sqrt(r2) >= bound
    shortest = min(math.sqrt(dist2(R.pts[a], R.pts[b])) for a, b in edges(R.tets))
    assert shortest >= bound


def test_measured_spacing_is_far_better_than_the_bound():
    R = run(3)
    shortest = min(math.sqrt(dist2(R.pts[a], R.pts[b])) for a, b in edges(R.tets)) / SCALE
    bound = d_min(*CASES[3][:2]) / 4
    assert bound == 0.125
    assert shortest == pytest.approx(0.5599, abs=1e-4)
    assert shortest > 4 * bound


def test_a_sliver_has_a_small_radius_edge_ratio():
    # four points near the equator of the unit sphere: nearly flat, ratio near 1/sqrt(2)
    eps = F(1, 20)
    t = ((1, 0, 0), (-1, 0, 0), (0, 1, eps), (0, -1, eps))
    assert orient3d(*t) != 0
    assert radius_edge2(*t) < F(4, 7) < 4  # ratio below 0.76, far below B = 2
    d = dihedral_angles_deg(*t)
    assert min(d) < 6 and max(d) > 174


def test_slivers_survive_refinement():
    for i in (3, 4):
        R = run(i)
        P = R.pts
        worst = min(R.tets, key=lambda t: min(dihedral_angles_deg(*[P[v] for v in t])))
        W = [P[v] for v in worst]
        # it passes the radius-edge test, yet it is nearly flat
        assert radius_edge2(*W) <= R.B2
        assert min(dihedral_angles_deg(*W)) < 7
        assert max(dihedral_angles_deg(*W)) > 165


def test_example_counts():
    R = run(3)
    assert len(R.pts) == 33 and len(R.tets) == 66
    assert Counter(R.kind) == {"input": 10, "segment": 16, "facet": 7}
    d = [a for t in R.tets for a in dihedral_angles_deg(*[R.pts[v] for v in t])]
    assert min(d) == pytest.approx(6.3185, abs=1e-3)
    assert max(d) == pytest.approx(166.5462, abs=1e-3)
    R = run(4)
    assert len(R.pts) == 63 and len(R.tets) == 167
    assert Counter(R.kind)["tet"] == 4


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        delaunay_refine((4, 3, 0))
    with pytest.raises(ValueError):
        delaunay_refine(SIDES, B=F(1, 2))
    with pytest.raises(ValueError):
        delaunay_refine(SIDES, ((0, 1, 1),))  # on the boundary, not strictly inside
    with pytest.raises(RuntimeError):
        delaunay_refine(SIDES, EXAMPLE, F(6, 5), max_vertices=40)
