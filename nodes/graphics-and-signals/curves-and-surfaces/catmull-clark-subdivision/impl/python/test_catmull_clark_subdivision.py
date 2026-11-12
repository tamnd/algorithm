# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/catmull-clark-subdivision/. The authors are listed in prov/8H54E8.jsonl.

import random
from fractions import Fraction

import pytest

from catmull_clark_subdivision import catmull_clark, euler_characteristic, half_edges

F = Fraction


def tetrahedron():
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    return v, [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]


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
        faces.append([i, j, k])
        faces.append([j, i, k + 1])
    return v, faces


def torus(n, m):
    idx = lambda i, j: (i % n) * m + (j % m)
    v = [(i, j, (i * j) % 3) for i in range(n) for j in range(m)]
    faces = [[idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)] for i in range(n) for j in range(m)]
    return v, faces


def counts(verts, faces):
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    return len(verts), len(edges), len(faces)


def random_positions(rng, nv, d=3):
    return [tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(d)) for _ in range(nv)]


def unit_positions(nv):
    return [tuple(F(int(i == j)) for j in range(nv)) for i in range(nv)]


ALL = [tetrahedron(), cube(), prism(), bipyramid(5), bipyramid(7), torus(3, 4), torus(4, 5)]


def quad_meshes():
    out = [cube(), torus(3, 3), torus(4, 5)]
    for base in (tetrahedron(), prism(), bipyramid(5), bipyramid(6)):
        out.append(catmull_clark(*base))
    return out


def test_cube_example():
    v, f = cube()
    nv, nf = catmull_clark(v, f)
    assert counts(nv, nf) == (26, 48, 24)
    assert nv[7] == (F(5, 9), F(5, 9), F(5, 9))
    assert nv[0] == (F(-5, 9), F(-5, 9), F(-5, 9))
    edges = sorted((a, b) for a, b in half_edges(f) if a < b)
    assert nv[8 + edges.index((6, 7))] == (F(3, 4), F(3, 4), F(0))
    assert nv[8 + 12 + 1] == (F(1), F(0), F(0))


def test_counts_and_euler_characteristic():
    for verts, faces in ALL:
        v, e, f = counts(verts, faces)
        deg = sum(len(x) for x in faces)
        nv, nf = catmull_clark(verts, faces)
        assert counts(nv, nf) == (v + e + f, 2 * e + deg, deg)
        assert deg == 2 * e
        assert euler_characteristic(nf) == euler_characteristic(faces)
        assert all(len(q) == 4 for q in nf)
        half_edges(nf)
    assert euler_characteristic(torus(4, 5)[1]) == 0
    assert euler_characteristic(cube()[1]) == 2


def test_two_steps_of_tetrahedron():
    v, f = catmull_clark(*catmull_clark(*tetrahedron()))
    assert counts(v, f) == (50, 96, 48)
    assert euler_characteristic(f) == 2


def stencil_reference(verts, faces):
    """Expected positions on an all-quad mesh, from the stencils computed by hand."""
    half = half_edges(faces)
    nv = len(verts)
    nbrs = [set() for _ in range(nv)]
    diag = [[] for _ in range(nv)]
    for f in faces:
        for i in range(4):
            nbrs[f[i]].add(f[(i + 1) % 4])
            nbrs[f[(i + 1) % 4]].add(f[i])
            diag[f[i]].append(f[(i + 2) % 4])

    def comb(weights):
        d = len(verts[0])
        return tuple(sum((w * verts[j][k] for j, w in weights), F(0)) for k in range(d))

    vert = []
    for v in range(nv):
        n = len(nbrs[v])
        w = [(v, 1 - F(7, 4 * n))] + [(u, F(3, 2 * n * n)) for u in nbrs[v]] + [(u, F(1, 4 * n * n)) for u in diag[v]]
        vert.append(comb(w))
    edge = []
    for a, b in sorted((a, b) for a, b in half if a < b):
        f, g = faces[half[(a, b)]], faces[half[(b, a)]]
        others = [x for x in f if x not in (a, b)] + [x for x in g if x not in (a, b)]
        edge.append(comb([(a, F(3, 8)), (b, F(3, 8))] + [(x, F(1, 16)) for x in others]))
    face = [comb([(x, F(1, 4)) for x in f]) for f in faces]
    return vert + edge + face


def test_exact_stencil_weights():
    v, f = torus(4, 4)
    nv, _ = catmull_clark(unit_positions(16), f)
    w = nv[5]
    assert w[5] == F(9, 16)
    assert sorted(w[j] for j in range(16) if j != 5 and w[j]) == [F(1, 64)] * 4 + [F(3, 32)] * 4
    v, f = cube()
    nv, _ = catmull_clark(unit_positions(8), f)
    assert nv[7][7] == F(5, 12)
    assert sorted(x for j, x in enumerate(nv[7]) if j != 7 and x) == [F(1, 36)] * 3 + [F(1, 6)] * 3
    for verts, faces in quad_meshes():
        assert catmull_clark(unit_positions(len(verts)), faces)[0] == stencil_reference(unit_positions(len(verts)), faces)


def test_random_positions_against_hand_stencils():
    rng = random.Random(1)
    meshes = quad_meshes()
    for _ in range(150):
        _, faces = meshes[rng.randrange(len(meshes))]
        nv = 1 + max(x for f in faces for x in f)
        verts = random_positions(rng, nv, rng.randint(1, 3))
        assert catmull_clark(verts, faces)[0] == stencil_reference(verts, faces)


def cubic_refine_rows(grid):
    n = len(grid)
    out = []
    for i in range(n):
        a, b, c = grid[i - 1], grid[i], grid[(i + 1) % n]
        out.append([(x + 6 * y + z) / 8 for x, y, z in zip(a, b, c)])
        out.append([(y + z) / 2 for y, z in zip(b, c)])
    return out


def test_regular_torus_is_bicubic_b_spline_refinement():
    rng = random.Random(2)
    for _ in range(350):
        n, m = rng.randint(3, 5), rng.randint(3, 5)
        _, faces = torus(n, m)
        vals = [F(rng.randint(-50, 50), rng.randint(1, 4)) for _ in range(n * m)]
        verts = [(x,) for x in vals]
        out, new_faces = catmull_clark(verts, faces)
        grid = [[vals[i * m + j] for j in range(m)] for i in range(n)]
        fine = cubic_refine_rows(grid)
        fine = [list(r) for r in zip(*cubic_refine_rows([list(c) for c in zip(*fine)]))]
        coord = {}
        for i in range(n):
            for j in range(m):
                coord[i * m + j] = (2 * i, 2 * j)
        edges = sorted((a, b) for a, b in half_edges(faces) if a < b)
        for e, (a, b) in enumerate(edges):
            (ia, ja), (ib, jb) = divmod(a, m), divmod(b, m)
            if ja == jb:
                i0 = ia if (ia + 1) % n == ib else ib
                coord[n * m + e] = (2 * i0 + 1, 2 * ja)
            else:
                j0 = ja if (ja + 1) % m == jb else jb
                coord[n * m + e] = (2 * ia, 2 * j0 + 1)
        for fi in range(n * m):
            i, j = divmod(fi, m)
            coord[n * m + len(edges) + fi] = (2 * i + 1, 2 * j + 1)
        for k, p in enumerate(out):
            r, c = coord[k]
            assert p == (fine[r][c],)
        cells = {frozenset(((r % (2 * n), c % (2 * m)), ((r + 1) % (2 * n), c % (2 * m)), ((r + 1) % (2 * n), (c + 1) % (2 * m)), (r % (2 * n), (c + 1) % (2 * m)))) for r in range(2 * n) for c in range(2 * m)}
        assert {frozenset(coord[x] for x in q) for q in new_faces} == cells


def test_affine_invariance_and_floats():
    rng = random.Random(3)
    verts, faces = prism()
    out = catmull_clark(verts, faces)[0]
    shifted = catmull_clark([(x + 3, y - 1, 2 * z) for x, y, z in verts], faces)[0]
    assert shifted == [(x + 3, y - 1, 2 * z) for x, y, z in out]
    fl = catmull_clark([tuple(float(c) for c in p) for p in verts], faces)[0]
    assert all(abs(a - float(b)) < 1e-12 for p, q in zip(fl, out) for a, b in zip(p, q))


def test_rejects_open_or_bad_meshes():
    with pytest.raises(ValueError):
        catmull_clark([(0, 0), (1, 0), (0, 1)], [[0, 1, 2]])
    v, f = cube()
    with pytest.raises(ValueError):
        catmull_clark(v, f + [f[0]])
    with pytest.raises(ValueError):
        catmull_clark(v, [[0, 1]] + f)
