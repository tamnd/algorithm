# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genie3/. The authors are listed in prov/NVTX2V.jsonl.

import math
import random

from genie3 import (
    auroc,
    best_split,
    genie3,
    grow_tree,
    predict,
    scale_to_unit_variance,
    sum_of_squares,
    target_importances,
)


def brute_force_best_reduction(x, y, idx, features):
    """Try every feature and every observed value as a threshold, with direct sums of squares."""
    best = None
    whole = sum_of_squares(y, idx)
    for f in features:
        for t in sorted(set(x[f][s] for s in idx)):
            left = [s for s in idx if x[f][s] <= t]
            right = [s for s in idx if x[f][s] > t]
            if not left or not right:
                continue
            red = whole - sum_of_squares(y, left) - sum_of_squares(y, right)
            if best is None or red > best:
                best = red
    return best


def simulate(rng, n):
    """Genes 0, 1, 2 are free regulators; 3, 4, 5 are targets.

    Draw order per sample: x0, x1, x2 with rng.gauss, then the noise of genes 3, 4 and 5.
    """
    data = [[0.0] * n for _ in range(6)]
    for s in range(n):
        x0, x1, x2 = rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)
        data[0][s], data[1][s], data[2][s] = x0, x1, x2
        data[3][s] = math.tanh(2 * x0) + 0.3 * rng.gauss(0, 1)
        data[4][s] = (x2 if x1 > 0 else 0.0) + 0.3 * rng.gauss(0, 1)
        data[5][s] = x2 * x2 + 0.3 * rng.gauss(0, 1)
    return data


TRUTH = {(0, 3), (1, 4), (2, 4), (2, 5)}


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sab = sum((u - ma) * (v - mb) for u, v in zip(a, b))
    sa = math.sqrt(sum((u - ma) ** 2 for u in a))
    sb = math.sqrt(sum((v - mb) ** 2 for v in b))
    return sab / (sa * sb)


def test_scale_to_unit_variance():
    y = scale_to_unit_variance([1.0, 2.0, 4.0, 7.0])
    mean = sum(y) / 4
    assert abs(sum((v - mean) ** 2 for v in y) / 4 - 1.0) < 1e-12
    assert scale_to_unit_variance([3.0, 3.0]) == [0.0, 0.0]


def test_split_matches_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        p, n = rng.randint(1, 4), rng.randint(2, 12)
        x = [[rng.choice([rng.random(), float(rng.randint(0, 3))]) for _ in range(n)] for _ in range(p)]
        y = [rng.gauss(0, 1) for _ in range(n)]
        idx = [rng.randrange(n) for _ in range(n)]  # repeats, as in a bootstrap sample
        feats = list(range(p))
        got = best_split(x, y, idx, feats)
        want = brute_force_best_reduction(x, y, idx, feats)
        if want is None:
            assert got is None
        else:
            assert abs(got[0] - want) < 1e-9


def test_full_tree_importances_sum_to_the_total_sum_of_squares():
    rng = random.Random(2)
    for _ in range(30):
        p, n = rng.randint(1, 4), rng.randint(5, 40)
        x = [[rng.random() for _ in range(n)] for _ in range(p)]
        y = scale_to_unit_variance([rng.gauss(0, 1) for _ in range(n)])
        imp = {}
        tree = grow_tree(rng, x, y, list(range(n)), list(range(p)), p, imp)
        # distinct inputs, so every leaf is pure and the tree fits the data
        assert abs(sum(imp.values()) - n) < 1e-8
        for s in range(n):
            assert abs(predict(tree, x, s) - y[s]) < 1e-9


def test_bootstrap_importances_sum_to_the_bootstrap_sum_of_squares():
    # with K equal to the number of inputs, the bootstrap draws are the only draws
    rng = random.Random(3)
    n, p, trees = 30, 3, 5
    x = [[rng.random() for _ in range(n)] for _ in range(p)]
    y = scale_to_unit_variance([rng.gauss(0, 1) for _ in range(n)])
    imp = target_importances(random.Random(9), x, y, list(range(p)), trees, p, bootstrap=True)
    replay = random.Random(9)
    want = 0.0
    for _ in range(trees):
        idx = [replay.randrange(n) for _ in range(n)]
        want += sum_of_squares(y, idx)
    assert abs(sum(imp.values()) - want / trees) < 1e-8


def test_step_target_gives_all_importance_to_its_regulator():
    rng = random.Random(4)
    n = 50
    x = [[rng.random() for _ in range(n)] for _ in range(3)]
    y = scale_to_unit_variance([1.0 if v > 0.5 else 0.0 for v in x[1]])
    imp = target_importances(rng, x, y, [0, 1, 2], 1, 3, bootstrap=False)
    assert abs(imp[1] - n) < 1e-9
    assert imp[0] == 0.0 and imp[2] == 0.0


def test_worked_example_of_the_page():
    # genes A, B, C = 0, 1, 2; C is 2 when B is low, plus 1 when A is high
    data = [[1.0, 2.0, 3.0, 4.0], [4.0, 1.0, 4.0, 1.0], [0.0, 2.0, 1.0, 3.0]]
    y = scale_to_unit_variance(data[2])
    rng = random.Random(0)
    imp = {}
    tree = grow_tree(rng, data, y, [0, 1, 2, 3], [0, 1], 2, imp)
    assert tree.feature == 1
    assert abs(imp[1] - 3.2) < 1e-12 and abs(imp[0] - 0.8) < 1e-12
    raw = best_split(data, data[2], [0, 1, 2, 3], [0])
    assert abs(raw[0] - 3.0) < 1e-12
    links = genie3(random.Random(0), data, n_trees=1, k=2, regulators=[0, 1], bootstrap=False)
    assert [(i, j) for i, j, _ in links if j == 2] == [(1, 2), (0, 2)]


def test_increasing_transform_of_the_inputs_changes_nothing():
    rng = random.Random(5)
    n, p = 40, 4
    x = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(p)]
    y = scale_to_unit_variance([x[0][s] * x[1][s] + rng.gauss(0, 0.2) for s in range(n)])
    x2 = [[math.exp(v) for v in row] if f % 2 == 0 else [v ** 3 for v in row] for f, row in enumerate(x)]
    a = target_importances(random.Random(11), x, y, list(range(p)), 10, 2)
    b = target_importances(random.Random(11), x2, y, list(range(p)), 10, 2)
    for f in range(p):
        assert abs(a[f] - b[f]) < 1e-9


def test_same_seed_same_ranking():
    data = simulate(random.Random(6), 40)
    a = genie3(random.Random(12), data, n_trees=5)
    b = genie3(random.Random(12), data, n_trees=5)
    assert a == b
    assert len(a) == 6 * 5
    assert all(a[q][2] >= a[q + 1][2] for q in range(len(a) - 1))


def test_auroc_small_case():
    assert auroc([3, 2, 1], [True, False, False]) == 1.0
    assert auroc([1, 2, 3], [True, False, False]) == 0.0
    assert auroc([1, 1], [True, False]) == 0.5


def test_recovery_on_simulated_data_is_measured():
    # a measurement for one seed, not a guarantee: 6 genes, 100 samples, 30 trees
    rng = random.Random(1)
    data = simulate(rng, 100)
    links = genie3(rng, data, n_trees=30, regulators=[0, 1, 2])
    pairs = [(i, j) for i, j, _ in links]
    assert len(pairs) == 15
    labels = [q in TRUTH for q in pairs]
    corr = {q: abs(pearson(data[q[0]], data[q[1]])) for q in pairs}
    by_corr = sorted(pairs, key=lambda q: (-corr[q], q))
    # the numbers quoted on the page
    assert sum(labels[:4]) == 3
    assert round(auroc([w for _, _, w in links], labels) * 44) == 38
    assert round(auroc([corr[q] for q in pairs], labels) * 44) == 34
    assert pairs.index((2, 5)) + 1 == 2 and by_corr.index((2, 5)) + 1 == 6
    assert pairs.index((1, 4)) + 1 == 10
    # each target's weights sum to about n, whether or not it has a regulator
    for j in range(6):
        total = sum(w for _, t, w in links if t == j)
        assert 90 < total < 110
