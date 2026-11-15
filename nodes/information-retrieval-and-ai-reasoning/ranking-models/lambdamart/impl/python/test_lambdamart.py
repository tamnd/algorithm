# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambdamart/. The authors are listed in prov/HY1P4E.jsonl.

import itertools
import random

from lambdamart import (
    Tree,
    build,
    delta_ndcg,
    fit,
    flatten,
    frozen_cost,
    leaf_value,
    ndcg,
    round_targets,
    sse,
    targets_and_weights,
)


def planted(seed, n_queries=8, n_docs=6, d=3):
    """Labels from a hidden rule that a linear scorer cannot fit: x0 * x1 > 0."""
    rng = random.Random(seed)
    queries = []
    for _ in range(n_queries):
        xs = [[round(rng.uniform(-1, 1), 3) for _ in range(d)] for _ in range(n_docs)]
        y = [2 if x[0] > 0 and x[1] > 0 else (1 if x[0] > 0 else 0) for x in xs]
        queries.append((xs, y))
    return queries


def derivatives_by_finite_differences(s, y, sigma, k, h=1e-4):
    """-dC/ds_i and d2C/ds_i2 of the frozen cost, by central differences."""
    weights = delta_ndcg(s, y, k)
    c0 = frozen_cost(s, y, weights, sigma)
    g, hh = [], []
    for i in range(len(s)):
        a = list(s)
        b = list(s)
        a[i] += h
        b[i] -= h
        ca = frozen_cost(a, y, weights, sigma)
        cb = frozen_cost(b, y, weights, sigma)
        g.append(-(ca - cb) / (2 * h))
        hh.append((ca - 2 * c0 + cb) / (h * h))
    return g, hh


def test_page_example():
    # One query: labels 2, 1, 0, 0 and scores 0.5, 1.5, 1.0, 2.0, sigma = 1.
    s = [0.5, 1.5, 1.0, 2.0]
    y = [2, 1, 0, 0]
    g, h = targets_and_weights(s, y)
    assert [round(v, 4) for v in g] == [0.5009, -0.0038, -0.0493, -0.4479]
    assert [round(v, 4) for v in h] == [0.1053, 0.0540, 0.0219, 0.0940]
    assert round(leaf_value([0, 1], g, h), 4) == 3.1196
    assert round(leaf_value([2, 3], g, h), 4) == -4.2863


def test_targets_and_weights_by_finite_differences():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(2, 6)
        y = [rng.randint(0, 3) for _ in range(n)]
        s = [rng.uniform(-2, 2) for _ in range(n)]
        sigma = rng.choice([0.5, 1.0, 2.0])
        k = rng.choice([None, 2, 3])
        if ndcg(s, y, k) is None:
            continue
        g, h = targets_and_weights(s, y, sigma, k)
        gn, hn = derivatives_by_finite_differences(s, y, sigma, k)
        assert all(abs(a - b) < 1e-6 for a, b in zip(g, gn))
        assert all(abs(a - b) < 1e-4 for a, b in zip(h, hn))


def test_leaf_values_against_direct_computation():
    queries = planted(seed=2)
    rng = random.Random(3)
    scores = [[rng.uniform(-1, 1) for _ in qx] for qx, _ in queries]
    xs, _ = flatten(queries)
    g, h = round_targets(queries, scores)
    tree = Tree(build(xs, g, h, list(range(len(xs))), depth=2))
    # Direct computation: finite-difference derivatives, grouped by leaf.
    gd, hd = [], []
    for (qx, y), s in zip(queries, scores):
        a, b = derivatives_by_finite_differences(s, y, 1.0, None)
        gd += a
        hd += b
    groups = {}
    for i, x in enumerate(xs):
        groups.setdefault(tree.leaf_of(x), []).append(i)
    for path, idx in groups.items():
        direct = sum(gd[i] for i in idx) / sum(hd[i] for i in idx)
        assert abs(tree.predict(xs[idx[0]]) - direct) < 1e-4


def test_split_is_least_squares():
    rng = random.Random(4)
    xs = [[round(rng.uniform(0, 1), 2), round(rng.uniform(0, 1), 2)] for _ in range(9)]
    g = [rng.uniform(-1, 1) for _ in xs]
    h = [1.0] * len(xs)
    root = build(xs, g, h, list(range(len(xs))), depth=1)
    _, f, t, _, _ = root
    got = sse([g[i] for i in range(9) if xs[i][f] <= t]) + sse([g[i] for i in range(9) if xs[i][f] > t])
    best = min(
        sse([g[i] for i in range(9) if xs[i][ff] <= tt]) + sse([g[i] for i in range(9) if xs[i][ff] > tt])
        for ff, tt in itertools.product(range(2), sorted(set(v for x in xs for v in x)))
    )
    assert got <= best + 1e-12


def test_query_with_one_label_gets_no_push():
    g, h = targets_and_weights([0.1, 0.2, 0.3], [1, 1, 1])
    assert g == [0.0, 0.0, 0.0] and h == [0.0, 0.0, 0.0]
    assert leaf_value([0, 1, 2], g, h) == 0.0


def test_training_on_planted_set():
    # Measured on this planted set, not a theorem: depth 2 trees learn the
    # interaction x0 * x1 > 0 that a linear scorer cannot express.
    queries = planted(seed=5)
    trees, history = fit(queries, rounds=30, depth=2, eta=0.3)
    assert history[-1] > history[0]
    assert history[-1] > 0.95
