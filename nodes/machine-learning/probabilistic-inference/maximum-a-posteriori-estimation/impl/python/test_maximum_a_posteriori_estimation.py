# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-a-posteriori-estimation/. The authors are listed in prov/WXKGVJ.jsonl.

import math
import random
from fractions import Fraction as F

from maximum_a_posteriori_estimation import (
    beta_bernoulli_map,
    beta_log_density_logit,
    beta_log_density_theta,
    dirichlet_map,
    grid_mode,
    lasso_map,
    neg_log_posterior,
    ridge_map,
)


def test_map_is_not_invariant_under_reparameterization() -> None:
    # prior Beta(2, 2), data with 6 ones and 2 zeros: posterior Beta(8, 4)
    assert beta_bernoulli_map(F(2), F(2), 6, 2) == F(7, 10)
    th = grid_mode(beta_log_density_theta(8, 4), 0.0, 1.0)
    eta = grid_mode(beta_log_density_logit(8, 4), -10.0, 10.0)
    back = 1 / (1 + math.exp(-eta))
    assert abs(th - 0.7) < 1e-4
    assert abs(back - 2 / 3) < 1e-4  # the mode in logit space maps back to 2/3, not 7/10
    assert abs(back - th) > 0.03


def test_map_approaches_mle() -> None:
    gaps = []
    for n in (8, 80, 800, 8000):
        s = 3 * n // 4
        gaps.append(abs(beta_bernoulli_map(F(2), F(2), s, n - s) - F(3, 4)))
    assert all(g1 > g2 for g1, g2 in zip(gaps, gaps[1:]))
    assert gaps[-1] * 8000 < 1


def test_dirichlet_map_is_add_one_smoothing() -> None:
    assert dirichlet_map([F(2)] * 3, [5, 2, 0]) == [F(6, 10), F(3, 10), F(1, 10)]
    assert dirichlet_map([F(1)] * 3, [5, 2, 0]) == [F(5, 7), F(2, 7), F(0)]  # flat prior: the MLE


def _data(rng: random.Random, n: int = 30, d: int = 3):
    X = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(n)]
    w = [1.5, 0.0, -0.7][:d]
    y = [sum(a * b for a, b in zip(r, w)) + rng.gauss(0, 0.5) for r in X]
    return X, y


def test_gaussian_prior_gives_ridge() -> None:
    rng = random.Random(42)
    X, y = _data(rng)
    w = ridge_map(X, y, 0.25, 0.5)
    # only the ratio lambda = noise_var / prior_var matters
    w2 = ridge_map(X, y, 1.0, 2.0)
    assert max(abs(a - b) for a, b in zip(w, w2)) < 1e-12
    best = neg_log_posterior(X, y, w, 0.25, "gauss", 0.5)
    for _ in range(200):
        v = [a + rng.gauss(0, 0.01) for a in w]
        assert neg_log_posterior(X, y, v, 0.25, "gauss", 0.5) > best


def test_laplace_prior_gives_lasso() -> None:
    rng = random.Random(1996)
    X, y = _data(rng)
    w = lasso_map(X, y, 0.25, 0.05)
    best = neg_log_posterior(X, y, w, 0.25, "laplace", 0.05)
    for _ in range(200):
        v = [a + rng.gauss(0, 0.01) for a in w]
        assert neg_log_posterior(X, y, v, 0.25, "laplace", 0.05) >= best - 1e-9
    # the Laplace prior puts the irrelevant weight exactly at zero; the Gaussian prior does not
    assert w[1] == 0.0
    assert ridge_map(X, y, 0.25, 0.05)[1] != 0.0


def test_lasso_against_grid_in_one_dimension() -> None:
    X = [[1.0], [2.0], [-1.0], [0.5]]
    y = [0.9, 2.2, -0.8, 0.3]
    for scale in (0.05, 0.5, 5.0):
        w = lasso_map(X, y, 1.0, scale)[0]
        g = grid_mode(lambda t: -neg_log_posterior(X, y, [t], 1.0, "laplace", scale), -3.0, 3.0, 60000)
        assert abs(w - g) < 1e-3
