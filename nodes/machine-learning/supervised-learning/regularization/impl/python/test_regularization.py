# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regularization/. The authors are listed in prov/M5KEQK.jsonl.

import random

from regularization import (constrained_least_squares, empirical_risk, gradient_descent_path, l2_shrink,
                            lambda_for_radius, make_data, map_gradient, moments, norm, ridge, soft_threshold,
                            stability_bound)

XS, YS = make_data(20, 3, random.Random(1))


def test_ridge_solves_its_normal_equations() -> None:
    lam = 0.1
    w = ridge(XS, YS, lam)
    sig, c = moments(XS, YS)
    for i in range(3):
        assert abs(sum(sig[i][j] * w[j] for j in range(3)) + lam * w[i] - c[i]) < 1e-12


def test_penalty_shrinks_norm_and_raises_training_error() -> None:
    lams = [0.0, 0.01, 0.1, 1.0, 10.0]
    ws = [ridge(XS, YS, lam) for lam in lams]
    norms = [norm(w) for w in ws]
    risks = [empirical_risk(w, XS, YS) for w in ws]
    assert all(a > b for a, b in zip(norms, norms[1:]))
    assert all(a < b for a, b in zip(risks, risks[1:]))


def test_penalized_and_constrained_forms_agree() -> None:
    w = ridge(XS, YS, 0.1)
    t = norm(w)
    wc = constrained_least_squares(XS, YS, t)
    assert max(abs(a - b) for a, b in zip(w, wc)) < 1e-8
    assert abs(lambda_for_radius(XS, YS, t) - 0.1) < 1e-8


def test_ridge_is_the_map_estimate() -> None:
    noise_var, prior_var = 0.09, 0.5
    lam = noise_var / (len(XS) * prior_var)
    w = ridge(XS, YS, lam)
    assert max(abs(g) for g in map_gradient(w, XS, YS, noise_var, prior_var)) < 1e-10


def test_shrinkage_maps_against_a_grid() -> None:
    grid = [i / 1000 for i in range(-4000, 4001)]
    for z in (-2.3, -0.4, 0.0, 0.7, 1.9):
        for a in (0.0, 0.5, 1.0):
            best = min(grid, key=lambda w: 0.5 * (w - z) ** 2 + a * abs(w))
            assert abs(best - soft_threshold(z, a)) <= 1e-3
            best = min(grid, key=lambda w: 0.5 * (w - z) ** 2 + 0.5 * a * w * w)
            assert abs(best - l2_shrink(z, a)) <= 1e-3
    assert soft_threshold(0.3, 0.5) == 0.0


def test_early_stopping_norm_grows_toward_least_squares() -> None:
    sig, _ = moments(XS, YS)
    eta = 1 / (2 * max(sum(abs(v) for v in row) for row in sig))
    path = gradient_descent_path(XS, YS, eta, 400)
    norms = [norm(w) for w in path]
    assert all(b >= a - 1e-12 for a, b in zip(norms, norms[1:]))
    w_ls = ridge(XS, YS, 0.0)
    assert norms[-1] <= norm(w_ls) + 1e-9
    assert max(abs(a - b) for a, b in zip(path[-1], w_ls)) < 1e-6


def test_replace_one_stability_bound() -> None:
    rng = random.Random(2)
    n = len(XS)
    for lam in (0.05, 0.1, 1.0):
        w = ridge(XS, YS, lam)
        for i in range(n):
            x_new, y_new = [rng.uniform(-1, 1) for _ in range(3)], rng.uniform(-2, 2)
            xs2, ys2 = XS[:i] + [x_new] + XS[i + 1:], YS[:i] + [y_new] + YS[i + 1:]
            w2 = ridge(xs2, ys2, lam)
            bound = stability_bound(XS + [x_new], YS + [y_new], lam, n)
            assert norm([a - b for a, b in zip(w, w2)]) <= bound
