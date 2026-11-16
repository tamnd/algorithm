# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-eight-point-algorithm/. The authors are listed in prov/6HV01C.jsonl.
"""Tests of the normalized eight-point algorithm."""

import math
import random

import pytest

from cvla import inv, matvec, mul, norm, skew, sub, svd, transpose
from normalized_eight_point_algorithm import (canonical, epipolar_distances,
                                              epipolar_row,
                                              normalized_eight_point,
                                              normalizing_similarity)

K1 = [[500.0, 0.0, 320.0], [0.0, 500.0, 240.0], [0.0, 0.0, 1.0]]
K2 = [[450.0, 0.0, 300.0], [0.0, 460.0, 250.0], [0.0, 0.0, 1.0]]


def rotation(axis, angle):
    """Rodrigues formula, written out."""
    a = [c / norm(axis) for c in axis]
    k = skew(a)
    k2 = mul(k, k)
    s, c = math.sin(angle), math.cos(angle)
    return [[(1.0 if i == j else 0.0) + s * k[i][j] + (1.0 - c) * k2[i][j]
             for j in range(3)] for i in range(3)]


def project(K, X):
    y = matvec(K, X)
    return [y[0] / y[2], y[1] / y[2]]


def two_views(rng, n):
    """A random relative pose and n pixel pairs of points in front of both
    cameras. Returns R, t, x1, x2."""
    R = rotation([rng.uniform(-1, 1) for _ in range(3)], rng.uniform(0.05, 0.3))
    t = [rng.uniform(-1, 1), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3)]
    x1, x2 = [], []
    while len(x1) < n:
        X1 = [rng.uniform(-2.0, 2.0), rng.uniform(-2.0, 2.0), rng.uniform(4.0, 8.0)]
        X2 = [a + b for a, b in zip(matvec(R, X1), t)]
        if X2[2] > 0.5:
            x1.append(project(K1, X1))
            x2.append(project(K2, X2))
    return R, t, x1, x2


def true_F(R, t):
    return canonical(mul(mul(transpose(inv(K2)), mul(skew(t), R)), inv(K1)))


def noisy(rng, pts, sigma):
    return [[c + rng.gauss(0.0, sigma) for c in p] for p in pts]


def test_similarity_values():
    T = normalizing_similarity([[0.0, 0.0], [2.0, 0.0], [2.0, 2.0], [0.0, 2.0]])
    s = math.sqrt(2.0) / math.sqrt(2.0)
    assert T == [[s, 0.0, -s], [0.0, s, -s], [0.0, 0.0, 1.0]]
    pts = [[3.0, 1.0], [7.0, 4.0], [-2.0, 5.0], [0.0, 0.0]]
    T = normalizing_similarity(pts)
    ys = [matvec(T, [p[0], p[1], 1.0]) for p in pts]
    assert abs(sum(y[0] for y in ys)) <= 1e-12 and abs(sum(y[1] for y in ys)) <= 1e-12
    assert abs(sum(math.hypot(y[0], y[1]) for y in ys) / 4 - math.sqrt(2.0)) <= 1e-12


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_exact_recovery(seed):
    rng = random.Random(seed)
    R, t, x1, x2 = two_views(rng, 15)
    F = normalized_eight_point(x1, x2)
    assert norm(sub(F, true_F(R, t))) <= 1e-8
    s = svd(F)[1]
    assert s[2] <= 1e-12
    assert max(epipolar_distances(F, x1, x2)) <= 1e-8


def test_rectified_pair():
    # Pure translation along +X with equal K: F ~ [[0,0,0],[0,0,-1],[0,1,0]].
    rng = random.Random(4)
    x1, x2 = [], []
    for _ in range(10):
        X = [rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(4, 8)]
        x1.append(project(K1, X))
        x2.append(project(K1, [X[0] - 0.5, X[1], X[2]]))
    F = normalized_eight_point(x1, x2)
    r = 1.0 / math.sqrt(2.0)
    assert norm(sub(F, [[0.0, 0.0, 0.0], [0.0, 0.0, -r], [0.0, r, 0.0]])) <= 1e-8 or \
        norm(sub(F, [[0.0, 0.0, 0.0], [0.0, 0.0, r], [0.0, -r, 0.0]])) <= 1e-8


def test_covariant_under_similarities():
    # Moving each image by a similarity S gives S2^-T F S1^-1, even with noise.
    rng = random.Random(5)
    _, _, x1, x2 = two_views(rng, 20)
    x1, x2 = noisy(rng, x1, 1.0), noisy(rng, x2, 1.0)
    F = normalized_eight_point(x1, x2)

    def sim(angle, s, tx, ty):
        c, d = s * math.cos(angle), s * math.sin(angle)
        return [[c, -d, tx], [d, c, ty], [0.0, 0.0, 1.0]]

    S1, S2 = sim(0.7, 2.5, 100.0, -40.0), sim(-1.2, 0.3, -7.0, 900.0)
    m1 = [matvec(S1, [p[0], p[1], 1.0])[:2] for p in x1]
    m2 = [matvec(S2, [p[0], p[1], 1.0])[:2] for p in x2]
    G = normalized_eight_point(m1, m2)
    expected = canonical(mul(mul(transpose(inv(S2)), F), inv(S1)))
    assert norm(sub(G, expected)) <= 1e-8


def test_normalization_improves_conditioning():
    rng = random.Random(6)
    _, _, x1, x2 = two_views(rng, 30)
    plain = [epipolar_row([p[0], p[1], 1.0], [q[0], q[1], 1.0]) for p, q in zip(x1, x2)]
    T1, T2 = normalizing_similarity(x1), normalizing_similarity(x2)
    moved = [epipolar_row(matvec(T1, [p[0], p[1], 1.0]), matvec(T2, [q[0], q[1], 1.0]))
             for p, q in zip(x1, x2)]
    sp, sn = svd(plain)[1], svd(moved)[1]
    # ratio of the largest to the second smallest singular value
    assert sp[0] / sp[7] > 1e4
    assert sn[0] / sn[7] < 1e2


def test_more_accurate_than_plain_under_noise():
    # sigma = 1 pixel, 30 points, 10 scenes: mean distance in pixels of the
    # noise-free points to the estimated epipolar lines.
    rng = random.Random(10)
    dn, dp = 0.0, 0.0
    for _ in range(10):
        _, _, x1, x2 = two_views(rng, 30)
        n1, n2 = noisy(rng, x1, 1.0), noisy(rng, x2, 1.0)
        dn += sum(epipolar_distances(normalized_eight_point(n1, n2), x1, x2)) / 300.0
        dp += sum(epipolar_distances(normalized_eight_point(n1, n2, normalize=False), x1, x2)) / 300.0
    assert dn < 1.0
    assert dp > 2.0 * dn


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        normalized_eight_point([[0.0, 0.0]] * 7, [[1.0, 1.0]] * 7)
    with pytest.raises(ValueError):
        normalized_eight_point([[0.0, 0.0]] * 8, [[1.0, 1.0]] * 8)
