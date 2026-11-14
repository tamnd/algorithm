# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boundary-recovery/. The authors are listed in prov/NKFBHW.jsonl.

import math
import random
from fractions import Fraction as F
from itertools import combinations

import pytest

from boundary_recovery import (
    add,
    check_complex,
    dist2,
    dot,
    edge_protect,
    edges_of,
    inside_polyhedron,
    lfs2,
    orient,
    scale,
    schonhardt,
    strongly_delaunay,
    strongly_delaunay_brute,
    sub,
)

EXAMPLE_P = [(0, 0, 0), (20, 0, 0), (16, 12, 0), (10, -3, 1), (10, 3, 1), (10, -3, -1), (10, 3, -1)]
EXAMPLE_S = [(0, 1), (0, 2), (3, 4), (5, 6)]


def random_complex(rng, nv=6, ne=7, span=20):
    while True:
        P = [tuple(rng.randint(-span, span) for _ in range(3)) for _ in range(nv)]
        S = set()
        while len(S) < ne:
            i, j = rng.sample(range(nv), 2)
            S.add((min(i, j), max(i, j)))
        S = sorted(S)
        try:
            check_complex(P, S)
        except ValueError:
            continue
        return P, S


def test_strongly_delaunay_matches_brute_force():
    rng = random.Random(1)
    seen = {True: 0, False: 0}
    for _ in range(400):
        k = rng.randint(2, 7)
        P = [tuple(rng.randint(-3, 3) for _ in range(3)) for _ in range(k)]
        if P[0] == P[1]:
            continue
        got = strongly_delaunay(P[0], P[1], P)
        assert (got is not None) == strongly_delaunay_brute(P[0], P[1], P)
        seen[got is not None] += 1
        if got is not None:  # the witness is a certificate
            r2 = dist2(got, P[0])
            assert dist2(got, P[1]) == r2
            assert all(dist2(got, p) > r2 for p in P if p not in (P[0], P[1]))
    assert seen[True] > 50 and seen[False] > 5


def test_cube_edges_and_diagonals():
    cube = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    # an edge: its diametral sphere already has the other six vertices outside
    assert strongly_delaunay((0, 0, 0), (1, 0, 0), cube) is not None
    # a face diagonal is Delaunay (the circumsphere of the cube) but not strongly
    assert strongly_delaunay((0, 0, 0), (1, 1, 0), cube) is None
    assert strongly_delaunay_brute((0, 0, 0), (1, 1, 0), cube) is False
    # a long diagonal is not even Delaunay
    assert strongly_delaunay((0, 0, 0), (1, 1, 1), cube) is None


def test_collinear_points():
    a, b = (0, 0, 0), (4, 0, 0)
    assert strongly_delaunay(a, b, [a, b, (2, 0, 0)]) is None  # a point inside ab
    assert strongly_delaunay(a, b, [a, b, (5, 0, 0), (-1, 0, 0)]) is not None


def test_worked_example():
    P, S = EXAMPLE_P, EXAMPLE_S
    assert strongly_delaunay(P[0], P[1], P) is None
    for i, j in S[1:]:
        assert strongly_delaunay(P[i], P[j], P) is not None
    pr = edge_protect(P, S)
    assert pr.radii2 == {0: F(400, 9)}  # r = min(lfs, l/3, 2d/3) = 20/3
    xs = [pr.points[i] for i in pr.chains[0]]
    assert xs == [(0, 0, 0), (F(20, 3), 0, 0), (10, 0, 0), (F(40, 3), 0, 0), (20, 0, 0)]
    assert [pr.points[i] for i in pr.chains[1]] == [(0, 0, 0), (F(16, 3), 4, 0), (16, 12, 0)]
    assert pr.chains[2] == [3, 4] and pr.chains[3] == [5, 6]
    assert pr.stats == {"step1": 2, "step2": 2}
    assert lfs2(P[0], P, S) == 101


def _check_protection(P, S, pr):
    sub_segs = pr.subsegments()
    # every subsegment is strongly Delaunay with respect to all the vertices
    for i, j in sub_segs:
        assert strongly_delaunay(pr.points[i], pr.points[j], pr.points) is not None
    # the cut-off ends are never split, and their diametral balls are empty
    present = set(sub_segs)
    for i, j in pr.ends:
        assert (i, j) in present
        m = scale(F(1, 2), add(pr.points[i], pr.points[j]))
        r2 = dist2(m, pr.points[i])
        assert all(dist2(m, p) > r2 for k, p in enumerate(pr.points) if k not in (i, j))
    # Steiner points lie in order on their segments
    for (u, v), chain in zip(S, pr.chains):
        a, b = pr.points[u], pr.points[v]
        ts = []
        for k in chain:
            d = sub(pr.points[k], a)
            t = F(dot(d, sub(b, a))) / dist2(a, b)
            assert add(a, scale(t, sub(b, a))) == pr.points[k]
            ts.append(t)
        assert ts == sorted(ts) and ts[0] == 0 and ts[-1] == 1 and len(set(ts)) == len(ts)


def _worst_ratio(P, S, pr, samples=4):
    """min over subsegments s and sample points u of |s|^2 / lfs(u)^2."""
    worst = None
    for i, j in pr.subsegments():
        a, b = pr.points[i], pr.points[j]
        s2 = dist2(a, b)
        for k in range(samples + 1):
            u = add(a, scale(F(k, samples), sub(b, a)))
            r = s2 / lfs2(u, P, S)
            worst = r if worst is None or r < worst else worst
    return worst


def test_theorem_2_bound_on_example():
    pr = edge_protect(EXAMPLE_P, EXAMPLE_S)
    _check_protection(EXAMPLE_P, EXAMPLE_S, pr)
    # proved: |s| >= lfs(u)/4; here the worst ratio |s|/lfs(u) is (20/3)/sqrt(101),
    # at the corner O of the end cut off there
    w = _worst_ratio(EXAMPLE_P, EXAMPLE_S, pr, samples=8)
    assert w == F(400, 909)


def test_random_complexes():
    rng = random.Random(7)
    worst = 1.0
    for _ in range(10):
        P, S = random_complex(rng)
        pr = edge_protect(P, S)
        _check_protection(P, S, pr)
        w = _worst_ratio(P, S, pr)
        assert w >= F(1, 16) * (1 - F(1, 10 ** 9))
        worst = min(worst, math.sqrt(w))
    assert worst > 0.25


def test_parallel_segments_need_nothing():
    # two parallel segments 1 apart: a large sphere bulging away clears each one
    P = [(0, 0, 0), (40, 0, 0), (0, 1, 0), (40, 1, 0)]
    pr = edge_protect(P, [(0, 1), (2, 3)])
    assert pr.stats == {"step1": 0, "step2": 0}


def test_closer_crossings_need_more_points():
    counts = []
    for k, h in ((3, 8), (3, 4), (3, 2), (1, 1)):
        P = [(0, 0, 0), (64, 0, 0), (21, -k, h), (21, k, h), (21, -k, -h), (21, k, -h)]
        S = [(0, 1), (2, 3), (4, 5)]
        pr = edge_protect(P, S)
        _check_protection(P, S, pr)
        assert _worst_ratio(P, S, pr) >= F(1, 16)
        counts.append(pr.stats["step2"])
    assert counts == [2, 3, 4, 5]


def _schonhardt_volume(pts, faces):
    o = (0, 0, 0)
    return sum(orient(pts[a], pts[b], pts[c], o) for a, b, c in faces)


def test_schonhardt_has_no_tetrahedralization():
    for twist in (10, 30, 50):
        pts, faces, reflex, outside = schonhardt(twist=twist)
        E = edges_of(faces)
        assert len(faces) == 8 and len(E) == 12
        assert set(map(tuple, map(sorted, reflex))) <= E
        # the three remaining pairs leave the polyhedron
        for p, q in outside:
            assert tuple(sorted((p, q))) not in E
            m = scale(F(1, 2), add(pts[p], pts[q]))
            assert not inside_polyhedron(m, pts, faces)
        # so every one of the 15 tetrahedra has an edge outside the polyhedron
        bad = {tuple(sorted(o)) for o in outside}
        for quad in combinations(range(6), 4):
            assert any(tuple(sorted(e)) in bad for e in combinations(quad, 2))
        # one Steiner point at the centroid sees all eight faces
        c = tuple(F(sum(p[i] for p in pts), 6) for i in range(3))
        assert inside_polyhedron(c, pts, faces)
        vols = [-orient(pts[a], pts[b], pts[cc], c) for a, b, cc in faces]
        assert all(v > 0 for v in vols)
        assert sum(vols) == -_schonhardt_volume(pts, faces)


def test_schonhardt_reflex_edges_never_all_strongly_delaunay():
    rng = random.Random(3)
    counts = set()
    for _ in range(40):
        pts, faces, reflex, _ = schonhardt(twist=rng.randint(8, 50), h=rng.randint(40, 200))
        pts = [tuple(x + rng.randint(-3, 3) for x in p) for p in pts]
        k = sum(strongly_delaunay(pts[a], pts[b], pts) is not None for a, b in reflex)
        counts.add(k)
        assert k <= 2
    assert 2 in counts  # Shewchuk: any two may be strongly Delaunay


def test_schonhardt_edge_protection():
    pts, faces, reflex, _ = schonhardt()
    S = sorted(edges_of(faces))
    pr = edge_protect(pts, S)
    _check_protection(pts, S, pr)
    assert pr.stats["step1"] == 24


def test_bad_input():
    with pytest.raises(ValueError):
        check_complex([(0, 0, 0), (1, 0, 0), (2, 0, 0)], [(0, 2)])  # vertex inside
    with pytest.raises(ValueError):
        check_complex([(0, 0, 0), (2, 0, 0), (1, -1, 0), (1, 1, 0)], [(0, 1), (2, 3)])  # crossing
    with pytest.raises(ValueError):
        check_complex([(0, 0, 0), (1, 0, 0), (2, 0, 0)], [(0, 1), (0, 2)])  # overlap
    with pytest.raises(ValueError):
        check_complex([(0, 0, 0), (0, 0, 0)], [(0, 1)])
    with pytest.raises(ValueError):
        check_complex([(0, 0, 0), (1, 0, 0)], [(0, 1), (1, 0)])
    with pytest.raises(RuntimeError):
        edge_protect([(0, 0, 0), (64, 0, 0), (21, -1, 1), (21, 1, 1), (21, -1, -1), (21, 1, -1)],
                     [(0, 1), (2, 3), (4, 5)], max_points=8)
