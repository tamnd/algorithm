# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitening/. The authors are listed in prov/H04HKR.jsonl.

import math
import random
from fractions import Fraction

import pytest

from whitening import (
    cholesky_whitening,
    covariance,
    fit_whitening,
    jacobi_eigen,
    mean,
    pca_q,
    transform,
    zca_q,
)

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def matmul(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(col) for col in zip(*a)]


def assert_identity(m, tol):
    for i in range(len(m)):
        for j in range(len(m)):
            assert abs(m[i][j] - (1.0 if i == j else 0.0)) < tol


def random_data(rng, n, d):
    mix = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(d)]
    return [[sum(mix[i][j] * g for j, g in enumerate([rng.gauss(0, 1) for _ in range(d)])) + 3.0 for i in range(d)] for _ in range(n)]


def test_worked_example():
    mu, w = fit_whitening(EXAMPLE, pca_q)
    z = transform(EXAMPLE, mu, w)
    # PCA whitening sends the eight points to the corners of the cube {-1, 1}^3.
    for row in z:
        for t in row:
            assert abs(abs(t) - 1.0) < 1e-9
    # ZCA whitening is C^(-1/2) = (1/162) [[38, -14, 4], [-14, 35, -10], [4, -10, 26]].
    mu, w = fit_whitening(EXAMPLE, zca_q)
    exact = [[38, -14, 4], [-14, 35, -10], [4, -10, 26]]
    for i in range(3):
        for j in range(3):
            assert abs(w[i][j] - exact[i][j] / 162) < 1e-12
    z0 = transform([EXAMPLE[0]], mu, w)[0]
    assert all(abs(a - b) < 1e-12 for a, b in zip(z0, [5 / 3, 1 / 3, 1 / 3]))


def test_exact_inverse_square_root():
    # (C^(-1/2))^2 C = I holds exactly in rational arithmetic for the example.
    mu = [Fraction(sum(p[j] for p in EXAMPLE), 8) for j in range(3)]
    c = covariance(EXAMPLE, mu)
    c = [[Fraction(v) for v in row] for row in c]
    w = [[Fraction(v, 162) for v in row] for row in [[38, -14, 4], [-14, 35, -10], [4, -10, 26]]]
    prod = matmul(matmul(w, c), transpose(w))
    assert prod == [[1 if i == j else 0 for j in range(3)] for i in range(3)]


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_whitened_covariance_is_identity(seed):
    rng = random.Random(seed)
    x = random_data(rng, 40, 4)
    fits = [fit_whitening(x, pca_q), fit_whitening(x, zca_q), cholesky_whitening(x)]
    for mu, w in fits:
        z = transform(x, mu, w)
        assert_identity(covariance(z, mean(z)), 1e-9)
        assert all(abs(t) < 1e-9 for t in mean(z))


def test_every_whitening_is_q_times_inverse_root():
    rng = random.Random(4)
    x = random_data(rng, 30, 3)
    mu, c = mean(x), covariance(x, mean(x))
    values, vectors = jacobi_eigen(c)
    root = [[sum(vectors[t][i] * math.sqrt(values[t]) * vectors[t][j] for t in range(3)) for j in range(3)] for i in range(3)]
    for _, w in [fit_whitening(x, pca_q), fit_whitening(x, zca_q), cholesky_whitening(x)]:
        q = matmul(w, root)
        assert_identity(matmul(q, transpose(q)), 1e-9)


def test_zca_is_closest_to_the_data():
    rng = random.Random(5)
    x = random_data(rng, 50, 3)
    mu = mean(x)

    def dist(w):
        z = transform(x, mu, w)
        return sum((z[i][j] - (x[i][j] - mu[j])) ** 2 for i in range(len(x)) for j in range(3)) / len(x)

    best = dist(fit_whitening(x, zca_q)[1])
    others = [fit_whitening(x, pca_q)[1], cholesky_whitening(x)[1]]
    for _ in range(20):
        # a random orthogonal Q by Gram-Schmidt
        q = []
        while len(q) < 3:
            v = [rng.gauss(0, 1) for _ in range(3)]
            for u in q:
                p = sum(a * b for a, b in zip(u, v))
                v = [a - p * b for a, b in zip(v, u)]
            nv = math.sqrt(sum(a * a for a in v))
            q.append([a / nv for a in v])
        others.append(fit_whitening(x, lambda vectors, q=q: q)[1])
    for w in others:
        assert best <= dist(w) + 1e-9


def test_regularized_whitening_shrinks_variances():
    rng = random.Random(6)
    x = random_data(rng, 30, 3)
    eps = 0.5
    values = jacobi_eigen(covariance(x, mean(x)))[0]
    mu, w = fit_whitening(x, pca_q, eps)
    z = transform(x, mu, w)
    cz = covariance(z, mean(z))
    for j in range(3):
        assert abs(cz[j][j] - values[j] / (values[j] + eps)) < 1e-9
        for k in range(3):
            if k != j:
                assert abs(cz[j][k]) < 1e-9


def test_singular_and_new_data():
    # Three points in R^3 have a covariance of rank at most 2.
    x = [(0.0, 0.0, 1.0), (1.0, 2.0, 0.0), (2.0, 1.0, 3.0)]
    with pytest.raises(ValueError):
        fit_whitening(x, zca_q)
    mu, w = fit_whitening(x, zca_q, eps=1e-3)
    assert len(w) == 3
    # New points use the training mean and matrix.
    mu, w = fit_whitening(EXAMPLE, zca_q)
    assert transform([(4, 5, 6)], mu, w) == [[0.0, 0.0, 0.0]]
