# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restricted-maximum-likelihood/. The authors are listed in prov/6YVPGK.jsonl.

import math
import random

import pytest

from restricted_maximum_likelihood import (
    anova_one_way, evaluate, fit_variance_components, one_way_design,
)

GROUPS = [[10, 12, 14], [15, 16, 17], [18, 20, 22]]


def test_one_sample_reml_uses_divisor_n_minus_1():
    rng = random.Random(20261114)
    for n in (2, 3, 5, 9):
        y = [rng.gauss(3.0, 2.0) for _ in range(n)]
        x = [[1.0] for _ in range(n)]
        eye = [[1.0 if i == k else 0.0 for k in range(n)] for i in range(n)]
        mean = math.fsum(y) / n
        ss = math.fsum((v - mean) ** 2 for v in y)
        reml = fit_variance_components(y, x, [eye], "reml")
        ml = fit_variance_components(y, x, [eye], "ml")
        assert math.isclose(reml.theta[0], ss / (n - 1), rel_tol=1e-9)
        assert math.isclose(ml.theta[0], ss / n, rel_tol=1e-9)
        assert math.isclose(reml.b[0], mean, rel_tol=1e-12)


def test_balanced_one_way_example():
    y, x, vs = one_way_design(GROUPS)
    reml = fit_variance_components(y, x, vs, "reml")
    assert math.isclose(reml.theta[0], 15.0, rel_tol=1e-8)
    assert math.isclose(reml.theta[1], 3.0, rel_tol=1e-8)
    assert reml.at_boundary == [False, False]
    assert all(abs(s) < 1e-7 for s in reml.score)
    ml = fit_variance_components(y, x, vs, "ml")
    assert math.isclose(ml.theta[0], 29.0 / 3.0, rel_tol=1e-8)
    assert math.isclose(ml.theta[1], 3.0, rel_tol=1e-8)
    assert anova_one_way(GROUPS) == (15.0, 3.0)


def test_reml_equals_anova_or_the_boundary_solution():
    rng = random.Random(7)
    seen_boundary = seen_inside = 0
    for _ in range(16):
        a, m = 4, 3
        su = rng.choice([0.0, 0.3, 2.0])
        groups = []
        for _ in range(a):
            u = rng.gauss(0.0, math.sqrt(su))
            groups.append([5.0 + u + rng.gauss(0.0, 1.0) for _ in range(m)])
        y, x, vs = one_way_design(groups)
        fit = fit_variance_components(y, x, vs, "reml")
        su_hat, se_hat = anova_one_way(groups)
        if su_hat > 0:
            seen_inside += 1
            assert math.isclose(fit.theta[0], su_hat, rel_tol=1e-7, abs_tol=1e-9)
            assert math.isclose(fit.theta[1], se_hat, rel_tol=1e-7)
        else:
            seen_boundary += 1
            mean = math.fsum(y) / len(y)
            sst = math.fsum((v - mean) ** 2 for v in y)
            assert fit.theta[0] == 0.0 and fit.at_boundary[0]
            assert math.isclose(fit.theta[1], sst / (a * m - 1), rel_tol=1e-8)
            assert fit.score[0] <= 1e-9  # the KKT condition at theta_u = 0
    assert seen_boundary > 0 and seen_inside > 0


def test_restricted_likelihood_is_the_likelihood_of_error_contrasts():
    # Helmert contrasts K (n x (n - 1)) satisfy K^T 1 = 0; then l_K = l_R - (1/2) log|K^T K|.
    y, x, vs = one_way_design(GROUPS)
    n = len(y)
    k = [[(1.0 if i < c + 1 else (-(c + 1.0) if i == c + 1 else 0.0)) for c in range(n - 1)] for i in range(n)]
    theta = [4.0, 2.0]
    v = [[theta[0] * vs[0][i][j] + theta[1] * vs[1][i][j] for j in range(n)] for i in range(n)]
    ktvk = [[math.fsum(k[i][a] * v[i][j] * k[j][b] for i in range(n) for j in range(n)) for b in range(n - 1)] for a in range(n - 1)]
    kty = [math.fsum(k[i][a] * y[i] for i in range(n)) for a in range(n - 1)]
    ktk = [[math.fsum(k[i][a] * k[i][b] for i in range(n)) for b in range(n - 1)] for a in range(n - 1)]

    def logdet_and_solve(a, b):
        size = len(a)
        m = [row[:] + [b[i]] for i, row in enumerate(a)]
        logdet = 0.0
        for c in range(size):
            logdet += math.log(m[c][c])
            for r in range(c + 1, size):
                f = m[r][c] / m[c][c]
                m[r] = [u - f * w for u, w in zip(m[r], m[c])]
        out = [0.0] * size
        for i in reversed(range(size)):
            out[i] = (m[i][size] - math.fsum(m[i][j] * out[j] for j in range(i + 1, size))) / m[i][i]
        return logdet, out

    ld, sol = logdet_and_solve(ktvk, kty)
    l_k = -0.5 * ((n - 1) * math.log(2 * math.pi) + ld + math.fsum(a * b for a, b in zip(kty, sol)))
    ld_ktk, _ = logdet_and_solve(ktk, [0.0] * (n - 1))
    assert math.isclose(l_k, evaluate(y, x, vs, theta).loglik - 0.5 * ld_ktk, rel_tol=1e-11)


def test_score_matches_a_numerical_derivative():
    y, x, vs = one_way_design(GROUPS)
    theta = [7.0, 2.5]
    for method in ("reml", "ml"):
        here = evaluate(y, x, vs, theta, method)
        for j in range(2):
            h = 1e-5
            up = list(theta)
            dn = list(theta)
            up[j] += h
            dn[j] -= h
            num = (evaluate(y, x, vs, up, method).loglik - evaluate(y, x, vs, dn, method).loglik) / (2 * h)
            assert math.isclose(here.score[j], num, rel_tol=1e-6, abs_tol=1e-8)


def test_bad_method():
    y, x, vs = one_way_design(GROUPS)
    with pytest.raises(ValueError):
        evaluate(y, x, vs, [1.0, 1.0], "mom")
    with pytest.raises(ValueError):
        anova_one_way([[1.0, 2.0], [3.0]])
