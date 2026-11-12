# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/probabilistic-pca/. The authors are listed in prov/V9B0Y7.jsonl.

import math
import random

import pytest

from probabilistic_pca import (
    closed_form,
    em_step,
    fit_em,
    log_likelihood,
    matmul,
    max_log_likelihood,
    mean_and_covariance,
    model_covariance,
    posterior_mean,
    transpose,
)

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def random_cov(seed, n=150, d=5):
    rng = random.Random(seed)
    scales = [3.0, 2.0, 1.2, 0.8, 0.5, 0.4][:d]
    x = [[scales[j] * rng.gauss(0, 1) + 0.5 * rng.gauss(0, 1) * (j % 2) for j in range(d)] for _ in range(n)]
    for row in x:
        row[1] += 0.7 * row[0]
    return mean_and_covariance(x)[1]


def test_worked_example():
    mu, s = mean_and_covariance(EXAMPLE)
    w, sigma2, values = closed_form(s, 1)
    assert abs(sigma2 - 22.5) < 1e-9  # (36 + 9) / 2
    for got, want in zip([r[0] for r in w], [1 / 3, 2 / 3, 2 / 3]):
        assert abs(got - want * math.sqrt(58.5)) < 1e-9
    # q = 2: sigma2 = 9 and W W^T + sigma2 I equals S, the saturated fit.
    w, sigma2, values = closed_form(s, 2)
    assert abs(sigma2 - 9.0) < 1e-9
    c = model_covariance(w, sigma2)
    assert all(abs(c[i][j] - s[i][j]) < 1e-9 for i in range(3) for j in range(3))
    want = -4.0 * (3 * math.log(2 * math.pi) + math.log(81 * 36 * 9) + 3)
    assert abs(log_likelihood(s, 8, w, sigma2) - want) < 1e-9
    z = posterior_mean(EXAMPLE[0], mu, w, sigma2)
    assert abs(abs(z[0]) - 9 * math.sqrt(72) / 81) < 1e-9
    assert abs(abs(z[1]) - 6 * math.sqrt(27) / 36) < 1e-9


@pytest.mark.parametrize("seed,q", [(1, 1), (2, 2), (3, 3)])
def test_closed_form_is_the_maximum(seed, q):
    s = random_cov(seed)
    n = 150
    w, sigma2, values = closed_form(s, q)
    best = log_likelihood(s, n, w, sigma2)
    assert abs(best - max_log_likelihood(values, n, q)) < 1e-8 * abs(best)
    rng = random.Random(seed + 100)
    for _ in range(30):
        w2 = [[t + rng.gauss(0, 0.05) for t in row] for row in w]
        s2 = sigma2 * math.exp(rng.gauss(0, 0.05))
        assert log_likelihood(s, n, w2, s2) <= best + 1e-9


@pytest.mark.parametrize("seed,q", [(4, 1), (5, 2), (6, 3)])
def test_em_reaches_closed_form(seed, q):
    s = random_cov(seed)
    n = 150
    w, sigma2, history = fit_em(s, n, q, random.Random(seed))
    for a, b in zip(history, history[1:]):
        assert b >= a - 1e-9 * abs(a)
    target = max_log_likelihood(closed_form(s, q)[2], n, q)
    assert abs(history[-1] - target) < 1e-6 * abs(target)
    wc, sc, _ = closed_form(s, q)
    assert abs(sigma2 - sc) < 1e-4 * sc
    a, b = matmul(w, transpose(w)), matmul(wc, transpose(wc))
    assert max(abs(a[i][j] - b[i][j]) for i in range(5) for j in range(5)) < 1e-3


def test_rotation_and_em_fixed_point():
    s = random_cov(7)
    w, sigma2, _ = closed_form(s, 2)
    c, sn = math.cos(0.7), math.sin(0.7)
    wr = matmul(w, [[c, -sn], [sn, c]])
    assert abs(log_likelihood(s, 150, wr, sigma2) - log_likelihood(s, 150, w, sigma2)) < 1e-8
    # The closed form is a fixed point of EM, up to the rotation.
    w2, s2 = em_step(s, wr, sigma2)
    a, b = matmul(w2, transpose(w2)), matmul(w, transpose(w))
    assert max(abs(a[i][j] - b[i][j]) for i in range(5) for j in range(5)) < 1e-9
    assert abs(s2 - sigma2) < 1e-9


def test_small_noise_gives_pca_projection():
    mu, s = mean_and_covariance(EXAMPLE)
    w, _, _ = closed_form(s, 2)
    # With sigma2 -> 0 the posterior mean of W z is the orthogonal projection on the principal plane.
    z = posterior_mean(EXAMPLE[0], mu, w, 1e-12)
    rec = [mu[i] + sum(w[i][t] * z[t] for t in range(2)) for i in range(3)]
    assert all(abs(a - b) < 1e-6 for a, b in zip(rec, [11, 13, 8]))
