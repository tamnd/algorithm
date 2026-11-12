# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/butterfly-subdivision/. The authors are listed in prov/SBR69E.jsonl.

import math
import random
from fractions import Fraction

import pytest

from butterfly_subdivision import (
    butterfly_stencil,
    butterfly_subdivision,
    euler_characteristic,
    half_edges,
    ring,
    zss_weights,
)

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


ALL = [tetrahedron(), octahedron(), bipyramid(5), bipyramid(8), torus(3, 3), torus(4, 5)]


def test_octahedron_example():
    v, f = octahedron()
    pts, nf = butterfly_subdivision(v, f)
    assert counts(pts, nf) == (18, 48, 32)
    assert pts[:6] == [tuple(p) for p in v]
    # Edge 0-2: c = 4, d = 5, and the wings are 1, 3, 3, 1.
    assert butterfly_stencil(half_edges(f), 0, 2) == {0: F(1, 2), 2: F(1, 2), 4: F(1, 8), 5: F(1, 8), 1: F(-1, 8), 3: F(-1, 8)}
    assert pts[6] == (F(5, 8), F(5, 8), F(0))
    assert butterfly_subdivision(v, f, modified=True)[0][6] == (F(5, 8), F(5, 8), F(0))


def test_interpolation_and_counts():
    rng = random.Random(1)
    for verts, faces in ALL:
        verts = [tuple(F(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(3)) for _ in verts]
        v, e, f = counts(verts, faces)
        for modified in (False, True):
            pts, nf = butterfly_subdivision(verts, faces, modified=modified)
            assert pts[:v] == verts
            assert counts(pts, nf) == (v + e, 2 * e + 3 * f, 4 * f)
            assert euler_characteristic(nf) == euler_characteristic(faces)
            half_edges(nf)
            pts2, nf2 = butterfly_subdivision(pts, nf, modified=modified)
            assert pts2[: v + e] == pts
            assert euler_characteristic(nf2) == euler_characteristic(faces)


def test_exact_weights_on_regular_mesh():
    _, faces = torus(6, 6)
    u = unit_positions(36)
    pts, _ = butterfly_subdivision(u, faces)
    half = half_edges(faces)
    edges = sorted(e for e in half if e[0] < e[1])
    for k, (a, b) in enumerate(edges):
        p = pts[36 + k]
        c, d = half[(a, b)], half[(b, a)]
        assert p[a] == p[b] == F(1, 2) and p[c] == p[d] == F(1, 8)
        others = sorted(x for i, x in enumerate(p) if i not in (a, b, c, d) and x)
        assert others == [F(-1, 16)] * 4
        assert sum(p) == 1


def test_zss_weights():
    assert zss_weights(3) == [F(5, 12), F(-1, 12), F(-1, 12)]
    assert zss_weights(4) == [F(3, 8), 0, F(-1, 8), 0]
    assert zss_weights(6) == [F(7, 24), F(1, 12), F(-1, 12), F(-1, 24), F(-1, 12), F(1, 12)]
    for k in range(3, 12):
        assert math.isclose(sum(zss_weights(k)), 0.25)
    s5 = zss_weights(5)
    assert math.isclose(s5[1], (0.25 + math.cos(2 * math.pi / 5) + 0.5 * math.cos(4 * math.pi / 5)) / 5)


def test_modified_rule_by_hand():
    v, f = octahedron()
    u = unit_positions(6)
    pts, _ = butterfly_subdivision(u, f, modified=True)
    half = half_edges(f)
    # Valence 4 at both ends: the average of 3/4 v + 3/8 u_0 - 1/8 u_2 from each end.
    assert ring(half, 0, 2)[2] == 3 and ring(half, 2, 0)[2] == 1
    assert pts[6] == (F(9, 16), F(-1, 16), F(9, 16), F(-1, 16), F(0), F(0))
    # A regular mesh: the modified rule is the butterfly rule.
    verts, faces = torus(6, 7)
    assert butterfly_subdivision(verts, faces, modified=True) == butterfly_subdivision(verts, faces)
    # One extraordinary end: the stencil of that end only.
    verts, faces = bipyramid(6)
    half = half_edges(faces)
    u = unit_positions(len(verts))
    pts, _ = butterfly_subdivision(u, faces, modified=True)
    edges = sorted(e for e in half if e[0] < e[1])
    k = edges.index((0, 6))
    r = ring(half, 0, 6)
    assert len(r) == 4 and len(ring(half, 6, 0)) == 6
    want = [F(0)] * 8
    want[0] = F(3, 4)
    for x, s in zip(r, zss_weights(4)):
        want[x] += s
    assert pts[8 + k] == tuple(want)


def cubic(rng):
    cs = {(i, j): F(rng.randint(-5, 5), rng.randint(1, 3)) for i in range(4) for j in range(4 - i)}
    return lambda x, y: sum(c * x**i * y**j for (i, j), c in cs.items())


def test_reproduces_cubics_on_regular_mesh():
    rng = random.Random(2)
    n = m = 9
    _, faces = torus(n, m)
    half = half_edges(faces)
    edges = sorted(e for e in half if e[0] < e[1])
    inner = [k for k, (a, b) in enumerate(edges) if all(2 <= t <= 6 for x in (a, b) for t in divmod(x, m))]
    assert len(inner) > 40
    def mid(k):
        (ia, ja), (ib, jb) = divmod(edges[k][0], m), divmod(edges[k][1], m)
        return F(ia + ib, 2), F(ja + jb, 2)

    def exact_on_inner_edges(p, w=F(1, 16)):
        vals = [(F(p(F(i), F(j))),) for i in range(n) for j in range(m)]
        pts, _ = butterfly_subdivision(vals, faces, w=w)
        return all(pts[n * m + k] == (p(*mid(k)),) for k in inner)

    for _ in range(40):
        assert exact_on_inner_edges(cubic(rng))
    # Not a quartic, and not a cubic with another tension.
    assert not exact_on_inner_edges(lambda x, y: x * x * y * y)
    assert not exact_on_inner_edges(lambda x, y: x**3, w=0)
    assert exact_on_inner_edges(lambda x, y: x + 2 * y, w=0)


def test_random_positions_against_stencils():
    rng = random.Random(3)
    meshes = [tetrahedron(), octahedron(), bipyramid(5), torus(3, 4), butterfly_subdivision(*octahedron())]
    for _ in range(200):
        _, faces = meshes[rng.randrange(len(meshes))]
        half = half_edges(faces)
        nv = 1 + max(x for f in faces for x in f)
        verts = [tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(2)) for _ in range(nv)]
        pts, _ = butterfly_subdivision(verts, faces)
        for k, (a, b) in enumerate(sorted(e for e in half if e[0] < e[1])):
            c, d = half[(a, b)], half[(b, a)]
            e, f, g, h = half[(c, b)], half[(a, c)], half[(d, a)], half[(b, d)]
            want = tuple(F(1, 2) * (verts[a][t] + verts[b][t]) + F(1, 8) * (verts[c][t] + verts[d][t]) - F(1, 16) * (verts[e][t] + verts[f][t] + verts[g][t] + verts[h][t]) for t in range(2))
            assert pts[nv + k] == want


def test_rejects_bad_meshes():
    with pytest.raises(ValueError):
        butterfly_subdivision([(0, 0), (1, 0), (0, 1)], [[0, 1, 2]])
    with pytest.raises(ValueError):
        butterfly_subdivision([(0, 0), (1, 0), (0, 1), (1, 1)], [[0, 1, 2, 3], [3, 2, 1, 0]])
