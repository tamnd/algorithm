# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambdarank/. The authors are listed in prov/6YEMD5.jsonl.

import math
import random

from lambdarank import (
    delta_ndcg,
    frozen_cost,
    lambdas,
    ndcg,
    ndcg_of_order,
    pair_lambdas,
    ranking,
    softplus,
    train,
)


def planted(seed, n_queries=8, n_docs=6, d=3):
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


def swapped_ndcg_change(s, y, i, j, k=None):
    """|NDCG after swapping the positions of i and j - NDCG now|, computed directly."""
    order = ranking(s)
    a, b = order.index(i), order.index(j)
    new = list(order)
    new[a], new[b] = new[b], new[a]
    return abs(ndcg_of_order(new, y, k) - ndcg_of_order(order, y, k))


def ranknet_pair_gradient_numeric(s, i, j, sigma, h=1e-6):
    def c(v):
        return softplus(-sigma * (v[i] - v[j]))

    a = list(s)
    b = list(s)
    a[i] += h
    b[i] -= h
    return (c(a) - c(b)) / (2 * h)


def test_page_example():
    # Four documents with labels 2, 1, 0, 0 and scores 0.5, 1.5, 1.0, 2.0.
    s = [0.5, 1.5, 1.0, 2.0]
    y = [2, 1, 0, 0]
    assert ranking(s) == [3, 1, 2, 0]
    assert abs(ndcg(s, y) - 0.5296) < 1e-4
    lam = lambdas(s, y)
    assert [round(v, 4) for v in lam] == [-0.5009, 0.0038, 0.0493, 0.4479]
    lam2 = lambdas(s, y, k=2)
    assert [round(v, 4) for v in lam2] == [-0.9296, 0.1252, 0.0656, 0.7388]


def test_lambda_is_ranknet_gradient_times_swap_change():
    rng = random.Random(1)
    for trial in range(200):
        n = rng.randint(2, 7)
        y = [rng.randint(0, 3) for _ in range(n)]
        s = [rng.uniform(-2, 2) for _ in range(n)]
        sigma = rng.choice([0.5, 1.0, 2.0])
        k = rng.choice([None, 1, 2, 3, 5])
        if ndcg(s, y, k) is None:
            continue
        lam = pair_lambdas(s, y, sigma, k)
        for (i, j), v in lam.items():
            direct = ranknet_pair_gradient_numeric(s, i, j, sigma) * swapped_ndcg_change(s, y, i, j, k)
            assert abs(v - direct) < 1e-6


def test_closed_form_delta_equals_direct_swap():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(2, 7)
        y = [rng.randint(0, 3) for _ in range(n)]
        s = [rng.uniform(-2, 2) for _ in range(n)]
        k = rng.choice([None, 1, 2, 4])
        if ndcg(s, y, k) is None:
            continue
        for (i, j), v in delta_ndcg(s, y, k).items():
            assert abs(v - swapped_ndcg_change(s, y, i, j, k)) < 1e-12


def test_lambdas_are_gradient_of_frozen_cost():
    rng = random.Random(3)
    h = 1e-6
    for _ in range(50):
        n = rng.randint(2, 6)
        y = [rng.randint(0, 2) for _ in range(n)]
        s = [rng.uniform(-2, 2) for _ in range(n)]
        if ndcg(s, y) is None:
            continue
        weights = delta_ndcg(s, y)
        lam = lambdas(s, y)
        for c in range(n):
            a = list(s)
            b = list(s)
            a[c] += h
            b[c] -= h
            num = (frozen_cost(a, y, weights) - frozen_cost(b, y, weights)) / (2 * h)
            assert abs(num - lam[c]) < 1e-6


def test_pairs_below_cutoff_get_zero():
    s = [4.0, 3.0, 2.0, 1.0]
    y = [0, 0, 1, 2]
    lam = pair_lambdas(s, y, k=2)
    assert lam[(3, 2)] == 0.0
    assert lam[(3, 0)] != 0.0


def test_lambdas_sum_to_zero():
    rng = random.Random(4)
    for _ in range(50):
        y = [rng.randint(0, 3) for _ in range(5)]
        s = [rng.uniform(-1, 1) for _ in range(5)]
        assert abs(sum(lambdas(s, y))) < 1e-12


def test_training_on_planted_set():
    # Measured on this planted set, not a theorem.
    queries = planted(seed=5)
    w, history = train(queries, 3, eta=0.5, steps=60)
    assert history[-1] > history[0]
    assert max(history) > 0.9


def test_no_relevant_document():
    assert ndcg([1.0, 2.0], [0, 0]) is None
    assert lambdas([1.0, 2.0], [0, 0]) == [0.0, 0.0]
    assert math.isclose(ndcg([2.0, 1.0], [1, 0]), 1.0)
