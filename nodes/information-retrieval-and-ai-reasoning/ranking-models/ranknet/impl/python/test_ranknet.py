# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranknet/. The authors are listed in prov/DHZW3Q.jsonl.

import math
import random

from ranknet import (
    cost,
    gradient,
    gradient_by_pairs,
    lambdas,
    ndcg,
    pair_cost,
    preferred_pairs,
    query_cost,
    ranking,
    scores,
    train,
)

TOL = 1e-6


def planted(seed, n_queries=6, n_docs=6, d=3):
    """Queries whose labels 0..2 come from a hidden linear score plus noise."""
    rng = random.Random(seed)
    w_true = [rng.uniform(-1, 1) for _ in range(d)]
    queries = []
    for _ in range(n_queries):
        xs = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(n_docs)]
        t = [sum(a * b for a, b in zip(w_true, x)) + rng.gauss(0, 0.1) for x in xs]
        order = sorted(t)
        lo, hi = order[n_docs // 3], order[2 * n_docs // 3]
        y = [0 if v < lo else (1 if v < hi else 2) for v in t]
        queries.append((xs, y))
    return queries


def numeric_gradient(f, w, h=1e-6):
    g = []
    for k in range(len(w)):
        a = list(w)
        b = list(w)
        a[k] += h
        b[k] -= h
        g.append((f(a) - f(b)) / (2 * h))
    return g


def test_page_example():
    # Two features, documents A, B, C with labels 1, 0, 2, sigma = 1.
    xs = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    y = [1, 0, 2]
    queries = [(xs, y)]
    assert abs(cost([0.0, 0.0], queries) - 3 * math.log(2)) < 1e-12
    assert lambdas([0.0, 0.0, 0.0], y) == [0.0, 1.0, -1.0]
    assert gradient([0.0, 0.0], queries) == [-1.0, 0.0]
    w, history = train(queries, 2, steps=1)
    assert w == [1.0, 0.0]
    s = scores(w, xs)
    assert round(query_cost(s, y), 4) == 1.3197
    assert [round(v, 4) for v in lambdas(s, y)] == [0.2311, 0.5379, -0.7689]
    assert [round(v, 4) for v in gradient(w, queries)] == [-0.5379, -0.2311]


def test_pair_cost_forms():
    # With pbar = 1 the general cross-entropy is softplus(-sigma o).
    for o in (-3.0, -0.5, 0.0, 0.7, 4.0):
        for sigma in (0.5, 1.0, 2.0):
            assert abs(pair_cost(o, 1.0, sigma) - math.log1p(math.exp(-sigma * o))) < 1e-12
    # With pbar = 1/2 the cost is log 2 at o = 0 and grows on both sides.
    assert abs(pair_cost(0.0, 0.5) - math.log(2)) < 1e-12
    assert pair_cost(1.0, 0.5) > math.log(2) and pair_cost(-1.0, 0.5) > math.log(2)


def test_gradient_against_finite_differences():
    rng = random.Random(1)
    for sigma in (0.5, 1.0, 2.0):
        queries = planted(seed=7)
        for _ in range(5):
            w = [rng.uniform(-2, 2) for _ in range(3)]
            g = gradient(w, queries, sigma)
            num = numeric_gradient(lambda v: cost(v, queries, sigma), w)
            assert all(abs(a - b) < TOL * max(1.0, abs(b)) for a, b in zip(g, num))


def test_factorized_equals_pairwise():
    rng = random.Random(2)
    queries = planted(seed=3)
    for _ in range(10):
        w = [rng.uniform(-2, 2) for _ in range(3)]
        a = gradient(w, queries)
        b = gradient_by_pairs(w, queries)
        assert all(abs(p - q) < 1e-9 for p, q in zip(a, b))


def test_lambdas_sum_to_zero():
    rng = random.Random(4)
    for xs, y in planted(seed=5):
        s = [rng.uniform(-1, 1) for _ in xs]
        assert abs(sum(lambdas(s, y))) < 1e-12


def test_cost_never_increases_and_falls():
    queries = planted(seed=11)
    w, history = train(queries, 3, steps=200)
    assert all(b <= a + 1e-12 for a, b in zip(history, history[1:]))
    assert history[-1] < history[0]
    # Measured on this planted set, not a theorem: the learned w ranks
    # better than w = 0, whose ranking is by document index only.
    before = sum(ndcg([0.0] * len(y), y) for _, y in queries)
    after = sum(ndcg(scores(w, xs), y) for xs, y in queries)
    assert after > before


def test_equal_labels_add_no_pair():
    assert preferred_pairs([1, 1, 1]) == []
    assert query_cost([0.3, -2.0, 5.0], [1, 1, 1]) == 0.0


def test_ranking_ties_by_index():
    assert ranking([1.0, 2.0, 2.0, 0.5]) == [1, 2, 0, 3]
    assert ndcg([0.0, 0.0], [0, 0]) is None
