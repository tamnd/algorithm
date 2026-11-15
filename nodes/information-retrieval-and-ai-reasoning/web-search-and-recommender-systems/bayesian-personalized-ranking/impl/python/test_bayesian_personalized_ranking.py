# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-personalized-ranking/. The authors are listed in prov/JYHKHX.jsonl.

import math
import random

import pytest

import bayesian_personalized_ranking as bpr

FD_STEP = 1e-6
FD_TOL = 1e-7
AUC_MIN = 0.8


def planted(seed: int) -> tuple[set, set, int, int]:
    """Two groups of 15 users. Group 0 uses items 0 to 9, group 1 items 10 to 19.

    Each user has 6 items of its own group; one of them is held out for test.
    The planted order: for every user, the items of its group come before
    the items of the other group.
    """
    rng = random.Random(seed)
    m, n = 30, 20
    train, test = set(), set()
    for u in range(m):
        base = 0 if u < 15 else 10
        items = rng.sample(range(base, base + 10), 6)
        test.add((u, items[0]))
        for i in items[1:]:
            train.add((u, i))
    return train, test, m, n


def test_gradient_matches_finite_differences():
    rng = random.Random(3)
    for _ in range(10):
        r = rng.randint(1, 4)
        w = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(3)]
        h = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(4)]
        regs = (rng.uniform(0, 0.5), rng.uniform(0, 0.5), rng.uniform(0, 0.5))
        u, i, j = 1, 0, 3
        gw, gi, gj = bpr.triple_grad(w, h, u, i, j, regs)
        for mat, row, g in ((w, u, gw), (h, i, gi), (h, j, gj)):
            for f in range(r):
                old = mat[row][f]
                mat[row][f] = old + FD_STEP
                up = bpr.triple_loss(w, h, u, i, j, regs)
                mat[row][f] = old - FD_STEP
                down = bpr.triple_loss(w, h, u, i, j, regs)
                mat[row][f] = old
                assert abs((up - down) / (2 * FD_STEP) - g[f]) <= FD_TOL


def test_page_example_step():
    w = [[0.1, 0.2]]
    h = [[0.3, -0.1], [0.2, 0.4]]
    zero = (0.0, 0.0, 0.0)
    assert abs(bpr.triple_loss(w, h, 0, 0, 1, zero) - 0.7391593390256102) <= 1e-12
    gw, gi, gj = bpr.triple_grad(w, h, 0, 0, 1, zero)
    w[0] = [a - 0.5 * g for a, g in zip(w[0], gw)]
    h[0] = [a - 0.5 * g for a, g in zip(h[0], gi)]
    h[1] = [a - 0.5 * g for a, g in zip(h[1], gj)]
    x = bpr.dot(w[0], h[0]) - bpr.dot(w[0], h[1])
    assert abs(x - (-0.008237299183673295)) <= 1e-12
    assert abs(bpr.triple_loss(w, h, 0, 0, 1, zero) - 0.6972743117650329) <= 1e-12


def test_log_sigmoid_is_stable_and_correct():
    for z in (-800.0, -30.0, -1.0, 0.0, 1.0, 30.0, 800.0):
        got = bpr.log_sigmoid(z)
        assert math.isfinite(got)
        if abs(z) < 30:
            assert abs(got - math.log(1 / (1 + math.exp(-z)))) <= 1e-12
    assert abs(bpr.sigmoid(0.0) - 0.5) <= 1e-15


def test_learned_auc_on_planted_order():
    train, test, m, n = planted(5)
    w, h = bpr.learn_bpr(train, m, n, 4, 40000, 0.05, (0.01, 0.01, 0.01), seed=7)
    assert bpr.auc(w, h, train, test, m, n) > AUC_MIN


def test_untrained_model_is_near_random():
    train, test, m, n = planted(5)
    w, h = bpr.learn_bpr(train, m, n, 4, 0, 0.05, (0.01, 0.01, 0.01), seed=7)
    assert abs(bpr.auc(w, h, train, test, m, n) - 0.5) < 0.2


def test_auc_by_brute_force_count():
    rng = random.Random(9)
    m, n, r = 4, 6, 2
    w = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(m)]
    h = [[rng.gauss(0, 1) for _ in range(r)] for _ in range(n)]
    train = {(0, 0), (0, 1), (1, 2), (2, 3), (3, 4)}
    test = {(0, 2), (1, 5), (2, 0), (3, 1)}
    # Brute force: the position of the test item in the sorted list of candidates.
    per_user = []
    for u, t in sorted(test):
        cands = [j for j in range(n) if (u, j) not in train and j != t]
        score = sum(bpr.dot(w[u], h[t]) > bpr.dot(w[u], h[j]) for j in cands)
        per_user.append(score / len(cands))
    want = sum(per_user) / len(per_user)
    assert abs(bpr.auc(w, h, train, test, m, n) - want) <= 1e-12


def test_ranking_leaves_out_used_items():
    train, _, m, n = planted(1)
    w, h = bpr.learn_bpr(train, m, n, 3, 2000, 0.05, (0.01, 0.01, 0.01))
    used = bpr.by_user(train, m)[0]
    top = bpr.rank(w, h, 0, used, 5)
    assert len(top) == 5 and not set(top) & used


def test_user_with_all_items_is_rejected():
    with pytest.raises(ValueError):
        bpr.learn_bpr({(0, 0), (0, 1)}, 1, 2, 2, 10, 0.1, (0.0, 0.0, 0.0))
