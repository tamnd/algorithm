# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loop-subdivision/. The authors are listed in prov/4625V7.jsonl.

import math
import random
from fractions import Fraction

import pytest

from loop_subdivision import euler_characteristic, half_edges, loop_beta, loop_subdivision

F = Fraction


def tetrahedron():
    return [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]


def octahedron():
    v = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    f = [[0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4], [2, 0, 5], [1, 2, 5], [3, 1, 5], [0, 3, 5]]
    return v, f


def bipyramid(k):
    v = [(i, i * i % 7, 0) for i in range(k)] + [(0, 0, 5), (0, 0, -5)]
    faces = []
    for i in range(k):
        j = (i + 1) % k
        faces += [[i, j, k], [j, i, k + 1]]
    return v, faces


def torus(n, m):
    idx = lambda i, j: (i % n) * m + (j % m)
    v = [(i, j, (i * j) % 3) for i in range(n) for j in range(m)]
    faces = []
    for i in range(n):
        for j in range(m):
            a, b, c, d = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            faces += [[a, b, c], [a, c, d]]
    return v, faces


def counts(verts, faces):
    edges = {frozenset((f[i], f[(i + 1) % 3])) for f in faces for i in range(3)}
    return len(verts), len(edges), len(faces)


def unit_positions(nv):
    return [tuple(F(int(i == j)) for j in range(nv)) for i in range(nv)]


def hand_reference(verts, faces, beta):
    """New points from the stencils written out by hand."""
    half = half_edges(faces)
    nv, d = len(verts), len(verts[0])
    nbrs = [sorted({b for (a, b) in half if a == v}) for v in range(nv)]
    out = []
    for v in range(nv):
        n = len(nbrs[v])
        b = beta[n]
        out.append(tuple((1 - n * b) * verts[v][k] + sum((b * verts[u][k] for u in nbrs[v]), F(0)) for k in range(d)))
    for a, b in sorted(e for e in half if e[0] < e[1]):
        c, e = half[(a, b)], half[(b, a)]
        out.append(tuple(F(3, 8) * verts[a][k] + F(3, 8) * verts[b][k] + F(1, 8) * verts[c][k] + F(1, 8) * verts[e][k] for k in range(d)))
    return out


HAND_BETA = {3: F(3, 16), 4: F(31, 256), 6: F(1, 16)}
ALL = [tetrahedron(), octahedron(), bipyramid(5), bipyramid(7), torus(3, 3), torus(4, 5)]


def test_beta_by_hand():
    for n, b in HAND_BETA.items():
        assert loop_beta(n) == b
    assert math.isclose(loop_beta(5), (5 / 8 - (3 / 8 + math.cos(2 * math.pi / 5) / 4) ** 2) / 5)
    assert loop_beta(3, "warren") == F(3, 16) and loop_beta(6, "warren") == F(1, 16) and loop_beta(5, "warren") == F(3, 40)
    with pytest.raises(ValueError):
        loop_beta(4, "other")


def test_tetrahedron_example():
    v, f = tetrahedron()
    pts, nf = loop_subdivision(v, f)
    assert counts(pts, nf) == (10, 24, 16)
    # Vertex rule: 7/16 of (1, 1, 1) plus 3/16 of each neighbor.
    assert pts[0] == (F(1, 4), F(1, 4), F(1, 4))
    # Edge 0-1: 3/8 (a + b) + 1/8 (c + d), with c = 2 and d = 3.
    assert pts[4] == (F(1, 2), F(0), F(0))


def test_counts_and_euler_characteristic():
    for verts, faces in ALL:
        v, e, f = counts(verts, faces)
        pts, nf = loop_subdivision(verts, faces)
        assert counts(pts, nf) == (v + e, 2 * e + 3 * f, 4 * f)
        assert euler_characteristic(nf) == euler_characteristic(faces)
        half_edges(nf)
        degrees = {}
        for t in nf:
            for x in t:
                degrees[x] = degrees.get(x, 0) + 1
        assert all(degrees[x] == 6 for x in range(v, v + e))


def test_exact_stencil_weights():
    for verts, faces in [tetrahedron(), octahedron(), torus(3, 4)]:
        u = unit_positions(len(verts))
        assert loop_subdivision(u, faces)[0] == hand_reference(u, faces, HAND_BETA)
    u = unit_positions(12)
    pts, _ = loop_subdivision(u, torus(3, 4)[1])
    assert pts[5][5] == F(5, 8) and sorted(x for x in pts[5] if x and x != F(5, 8)) == [F(1, 16)] * 6
    u = unit_positions(4)
    assert loop_subdivision(u, tetrahedron()[1])[0][0] == (F(7, 16), F(3, 16), F(3, 16), F(3, 16))
    u = unit_positions(6)
    assert loop_subdivision(u, octahedron()[1])[0][0][0] == F(33, 64)


def test_warren_rule():
    verts, faces = bipyramid(5)
    u = unit_positions(len(verts))
    pts, _ = loop_subdivision(u, faces, rule="warren")
    beta = {3: F(3, 16), 4: F(3, 32), 5: F(3, 40)}
    assert pts == hand_reference(u, faces, beta)


def test_random_positions_against_hand_stencils():
    rng = random.Random(1)
    meshes = [tetrahedron(), octahedron(), torus(3, 3), torus(3, 4), loop_subdivision(*octahedron())]
    for _ in range(250):
        _, faces = meshes[rng.randrange(len(meshes))]
        nv = 1 + max(x for f in faces for x in f)
        d = rng.randint(1, 3)
        verts = [tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(d)) for _ in range(nv)]
        assert loop_subdivision(verts, faces)[0] == hand_reference(verts, faces, HAND_BETA)


def test_limit_position_is_kept():
    # L(v) = (w v + sum of the neighbors) / (w + n) with w = 3 / (8 beta) is the same after a step.
    rng = random.Random(4)
    for _ in range(40):
        verts, faces = [tetrahedron(), octahedron(), torus(3, 4)][rng.randrange(3)]
        verts = [tuple(F(rng.randint(-9, 9)) for _ in range(3)) for _ in verts]
        pts, nf = loop_subdivision(verts, faces)
        half, half2 = half_edges(faces), half_edges(nf)
        for v in range(len(verts)):
            for p, h in [(verts, half), (pts, half2)]:
                ring = [b for (a, b) in h if a == v]
                n = len(ring)
                w = F(3, 8) / loop_beta(n)
                val = tuple((w * p[v][k] + sum(p[u][k] for u in ring)) / (w + n) for k in range(3))
                if p is verts:
                    before = val
            assert val == before
    v, f = tetrahedron()
    for _ in range(4):
        v, f = loop_subdivision(v, f)
    assert all(abs(x - 0.2) < 0.02 for x in v[0])


def box_spline_mask():
    """The mask of the quartic box spline with directions (1,0), (0,1), (1,1), each twice."""
    poly = {(0, 0): F(1, 16)}
    for d in [(1, 0), (1, 0), (0, 1), (0, 1), (1, 1), (1, 1)]:
        nxt = {}
        for (x, y), c in poly.items():
            for dx, dy in [(0, 0), d]:
                nxt[(x + dx, y + dy)] = nxt.get((x + dx, y + dy), 0) + c
        poly = nxt
    return poly


def test_regular_torus_is_box_spline_refinement():
    mask = box_spline_mask()
    assert sum(mask.values()) == 4 and mask[(2, 2)] == F(10, 16)
    rng = random.Random(2)
    for _ in range(250):
        n, m = rng.randint(3, 5), rng.randint(3, 5)
        _, faces = torus(n, m)
        vals = [F(rng.randint(-50, 50), rng.randint(1, 4)) for _ in range(n * m)]
        pts, nf = loop_subdivision([(x,) for x in vals], faces)
        N, M = 2 * n, 2 * m
        # fine[alpha] = sum over beta of a[alpha - 2 beta] p[beta], with the mask centered at (2, 2).
        fine = {(r, c): F(0) for r in range(N) for c in range(M)}
        for i in range(n):
            for j in range(m):
                for (dx, dy), w in mask.items():
                    fine[((2 * i + dx - 2) % N, (2 * j + dy - 2) % M)] += w * vals[i * m + j]
        coord = {i * m + j: (2 * i, 2 * j) for i in range(n) for j in range(m)}
        edges = sorted(e for e in half_edges(faces) if e[0] < e[1])
        for k, (a, b) in enumerate(edges):
            (ia, ja), (ib, jb) = divmod(a, m), divmod(b, m)
            for (p, q), (s, t) in [((ia, ja), (ib, jb)), ((ib, jb), (ia, ja))]:
                di, dj = (s - p) % n, (t - q) % m
                if (di, dj) in [(1, 0), (0, 1), (1, 1)]:
                    coord[n * m + k] = ((2 * p + di) % N, (2 * q + dj) % M)
        for k, p in enumerate(pts):
            assert p == (fine[coord[k]],)
