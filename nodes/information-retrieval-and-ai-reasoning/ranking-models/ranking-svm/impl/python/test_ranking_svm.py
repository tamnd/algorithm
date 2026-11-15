# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranking-svm/. The authors are listed in prov/VTCXN6.jsonl.

import random

from ranking_svm import (
    bound,
    dot,
    dual,
    dual_coordinate_ascent,
    misordered_pairs,
    objective,
    pairs,
    ranking,
    subgradient,
    train,
)


def noisy(seed, n_queries=5, n_docs=5, d=3):
    rng = random.Random(seed)
    w_true = [rng.uniform(-1, 1) for _ in range(d)]
    queries = []
    for _ in range(n_queries):
        xs = [[round(rng.uniform(-1, 1), 3) for _ in range(d)] for _ in range(n_docs)]
        t = [dot(w_true, x) + rng.gauss(0, 0.3) for x in xs]
        order = sorted(t)
        y = [0 if v < order[2] else (1 if v < order[4] else 2) for v in t]
        queries.append((xs, y))
    return queries


def separable(seed, n_queries=5, n_docs=5, d=3):
    """Labels from a hidden w_true with a gap of at least 0.2 between levels."""
    rng = random.Random(seed)
    w_true = [rng.uniform(-1, 1) for _ in range(d)]
    queries = []
    for _ in range(n_queries):
        xs, y = [], []
        while len(xs) < n_docs:
            x = [round(rng.uniform(-1, 1), 3) for _ in range(d)]
            t = dot(w_true, x)
            label = 2 if t > 0.4 else (1 if -0.2 < t < 0.2 else (0 if t < -0.6 else None))
            if label is not None:
                xs.append(x)
                y.append(label)
        queries.append((xs, y))
    return w_true, queries


def test_page_example():
    # One query, three documents with labels 2, 1, 0.
    queries = [([[2.0, 0.0], [1.0, 1.0], [0.0, 1.0]], [2, 1, 0])]
    zs = pairs(queries)
    assert zs == [[1.0, -1.0], [2.0, -1.0], [1.0, 0.0]]
    lam = 0.1
    assert objective([0.0, 0.0], zs, lam) == 1.0
    assert abs(objective([1.0, 0.0], zs, lam) - 0.05) < 1e-12
    alpha, wd = dual_coordinate_ascent(zs, lam, 100)
    assert abs(dual(alpha, zs, lam) - 0.05) < 1e-12
    w, history = train(queries, lam, 2000)
    assert history[-1] - 0.05 < 1e-6
    assert ranking([dot(w, x) for x in queries[0][0]]) == [0, 1, 2]


def test_best_objective_never_increases_and_falls():
    queries = noisy(seed=1)
    w, history = train(queries, 0.1, 500)
    assert all(b <= a for a, b in zip(history, history[1:]))
    assert history[-1] < history[0] == 1.0


def test_rate_bound_against_dual_lower_bound():
    for seed in (2, 3):
        queries = noisy(seed)
        zs = pairs(queries)
        for lam in (0.1, 0.3):
            alpha, wd = dual_coordinate_ascent(zs, lam, 300)
            lower = dual(alpha, zs, lam)
            # Weak duality: D(alpha) <= J(w) for every alpha in the box and every w.
            assert lower <= objective(wd, zs, lam) + 1e-12
            for steps in (50, 200, 800):
                _, history = train(queries, lam, steps)
                assert history[-1] >= lower - 1e-12
                assert history[-1] - lower <= bound(zs, lam, steps)


def test_subgradient_inequality():
    # J(u) >= J(w) + g . (u - w) + (lambda / 2) ||u - w||^2 for the returned g.
    rng = random.Random(4)
    zs = pairs(noisy(seed=5))
    lam = 0.2
    for _ in range(200):
        w = [rng.uniform(-2, 2) for _ in range(3)]
        u = [rng.uniform(-2, 2) for _ in range(3)]
        g = subgradient(w, zs, lam)
        diff = [a - b for a, b in zip(u, w)]
        rhs = objective(w, zs, lam) + dot(g, diff) + lam / 2 * dot(diff, diff)
        assert objective(u, zs, lam) >= rhs - 1e-12


def test_separable_instance_is_ranked_correctly():
    w_true, queries = separable(seed=1)
    zs = pairs(queries)
    margin = min(dot(w_true, z) for z in zs)
    assert margin > 0
    # Pick lambda so that the scaled w_true has J = 1 / (4P) < 1 / P.
    lam = margin * margin / (2.0 * len(zs) * dot(w_true, w_true))
    w, history = train(queries, lam, 500)
    # J(w) < 1 / P implies that every pair has w . z > 0 (proofs/correctness.md).
    assert history[-1] < 1.0 / len(zs)
    assert misordered_pairs(w, queries) == 0
    assert misordered_pairs(w_true, queries) == 0


def test_low_objective_lemma():
    # A misordered pair costs at least 1 / P, so J(w) < 1 / P forces zero errors.
    rng = random.Random(6)
    w_true, queries = separable(seed=1)
    zs = pairs(queries)
    scale = 1.0 / min(dot(w_true, z) for z in zs)
    low = 0
    for _ in range(500):
        w = [scale * a + rng.gauss(0, 1.5) for a in w_true]
        if objective(w, zs, 0.001) < 1.0 / len(zs):
            low += 1
            assert misordered_pairs(w, queries) == 0
        if misordered_pairs(w, queries) > 0:
            assert objective(w, zs, 0.001) >= 1.0 / len(zs)
    assert low > 0


def test_pairs_stay_inside_queries():
    queries = [([[1.0], [0.0]], [1, 0]), ([[5.0], [9.0]], [0, 0])]
    assert pairs(queries) == [[1.0]]
