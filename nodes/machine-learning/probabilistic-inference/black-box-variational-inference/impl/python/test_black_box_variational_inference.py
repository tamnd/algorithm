# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/black-box-variational-inference/. The authors are listed in prov/3YYRHH.jsonl.

import math
import random

from black_box_variational_inference import GaussianTarget, bbvi, reparam_gradient, score_gradient

TARGET = GaussianTarget([[2.0, 0.8], [0.8, 1.0]], [1.0, -1.0])
MU, OM = [3.0, 3.0], [0.0, 0.0]


def moments(draw, n):
    flat = [[x for pair in draw() for x in pair] for _ in range(n)]
    cols = list(zip(*flat))
    mean = [sum(c) / n for c in cols]
    var = [sum((x - m) ** 2 for x in c) / (n - 1) for c, m in zip(cols, mean)]
    return mean, var


def test_exact_gradient_matches_finite_differences_of_the_elbo():
    mu, om = [0.4, -0.3], [0.2, -0.5]
    g = TARGET.exact_gradient(mu, om)
    h = 1e-6
    for i in range(2):
        for d in range(2):
            a = [list(mu), list(om)]
            b = [list(mu), list(om)]
            a[d][i] += h
            b[d][i] -= h
            fd = (TARGET.elbo(*a) - TARGET.elbo(*b)) / (2 * h)
            assert abs(fd - g[i][d]) < 1e-6


def test_both_estimators_are_unbiased():
    rng = random.Random(11)
    exact = [x for pair in TARGET.exact_gradient(MU, OM) for x in pair]
    assert exact == [-7.4, -1.0, -6.4, 0.0]
    n = 2000
    estimators = [
        lambda: score_gradient(TARGET.log_p_i, MU, OM, 10, rng, rao_blackwell=False, control_variate=False),
        lambda: score_gradient(TARGET.log_p_i, MU, OM, 10, rng),
        lambda: reparam_gradient(TARGET.grad_log_p, MU, OM, 10, rng),
    ]
    for draw in estimators:
        mean, var = moments(draw, n)
        for m, v, e in zip(mean, var, exact):
            assert abs(m - e) < 5 * math.sqrt(v / n) + 1e-9


def test_score_estimator_has_larger_variance():
    rng = random.Random(12)
    n = 2000
    _, v_basic = moments(lambda: score_gradient(TARGET.log_p_i, MU, OM, 10, rng, False, False), n)
    _, v_rb = moments(lambda: score_gradient(TARGET.log_p_i, MU, OM, 10, rng, True, False), n)
    _, v_cv = moments(lambda: score_gradient(TARGET.log_p_i, MU, OM, 10, rng), n)
    _, v_rep = moments(lambda: reparam_gradient(TARGET.grad_log_p, MU, OM, 10, rng), n)
    assert sum(v_basic) > sum(v_rb) > sum(v_cv) > 5 * sum(v_rep)


def test_bbvi_reaches_the_optimum():
    # The best mean-field Gaussian has mean L^{-1} eta and variances 1 / L_ii.
    mu_star = [(1.0 + 0.8) / 1.36, (-2.0 - 0.8) / 1.36]
    mu, om = bbvi(TARGET.log_p_i, 2, 10, 2000, random.Random(7))
    assert max(abs(a - b) for a, b in zip(mu, mu_star)) < 0.1
    assert abs(math.exp(2 * om[0]) - 0.5) < 0.1 and abs(math.exp(2 * om[1]) - 1.0) < 0.1
    assert TARGET.elbo(mu, om) > TARGET.elbo(mu_star, [math.log(0.5) / 2, 0.0]) - 0.02
