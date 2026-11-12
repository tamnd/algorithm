# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precision-and-recall/. The authors are listed in prov/1ZSBS6.jsonl.

import random
from fractions import Fraction as F

from precision_and_recall import (average_precision, averaged, eleven_point_ap, f_beta, pr_curve,
                                  precision, recall, trapezoid_pr_area)

SCORES = [0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.3]
LABELS = [1, 1, 0, 1, 0, 1, 0, 0]
C3 = [[8, 1, 1], [2, 3, 1], [0, 1, 3]]


def test_counts_and_zero_division() -> None:
    assert precision(40, 5) == F(8, 9) and recall(40, 10) == F(4, 5)
    assert f_beta(40, 5, 10) == F(80, 95)
    assert precision(0, 0) == 0 and recall(0, 0) == 0 and f_beta(0, 0, 0) == 0
    assert precision(0, 0, zero_division=F(1)) == 1


def test_f_beta_is_weighted_harmonic_mean() -> None:
    r = random.Random(3)
    for _ in range(2000):
        tp, fp, fn = r.randint(1, 50), r.randint(0, 50), r.randint(0, 50)
        beta = F(r.randint(1, 8), r.randint(1, 4))
        p, rc = precision(tp, fp), recall(tp, fn)
        assert f_beta(tp, fp, fn, beta) == (1 + beta ** 2) * p * rc / (beta ** 2 * p + rc)
        alpha = 1 / (beta ** 2 + 1)
        e = 1 - 1 / (alpha / p + (1 - alpha) / rc)
        assert f_beta(tp, fp, fn, beta) == 1 - e


def test_three_class_averages() -> None:
    assert averaged(C3, "micro") == (F(7, 10), F(7, 10), F(7, 10))
    p, r, f = averaged(C3, "macro")
    assert p == F(2, 3) and r == F(41, 60) and f == (F(4, 5) + F(6, 11) + F(2, 3)) / 3
    p, r, f = averaged(C3, "weighted")
    assert r == F(7, 10) and f == F(23, 33)


def test_micro_equals_accuracy_and_weighted_recall_equals_accuracy() -> None:
    rnd = random.Random(6)
    for _ in range(500):
        k = rnd.randint(2, 5)
        c = [[rnd.randint(0, 9) for _ in range(k)] for _ in range(k)]
        n = sum(map(sum, c))
        if n == 0 or any(sum(row) == 0 for row in c):
            continue
        acc = F(sum(c[i][i] for i in range(k)), n)
        assert averaged(c, "micro") == (acc, acc, acc)
        assert averaged(c, "weighted")[1] == acc


def test_worked_curve_and_three_summaries() -> None:
    pts = pr_curve(SCORES, LABELS)
    assert pts[:4] == [(F(1, 4), F(1)), (F(1, 2), F(1)), (F(1, 2), F(2, 3)), (F(3, 4), F(3, 4))]
    assert average_precision(SCORES, LABELS) == F(41, 48)
    assert trapezoid_pr_area(SCORES, LABELS) == F(401, 480)
    assert eleven_point_ap(SCORES, LABELS) == F(19, 22)


def ap_by_ranks(scores: list[float], labels: list[int]) -> F:
    """Without ties: the mean over positives of the precision at the rank of that positive."""
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    tp, total = 0, F(0)
    for rank, i in enumerate(order, 1):
        if labels[i] == 1:
            tp += 1
            total += F(tp, rank)
    return total / sum(labels)


def ap_brute_force(scores: list[float], labels: list[int]) -> F:
    """Recompute P and R at each distinct threshold from scratch, then take the step sum."""
    pos = sum(labels)
    ap, prev = F(0), F(0)
    for t in sorted(set(scores), reverse=True):
        tp = sum(1 for s, y in zip(scores, labels) if s >= t and y == 1)
        pp = sum(1 for s in scores if s >= t)
        ap += (F(tp, pos) - prev) * F(tp, pp)
        prev = F(tp, pos)
    return ap


def test_ap_against_definitions() -> None:
    rnd = random.Random(10)
    for _ in range(1500):
        n = rnd.randint(1, 12)
        labels = [rnd.randint(0, 1) for _ in range(n)]
        if sum(labels) == 0:
            labels[0] = 1
        distinct = [rnd.random() for _ in range(n)]
        assert average_precision(distinct, labels) == ap_by_ranks(distinct, labels)
        tied = [rnd.randint(0, 3) for _ in range(n)]
        assert average_precision(tied, labels) == ap_brute_force(tied, labels)


def test_recall_never_decreases_along_curve() -> None:
    rnd = random.Random(12)
    for _ in range(300):
        n = rnd.randint(2, 15)
        labels = [rnd.randint(0, 1) for _ in range(n)]
        labels[0] = 1
        pts = pr_curve([rnd.randint(0, 5) for _ in range(n)], labels)
        assert all(a[0] <= b[0] for a, b in zip(pts, pts[1:])) and pts[-1][0] == 1
