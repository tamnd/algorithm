# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremely-randomized-trees/. The authors are listed in prov/ZH6FA9.jsonl.

import math
import random

from extremely_randomized_trees import build_tree, default_k, default_n_min, extra_trees, pick_random_split, predict, score, tree_predict


def data(rng: random.Random, n: int, d: int):
    xs = [tuple(rng.random() for _ in range(d)) for _ in range(n)]
    ys = [int(x[0] > 0.4) if rng.random() > 0.1 else int(x[0] <= 0.4) for x in xs]
    return xs, ys


def walk(nodes, i=0, ids=None, xs=None):
    """Yield (node, rows that reach it) by sending the rows down the tree."""
    node = nodes[i]
    yield node, ids
    if node[0] == "split":
        _, a, c, left, right, _ = node
        yield from walk(nodes, left, [j for j in ids if xs[j][a] < c], xs)
        yield from walk(nodes, right, [j for j in ids if xs[j][a] >= c], xs)


def test_defaults() -> None:
    assert default_k(16, "classification") == 4
    assert default_k(10, "classification") == 3
    assert default_k(7, "regression") == 7
    assert (default_n_min("classification"), default_n_min("regression")) == (2, 5)


def test_cut_point_is_uniform_between_min_and_max() -> None:
    xs = [(0.0,), (1.0,), (4.0,), (10.0,)]
    rng = random.Random(1)
    lefts = [0] * 4
    trials = 20000
    for _ in range(trials):
        c = pick_random_split(xs, [0, 1, 2, 3], 0, rng)
        assert 0.0 < c <= 10.0
        lefts[sum(x[0] < c for x in xs)] += 1
    # One row left with probability 1/10, two with 3/10, three with 6/10; never zero or four.
    assert lefts[0] == 0
    for j, p in ((1, 0.1), (2, 0.3), (3, 0.6)):
        assert abs(lefts[j] / trials - p) < 0.015


def test_scores_against_definitions() -> None:
    ys = ["a", "a", "b", "b"]
    assert abs(score(ys, [0, 1], [2, 3], "classification") - 1.0) < 1e-12  # perfect and balanced
    assert abs(score(ys, [0, 2], [1, 3], "classification")) < 1e-12  # independent of the class
    rng = random.Random(2)
    for _ in range(50):
        n = rng.randrange(2, 12)
        ys = [rng.choice("abc") for _ in range(n)]
        cut = rng.randrange(1, n)
        left, right = list(range(cut)), list(range(cut, n))
        sc = score(ys, left, right, "classification")
        if len(set(ys)) > 1:
            assert -1e-12 <= sc <= 1 + 1e-12
        # The mutual information computed from the joint table gives the same score.
        joint = {}
        for i in range(n):
            key = (i < cut, ys[i])
            joint[key] = joint.get(key, 0) + 1
        mi = sum(c / n * math.log((c / n) / ((cut if s else n - cut) / n * ys.count(y) / n)) for (s, y), c in joint.items())
        hc = -sum(ys.count(y) / n * math.log(ys.count(y) / n) for y in set(ys))
        hs = -sum(p * math.log(p) for p in (cut / n, 1 - cut / n))
        assert abs(sc - 2 * mi / (hc + hs)) < 1e-9
    yr = [1.0, 2.0, 3.0, 10.0]
    assert abs(score(yr, [0, 1, 2], [3], "regression") - (1 - 0.75 * (2 / 3) / 12.5)) < 1e-12


def test_tree_invariants() -> None:
    rng = random.Random(3)
    xs, ys = data(rng, 40, 5)
    for n_min in (2, 5, 12):
        tree = build_tree(xs, ys, "classification", 2, n_min, rng)
        sizes = 0
        for node, ids in walk(tree, 0, list(range(40)), xs):
            if node[0] == "leaf":
                sizes += len(ids)
                assert node[2] == len(ids)
                assert len(ids) < n_min or len({ys[i] for i in ids}) == 1
            else:
                _, a, c, _, _, cands = node
                assert len(ids) >= n_min and len(cands) == 2 and len({b for _, b, _ in cands}) == 2
                assert (score(ys, [i for i in ids if xs[i][a] < c], [i for i in ids if xs[i][a] >= c], "classification")
                        == max(s for s, _, _ in cands))
                assert min(xs[i][a] for i in ids) < c <= max(xs[i][a] for i in ids)
        assert sizes == 40  # the root holds the whole sample, with no bootstrap


def test_full_trees_fit_distinct_training_inputs() -> None:
    rng = random.Random(4)
    xs, ys = data(rng, 30, 3)
    trees = extra_trees(xs, ys, "classification", 5, rng)
    for t in trees:
        assert all(tree_predict(t, x) == y for x, y in zip(xs, ys))


def test_constant_attributes_are_never_drawn() -> None:
    rng = random.Random(5)
    xs = [(rng.random(), 7.0, rng.random()) for _ in range(20)]
    ys = [x[0] + x[2] for x in xs]
    trees = extra_trees(xs, ys, "regression", 4, rng)
    for t in trees:
        for node in t:
            if node[0] == "split":
                assert node[1] != 1 and all(a != 1 for _, a, _ in node[5])
                assert len(node[5]) == 2  # K = d, but only two attributes are not constant
    x = (0.5, 7.0, 0.5)
    assert abs(predict(trees, x, "regression") - sum(tree_predict(t, x) for t in trees) / 4) < 1e-12
