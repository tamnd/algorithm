# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/classical-mds/. The authors are listed in prov/H05ZK6.jsonl.

import math
import random
from fractions import Fraction as F

from classical_mds import (
    classical_mds,
    distances,
    double_center,
    double_center_squared,
    is_euclidean,
    is_psd,
    jacobi_eigh,
)


def centered_gram(points):
    n, k = len(points), len(points[0])
    mean = [sum(p[t] for p in points) / n for t in range(k)]
    c = [[p[t] - mean[t] for t in range(k)] for p in points]
    return [[sum(a * b for a, b in zip(u, v)) for v in c] for u in c]


def sq_dist_matrix(points):
    return [[sum((a - b) ** 2 for a, b in zip(p, q)) for q in points] for p in points]


def test_b_is_centered_gram_exactly():
    rng = random.Random(1)
    pts = [tuple(F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(3)) for _ in range(6)]
    b = double_center_squared(sq_dist_matrix(pts))
    assert b == centered_gram(pts)
    assert is_psd(b)


def test_double_center_with_rational_distances():
    pts = [(F(0), F(0)), (F(3), F(0)), (F(3), F(4)), (F(0), F(4))]
    d = [[F(int(math.isqrt(int(x)))) for x in row] for row in sq_dist_matrix(pts)]
    assert double_center(d) == centered_gram(pts)
    assert is_euclidean(d)


def test_rectangle_eigenvalues_and_recovery():
    pts = [(0.0, 0.0), (3.0, 0.0), (3.0, 4.0), (0.0, 4.0)]
    d = distances(pts)
    x, lam = classical_mds(d, 2)
    assert abs(lam[0] - 16) < 1e-9 and abs(lam[1] - 9) < 1e-9
    assert all(abs(v) < 1e-9 for v in lam[2:])
    dx = distances(x)
    assert all(abs(dx[i][j] - d[i][j]) < 1e-9 for i in range(4) for j in range(4))


def test_recovery_up_to_rigid_motion_random():
    rng = random.Random(7)
    for dim in (1, 2, 3):
        pts = [tuple(rng.uniform(-5, 5) for _ in range(dim)) for _ in range(9)]
        d = distances(pts)
        x, lam = classical_mds(d, dim)
        dx = distances(x)
        assert max(abs(dx[i][j] - d[i][j]) for i in range(9) for j in range(9)) < 1e-8
        assert all(abs(v) < 1e-8 for v in lam[dim:])
        assert sum(sum(p[t] for p in x) for t in range(dim)) < 1e-8  # centered


def test_equals_pca_scores():
    rng = random.Random(3)
    pts = [tuple(rng.gauss(0, s) for s in (3.0, 1.0, 0.3)) for _ in range(8)]
    x, _ = classical_mds(distances(pts), 2)
    n = len(pts)
    mean = [sum(p[t] for p in pts) / n for t in range(3)]
    c = [[p[t] - mean[t] for t in range(3)] for p in pts]
    cov = [[sum(r[a] * r[b] for r in c) for b in range(3)] for a in range(3)]
    _, vecs = jacobi_eigh(cov)
    for j in range(2):
        scores = [sum(r[t] * vecs[j][t] for t in range(3)) for r in c]
        sign = 1.0 if scores[0] * x[0][j] >= 0 else -1.0
        assert max(abs(sign * scores[i] - x[i][j]) for i in range(n)) < 1e-8


def test_non_euclidean_star_metric():
    # the shortest path metric of the star with three leaves
    d = [[F(0), F(1), F(1), F(1)],
         [F(1), F(0), F(2), F(2)],
         [F(1), F(2), F(0), F(2)],
         [F(1), F(2), F(2), F(0)]]
    assert not is_euclidean(d)
    _, lam = classical_mds(d, 2)
    assert lam[-1] < -1e-6


def test_violates_triangle_inequality():
    d = [[F(0), F(1), F(5)], [F(1), F(0), F(1)], [F(5), F(1), F(0)]]
    assert not is_euclidean(d)


def test_is_psd_small_cases():
    assert is_psd([[F(0), F(0)], [F(0), F(0)]])
    assert not is_psd([[F(0), F(1)], [F(1), F(0)]])
    assert is_psd([[F(1), F(1)], [F(1), F(1)]])
    assert not is_psd([[F(1), F(2)], [F(2), F(1)]])


def test_one_point_and_two_points():
    x, lam = classical_mds([[0.0]], 1)
    assert x == [(0.0,)]
    x, _ = classical_mds([[0.0, 2.0], [2.0, 0.0]], 1)
    assert abs(abs(x[0][0] - x[1][0]) - 2.0) < 1e-12
