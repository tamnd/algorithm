# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-smoothing/. The authors are listed in prov/8BS9ES.jsonl.

import random
from fractions import Fraction as Fr

from laplacian_smoothing import laplacian_smoothing, umbrella
from mp2mesh import boundary_vertices, grid_mesh, icosphere, neighbours, norm, octahedron, signed_volume


def exact(points):
    return [tuple(Fr(c) for c in p) for p in points]


def noisy_grid(m, n, rng, den=8):
    p, f = grid_mesh(m, n)
    q = [(Fr(x) + Fr(rng.randrange(-2, 3), den), Fr(y) + Fr(rng.randrange(-2, 3), den), Fr(rng.randrange(-4, 5), den))
         for x, y, _ in p]
    return q, f


# ---- brute force: the step as a dense matrix, applied K times ----


def matrix_smoothing(points, faces, lam, iterations, fixed):
    n = len(points)
    nb = neighbours(n, faces)
    S = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        if i in fixed or not nb[i]:
            S[i][i] = Fr(1)
            continue
        S[i][i] = 1 - lam
        for j in nb[i]:
            S[i][j] += lam / len(nb[i])
    x = [list(p) for p in points]
    for _ in range(iterations):
        x = [[sum(S[i][j] * x[j][k] for j in range(n)) for k in range(3)] for i in range(n)]
    return [tuple(r) for r in x]


def test_example_trace() -> None:
    p, f = grid_mesh(3, 3)
    p = exact(p)
    p[5] = (Fr(1), Fr(1), Fr(1))
    x1 = laplacian_smoothing(p, f, Fr(1, 2), 1)
    assert [x1[i][2] for i in (5, 6, 9, 10)] == [Fr(1, 2), Fr(1, 12), Fr(1, 12), Fr(1, 12)]
    x2 = laplacian_smoothing(x1, f, Fr(1, 2), 1)
    assert [x2[i][2] for i in (5, 6, 9, 10)] == [Fr(13, 48), Fr(13, 144), Fr(13, 144), Fr(7, 72)]
    assert laplacian_smoothing(p, f, Fr(1, 2), 2) == x2


def test_octahedron_halves() -> None:
    p, f = octahedron()
    p = exact(p)
    x = laplacian_smoothing(p, f, Fr(1, 2), 3)
    assert x == [tuple(c / 8 for c in q) for q in p]


def test_against_matrix_form() -> None:
    rng = random.Random(7)
    for _ in range(20):
        p, f = noisy_grid(rng.randrange(1, 4), rng.randrange(1, 4), rng)
        lam = Fr(rng.randrange(1, 10), 10)
        k = rng.randrange(1, 4)
        fixed = boundary_vertices(f)
        assert laplacian_smoothing(p, f, lam, k) == matrix_smoothing(p, f, lam, k, fixed)
        none = set()
        assert laplacian_smoothing(p, f, lam, k, fixed=none) == matrix_smoothing(p, f, lam, k, none)


def test_border_fixed() -> None:
    rng = random.Random(3)
    p, f = noisy_grid(4, 3, rng)
    x = laplacian_smoothing(p, f, Fr(1, 3), 5)
    for v in boundary_vertices(f):
        assert x[v] == p[v]


def test_flat_regular_grid_is_fixed() -> None:
    p, f = grid_mesh(5, 4)
    p = exact(p)
    assert laplacian_smoothing(p, f, Fr(1, 2), 4) == p
    assert all(u == (0, 0, 0) for i, u in enumerate(umbrella(p, f)) if i not in boundary_vertices(f))


def test_flat_irregular_fan_drifts() -> None:
    pts = exact([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0)])
    fs = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 5, 1)]
    x = laplacian_smoothing(pts, fs, Fr(1, 2), 1)
    assert x[0] == (Fr(1, 10), Fr(1, 10), 0)       # moves inside a flat region
    assert all(q[2] == 0 for q in x)                # but stays in the plane


def test_degree_weighted_centroid_is_conserved() -> None:
    rng = random.Random(11)
    p, f = icosphere(1)
    p = [tuple(Fr(round(c * 64)) / 64 + Fr(rng.randrange(-3, 4), 256) for c in q) for q in p]
    nb = neighbours(len(p), f)

    def moment(x):
        return tuple(sum(len(nb[i]) * x[i][k] for i in range(len(x))) for k in range(3))

    m0 = moment(p)
    x = p
    for _ in range(3):
        x = laplacian_smoothing(x, f, Fr(2, 5), 1)
        assert moment(x) == m0


def test_closed_mesh_shrinks_to_a_point() -> None:
    p, f = icosphere(2)
    v0 = signed_volume(p, f)
    prev = v0
    x = p
    for _ in range(10):
        x = laplacian_smoothing(x, f, 0.5, 5)
        v = signed_volume(x, f)
        assert v < prev
        prev = v
    assert prev / v0 < 0.05                           # measured: 0.034 after 50 steps
    x = laplacian_smoothing(x, f, 0.5, 300)
    assert max(norm(q) for q in x) < 1e-3           # the centroid of the sphere is the origin
    p, f = icosphere(1)
    x = laplacian_smoothing(p, f, 0.5, 200)
    assert max(norm(q) for q in x) < 1e-7           # measured: 2e-8
