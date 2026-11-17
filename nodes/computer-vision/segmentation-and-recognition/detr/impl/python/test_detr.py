# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/detr/. The authors are listed in prov/WE3F6C.jsonl.

import itertools
import math
import random

from detr import detect, giou, hungarian, match_cost, set_loss, to_corners

T1, T2 = (0.25, 0.5, 0.2, 0.2), (0.75, 0.5, 0.2, 0.2)
PAGE_PROBS = [[0.5, 0.1, 0.4], [0.2, 0.3, 0.5], [0.7, 0.1, 0.2]]
PAGE_BOXES = [T1, T2, (0.3, 0.5, 0.2, 0.2)]


def brute_force(cost):
    n, m = len(cost), len(cost[0])
    return min(sum(cost[r][c] for r, c in enumerate(cols)) for cols in itertools.permutations(range(m), n))


def test_giou_values():
    a = to_corners(T1)
    assert abs(giou(a, a) - 1) < 1e-12
    assert abs(giou(a, to_corners(T2)) - (-3 / 7)) < 1e-12
    assert abs(giou(a, to_corners(PAGE_BOXES[2])) - 0.6) < 1e-12
    rng = random.Random(10)
    for _ in range(200):
        x, y = rng.random(), rng.random()
        p = (x, y, x + rng.uniform(0.01, 1), y + rng.uniform(0.01, 1))
        x, y = rng.random(), rng.random()
        q = (x, y, x + rng.uniform(0.01, 1), y + rng.uniform(0.01, 1))
        g = giou(p, q)
        assert -1 < g <= 1 and abs(g - giou(q, p)) < 1e-12


def test_hungarian_matches_brute_force():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 5)
        m = rng.randint(n, 6)
        if rng.random() < 0.5:
            cost = [[rng.randint(-3, 3) for _ in range(m)] for _ in range(n)]
        else:
            cost = [[rng.uniform(-2, 5) for _ in range(m)] for _ in range(n)]
        col = hungarian(cost)
        assert len(set(col)) == n and all(0 <= c < m for c in col)
        assert abs(sum(cost[r][c] for r, c in enumerate(col)) - brute_force(cost)) < 1e-9
    assert hungarian([]) == []


def test_page_example():
    costs = [[match_cost(PAGE_PROBS[i], PAGE_BOXES[i], c, t) for i in range(3)]
             for c, t in [(0, T1), (1, T2)]]
    assert abs(costs[0][0] + 0.5) < 1e-12 and abs(costs[1][1] + 0.3) < 1e-12
    assert abs(costs[0][2] - 0.35) < 1e-12
    loss, sigma = set_loss(PAGE_PROBS, PAGE_BOXES, [0, 1], [T1, T2])
    assert sigma == [0, 1]
    want = (-math.log(0.5) - math.log(0.3) - 0.1 * math.log(0.2)) / 2.1
    assert abs(loss - want) < 1e-12
    # Matching by class probability alone would give the first truth to query 2.
    assert max(range(3), key=lambda i: PAGE_PROBS[i][0]) == 2


def test_no_truths():
    loss, sigma = set_loss(PAGE_PROBS, PAGE_BOXES, [], [])
    assert sigma == []
    assert abs(loss - (-(math.log(0.4) + math.log(0.5) + math.log(0.2)) / 3)) < 1e-12


def test_loss_ignores_the_order_of_queries():
    rng = random.Random(12)
    for _ in range(30):
        n, c, m = 6, 3, rng.randint(1, 4)
        probs = []
        for _ in range(n):
            z = [rng.random() + 0.01 for _ in range(c + 1)]
            probs.append([v / sum(z) for v in z])
        boxes = [(rng.uniform(0.2, 0.8), rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4))
                 for _ in range(n)]
        gts = [(rng.uniform(0.2, 0.8), rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.4), rng.uniform(0.05, 0.4))
               for _ in range(m)]
        labels = [rng.randrange(c) for _ in range(m)]
        loss, sigma = set_loss(probs, boxes, labels, gts)
        assert len(set(sigma)) == m
        perm = list(range(n))
        rng.shuffle(perm)
        loss2, _ = set_loss([probs[i] for i in perm], [boxes[i] for i in perm], labels, gts)
        assert abs(loss - loss2) < 1e-9
        order = list(range(m))
        rng.shuffle(order)
        loss3, _ = set_loss(probs, boxes, [labels[j] for j in order], [gts[j] for j in order])
        assert abs(loss - loss3) < 1e-9


def test_detect_has_no_nms():
    out = detect(PAGE_PROBS, PAGE_BOXES, score_thr=0.45)
    assert [(s, c) for s, c, _ in out] == [(0.7, 0), (0.5, 0)]
    assert detect(PAGE_PROBS, PAGE_BOXES) == []
