# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/locally-linear-embedding/. The authors are listed in prov/QVE4K5.jsonl.

import math
import random
from fractions import Fraction as F

from locally_linear_embedding import cost_matrix, lle, nearest_neighbors, reconstruction_weights


def plane_points(seed, n):
    """Rational points of the plane x = (u, v, 2u - 3v + 1) in R^3, with the true (u, v)."""
    rng = random.Random(seed)
    uv = [(F(rng.randint(0, 80000), 10000), F(rng.randint(0, 50000), 10000)) for _ in range(n)]
    return [(u, v, 2 * u - 3 * v + 1) for u, v in uv], uv


def test_line_example_weights():
    pts = [(F(i),) for i in range(5)]
    w = reconstruction_weights(pts, nearest_neighbors(pts, 2), reg=0)
    assert w[0] == {1: 2, 2: -1}
    assert w[2] == {1: F(1, 2), 3: F(1, 2)}
    assert w[4] == {3: 2, 2: -1}


def test_line_example_embedding():
    y, lam = lle([(float(i),) for i in range(5)], k=2, m=1, reg=0)
    s = 1.0 if y[4][0] > 0 else -1.0
    for i, (v,) in enumerate(y):
        assert abs(s * v - (i - 2) / math.sqrt(2)) < 1e-9
    assert abs(lam[0]) < 1e-12 and lam[1] > 0.3


def test_zero_reconstruction_error_on_affine_plane():
    pts, _ = plane_points(1, 25)
    nbrs = nearest_neighbors(pts, 3)
    w = reconstruction_weights(pts, nbrs, reg=0)
    for i, row in enumerate(w):
        assert sum(row.values()) == 1
        rec = [sum(wij * pts[j][c] for j, wij in row.items()) for c in range(3)]
        assert rec == list(pts[i])


def test_constant_vector_in_null_space():
    pts, _ = plane_points(2, 12)
    m = cost_matrix(reconstruction_weights(pts, nearest_neighbors(pts, 3), reg=0))
    assert all(sum(row) == 0 for row in m)
    assert all(m[i][j] == m[j][i] for i in range(12) for j in range(12))


def test_true_coordinates_in_null_space():
    pts, uv = plane_points(3, 12)
    m = cost_matrix(reconstruction_weights(pts, nearest_neighbors(pts, 3), reg=0))
    for c in range(2):
        z = [p[c] for p in uv]
        assert all(sum(m[i][j] * z[j] for j in range(12)) == 0 for i in range(12))


def residual_of_fit(y, z):
    """Least squares residual of z on the columns [1, y], relative to the spread of z."""
    n, m = len(y), len(y[0])
    cols = [[1.0] * n] + [[r[l] for r in y] for l in range(m)]
    q = []
    for col in cols:
        v = col[:]
        for u in q:
            d = sum(a * b for a, b in zip(u, v))
            v = [a - d * b for a, b in zip(v, u)]
        nv = math.sqrt(sum(a * a for a in v))
        if nv > 1e-12:
            q.append([a / nv for a in v])
    r = list(z)
    for u in q:
        d = sum(a * b for a, b in zip(u, r))
        r = [a - d * b for a, b in zip(r, u)]
    mean = sum(z) / n
    return math.sqrt(sum(a * a for a in r) / sum((a - mean) ** 2 for a in z))


def test_embedding_recovers_plane_up_to_affine_map():
    pts, uv = plane_points(4, 30)
    pts = [tuple(float(a) for a in p) for p in pts]
    y, lam = lle(pts, k=6, m=2, reg=1e-6)
    assert abs(lam[0]) < 1e-9 and abs(lam[1]) < 1e-9
    assert all(abs(sum(r[l] for r in y)) < 1e-6 for l in range(2))
    for c in range(2):
        assert residual_of_fit(y, [float(p[c]) for p in uv]) < 1e-3


def test_arc_is_unrolled():
    # 40 points on an arc of about 4 radians, spacing 0.1 with a jitter of 0.03.
    rng = random.Random(5)
    ts = [0.1 * i + rng.uniform(-0.03, 0.03) for i in range(40)]
    pts = [(math.cos(t), math.sin(t)) for t in ts]
    y, _ = lle(pts, k=4, m=1)
    coords = [v for (v,) in y]
    inc = all(a < b for a, b in zip(coords, coords[1:]))
    dec = all(a > b for a, b in zip(coords, coords[1:]))
    assert inc or dec
    assert abs(sum(v * v for v in coords) / len(coords) - 1) < 1e-9
