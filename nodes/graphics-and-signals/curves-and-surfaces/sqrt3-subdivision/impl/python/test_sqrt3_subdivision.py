# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sqrt3-subdivision/. The authors are listed in prov/E9X6ZR.jsonl.

import math
import random
from fractions import Fraction

import pytest

from sqrt3_subdivision import euler_characteristic, half_edges, sqrt3_alpha, sqrt3_subdivision

F = Fraction
HAND_ALPHA = {3: F(5, 9), 4: F(4, 9), 6: F(1, 3)}


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


def valences(faces):
    nb = {}
    for f in faces:
        for i in range(3):
            nb.setdefault(f[i], set()).add(f[(i + 1) % 3])
    return {v: len(s) for v, s in nb.items()}


def hand_reference(verts, faces):
    """The new points from the rules written out by hand, for valences 3, 4 and 6."""
    d = len(verts[0])
    nb = {}
    for f in faces:
        for i in range(3):
            nb.setdefault(f[i], set()).add(f[(i + 1) % 3])
    out = []
    for v in range(len(verts)):
        n = len(nb[v])
        a = HAND_ALPHA[n]
        out.append(tuple((1 - a) * verts[v][k] + sum((a / n * verts[u][k] for u in nb[v]), F(0)) for k in range(d)))
    for f in faces:
        out.append(tuple(sum((F(verts[x][k]) for x in f), F(0)) / 3 for k in range(d)))
    return out


ALL = [tetrahedron(), octahedron(), bipyramid(5), bipyramid(8), torus(3, 3), torus(4, 5)]


def test_alpha_by_hand():
    for n, a in HAND_ALPHA.items():
        assert sqrt3_alpha(n) == a
    assert math.isclose(sqrt3_alpha(5), (4 - 2 * math.cos(2 * math.pi / 5)) / 9)


def test_tetrahedron_example():
    v, f = tetrahedron()
    pts, nf = sqrt3_subdivision(v, f)
    assert counts(pts, nf) == (8, 18, 12)
    # alpha_3 = 5/9: 4/9 of the corner and 5/27 of each neighbor.
    assert pts[0] == (F(7, 27),) * 3
    assert pts[4] == (F(1, 3), F(1, 3), F(-1, 3))
    # The edge 0-1 is in the faces 0 (0 -> 1) and 1 (1 -> 0).
    assert nf[0] == [4, 0, 5] and nf[1] == [5, 1, 4]


def test_counts_and_euler_characteristic():
    for verts, faces in ALL:
        v, e, f = counts(verts, faces)
        pts, nf = sqrt3_subdivision(verts, faces)
        assert counts(pts, nf) == (v + f, e + 3 * f, 3 * f)
        assert euler_characteristic(nf) == euler_characteristic(faces)
        half_edges(nf)
        val, val1 = valences(faces), valences(nf)
        assert all(val1[x] == val[x] for x in range(v))
        assert all(val1[x] == 6 for x in range(v, v + f))
        pts2, nf2 = sqrt3_subdivision(pts, nf)
        assert counts(pts2, nf2) == (v + 4 * f, e + 12 * f, 9 * f)
        assert euler_characteristic(nf2) == euler_characteristic(faces)
        half_edges(nf2)


def test_exact_stencil_weights():
    for verts, faces in [tetrahedron(), octahedron(), torus(3, 4), sqrt3_subdivision(*octahedron())]:
        u = unit_positions(len(verts))
        assert sqrt3_subdivision(u, faces)[0] == hand_reference(u, faces)
    u = unit_positions(12)
    pts, _ = sqrt3_subdivision(u, torus(3, 4)[1])
    assert pts[5][5] == F(2, 3) and sorted(x for x in pts[5] if x and x != F(2, 3)) == [F(1, 18)] * 6
    pts, _ = sqrt3_subdivision(unit_positions(4), tetrahedron()[1])
    assert pts[0] == (F(4, 9), F(5, 27), F(5, 27), F(5, 27))


def test_random_positions_against_hand_rules():
    rng = random.Random(1)
    meshes = [tetrahedron(), octahedron(), torus(3, 3), torus(3, 4), sqrt3_subdivision(*octahedron())]
    for _ in range(300):
        _, faces = meshes[rng.randrange(len(meshes))]
        nv = 1 + max(x for f in faces for x in f)
        d = rng.randint(1, 3)
        verts = [tuple(F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(d)) for _ in range(nv)]
        assert sqrt3_subdivision(verts, faces)[0] == hand_reference(verts, faces)


def test_limit_position_is_kept():
    # L(v) = (v + 3 alpha mean(ring)) / (1 + 3 alpha) is the same after a step.
    rng = random.Random(2)
    for _ in range(60):
        _, faces = [tetrahedron(), octahedron(), torus(3, 4)][rng.randrange(3)]
        nv = 1 + max(x for f in faces for x in f)
        verts = [tuple(F(rng.randint(-9, 9)) for _ in range(3)) for _ in range(nv)]
        pts, nf = sqrt3_subdivision(verts, faces)
        vals = []
        for p, fs in [(verts, faces), (pts, nf)]:
            nb = {}
            for f in fs:
                for i in range(3):
                    nb.setdefault(f[i], set()).add(f[(i + 1) % 3])
            row = []
            for v in range(nv):
                a = sqrt3_alpha(len(nb[v]))
                row.append(tuple((p[v][k] + 3 * a * sum(p[u][k] for u in nb[v]) / len(nb[v])) / (1 + 3 * a) for k in range(3)))
            vals.append(row)
        assert vals[0] == vals[1]
    v, f = tetrahedron()
    for _ in range(6):
        v, f = sqrt3_subdivision(v, f)
    assert all(abs(x - 1 / 6) < 0.01 for x in v[0])


def test_two_steps_on_a_plane_give_the_triadic_grid():
    n = m = 9
    _, faces = torus(n, m)
    verts = [(F(i), F(j)) for i in range(n) for j in range(m)]
    pts, nf = sqrt3_subdivision(*sqrt3_subdivision(verts, faces))
    assert set(valences(nf).values()) == {6}
    # The old vertices that each new point depends on. A point is clean if they do not wrap around the torus.
    deps, _ = sqrt3_subdivision(*sqrt3_subdivision(unit_positions(n * m), faces))
    clean = set()
    for k, row in enumerate(deps):
        cells = [divmod(x, m) for x, c in enumerate(row) if c]
        if all(max(t[s] for t in cells) - min(t[s] for t in cells) <= 3 for s in (0, 1)):
            clean.add(k)
    inside = [k for k in clean if all(3 <= c <= 5 for c in pts[k])]
    assert sorted(pts[k] for k in inside) == sorted((F(p, 3), F(q, 3)) for p in range(9, 16) for q in range(9, 16))
    short = {(F(s, 3), F(t, 3)) for s, t in [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1)]}
    nb = {}
    for f in nf:
        for i in range(3):
            a, b = f[i], f[(i + 1) % 3]
            if a in inside:
                nb.setdefault(a, set()).add((pts[b][0] - pts[a][0], pts[b][1] - pts[a][1]))
    assert len(nb) == len(inside) and all(s == short for s in nb.values())


def test_rejects_bad_meshes():
    with pytest.raises(ValueError):
        sqrt3_subdivision([(0, 0), (1, 0), (0, 1)], [[0, 1, 2]])
    with pytest.raises(ValueError):
        sqrt3_subdivision([(0, 0), (1, 0), (0, 1), (1, 1)], [[0, 1, 2, 3], [3, 2, 1, 0]])
