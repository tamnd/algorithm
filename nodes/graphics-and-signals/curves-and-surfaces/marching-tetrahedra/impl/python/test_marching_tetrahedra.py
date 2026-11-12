# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-tetrahedra/. The authors are listed in prov/2FMDJR.jsonl.

import math
import random
from collections import Counter, defaultdict
from fractions import Fraction

from marching_tetrahedra import CORNERS, TET_TABLE, TETS, marching_tetrahedra


def kuhn_edges(nx, ny, nz):
    """All edges of the Kuhn tetrahedralization of the grid, by brute force over the cells."""
    out = set()
    for z in range(nz - 1):
        for y in range(ny - 1):
            for x in range(nx - 1):
                pts = [(x + dx, y + dy, z + dz) for dx, dy, dz in CORNERS]
                for tet in TETS:
                    for i in range(4):
                        for j in range(i + 1, 4):
                            out.add(tuple(sorted((pts[tet[i]], pts[tet[j]]))))
    return out


def crossings_brute(field, c):
    nz, ny, nx = len(field), len(field[0]), len(field[0][0])
    pts = set()
    for pa, pb in kuhn_edges(nx, ny, nz):
        fa, fb = field[pa[2]][pa[1]][pa[0]], field[pb[2]][pb[1]][pb[0]]
        if (fa < c) != (fb < c):
            t = Fraction(c - fa) / (fb - fa)
            pts.add(tuple(pa[k] + t * (pb[k] - pa[k]) for k in range(3)))
    return pts


def mesh_stats(verts, tris):
    """Check a closed oriented 2-manifold and return V - E + F."""
    directed = Counter()
    for a, b, c in tris:
        assert len({a, b, c}) == 3
        for e in ((a, b), (b, c), (c, a)):
            directed[e] += 1
    assert all(k == 1 for k in directed.values())
    assert all(directed[(b, a)] == 1 for a, b in list(directed))
    star = defaultdict(dict)
    for a, b, c in tris:
        star[a][b] = c
        star[b][c] = a
        star[c][a] = b
    for v, nxt in star.items():
        start = next(iter(nxt))
        u, n = nxt[start], 1
        while u != start:
            u, n = nxt[u], n + 1
        assert n == len(nxt)
    assert {v for t in tris for v in t} == set(range(len(verts)))
    return len(verts) - len(directed) // 2 + len(tris)


def signed_volume(verts, tris):
    s = 0
    for a, b, c in tris:
        p, q, r = verts[a], verts[b], verts[c]
        s += p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0]) + p[2] * (q[0] * r[1] - q[1] * r[0])
    return s / 6


def winding_number(verts, tris, p):
    """Generalized winding number of a closed mesh around p, by the solid angles of the triangles."""
    total = 0.0
    for a, b, c in tris:
        u = [float(verts[a][k] - p[k]) for k in range(3)]
        v = [float(verts[b][k] - p[k]) for k in range(3)]
        w = [float(verts[c][k] - p[k]) for k in range(3)]
        lu, lv, lw = (math.sqrt(sum(t * t for t in x)) for x in (u, v, w))
        det = u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0])
        dots = sum(u[k] * v[k] for k in range(3)) * lw + sum(v[k] * w[k] for k in range(3)) * lu + sum(w[k] * u[k] for k in range(3)) * lv
        total += 2 * math.atan2(det, lu * lv * lw + dots)
    return total / (4 * math.pi)


def pl_value(field, p):
    """The piecewise linear interpolant on the Kuhn tetrahedralization at p (exact with Fraction)."""
    x0, y0, z0 = (min(int(p[k]), (len(field[0][0]), len(field[0]), len(field))[k] - 2) for k in range(3))
    u = (p[0] - x0, p[1] - y0, p[2] - z0)
    # the Kuhn simplex: sort the local coordinates in decreasing order
    order = sorted(range(3), key=lambda k: -u[k])
    vals, corner = [], [0, 0, 0]
    vals.append(field[z0][y0][x0])
    for k in order:
        corner[k] = 1
        vals.append(field[z0 + corner[2]][y0 + corner[1]][x0 + corner[0]])
    w = [1 - u[order[0]], u[order[0]] - u[order[1]], u[order[1]] - u[order[2]], u[order[2]]]
    return sum(wi * vi for wi, vi in zip(w, vals))


def grid(n, f):
    return [[[f(x, y, z) for x in range(n)] for y in range(n)] for z in range(n)]


def test_tets_tile_the_cube() -> None:
    # each tetrahedron has volume 1/6, they share only faces, and they cover the cube
    for tet in TETS:
        p = [CORNERS[k] for k in tet]
        u = [[p[i][k] - p[0][k] for k in range(3)] for i in (1, 2, 3)]
        det = u[0][0] * (u[1][1] * u[2][2] - u[1][2] * u[2][1]) - u[0][1] * (u[1][0] * u[2][2] - u[1][2] * u[2][0]) + u[0][2] * (u[1][0] * u[2][1] - u[1][1] * u[2][0])
        # positive: the table orients triangles on a positively oriented reference tetrahedron
        assert det == 1
    rng = random.Random(3)
    for _ in range(300):
        q = [Fraction(k, 1000) for k in rng.sample(range(1, 1000), 3)]  # distinct, so q is in no shared face
        n_in = 0
        for tet in TETS:
            # q is in the tetrahedron 0 -> e_a -> e_a + e_b -> 7 iff q_a >= q_b >= q_c
            path = sorted((CORNERS[k] for k in tet), key=sum)
            axes = [next(k for k in range(3) if path[i + 1][k] != path[i][k]) for i in range(3)]
            if q[axes[0]] >= q[axes[1]] >= q[axes[2]]:
                n_in += 1
        assert n_in == 1


def test_tet_table() -> None:
    assert TET_TABLE[0] == [] and TET_TABLE[15] == []
    for m in range(1, 15):
        k = bin(m).count("1")
        assert len(TET_TABLE[m]) == (2 if k == 2 else 1)
        edges = {e for tri in TET_TABLE[m] for e in tri}
        change = {(i, j) for i in range(4) for j in range(4) if (m >> i & 1) and not (m >> j & 1)}
        assert edges == change


def test_example_one_cell() -> None:
    # one inside corner at the origin, which is in all 6 tetrahedra
    field = [[[0, 4], [4, 4]], [[4, 4], [4, 4]]]
    verts, tris = marching_tetrahedra(field, 1)
    q = Fraction(1, 4)
    assert set(verts) == {(q, 0, 0), (0, q, 0), (0, 0, q), (q, q, 0), (q, 0, q), (0, q, q), (q, q, q)}
    assert len(tris) == 6
    # the 6 triangles form a fan around the vertex on the diagonal 0-7
    center = verts.index((q, q, q))
    assert all(center in t for t in tris)


def test_linear_field_is_exact() -> None:
    # for a linear field the interpolant is the field, so every vertex is on the plane
    field = grid(5, lambda x, y, z: 2 * x + 3 * y - z)
    c = Fraction(7, 2)
    verts, tris = marching_tetrahedra(field, c)
    assert verts and all(2 * x + 3 * y - z == c for x, y, z in verts)
    # the normals point along the gradient (2, 3, -1)
    for a, b, d in tris:
        p, q, r = verts[a], verts[b], verts[d]
        u = [q[k] - p[k] for k in range(3)]
        v = [r[k] - p[k] for k in range(3)]
        n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        assert 2 * n[0] + 3 * n[1] - n[2] > 0


def test_edges() -> None:
    assert marching_tetrahedra(grid(3, lambda x, y, z: 5), 1) == ([], [])
    assert marching_tetrahedra(grid(2, lambda x, y, z: 1), 1) == ([], [])
    verts, tris = marching_tetrahedra([[[0.0, 2.0], [2.0, 2.0]], [[2.0, 2.0], [2.0, 2.0]]], 1.0)
    assert len(verts) == 7 and len(tris) == 6


def test_sphere_torus_two_spheres() -> None:
    verts, tris = marching_tetrahedra(grid(10, lambda x, y, z: (x - 4) ** 2 + (y - 4) ** 2 + (z - 5) ** 2), Fraction(21, 2))
    assert mesh_stats(verts, tris) == 2
    R, r = 4, 2
    verts, tris = marching_tetrahedra(grid(15, lambda x, y, z: ((x - 7) ** 2 + (y - 7) ** 2 + (z - 7) ** 2 + R * R - r * r) ** 2 - 4 * R * R * ((x - 7) ** 2 + (y - 7) ** 2)), Fraction(1, 2))
    assert mesh_stats(verts, tris) == 0
    verts, tris = marching_tetrahedra(grid(10, lambda x, y, z: min((x - 2) ** 2 + (y - 2) ** 2 + (z - 2) ** 2, (x - 7) ** 2 + (y - 7) ** 2 + (z - 7) ** 2)), Fraction(5, 2))
    assert mesh_stats(verts, tris) == 4


def test_random_against_brute_force() -> None:
    rng = random.Random(11)
    for trial in range(300):
        nx, ny, nz = rng.randint(2, 4), rng.randint(2, 4), rng.randint(2, 4)
        field = [[[rng.randint(-5, 5) for _ in range(nx)] for _ in range(ny)] for _ in range(nz)]
        closed = trial % 2 == 0
        if closed:
            for z in range(nz):
                for y in range(ny):
                    for x in range(nx):
                        if x in (0, nx - 1) or y in (0, ny - 1) or z in (0, nz - 1):
                            field[z][y][x] = 9
        c = Fraction(2 * rng.randint(-5, 4) + 1, 2)
        verts, tris = marching_tetrahedra(field, c)
        assert set(verts) == crossings_brute(field, c)
        assert len(set(verts)) == len(verts)
        if not closed:
            continue
        chi = mesh_stats(verts, tris)
        assert chi % 2 == 0
        if tris:
            assert signed_volume(verts, tris) > 0
        # the mesh bounds exactly the region where the interpolant is below c
        for _ in range(4):
            p = tuple(Fraction(rng.randint(1, 100 * (n - 1) - 1), 100) for n in (nx, ny, nz))
            v = pl_value(field, p)
            if abs(v - c) < Fraction(1, 10):
                continue
            wn = winding_number(verts, tris, p) if tris else 0.0
            assert abs(wn - (1.0 if v < c else 0.0)) < 1e-6
