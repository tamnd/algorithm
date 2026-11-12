# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doo-sabin-subdivision/. The authors are listed in prov/4NCX83.jsonl.

import math
import random
from fractions import Fraction

import pytest

from doo_sabin_subdivision import cos_turn, doo_sabin, doo_sabin_weights, euler_characteristic, half_edges

F = Fraction

# The weights by hand: a_0 = 1/4 + 5/(4k), a_i = (3 + 2 cos(2 pi i / k)) / (4k).
HAND = {
    3: [F(2, 3), F(1, 6), F(1, 6)],
    4: [F(9, 16), F(3, 16), F(1, 16), F(3, 16)],
    6: [F(11, 24), F(1, 6), F(1, 12), F(1, 24), F(1, 12), F(1, 6)],
}


def tetrahedron():
    return [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]


def cube():
    v = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    return v, [[0, 1, 3, 2], [4, 6, 7, 5], [0, 4, 5, 1], [2, 3, 7, 6], [0, 2, 6, 4], [1, 5, 7, 3]]


def prism():
    v = [(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (2, 0, 2), (0, 2, 2)]
    return v, [[0, 2, 1], [3, 4, 5], [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]]


def bipyramid(k):
    v = [(i, i * i % 7, 0) for i in range(k)] + [(0, 0, 5), (0, 0, -5)]
    faces = []
    for i in range(k):
        j = (i + 1) % k
        faces += [[i, j, k], [j, i, k + 1]]
    return v, faces


def torus(n, m, tri=False):
    idx = lambda i, j: (i % n) * m + (j % m)
    v = [(i, j, (i * j) % 3) for i in range(n) for j in range(m)]
    faces = []
    for i in range(n):
        for j in range(m):
            a, b, c, d = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            faces += [[a, b, c], [a, c, d]] if tri else [[a, b, c, d]]
    return v, faces


def counts(verts, faces):
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts), len(edges), len(faces)


def unit_positions(nv):
    return [tuple(F(int(i == j)) for j in range(nv)) for i in range(nv)]


def reference_points(verts, faces):
    """The new corner points by the hand weights, for faces with 3, 4 or 6 sides."""
    out = []
    for f in faces:
        k = len(f)
        for i in range(k):
            out.append(tuple(sum((HAND[k][(j - i) % k] * verts[f[j]][c] for j in range(k)), F(0)) for c in range(len(verts[0]))))
    return out


ALL = [tetrahedron(), cube(), prism(), bipyramid(5), torus(3, 4), torus(3, 3, tri=True)]


def test_weights_by_hand():
    for k, w in HAND.items():
        assert doo_sabin_weights(k) == w
        assert sum(w) == 1
    s5 = math.sqrt(5)
    w5 = doo_sabin_weights(5)
    assert math.isclose(w5[0], 0.5)
    assert math.isclose(w5[1], (3 + (s5 - 1) / 2) / 20)
    assert math.isclose(w5[2], (3 - (s5 + 1) / 2) / 20)
    assert math.isclose(sum(w5), 1)
    assert cos_turn(1, 6) == F(1, 2) and cos_turn(7, 4) == 0


def test_quad_rule_is_the_simple_average():
    # For a quad, the new point is the average of the corner, the centroid and the two edge midpoints.
    rng = random.Random(1)
    for _ in range(100):
        q = [tuple(F(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(3)) for _ in range(4)]
        pts, _ = doo_sabin(q, [[0, 1, 2, 3], [3, 2, 1, 0]])
        for i in range(4):
            v, a, b = q[i], q[(i + 1) % 4], q[i - 1]
            c = tuple(sum(x) / 4 for x in zip(*q))
            simple = tuple((v[t] + c[t] + (v[t] + a[t]) / 2 + (v[t] + b[t]) / 2) / 4 for t in range(3))
            assert pts[i] == simple


def test_cube_example():
    v, f = cube()
    pts, nf = doo_sabin(v, f)
    assert counts(pts, nf) == (24, 48, 26)
    # Corner (-1, -1, -1) of the face x = -1.
    assert pts[0] == (F(-1), F(-1, 2), F(-1, 2))
    assert sorted(len(x) for x in nf) == [3] * 8 + [4] * 18


def test_counts_and_euler_characteristic():
    for verts, faces in ALL:
        v, e, f = counts(verts, faces)
        pts, nf = doo_sabin(verts, faces)
        assert counts(pts, nf) == (2 * e, 4 * e, f + e + v)
        assert euler_characteristic(nf) == euler_characteristic(faces)
        half_edges(nf)
        pts2, nf2 = doo_sabin(pts, nf)
        assert euler_characteristic(nf2) == euler_characteristic(faces)
        half_edges(nf2)


def test_exact_stencils_on_meshes():
    for verts, faces in [cube(), tetrahedron(), prism(), torus(3, 3, tri=True), doo_sabin(*torus(3, 3, tri=True))]:
        if any(len(f) not in HAND for f in faces):
            continue
        u = unit_positions(len(verts))
        assert doo_sabin(u, faces)[0] == reference_points(u, faces)


def test_random_positions_against_hand_weights():
    rng = random.Random(2)
    meshes = [cube(), tetrahedron(), prism(), torus(3, 4), torus(3, 3, tri=True), doo_sabin(*cube())]
    for _ in range(200):
        _, faces = meshes[rng.randrange(len(meshes))]
        nv = 1 + max(x for f in faces for x in f)
        d = rng.randint(1, 3)
        verts = [tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(d)) for _ in range(nv)]
        assert doo_sabin(verts, faces)[0] == reference_points(verts, faces)


def chaikin_rows(grid):
    n = len(grid)
    out = []
    for i in range(n):
        a, b = grid[i], grid[(i + 1) % n]
        out.append([3 * x / F(4) + y / F(4) for x, y in zip(a, b)])
        out.append([x / F(4) + 3 * y / F(4) for x, y in zip(a, b)])
    return out


def test_regular_torus_is_biquadratic_chaikin():
    rng = random.Random(3)
    for _ in range(300):
        n, m = rng.randint(3, 4), rng.randint(3, 5)
        _, faces = torus(n, m)
        vals = [F(rng.randint(-50, 50), rng.randint(1, 4)) for _ in range(n * m)]
        pts, nf = doo_sabin([(x,) for x in vals], faces)
        grid = [[vals[i * m + j] for j in range(m)] for i in range(n)]
        fine = chaikin_rows(grid)
        fine = [list(r) for r in zip(*chaikin_rows([list(c) for c in zip(*fine)]))]
        coord = {}
        for fi in range(n * m):
            i, j = divmod(fi, m)
            for c, (a, b) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
                coord[4 * fi + c] = (2 * i + a, 2 * j + b)
        for k, p in enumerate(pts):
            r, c = coord[k]
            assert p == (fine[r][c],)
        N, M = 2 * n, 2 * m
        cells = {frozenset(((r % N, c % M), ((r + 1) % N, c % M), ((r + 1) % N, (c + 1) % M), (r % N, (c + 1) % M))) for r in range(N) for c in range(M)}
        assert {frozenset(coord[x] for x in q) for q in nf} == cells


def test_pentagon_faces_use_floats():
    once, faces1 = doo_sabin(*bipyramid(5))
    pts, nf = doo_sabin(once, faces1)
    pent = [fi for fi, f in enumerate(faces1) if len(f) == 5]
    assert len(pent) == 2
    start = sum(len(f) for f in faces1[: pent[0]])
    assert all(isinstance(c, float) for p in pts[start : start + 5] for c in p)
    assert euler_characteristic(nf) == 2
    assert sorted({len(f) for f in nf}) == [3, 4, 5]


def test_rejects_open_meshes():
    with pytest.raises(ValueError):
        doo_sabin([(0, 0), (1, 0), (0, 1)], [[0, 1, 2]])
    with pytest.raises(ValueError):
        doo_sabin([(0, 0), (1, 0), (0, 1), (5, 5)], [[0, 1, 2], [2, 1, 0]])
