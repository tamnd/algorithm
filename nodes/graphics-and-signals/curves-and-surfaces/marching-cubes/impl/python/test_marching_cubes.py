# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marching-cubes/. The authors are listed in prov/N004FS.jsonl.

import math
import random
from collections import Counter, defaultdict
from fractions import Fraction

from marching_cubes import CORNERS, EDGES, FACES, TABLE, face_segments, marching_cubes


def crossings_brute(field, c):
    """All points where the linear interpolant along a grid edge equals c, by a scan of all grid edges."""
    nz, ny, nx = len(field), len(field[0]), len(field[0][0])
    pts = set()
    for z in range(nz):
        for y in range(ny):
            for x in range(nx):
                for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                    x2, y2, z2 = x + d[0], y + d[1], z + d[2]
                    if x2 >= nx or y2 >= ny or z2 >= nz:
                        continue
                    fa, fb = field[z][y][x], field[z2][y2][x2]
                    if (fa < c) != (fb < c):
                        t = Fraction(c - fa) / (fb - fa)
                        pts.add((x + t * d[0], y + t * d[1], z + t * d[2]))
    return pts


def mesh_stats(verts, tris):
    """Check a closed oriented 2-manifold and return its Euler characteristic V - E + F."""
    directed = Counter()
    for a, b, c in tris:
        assert len({a, b, c}) == 3
        for e in ((a, b), (b, c), (c, a)):
            directed[e] += 1
    assert all(k == 1 for k in directed.values())  # each directed edge once
    assert all(directed[(b, a)] == 1 for a, b in directed)  # closed: the twin is there
    # vertex links are single cycles: no pinched vertex
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
    used = {v for t in tris for v in t}
    assert used == set(range(len(verts)))
    return len(verts) - len(directed) // 2 + len(tris)


def signed_volume(verts, tris):
    s = 0
    for a, b, c in tris:
        p, q, r = verts[a], verts[b], verts[c]
        s += p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0]) + p[2] * (q[0] * r[1] - q[1] * r[0])
    return s / 6


def grid(n, f):
    return [[[f(x, y, z) for x in range(n)] for y in range(n)] for z in range(n)]


def test_example_one_corner() -> None:
    # one inside corner at the origin: one triangle cutting the corner off
    field = [[[0, 4], [4, 4]], [[4, 4], [4, 4]]]
    verts, tris = marching_cubes(field, 1)
    q = Fraction(1, 4)
    assert sorted(verts) == sorted([(q, 0, 0), (0, q, 0), (0, 0, q)])
    assert len(tris) == 1
    # the normal points away from the inside corner, toward the outside
    (a, b, c), = tris
    p, r, s = verts[a], verts[b], verts[c]
    u = [r[i] - p[i] for i in range(3)]
    w = [s[i] - p[i] for i in range(3)]
    n = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    assert all(k > 0 for k in n)


def test_table_covers_sign_changes() -> None:
    for case in range(256):
        used = {e for t in TABLE[case] for e in t}
        change = {i for i, (a, b) in enumerate(EDGES) if (case >> a & 1) != (case >> b & 1)}
        assert used == change
        # the boundary of the triangles of one case is the reversed face segments
        bd = Counter()
        for a, b, c in TABLE[case]:
            for e in ((a, b), (b, c), (c, a)):
                bd[e] += 1
                bd[e[::-1]] -= 1
        seg = Counter()
        for ring in FACES:
            for a, b in face_segments(case, ring):
                seg[(b, a)] += 1
                seg[(a, b)] -= 1
        assert {k: v for k, v in bd.items() if v} == {k: v for k, v in seg.items() if v}
        # no triangle edge lies on a cube face unless it is a face segment
        segs = {frozenset(s) for ring in FACES for s in face_segments(case, ring)}
        for a, b, c in TABLE[case]:
            for e in ((a, b), (b, c), (c, a)):
                if frozenset(e) not in segs:
                    pts = EDGES[e[0]] + EDGES[e[1]]
                    assert not any(len({p >> d & 1 for p in pts}) == 1 for d in range(3))
    assert TABLE[0] == [] and TABLE[255] == []
    assert max(len(t) for t in TABLE) <= 5


def _rotations():
    """The 24 rotations of the cube as permutations of the 8 corners."""
    def perm(m):
        out = []
        for x, y, z in CORNERS:
            v = [2 * x - 1, 2 * y - 1, 2 * z - 1]
            w = [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]
            out.append(CORNERS.index(tuple((k + 1) // 2 for k in w)))
        return tuple(out)
    rx = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
    ry = ((0, 0, 1), (0, 1, 0), (-1, 0, 0))
    gens = [perm(rx), perm(ry)]
    group = {tuple(range(8))}
    frontier = list(group)
    while frontier:
        g = frontier.pop()
        for h in gens:
            k = tuple(h[g[i]] for i in range(8))
            if k not in group:
                group.add(k)
                frontier.append(k)
    return group


def test_symmetry_classes() -> None:
    rots = _rotations()
    assert len(rots) == 24

    def act(g, case):
        return sum(1 << g[k] for k in range(8) if case >> k & 1)

    def classes(with_complement):
        seen, n = set(), 0
        for case in range(256):
            if case in seen:
                continue
            n += 1
            for g in rots:
                seen.add(act(g, case))
                if with_complement:
                    seen.add(255 - act(g, case))
        return n

    assert classes(False) == 23
    assert classes(True) == 15  # the 15 patterns of Lorensen and Cline, the empty one included
    # the table is invariant under rotation (but not under complement)
    for case in range(256):
        for g in rots:
            assert len(TABLE[act(g, case)]) == len(TABLE[case])


def test_complement_symmetric_table_leaves_holes() -> None:
    # Use the complement of the case when more than 4 corners are inside, as a
    # table built from complement symmetry does. Two cells that share an ambiguous
    # face can then cut it in two different ways.
    hybrid = []
    for case in range(256):
        if bin(case).count("1") <= 4:
            hybrid.append(TABLE[case])
        else:
            hybrid.append([(a, c, b) for a, b, c in TABLE[255 - case]])
    # cell 0 (x = 0..1) has inside corners on the diagonal of the shared face x = 1;
    # cell 1 (x = 1..2) has 6 inside corners.
    field = [[[9, 0, 0], [9, 9, 0]], [[9, 9, 0], [9, 0, 0]]]
    c = Fraction(1, 2)
    nz, ny, nx = 2, 2, 3

    def boundary(table):
        directed = Counter()
        for x in range(nx - 1):
            case = 0
            for k, (dx, dy, dz) in enumerate(CORNERS):
                if field[dz][dy][x + dx] < c:
                    case |= 1 << k
            for t in table[case]:
                keys = []
                for e in t:
                    a, b = EDGES[e]
                    pa = tuple(CORNERS[a][i] + (x if i == 0 else 0) for i in range(3))
                    pb = tuple(CORNERS[b][i] + (x if i == 0 else 0) for i in range(3))
                    keys.append((pa, pb))
                for i in range(3):
                    directed[(keys[i], keys[(i + 1) % 3])] += 1
        return {e for e in directed if (e[1], e[0]) not in directed}

    def on_shared_face(e):
        return all(p[0] == 1 and q[0] == 1 for p, q in e)

    assert not any(on_shared_face(e) for e in boundary(TABLE))
    assert any(on_shared_face(e) for e in boundary(hybrid))


def test_edges() -> None:
    assert marching_cubes(grid(3, lambda x, y, z: 5), 1) == ([], [])
    assert marching_cubes(grid(3, lambda x, y, z: 0), 1) == ([], [])
    # a sample equal to c is outside
    assert marching_cubes(grid(2, lambda x, y, z: 1), 1) == ([], [])
    # float input
    verts, tris = marching_cubes([[[0.0, 2.0], [2.0, 2.0]], [[2.0, 2.0], [2.0, 2.0]]], 1.0)
    assert len(tris) == 1 and len(verts) == 3


def test_sphere_torus_two_spheres() -> None:
    verts, tris = marching_cubes(grid(12, lambda x, y, z: (x - 5) ** 2 + (y - 5) ** 2 + (z - 6) ** 2), Fraction(33, 2))
    assert mesh_stats(verts, tris) == 2
    vol = signed_volume(verts, tris)
    exact = 4 / 3 * math.pi * (33 / 2) ** 1.5
    assert 0.9 * exact < vol < exact  # the mesh is inscribed: a bit less than the ball
    R, r = 5, 2
    verts, tris = marching_cubes(grid(17, lambda x, y, z: ((x - 8) ** 2 + (y - 8) ** 2 + (z - 8) ** 2 + R * R - r * r) ** 2 - 4 * R * R * ((x - 8) ** 2 + (y - 8) ** 2)), Fraction(1, 2))
    assert mesh_stats(verts, tris) == 0
    verts, tris = marching_cubes(grid(12, lambda x, y, z: min((x - 3) ** 2 + (y - 3) ** 2 + (z - 3) ** 2, (x - 8) ** 2 + (y - 8) ** 2 + (z - 8) ** 2)), Fraction(9, 2))
    assert mesh_stats(verts, tris) == 4
    assert signed_volume(verts, tris) > 0


def test_random_against_brute_force() -> None:
    rng = random.Random(7)
    for trial in range(400):
        nx, ny, nz = rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 5)
        field = [[[rng.randint(-5, 5) for _ in range(nx)] for _ in range(ny)] for _ in range(nz)]
        closed = trial % 2 == 0
        if closed:
            for z in range(nz):
                for y in range(ny):
                    for x in range(nx):
                        if x in (0, nx - 1) or y in (0, ny - 1) or z in (0, nz - 1):
                            field[z][y][x] = 9
        c = Fraction(2 * rng.randint(-5, 4) + 1, 2)  # never equal to a sample
        verts, tris = marching_cubes(field, c)
        assert set(verts) == crossings_brute(field, c)
        assert len(set(verts)) == len(verts)
        if closed:
            chi = mesh_stats(verts, tris)
            assert chi % 2 == 0
            if tris:
                assert signed_volume(verts, tris) > 0
        else:
            # every edge is in one or two triangles; edges in one lie on the box border
            und = Counter()
            for a, b, c3 in tris:
                for e in ((a, b), (b, c3), (c3, a)):
                    und[frozenset(e)] += 1
            for e, k in und.items():
                assert k in (1, 2)
                if k == 1:
                    p, q = (verts[i] for i in e)
                    assert any(p[i] == q[i] and p[i] in (0, (nx, ny, nz)[i] - 1) for i in range(3))
