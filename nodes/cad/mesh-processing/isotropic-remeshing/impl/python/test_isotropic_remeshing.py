# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isotropic-remeshing/. The authors are listed in prov/0E9HMJ.jsonl.

import random
from math import acos, degrees, sqrt

from isotropic_remeshing import (Mesh, collapse_short_edges, cross, dot, equalize_valences, isotropic_remeshing,
                                 length, split_long_edges, sub)


def sphere(p):
    n = sqrt(dot(p, p))
    return tuple(c / n for c in p)


def icosphere(level):
    t = (1 + sqrt(5)) / 2
    raw = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
           (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    pts = [sphere(p) for p in raw]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
             (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
             (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    for _ in range(level):
        memo = {}

        def m(i, j):
            k = (min(i, j), max(i, j))
            if k not in memo:
                pts.append(sphere(tuple((a + b) / 2 for a, b in zip(pts[i], pts[j]))))
                memo[k] = len(pts) - 1
            return memo[k]

        faces = [g for a, b, c in faces for g in
                 ((a, m(a, b), m(c, a)), (b, m(b, c), m(a, b)), (c, m(c, a), m(b, c)), (m(a, b), m(b, c), m(c, a)))]
    return pts, faces


def rectangle():
    """An 8 x 4 rectangle cut into 32 long thin triangles (cells 4 x 0.5)."""
    pts = [(4.0 * i, 0.5 * j, 0.0) for j in range(9) for i in range(3)]
    faces = []
    for j in range(8):
        for i in range(2):
            a, b, c, d = 3 * j + i, 3 * j + i + 1, 3 * (j + 1) + i + 1, 3 * (j + 1) + i
            faces += [(a, b, c), (a, c, d)]
    return pts, faces


# ---- brute force: the topology recomputed from the face list ----


def check_manifold(points, faces, closed):
    directed = {}
    for f in faces:
        assert len(set(f)) == 3
        for k in range(3):
            e = (f[k], f[(k + 1) % 3])
            assert e not in directed                          # consistent orientation, no edge used twice
            directed[e] = f
    if closed:
        assert all((v, u) in directed for u, v in directed)
    for v in {w for f in faces for w in f}:                  # the link of each vertex is one cycle or one path
        nxt = {}
        for f in faces:
            if v in f:
                k = f.index(v)
                nxt[f[(k + 1) % 3]] = f[(k + 2) % 3]
        starts = set(nxt) - set(nxt.values())
        assert len(starts) <= 1
        start = next(iter(starts)) if starts else next(iter(nxt))
        seen, w = 0, start
        while w in nxt and seen <= len(nxt):
            w = nxt[w]
            seen += 1
            if w == start:
                break
        assert seen == len(nxt)


def euler(points, faces):
    es = {(min(f[k], f[(k + 1) % 3]), max(f[k], f[(k + 1) % 3])) for f in faces for k in range(3)}
    return len({w for f in faces for w in f}) - len(es) + len(faces)


def area(points, faces):
    return sum(length(cross(sub(points[b], points[a]), sub(points[c], points[a]))) / 2 for a, b, c in faces)


def edge_lengths(points, faces):
    es = {(min(f[k], f[(k + 1) % 3]), max(f[k], f[(k + 1) % 3])) for f in faces for k in range(3)}
    return [length(sub(points[i], points[j])) for i, j in es]


def test_square_example() -> None:
    p = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0)]
    mesh = Mesh(p, [(0, 1, 2), (0, 2, 3)])
    assert split_long_edges(mesh, 4 * 0.5 / 3) == 9          # the diagonal, the 4 sides, the 4 half-diagonals
    P, F = mesh.compact()
    assert (len(P), len(F)) == (13, 16)
    assert sorted(set(round(x, 12) for x in edge_lengths(P, F))) == [round(sqrt(2) / 4, 12), 0.5]
    assert (0.5, 0.5, 0.0) in P and (0.25, 0.25, 0.0) in P


def test_split_bounds_every_edge_and_keeps_the_surface() -> None:
    for (p, f), L in ((icosphere(0), 0.3), (rectangle(), 0.5)):
        mesh = Mesh(p, f)
        a0 = area(p, f)
        k = split_long_edges(mesh, 4 * L / 3)
        P, F = mesh.compact()
        assert max(edge_lengths(P, F)) <= 4 * L / 3
        assert abs(area(P, F) - a0) < 1e-9 * a0              # midpoints stay in the planes of the faces
        assert euler(P, F) == euler(p, f)
        assert len(F) >= len(f) + k                          # each split adds one or two faces
        check_manifold(P, F, closed=(len(p) == 12))


def test_collapse_respects_the_upper_bound() -> None:
    p, f = icosphere(2)
    L = 0.5                                                  # the edges of the input are about 0.3
    mesh = Mesh(p, f)
    split_long_edges(mesh, 4 * L / 3)
    n0 = len({w for g in mesh.F.values() for w in g})
    k = collapse_short_edges(mesh, 4 * L / 5, 4 * L / 3)
    P, F = mesh.compact()
    assert k > 0 and len(P) == n0 - k                        # each collapse removes one vertex
    assert max(edge_lengths(P, F)) <= 4 * L / 3
    assert euler(P, F) == 2
    check_manifold(P, F, closed=True)


def test_flips_reach_a_local_optimum() -> None:
    rng = random.Random(5)
    p, f = icosphere(2)
    p = [sphere(tuple(c + 0.04 * (rng.random() - 0.5) for c in v)) for v in p]
    mesh = Mesh(p, f)
    for u, v in rng.sample(sorted(mesh.he), 60):             # scramble the valences first
        if (u, v) in mesh.he and mesh.opposite(u, v) != mesh.opposite(v, u):
            c, d = mesh.opposite(u, v), mesh.opposite(v, u)
            if d not in mesh.neighbours(c) and len(mesh.neighbours(u)) > 3 and len(mesh.neighbours(v)) > 3:
                mesh.flip(u, v)

    def excess():
        live = {w for g in mesh.F.values() for w in g}
        return sum(abs(len(mesh.neighbours(w)) - 6) for w in live)

    e0 = excess()
    equalize_valences(mesh)
    assert excess() < e0
    for u, v in mesh.he:                                     # the brute-force scan: no improving flip is left
        assert mesh.flip_gain(u, v) == 0
    P, F = mesh.compact()
    check_manifold(P, F, closed=True)


def test_random_operations_keep_a_manifold() -> None:
    rng = random.Random(11)
    p, f = icosphere(1)
    mesh = Mesh(p, f)
    for _ in range(150):
        u, v = rng.choice(sorted(mesh.he))
        op = rng.randrange(3)
        if op == 0:
            mesh.split(u, v)
        elif op == 1 and mesh.can_collapse(u, v, float("inf")):
            mesh.collapse(u, v)
        elif op == 2 and mesh.flip_gain(u, v) > 0:
            mesh.flip(u, v)
        P, F = mesh.compact()
        check_manifold(P, F, closed=True)
        assert euler(P, F) == 2


def test_sphere_is_remeshed_to_the_target_length() -> None:
    rng = random.Random(3)
    p, f = icosphere(2)
    p = [sphere(tuple(c + 0.05 * (rng.random() - 0.5) for c in v)) for v in p]
    L = 0.15
    P, F = isotropic_remeshing(p, f, L, 5, project=sphere)
    check_manifold(P, F, closed=True)
    assert euler(P, F) == 2
    assert all(abs(length(q) - 1) < 1e-12 for q in P)
    vol = sum(dot(P[a], cross(P[b], P[c])) for a, b, c in F) / 6
    assert vol > 0                                           # the orientation is kept
    ls = edge_lengths(P, F)
    mean = sum(ls) / len(ls)
    assert abs(mean / L - 1) < 0.05                          # measured: 1.021
    assert sum(1 for x in ls if 4 * L / 5 <= x <= 4 * L / 3) / len(ls) > 0.98   # measured: 0.995
    angles = []
    for t in F:
        for k in range(3):
            a, b, c = P[t[k]], P[t[(k + 1) % 3]], P[t[(k + 2) % 3]]
            x, y = sub(b, a), sub(c, a)
            angles.append(degrees(acos(dot(x, y) / (length(x) * length(y)))))
    assert min(angles) > 35                                 # measured: 41 degrees, from 44 in the input


def test_border_is_kept() -> None:
    p, f = rectangle()
    P, F = isotropic_remeshing(p, f, 0.5, 5)
    check_manifold(P, F, closed=False)
    assert euler(P, F) == 1
    assert abs(area(P, F) - 32) < 1e-9
    assert all(q[2] == 0.0 for q in P)
    for q in p:
        if q[0] in (0.0, 8.0) and q[1] in (0.0, 4.0):
            assert q in P                                    # the corners stay
    directed = {(t[k], t[(k + 1) % 3]) for t in F for k in range(3)}
    for u, v in directed:
        if (v, u) not in directed:                           # a border edge lies on the rectangle
            a, b = P[u], P[v]
            assert (a[0] == b[0] and a[0] in (0.0, 8.0)) or (a[1] == b[1] and a[1] in (0.0, 4.0))
    angles = []
    for t in F:
        for k in range(3):
            a, b, c = P[t[k]], P[t[(k + 1) % 3]], P[t[(k + 2) % 3]]
            x, y = sub(b, a), sub(c, a)
            angles.append(degrees(acos(dot(x, y) / (length(x) * length(y)))))
    assert min(angles) > 20                                 # measured: 27 degrees, from 7 in the input
