# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/batch-normalization/. The authors are listed in prov/3YR4QN.jsonl.

import math
import random

from batch_normalization import (BatchNorm, bn_backward, bn_forward, column_stats, folded_affine,
                                 population_statistics)


def batch(rng: random.Random, m: int, d: int) -> list[list[float]]:
    return [[rng.gauss(3.0 * j - 2.0, 1.0 + j) for j in range(d)] for _ in range(m)]


def test_normalized_output_has_mean_zero_and_variance_about_one() -> None:
    rng = random.Random(0)
    x = batch(rng, 16, 4)
    eps = 1e-5
    _, (xhat, _) = bn_forward(x, [1.0] * 4, [0.0] * 4, eps)
    mean, var = column_stats(xhat)
    _, raw_var = column_stats(x)
    for j in range(4):
        assert abs(mean[j]) < 1e-12
        assert math.isclose(var[j], raw_var[j] / (raw_var[j] + eps), rel_tol=1e-12)
        assert abs(var[j] - 1) < 1e-4


def test_gamma_and_beta_set_the_output_moments() -> None:
    x = batch(random.Random(1), 10, 3)
    y, _ = bn_forward(x, [2.0, 0.5, -1.0], [1.0, -3.0, 0.0], 0.0)
    mean, var = column_stats(y)
    for j, (g, b) in enumerate([(2.0, 1.0), (0.5, -3.0), (-1.0, 0.0)]):
        assert math.isclose(mean[j], b, abs_tol=1e-12)
        assert math.isclose(var[j], g * g, rel_tol=1e-12)


def loss(x, gamma, beta, c):
    y, _ = bn_forward(x, gamma, beta)
    return sum(ci * yi for cr, yr in zip(c, y) for ci, yi in zip(cr, yr))


def test_backward_pass_matches_central_differences() -> None:
    rng = random.Random(2)
    m, d = 6, 3
    x = batch(rng, m, d)
    gamma = [rng.uniform(0.5, 2.0) for _ in range(d)]
    beta = [rng.uniform(-1.0, 1.0) for _ in range(d)]
    c = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(m)]
    _, cache = bn_forward(x, gamma, beta)
    dx, dgamma, dbeta = bn_backward(c, cache, gamma)
    h = 1e-6
    for i in range(m):
        for j in range(d):
            xp = [r[:] for r in x]
            xm = [r[:] for r in x]
            xp[i][j] += h
            xm[i][j] -= h
            num = (loss(xp, gamma, beta, c) - loss(xm, gamma, beta, c)) / (2 * h)
            assert abs(num - dx[i][j]) < 1e-6
    for j in range(d):
        gp, gm = gamma[:], gamma[:]
        gp[j] += h
        gm[j] -= h
        assert abs((loss(x, gp, beta, c) - loss(x, gm, beta, c)) / (2 * h) - dgamma[j]) < 1e-6
        bp, bm = beta[:], beta[:]
        bp[j] += h
        bm[j] -= h
        assert abs((loss(x, gamma, bp, c) - loss(x, gamma, bm, c)) / (2 * h) - dbeta[j]) < 1e-6


def test_input_gradient_is_orthogonal_to_ones_and_xhat() -> None:
    rng = random.Random(3)
    x = batch(rng, 8, 2)
    _, cache = bn_forward(x, [1.5, 0.7], [0.0, 0.0], 0.0)  # orthogonality to x_hat is exact for eps = 0
    dy = [[rng.gauss(0.0, 1.0) for _ in range(2)] for _ in range(8)]
    dx, _, _ = bn_backward(dy, cache, [1.5, 0.7])
    xhat = cache[0]
    for j in range(2):
        assert abs(sum(dx[i][j] for i in range(8))) < 1e-12
        assert abs(sum(dx[i][j] * xhat[i][j] for i in range(8))) < 1e-12


def test_invariant_to_affine_change_of_each_feature() -> None:
    x = batch(random.Random(4), 7, 2)
    z = [[5.0 * r[0] + 3.0, 0.01 * r[1] - 8.0] for r in x]
    y1, _ = bn_forward(x, [1.0, 1.0], [0.0, 0.0], 0.0)
    y2, _ = bn_forward(z, [1.0, 1.0], [0.0, 0.0], 0.0)
    assert all(abs(a - b) < 1e-9 for r1, r2 in zip(y1, y2) for a, b in zip(r1, r2))


def test_population_statistics_and_inference() -> None:
    rng = random.Random(5)
    batches = [batch(rng, 4, 2) for _ in range(50)]
    mean, var = population_statistics(batches)
    stats = [column_stats(b) for b in batches]
    assert math.isclose(mean[0], sum(s[0][0] for s in stats) / 50, rel_tol=1e-12)
    assert math.isclose(var[1], 4 / 3 * sum(s[1][1] for s in stats) / 50, rel_tol=1e-12)
    a, c = folded_affine([2.0, 1.0], [0.5, 0.0], mean, var)
    layer = BatchNorm(2)
    layer.gamma, layer.beta = [2.0, 1.0], [0.5, 0.0]
    layer.running_mean, layer.running_var = mean, var
    row = [1.0, -2.0]
    assert all(math.isclose(u, ai * xi + ci, rel_tol=1e-12) for u, ai, xi, ci in zip(layer.infer(row), a, row, c))


def test_running_averages_converge_on_a_fixed_batch() -> None:
    x = batch(random.Random(6), 5, 2)
    layer = BatchNorm(2, momentum=0.1)
    for _ in range(400):
        layer.train_step(x)
    mean, var = column_stats(x)
    for j in range(2):
        assert math.isclose(layer.running_mean[j], mean[j], rel_tol=1e-9)
        assert math.isclose(layer.running_var[j], var[j] * 5 / 4, rel_tol=1e-9)
    one = layer.infer(x[0])
    assert one == layer.infer(x[0][:])
