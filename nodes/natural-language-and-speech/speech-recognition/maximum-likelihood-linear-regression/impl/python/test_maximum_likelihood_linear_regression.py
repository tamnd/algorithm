# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-linear-regression/. The authors are listed in prov/TR4HQ1.jsonl.

import math
import random

import pytest

from maximum_likelihood_linear_regression import (
    accumulate,
    adapt_means,
    apply_transform,
    auxiliary,
    estimate_transforms,
    identity_transform,
    log_gauss_diag,
    mllr,
    posteriors,
    solve,
)


def sample_frames(rng, weights, means, variances, T):
    out = []
    for _ in range(T):
        u = rng.random()
        m = 0
        acc = weights[0]
        while u > acc and m < len(weights) - 1:
            m += 1
            acc += weights[m]
        out.append([rng.gauss(mu, math.sqrt(v)) for mu, v in zip(means[m], variances[m])])
    return out


def test_page_example():
    # 1-dimensional means 0, 1, 3 with unit variances, occupancies 4, 2, 2 and
    # data means 1, 2, 8: the transform is mu' = (7/3) mu + 2/3.
    means = [[0.0], [1.0], [3.0], [2.0]]
    variances = [[1.0]] * 4
    occ = [4.0, 2.0, 2.0, 0.0]
    s = [[4.0], [4.0], [16.0], [0.0]]
    (W,) = estimate_transforms(means, variances, occ, s)
    assert W[0][0] == pytest.approx(2.0 / 3.0, abs=1e-12)
    assert W[0][1] == pytest.approx(7.0 / 3.0, abs=1e-12)
    adapted = adapt_means(means, [W])
    assert [round(a[0], 9) for a in adapted] == [round(2 / 3, 9), 3.0, round(23 / 3, 9), round(16 / 3, 9)]


def test_planted_transform_recovered_from_exact_statistics():
    rng = random.Random(1)
    n, M = 3, 7
    means = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(M)]
    variances = [[rng.uniform(0.5, 2.0) for _ in range(n)] for _ in range(M)]
    W_true = [[rng.uniform(-1, 1)] + [(1.0 if i == j else 0.0) + rng.uniform(-0.3, 0.3) for j in range(n)]
              for i in range(n)]
    occ = [rng.uniform(1, 20) for _ in range(M)]
    s = [[o * v for v in apply_transform(W_true, mu)] for o, mu in zip(occ, means)]
    (W,) = estimate_transforms(means, variances, occ, s)
    for i in range(n):
        for j in range(n + 1):
            assert W[i][j] == pytest.approx(W_true[i][j], abs=1e-9)


def test_identity_when_data_match_the_model():
    rng = random.Random(2)
    n, M = 2, 4
    means = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(M)]
    variances = [[1.0, 2.0]] * M
    occ = [3.0, 1.0, 5.0, 2.0]
    s = [[o * v for v in mu] for o, mu in zip(occ, means)]
    (W,) = estimate_transforms(means, variances, occ, s)
    I = identity_transform(n)
    for i in range(n):
        for j in range(n + 1):
            assert W[i][j] == pytest.approx(I[i][j], abs=1e-9)


def test_m_step_maximizes_the_auxiliary_function():
    rng = random.Random(3)
    n, M = 2, 5
    means = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(M)]
    variances = [[rng.uniform(0.5, 2.0) for _ in range(n)] for _ in range(M)]
    occ = [rng.uniform(0.5, 5) for _ in range(M)]
    s = [[o * rng.uniform(-4, 4) for _ in range(n)] for o in occ]
    Ws = estimate_transforms(means, variances, occ, s)
    best = auxiliary(means, variances, occ, s, Ws)
    for _ in range(50):
        P = [[[v + rng.uniform(-0.1, 0.1) for v in row] for row in Ws[0]]]
        assert auxiliary(means, variances, occ, s, P) < best
    h = 1e-6
    for i in range(n):
        for j in range(n + 1):
            up = [[row[:] for row in Ws[0]]]
            dn = [[row[:] for row in Ws[0]]]
            up[0][i][j] += h
            dn[0][i][j] -= h
            g = (auxiliary(means, variances, occ, s, up) - auxiliary(means, variances, occ, s, dn)) / (2 * h)
            assert abs(g) < 1e-5


def test_em_recovers_planted_transform_and_likelihood_never_decreases():
    rng = random.Random(4)
    weights = [0.25, 0.25, 0.25, 0.25]
    means = [[-4.0, 0.0], [4.0, 0.0], [0.0, 4.0], [0.0, -4.0]]
    variances = [[0.5, 0.5], [0.5, 0.8], [0.6, 0.5], [0.5, 0.5]]
    W_true = [[1.0, 1.1, 0.2], [-0.5, -0.1, 0.9]]
    adapted_true = [apply_transform(W_true, mu) for mu in means]
    frames = sample_frames(rng, weights, adapted_true, variances, 800)
    Ws, adapted, history = mllr(frames, weights, means, variances, iterations=8)
    for a, b in zip(history, history[1:]):
        assert b >= a - 1e-9
    assert history[-1] > history[0] + 100
    for i in range(2):
        for j in range(3):
            assert Ws[0][i][j] == pytest.approx(W_true[i][j], abs=0.1)


def test_regression_classes_are_independent():
    rng = random.Random(5)
    n = 2
    means = [[rng.uniform(-3, 3) for _ in range(n)] for _ in range(6)]
    variances = [[1.0, 1.0]] * 6
    classes = [0, 0, 0, 1, 1, 1]
    W0 = [[0.5, 1.0, 0.1], [0.0, -0.2, 1.2]]
    W1 = [[-1.0, 0.8, 0.0], [2.0, 0.0, 0.7]]
    occ = [2.0] * 6
    s = [[2.0 * v for v in apply_transform([W0, W1][classes[m]], means[m])] for m in range(6)]
    Ws = estimate_transforms(means, variances, occ, s, classes)
    for W, Wt in zip(Ws, [W0, W1]):
        for i in range(n):
            for j in range(n + 1):
                assert W[i][j] == pytest.approx(Wt[i][j], abs=1e-9)


def test_too_little_data_is_singular():
    # Two Gaussians cannot fix a 2 x 3 transform: G has rank 2.
    means = [[0.0, 0.0], [1.0, 1.0], [5.0, 5.0]]
    variances = [[1.0, 1.0]] * 3
    occ = [3.0, 3.0, 0.0]
    s = [[0.0, 0.0], [3.0, 3.0], [0.0, 0.0]]
    with pytest.raises(ValueError):
        estimate_transforms(means, variances, occ, s)
    with pytest.raises(ValueError):
        solve([[0.0, 0.0], [0.0, 0.0]], [1.0, 1.0])


def test_solve_against_known_solution():
    G = [[4.0, 1.0, 2.0], [1.0, 3.0, 0.0], [2.0, 0.0, 5.0]]
    x = [1.0, -2.0, 0.5]
    k = [sum(a * b for a, b in zip(row, x)) for row in G]
    assert solve(G, k) == pytest.approx(x, abs=1e-12)


def test_log_space_posteriors_where_plain_densities_underflow():
    weights = [0.5, 0.5]
    means = [[0.0], [2.0]]
    variances = [[1.0], [1.0]]
    x = [1000.0]
    plain = [w * math.exp(-0.5 * (x[0] - m[0]) ** 2) for w, m in zip(weights, means)]
    assert plain == [0.0, 0.0]
    g, z = posteriors(x, weights, means, variances)
    assert sum(g) == pytest.approx(1.0)
    assert g[1] == pytest.approx(1.0)
    assert g[0] < 1e-300
    assert math.isfinite(z)
    assert z == pytest.approx(math.log(0.5) + log_gauss_diag(x, means[1], variances[1]) + math.log1p(math.exp(-1996.0)))


def test_accumulate_statistics():
    weights = [1.0]
    means = [[0.0, 0.0]]
    variances = [[1.0, 1.0]]
    frames = [[1.0, 2.0], [3.0, -1.0]]
    occ, s, ll = accumulate(frames, weights, means, variances)
    assert occ == [2.0]
    assert s == [[4.0, 1.0]]
    assert ll == pytest.approx(sum(log_gauss_diag(o, means[0], variances[0]) for o in frames))
