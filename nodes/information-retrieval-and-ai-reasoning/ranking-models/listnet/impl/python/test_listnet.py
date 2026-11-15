# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/listnet/. The authors are listed in prov/TRPVZ8.jsonl.

import itertools
import math
import random

from listnet import (
    curvature_bound,
    gradient,
    loss,
    mean_ndcg,
    plackett_luce,
    query_loss,
    query_score_gradient,
    softmax,
    train,
)


def planted(seed, n_queries=6, n_docs=5, d=3):
    rng = random.Random(seed)
    w_true = [rng.uniform(-1, 1) for _ in range(d)]
    queries = []
    for _ in range(n_queries):
        xs = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(n_docs)]
        t = [sum(a * b for a, b in zip(w_true, x)) + rng.gauss(0, 0.1) for x in xs]
        order = sorted(t)
        y = [0 if v < order[2] else (1 if v < order[4] else 2) for v in t]
        queries.append((xs, y))
    return queries


def test_page_example():
    # Labels 2, 0, 1 and scores 1.0, 0.0, 0.5.
    s = [1.0, 0.0, 0.5]
    y = [2, 0, 1]
    assert [round(v, 4) for v in softmax(s)] == [0.5065, 0.1863, 0.3072]
    assert [round(v, 4) for v in softmax([2.0, 0.0, 1.0])] == [0.6652, 0.0900, 0.2447]
    assert round(query_loss(s, y), 4) == 0.8927
    assert [round(v, 4) for v in query_score_gradient(s, y)] == [-0.1588, 0.0963, 0.0625]
    # At s = 0 the loss is log 3.
    assert abs(query_loss([0.0, 0.0, 0.0], y) - math.log(3)) < 1e-12


def test_score_gradient_by_finite_differences():
    rng = random.Random(1)
    h = 1e-6
    for _ in range(100):
        n = rng.randint(1, 6)
        y = [rng.randint(0, 3) for _ in range(n)]
        s = [rng.uniform(-3, 3) for _ in range(n)]
        g = query_score_gradient(s, y)
        for i in range(n):
            a = list(s)
            b = list(s)
            a[i] += h
            b[i] -= h
            assert abs((query_loss(a, y) - query_loss(b, y)) / (2 * h) - g[i]) < 1e-6


def test_weight_gradient_by_finite_differences():
    rng = random.Random(2)
    queries = planted(seed=3)
    h = 1e-6
    for _ in range(5):
        w = [rng.uniform(-2, 2) for _ in range(3)]
        g = gradient(w, queries)
        for c in range(3):
            a = list(w)
            b = list(w)
            a[c] += h
            b[c] -= h
            assert abs((loss(a, queries) - loss(b, queries)) / (2 * h) - g[c]) < 1e-6


def test_top_one_probability_is_sum_of_plackett_luce():
    rng = random.Random(4)
    s = [rng.uniform(-1, 1) for _ in range(4)]
    p = softmax(s)
    total = 0.0
    for j in range(4):
        pj = sum(plackett_luce(s, perm) for perm in itertools.permutations(range(4)) if perm[0] == j)
        assert abs(pj - p[j]) < 1e-12
        total += pj
    assert abs(total - 1.0) < 1e-12


def test_loss_is_convex_in_w_on_segments():
    rng = random.Random(5)
    queries = planted(seed=6)
    for _ in range(30):
        u = [rng.uniform(-3, 3) for _ in range(3)]
        v = [rng.uniform(-3, 3) for _ in range(3)]
        t = rng.random()
        mid = [t * a + (1 - t) * b for a, b in zip(u, v)]
        assert loss(mid, queries) <= t * loss(u, queries) + (1 - t) * loss(v, queries) + 1e-12


def test_shift_invariance():
    s = [0.3, -1.2, 2.0]
    y = [1, 0, 2]
    assert abs(query_loss(s, y) - query_loss([v + 5.0 for v in s], y)) < 1e-12


def test_step_one_over_m_never_increases_loss():
    queries = planted(seed=7)
    assert curvature_bound(queries) > 0
    w, history = train(queries, 3, steps=200)
    assert all(b <= a + 1e-12 for a, b in zip(history, history[1:]))
    assert history[-1] < history[0]
    # Measured on this planted set, not a theorem.
    assert mean_ndcg(w, queries) > mean_ndcg([0.0, 0.0, 0.0], queries)


def test_minimum_is_not_zero():
    # The loss is at least the entropy of P_y, and equals it only if P_s = P_y.
    y = [2, 0, 1]
    py = softmax([2.0, 0.0, 1.0])
    entropy = -sum(p * math.log(p) for p in py)
    assert abs(query_loss([2.0, 0.0, 1.0], y) - entropy) < 1e-12
    assert query_loss([5.0, 0.0, 1.0], y) > entropy
