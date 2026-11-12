# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-to-rank/. The authors are listed in prov/B37NWE.jsonl.

import math
import random

import pytest

from learning_to_rank import (
    dcg,
    gradient,
    lambdas,
    listnet_gradient,
    listnet_loss,
    ndcg,
    pairs,
    query_ndcg,
    ranking,
    ranknet_loss,
    scores,
    train,
)


def test_ndcg_hand_worked() -> None:
    # Ranked relevances 2, 0, 1: DCG = 3/1 + 0 + 1/log2(4) = 3.5.
    assert dcg([2, 0, 1]) == pytest.approx(3.5)
    ideal = 3 + 1 / math.log2(3)
    assert ndcg([2, 0, 1]) == pytest.approx(3.5 / ideal)
    assert ndcg([2, 0, 1]) == pytest.approx(0.96394, abs=1e-5)
    # Cutoffs.
    assert ndcg([0, 2, 1], k=1) == 0.0
    assert ndcg([0, 2, 1], k=2) == pytest.approx((3 / math.log2(3)) / ideal)
    assert ndcg([0, 2, 1], k=2) == pytest.approx(0.52129, abs=1e-5)
    # Perfect order and no relevant item.
    assert ndcg([3, 2, 2, 0]) == 1.0
    assert ndcg([0, 0, 0]) == 0.0


def test_ndcg_linear_gain() -> None:
    # Gain rel with discount 1/log2(i + 1): relevances 3, 2, 3, 0, 1, 2.
    rels = [3, 2, 3, 0, 1, 2]
    assert dcg(rels, kind="linear") == pytest.approx(6.861, abs=1e-3)
    assert dcg(sorted(rels, reverse=True), kind="linear") == pytest.approx(7.141, abs=1e-3)
    assert ndcg(rels, kind="linear") == pytest.approx(0.961, abs=1e-3)


def test_ranking_breaks_ties_by_index() -> None:
    assert ranking([1.0, 2.0, 1.0, 3.0]) == [3, 1, 0, 2]


def random_queries(rng, dim, count, size, w_true):
    out = []
    for _ in range(count):
        q = []
        for _ in range(size):
            x = [rng.gauss(0, 1) for _ in range(dim)]
            t = sum(a * b for a, b in zip(w_true, x)) + rng.gauss(0, 0.3)
            q.append((x, 0 if t < -0.5 else 1 if t < 0.5 else 2 if t < 1.5 else 3))
        out.append(q)
    return out


def test_ranknet_gradient_matches_finite_differences() -> None:
    rng = random.Random(1)
    qs = random_queries(rng, 3, 3, 6, [1.0, -0.5, 0.25])
    for _ in range(5):
        w = [rng.uniform(-2, 2) for _ in range(3)]
        for sigma in (1.0, 2.5):
            g = gradient(w, qs, sigma)
            h = 1e-6
            for t in range(3):
                wp, wm = list(w), list(w)
                wp[t] += h
                wm[t] -= h
                fd = (ranknet_loss(wp, qs, sigma) - ranknet_loss(wm, qs, sigma)) / (2 * h)
                assert g[t] == pytest.approx(fd, rel=1e-5, abs=1e-6)


def test_lambdas_equal_the_pairwise_sum() -> None:
    rng = random.Random(2)
    q = random_queries(rng, 2, 1, 7, [1.0, 1.0])[0]
    w = [0.3, -0.7]
    s = scores(w, q)
    direct = [0.0, 0.0]
    for i, j in pairs(q):
        lij = -1 / (1 + math.exp(s[i] - s[j]))
        for t in range(2):
            direct[t] += lij * (q[i][0][t] - q[j][0][t])
    assert gradient(w, [q]) == pytest.approx(direct)
    assert sum(lambdas(w, q)) == pytest.approx(0.0, abs=1e-12)


def test_lambdarank_weights_are_swap_ndcg_changes() -> None:
    q = [([0.0], 2), ([1.0], 0), ([2.0], 1)]
    w = [1.0]  # scores 0, 1, 2: ranking is items 2, 1, 0
    s = scores(w, q)
    rels_ranked = [q[i][1] for i in ranking(s)]
    base = ndcg(rels_ranked)
    lam = lambdas(w, q, lambdarank=True)
    want = [0.0, 0.0, 0.0]
    for i, j in pairs(q):
        order = ranking(s)
        a, b = order.index(i), order.index(j)
        order[a], order[b] = order[b], order[a]
        delta = abs(ndcg([q[t][1] for t in order]) - base)
        lij = -1 / (1 + math.exp(s[i] - s[j])) * delta
        want[i] += lij
        want[j] -= lij
    assert lam == pytest.approx(want)


def test_ranknet_training_decreases_loss_and_learns_order() -> None:
    rng = random.Random(3)
    w_true = [2.0, -1.0, 0.5]
    qs = random_queries(rng, 3, 8, 8, w_true)
    w, hist = train(qs, 3, 300)
    assert all(b <= a + 1e-9 for a, b in zip(hist, hist[1:]))
    assert hist[-1] < 0.6 * hist[0]
    test = random_queries(random.Random(4), 3, 30, 8, w_true)
    learned = sum(query_ndcg(w, q) for q in test) / len(test)
    flat = sum(query_ndcg([0.0, 0.0, 0.0], q) for q in test) / len(test)
    assert learned > 0.9 and learned > flat + 0.05


def test_lambdarank_training_improves_ndcg() -> None:
    rng = random.Random(5)
    w_true = [1.0, 1.0, -1.0]
    qs = random_queries(rng, 3, 8, 8, w_true)
    w, _ = train(qs, 3, 200, lambdarank=True, step_size=0.5)
    start = sum(query_ndcg([1.0, -1.0, 1.0], q) for q in qs) / len(qs)
    end = sum(query_ndcg(w, q) for q in qs) / len(qs)
    assert end > 0.9 and end > start


def test_listnet_gradient_matches_finite_differences() -> None:
    rng = random.Random(6)
    q = random_queries(rng, 3, 1, 5, [1.0, 0.0, -1.0])[0]
    w = [0.4, -0.2, 0.9]
    g = listnet_gradient(w, q)
    h = 1e-6
    for t in range(3):
        wp, wm = list(w), list(w)
        wp[t] += h
        wm[t] -= h
        assert g[t] == pytest.approx((listnet_loss(wp, q) - listnet_loss(wm, q)) / (2 * h), rel=1e-5, abs=1e-7)
