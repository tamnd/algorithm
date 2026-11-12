# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autoencoder/. The authors are listed in prov/GR8CEC.jsonl.

import random

from autoencoder import (
    center,
    gradients,
    loss,
    matmul,
    orthonormal_columns,
    pca_basis,
    principal_angles,
    second_moment,
    train_linear_autoencoder,
    transpose,
)


def dataset(seed=3, n=200, scales=(3.0, 2.0, 1.0, 0.6, 0.3)):
    r = random.Random(seed)
    d = len(scales)
    rot = orthonormal_columns([[r.gauss(0.0, 1.0) for _ in range(d)] for _ in range(d)])
    xs = []
    for _ in range(n):
        z = [r.gauss(0.0, s) for s in scales]
        xs.append([sum(rot[i][j] * z[j] for j in range(d)) for i in range(d)])
    return center(xs)[0]


def test_loss_formula_matches_direct_sum():
    x = dataset(n=50)
    r = random.Random(0)
    w1 = [[r.gauss(0, 1) for _ in range(5)] for _ in range(2)]
    w2 = [[r.gauss(0, 1) for _ in range(2)] for _ in range(5)]
    p = matmul(w2, w1)
    direct = sum(sum((xi[a] - sum(p[a][b] * xi[b] for b in range(5))) ** 2 for a in range(5)) for xi in x) / len(x)
    assert abs(loss(second_moment(x), w1, w2) - direct) < 1e-9


def test_gradient_matches_finite_differences():
    s = second_moment(dataset(n=50))
    r = random.Random(1)
    w1 = [[r.gauss(0, 1) for _ in range(5)] for _ in range(2)]
    w2 = [[r.gauss(0, 1) for _ in range(2)] for _ in range(5)]
    g1, g2 = gradients(s, w1, w2)
    h = 1e-6
    for w, g in ((w1, g1), (w2, g2)):
        for i in range(len(w)):
            for j in range(len(w[0])):
                w[i][j] += h
                up = loss(s, w1, w2)
                w[i][j] -= 2 * h
                down = loss(s, w1, w2)
                w[i][j] += h
                assert abs((up - down) / (2 * h) - g[i][j]) < 1e-5 * max(1.0, abs(g[i][j]))


def test_linear_autoencoder_spans_the_pca_subspace():
    x = dataset()
    vals, v = pca_basis(x, 2)
    w1, w2, history = train_linear_autoencoder(x, 2, random.Random(1))
    assert max(principal_angles(w2, v)) < 1e-3  # decoder columns span the top-2 eigenvectors
    assert max(principal_angles(transpose(w1), v)) < 1e-3  # and so do the encoder rows
    assert abs(history[-1] - sum(vals[2:])) < 1e-6 * sum(vals)  # the PCA reconstruction error


def test_weights_need_not_be_orthogonal():
    x = dataset()
    _, v = pca_basis(x, 2)
    w1, w2, _ = train_linear_autoencoder(x, 2, random.Random(1), enc_scale=1.0, dec_scale=0.1)
    assert max(principal_angles(w2, v)) < 1e-3
    g = matmul(w1, transpose(w1))
    assert max(abs(g[i][j] - (1.0 if i == j else 0.0)) for i in range(2) for j in range(2)) > 0.5
