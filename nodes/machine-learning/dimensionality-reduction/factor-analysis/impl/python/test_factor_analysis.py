# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factor-analysis/. The authors are listed in prov/7FPPGW.jsonl.

import math
import random

import pytest

from factor_analysis import (
    em_step,
    fit,
    inverse,
    log_likelihood,
    logdet_spd,
    matmul,
    mean_and_covariance,
    model_covariance,
    varimax,
    varimax_criterion,
)

TRUE = [[0.9, 0.0], [0.8, 0.0], [0.7, 0.0], [0.0, 0.8], [0.0, 0.7], [0.0, 0.6]]


def sample(rng, n, lam, psi):
    d, k = len(lam), len(lam[0])
    x = []
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in range(k)]
        x.append([sum(lam[i][f] * z[f] for f in range(k)) + math.sqrt(psi[i]) * rng.gauss(0, 1) + i for i in range(d)])
    return x


def two_factor_data(seed, n=300):
    psi = [1 - sum(t * t for t in r) for r in TRUE]
    return mean_and_covariance(sample(random.Random(seed), n, TRUE, psi))[1]


def rotation(angle):
    c, s = math.cos(angle), math.sin(angle)
    return [[c, -s], [s, c]]


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_log_likelihood_never_decreases(seed):
    s = two_factor_data(seed)
    lam, psi, history = fit(s, 300, 2, random.Random(seed + 10), max_iter=300)
    for a, b in zip(history, history[1:]):
        assert b >= a - 1e-9 * abs(a)
    assert history[-1] > history[0]


def test_one_factor_exact_recovery():
    # d = 3 and k = 1: the model is just identified, lambda_i^2 = s_ij s_ik / s_jk.
    s = [[1.0, 0.72, 0.63], [0.72, 1.0, 0.56], [0.63, 0.56, 1.0]]
    lam, psi = [[0.5], [0.5], [0.5]], [0.5, 0.5, 0.5]
    for _ in range(400):
        lam, psi = em_step(s, lam, psi)
    for got, want in zip(lam, [0.9, 0.8, 0.7]):
        assert abs(abs(got[0]) - want) < 1e-6
    for got, want in zip(psi, [0.19, 0.36, 0.51]):
        assert abs(got - want) < 1e-6
    # The fit is exact, so the log likelihood equals that of the saturated model Sigma = S.
    n, d = 100, 3
    saturated = -0.5 * n * (d * math.log(2 * math.pi) + logdet_spd(s) + d)
    assert abs(log_likelihood(s, n, lam, psi) - saturated) < 1e-8


def test_fixed_point_matches_diagonal_of_s():
    s = two_factor_data(4)
    lam, psi, _ = fit(s, 300, 2, random.Random(5), max_iter=3000, tol=1e-14)
    sigma = model_covariance(lam, psi)
    for i in range(len(s)):
        assert abs(sigma[i][i] - s[i][i]) < 1e-5


def test_rotation_does_not_change_the_likelihood():
    s = two_factor_data(6)
    lam, psi, _ = fit(s, 300, 2, random.Random(7))
    base = log_likelihood(s, 300, lam, psi)
    for angle in [0.3, 1.0, 2.5]:
        assert abs(log_likelihood(s, 300, matmul(lam, rotation(angle)), psi) - base) < 1e-8


def test_varimax():
    s = two_factor_data(8, n=500)
    lam, psi, _ = fit(s, 500, 2, random.Random(9))
    mixed = matmul(lam, rotation(math.pi / 4))
    rot, r = varimax(mixed)
    # R is orthogonal and Lambda Lambda^T does not change.
    rrt = matmul(r, [list(c) for c in zip(*r)])
    assert all(abs(rrt[i][j] - (i == j)) < 1e-12 for i in range(2) for j in range(2))
    a, b = matmul(mixed, [list(c) for c in zip(*mixed)]), matmul(rot, [list(c) for c in zip(*rot)])
    assert all(abs(a[i][j] - b[i][j]) < 1e-12 for i in range(6) for j in range(6))
    # The simple structure comes back: each variable loads on one factor.
    for i in range(6):
        big = max(abs(t) for t in rot[i])
        small = min(abs(t) for t in rot[i])
        assert big > 0.5 and small < 0.15
    # Without normalization, the angle is the best one on a fine grid.
    raw, _ = varimax(mixed, normalize=False)
    best = varimax_criterion(raw)
    for step in range(720):
        assert varimax_criterion(matmul(mixed, rotation(step * math.pi / 360))) <= best + 1e-12


def test_helpers():
    a = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 2.0]]
    p = matmul(a, inverse(a))
    assert all(abs(p[i][j] - (i == j)) < 1e-12 for i in range(3) for j in range(3))
    with pytest.raises(ValueError):
        logdet_spd([[1.0, 2.0], [2.0, 1.0]])
