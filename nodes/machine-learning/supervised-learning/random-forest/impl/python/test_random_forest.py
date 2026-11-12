# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-forest/. The authors are listed in prov/N15Y9F.jsonl.

import random

from random_forest import (best_split_on, default_mtry, grow_tree, oob_error, oob_predict, oob_trees,
                           permutation_importance, predict, random_forest, strength_correlation, tree_predict)


def noisy_data(rng: random.Random, n: int, d: int, noise: float):
    xs = [tuple(rng.random() for _ in range(d)) for _ in range(n)]
    ys = []
    for x in xs:
        y = int(x[0] + 0.5 * x[1] > 0.75)
        ys.append(1 - y if rng.random() < noise else y)
    return xs, ys


def gini_cost(ys, ids):
    n = len(ids)
    counts = {}
    for i in ids:
        counts[ys[i]] = counts.get(ys[i], 0) + 1
    return n - sum(c * c for c in counts.values()) / n


def test_default_mtry() -> None:
    assert default_mtry(16, "classification") == 4
    assert default_mtry(10, "classification") == 3
    assert default_mtry(9, "regression") == 3
    assert default_mtry(2, "regression") == 1
    assert default_mtry(1, "classification") == 1


def test_split_is_best_over_the_drawn_features() -> None:
    rng = random.Random(1)
    xs, ys = noisy_data(rng, 40, 6, 0.1)
    for _ in range(10):
        sample = [rng.randrange(40) for _ in range(40)]
        tree = grow_tree(xs, ys, sample, "classification", 2, 1, rng)
        _, k, thr, _, _, cand = tree[0]
        assert len(cand) == 2 and len(set(cand)) == 2 and k in cand
        costs = {f: best_split_on(xs, ys, sample, f, "classification", 1) for f in cand}
        assert costs[k][1] == thr
        assert all(costs[k][0] <= c[0] + 1e-12 for c in costs.values())
    rng = random.Random(2)
    xs, ys = noisy_data(rng, 25, 3, 0.2)
    ids = list(range(25))
    for f in range(3):
        cost, thr = best_split_on(xs, ys, ids, f, "classification", 1)
        brute = min(gini_cost(ys, [i for i in ids if xs[i][f] <= t]) + gini_cost(ys, [i for i in ids if xs[i][f] > t])
                    for t in sorted(set(x[f] for x in xs))[:-1])
        assert abs(cost - brute) < 1e-9


def test_regression_split_against_brute_force() -> None:
    rng = random.Random(3)
    xs = [(rng.random(), float(rng.randrange(4))) for _ in range(30)]
    ys = [x[0] * 3 + x[1] + rng.gauss(0, 0.3) for x in xs]
    ids = list(range(30))

    def sse(part):
        mu = sum(ys[i] for i in part) / len(part)
        return sum((ys[i] - mu) ** 2 for i in part)

    for f in range(2):
        for n_leaf in (1, 5):
            cost, _ = best_split_on(xs, ys, ids, f, "regression", n_leaf)
            brute = []
            for t in sorted(set(x[f] for x in xs))[:-1]:
                left = [i for i in ids if xs[i][f] <= t]
                right = [i for i in ids if xs[i][f] > t]
                if len(left) >= n_leaf and len(right) >= n_leaf:
                    brute.append(sse(left) + sse(right))
            assert abs(cost - min(brute)) < 1e-9


def test_oob_uses_exactly_the_trees_that_did_not_see_the_row() -> None:
    rng = random.Random(4)
    xs, ys = noisy_data(rng, 30, 4, 0.1)
    forest = random_forest(xs, ys, "classification", 25, rng)
    for i in range(30):
        used = oob_trees(forest, i)
        expected = [t for t, in_bag in forest if i not in in_bag]
        assert used == expected
        assert all(i not in in_bag for t, in_bag in forest if any(t is u for u in used))
        p = oob_predict(forest, xs, i, "classification")
        if used:
            votes = [tree_predict(t, xs[i]) for t in used]
            assert votes.count(p) == max(votes.count(c) for c in set(votes))
        else:
            assert p is None
    # Fully grown trees fit their own sample, so the in-bag error is 0; the OOB error does not see that fit.
    assert all(tree_predict(t, xs[i]) == ys[i] for t, in_bag in forest for i in in_bag)
    assert 0.0 <= oob_error(forest, xs, ys, "classification") <= 1.0


def test_unused_feature_has_zero_importance() -> None:
    rng = random.Random(5)
    xs, ys = noisy_data(rng, 40, 3, 0.0)
    forest = random_forest(xs, ys, "classification", 15, rng, mtry=3)
    used = {node[1] for tree, _ in forest for node in tree if node[0] == "split"}
    imp = permutation_importance(forest, xs, ys, "classification", random.Random(6))
    for k in range(3):
        if k not in used:
            assert imp[k] == 0.0
    assert imp[0] > 0.0


def test_theorem_2_3_bound_on_a_finite_distribution() -> None:
    for seed in range(8):
        rng = random.Random(100 + seed)
        xs, ys = noisy_data(rng, 50, 4, 0.15)
        test_x, test_y = noisy_data(rng, 60, 4, 0.15)
        forest = random_forest(xs, ys, "classification", 9, rng, mtry=1 + seed % 3, n_leaf=1 + 4 * (seed % 2))
        q = strength_correlation([t for t, _ in forest], test_x, test_y)
        # var(mg) = E[rho sd sd] = rho_bar (E sd)^2, by the definition of rho_bar.
        assert abs(q["var_mg"] - q["cov_sum"]) < 1e-12
        assert abs(q["var_mg"] - q["rho_bar"] * q["mean_sd"] ** 2) < 1e-12
        # (E sd)^2 <= E var <= 1 - s^2.
        assert q["mean_sd"] ** 2 <= q["mean_var"] + 1e-12
        assert q["mean_var"] <= 1 - q["s"] ** 2 + 1e-12
        if q["s"] > 0:
            assert q["pe"] <= q["var_mg"] / q["s"] ** 2 + 1e-12
            assert q["pe"] <= q["bound"] + 1e-12


def test_regression_forest_averages_trees() -> None:
    rng = random.Random(7)
    xs = [(rng.random(), rng.random(), rng.random()) for _ in range(30)]
    ys = [2 * x[0] + rng.gauss(0, 0.1) for x in xs]
    forest = random_forest(xs, ys, "regression", 6, rng)
    x = (0.3, 0.6, 0.1)
    assert abs(predict(forest, x, "regression") - sum(tree_predict(t, x) for t, _ in forest) / 6) < 1e-12
    for tree, _ in forest:
        for node in tree:
            if node[0] == "split":
                assert len(node[5]) == 1  # floor(3/3) features per node
