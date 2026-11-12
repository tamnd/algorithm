# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gaussian-mixture-model/. The authors are listed in prov/4RQ4DM.jsonl.

import math
import random

from gaussian_mixture_model import (bic, e_step, em, log_likelihood, log_normal, m_step,
                                    num_params, penalized, sample)

TRUE2 = ([0.4, 0.6], [[0.0, 0.0], [5.0, 1.0]], [[[1.0, 0.3], [0.3, 0.5]], [[0.8, -0.2], [-0.2, 1.5]]])


def test_log_likelihood_does_not_decrease():
    rng = random.Random(1)
    pts, _ = sample(TRUE2, 120, rng)
    for seed in range(4):
        for lam in [0.0, 0.5]:
            trace = []
            em(pts, 2, rng=random.Random(seed), lam=lam, max_iter=60, trace=trace)
            assert all(b >= a - 1e-9 * (1 + abs(a)) for a, b in zip(trace, trace[1:]))
            assert len(trace) >= 3


def test_one_dimensional_e_step_by_hand():
    pts = [[1.0], [2.0], [4.0], [7.0], [8.0]]
    model = ([0.5, 0.5], [[2.0], [6.0]], [[[1.0]], [[4.0]]])
    R = e_step(pts, model)

    def dens(x, m, v):
        return math.exp(-(x - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)

    for (x,), row in zip(pts, R):
        a, b = 0.5 * dens(x, 2, 1), 0.5 * dens(x, 6, 4)
        assert abs(row[0] - a / (a + b)) < 1e-12 and abs(sum(row) - 1) < 1e-12
    assert abs(log_normal([1.0, 2.0], [0.0, 0.0], [[2.0, 0.0], [0.0, 3.0]])
               - math.log(dens(1, 0, 2) * dens(2, 0, 3))) < 1e-12


def test_m_step_is_weighted_mle():
    pts = [[1.0], [2.0], [4.0], [7.0], [8.0]]
    R = [[1, 0], [1, 0], [0.5, 0.5], [0, 1], [0, 1]]
    w, mu, cov = m_step(pts, R, 0.0, None)
    assert w == [0.5, 0.5]
    assert abs(mu[0][0] - 5 / 2.5) < 1e-12 and abs(mu[1][0] - 17 / 2.5) < 1e-12
    v0 = (1 ** 2 + 0 ** 2 + 0.5 * 2 ** 2) / 2.5
    assert abs(cov[0][0][0] - v0) < 1e-12
    w, mu, cov = m_step(pts, R, 0.5, None)  # the regularized covariance
    assert abs(cov[0][0][0] - (3 + 0.5) / 2.5) < 1e-12


def test_label_permutation_does_not_change_anything():
    rng = random.Random(2)
    pts, _ = sample(TRUE2, 80, rng)
    model, R, _ = em(pts, 2, rng=random.Random(5), lam=0.0, max_iter=30)
    swapped = tuple(list(reversed(part)) for part in model)
    assert abs(log_likelihood(pts, model) - log_likelihood(pts, swapped)) < 1e-9
    R2 = e_step(pts, swapped)
    assert all(abs(a[0] - b[1]) < 1e-12 for a, b in zip(R, R2))


def test_likelihood_is_unbounded_without_regularization():
    pts = [[0.0], [1.0], [2.0], [3.0], [10.0]]
    values, pen = [], []
    for s in [1e-1, 1e-2, 1e-4, 1e-8]:
        model = ([0.5, 0.5], [[10.0], [1.5]], [[[s]], [[1.25]]])
        values.append(log_likelihood(pts, model))
        pen.append(penalized(pts, model, 0.1))
    assert all(b > a + 1 for a, b in zip(values, values[1:]))  # grows like -log(s)/2
    assert pen[-1] < pen[0] - 1e5  # the penalty wins


def test_hard_limit_is_k_means():
    rng = random.Random(3)
    pts = [[rng.uniform(0, 10), rng.uniform(0, 10)] for _ in range(30)]
    means = [[2.0, 2.0], [8.0, 3.0], [5.0, 9.0]]
    s = 1e-3
    model = ([1 / 3] * 3, means, [[[s, 0.0], [0.0, s]]] * 3)
    R = e_step(pts, model)
    for x, row in zip(pts, R):
        near = min(range(3), key=lambda j: sum((a - b) ** 2 for a, b in zip(x, means[j])))
        assert row[near] > 1 - 1e-9
    _, mu, _ = m_step(pts, R, 0.0, model)
    for j in range(3):
        members = [x for x, row in zip(pts, R) if max(range(3), key=row.__getitem__) == j]
        centroid = [sum(p[t] for p in members) / len(members) for t in range(2)]
        assert all(abs(a - b) < 1e-6 for a, b in zip(mu[j], centroid))


def test_bic():
    assert num_params(1, 1) == 2 and num_params(2, 2) == 11 and num_params(3, 3) == 29
    rng = random.Random(4)
    model = ([0.5, 0.5], [[0.0], [8.0]], [[[1.0]], [[1.0]]])
    pts, _ = sample(model, 150, rng)
    scores = {}
    for k in [1, 2, 3]:
        fit, _, _ = em(pts, k, rng=random.Random(k), lam=1e-6, max_iter=200)
        scores[k] = bic(pts, fit)
        assert abs(scores[k] - (-2 * log_likelihood(pts, fit) + num_params(k, 1) * math.log(150))) < 1e-9
    assert min(scores, key=scores.get) == 2
