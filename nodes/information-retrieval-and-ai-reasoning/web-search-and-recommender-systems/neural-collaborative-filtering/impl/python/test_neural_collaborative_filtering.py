# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-collaborative-filtering/. The authors are listed in prov/9XDZVT.jsonl.

import math
import random

import pytest

import neural_collaborative_filtering as ncf

FD_STEP = 1e-6
FD_TOL = 1e-6
AUC_MIN = 0.75


def planted(seed: int) -> tuple[set, set, int, int]:
    """Two groups of 15 users; group 0 uses items 0 to 9 and group 1 items 10 to 19."""
    rng = random.Random(seed)
    m, n = 30, 20
    train, test = set(), set()
    for u in range(m):
        base = 0 if u < 15 else 10
        items = rng.sample(range(base, base + 10), 6)
        test.add((u, items[0]))
        train.update((u, i) for i in items[1:])
    return train, test, m, n


def held_out_auc(p, train, test, m, n) -> float:
    total = 0.0
    for u, t in sorted(test):
        others = [j for j in range(n) if (u, j) not in train and j != t]
        st = ncf.forward(p, u, t)[0]
        total += sum(1.0 if st > ncf.forward(p, u, j)[0] else 0.0 for j in others) / len(others)
    return total / len(test)


def test_every_gradient_matches_finite_differences():
    for seed, hidden in ((1, [5, 3]), (2, [4]), (3, [])):
        p = ncf.init(3, 4, 3, hidden, seed=seed, scale=0.7)
        examples = [(0, 1, 1), (2, 3, 0), (1, 1, 0), (0, 2, 1)]
        grads = ncf.gradient(p, examples)
        for name, mat in p.items():
            for r in range(len(mat)):
                for c in range(len(mat[r])):
                    old = mat[r][c]
                    mat[r][c] = old + FD_STEP
                    up = ncf.loss(p, examples)
                    mat[r][c] = old - FD_STEP
                    down = ncf.loss(p, examples)
                    mat[r][c] = old
                    fd = (up - down) / (2 * FD_STEP)
                    assert abs(fd - grads[name][r][c]) <= FD_TOL * max(1.0, abs(fd)), (name, r, c)


def test_sparse_step_equals_dense_step():
    p = ncf.init(4, 5, 2, [3], seed=4, scale=0.5)
    q = {name: [row[:] for row in mat] for name, mat in p.items()}
    s, cache = ncf.forward(p, 2, 3)
    dense = ncf.zeros_like(p)
    ncf.backward(p, cache, ncf.sigmoid(s) - 1, dense)
    sparse = ncf.zeros_like_used(q, 2, 3)
    ncf.backward(q, cache, ncf.sigmoid(s) - 1, sparse)
    for name, mat in p.items():
        for r in range(len(mat)):
            for c in range(len(mat[r])):
                mat[r][c] -= 0.1 * dense[name][r][c]
    ncf.step(q, sparse, 2, 3, 0.1)
    for name in p:
        for a, b in zip(p[name], q[name]):
            for x, y in zip(a, b):
                assert abs(x - y) <= 1e-15


def test_gmf_with_unit_weights_is_the_dot_product():
    p = ncf.init(3, 3, 4, [2], seed=5)
    p["h"] = [[1.0, 1.0, 1.0, 1.0, 0.0, 0.0]]
    for u in range(3):
        for i in range(3):
            dot = sum(a * b for a, b in zip(p["PG"][u], p["QG"][i]))
            assert abs(ncf.forward(p, u, i)[0] - dot) <= 1e-12


def test_page_example():
    p = {
        "PG": [[1.0, 2.0]],
        "QG": [[0.5, -1.0]],
        "PM": [[1.0, 0.0]],
        "QM": [[0.0, 1.0]],
        "W0": [[1.0, -1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0]],
        "b0": [[0.0, -0.5]],
        "h": [[1.0, 0.5, 2.0, -1.0]],
    }
    s, cache = ncf.forward(p, 0, 0)
    assert cache["g"] == [0.5, -2.0]
    assert cache["pre"][0] == [1.0, 0.5]
    assert abs(s - 1.0) <= 1e-12
    assert abs(ncf.score(p, 0, 0) - 1 / (1 + math.exp(-1.0))) <= 1e-12
    grads = ncf.gradient(p, [(0, 0, 1)])
    d = 1 / (1 + math.exp(-1.0)) - 1
    assert abs(grads["h"][0][2] - d * 1.0) <= 1e-12
    assert abs(grads["W0"][1][3] - d * (-1.0) * 1.0) <= 1e-12


def test_training_learns_the_planted_groups():
    train, test, m, n = planted(5)
    before = ncf.init(m, n, 4, [4], seed=3)
    p = ncf.train(train, m, n, 4, [4], 15, 0.1, negatives=4, seed=3)
    assert held_out_auc(before, train, test, m, n) < 0.7
    assert held_out_auc(p, train, test, m, n) > AUC_MIN
    pairs = [(u, i, 1) for u, i in sorted(train)]
    assert ncf.loss(p, pairs) < ncf.loss(before, pairs)


def test_user_with_all_items_is_rejected():
    with pytest.raises(ValueError):
        ncf.train({(0, 0), (0, 1)}, 1, 2, 2, [2], 1, 0.1)
