# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roc-auc/. The authors are listed in prov/D427XN.jsonl.

import random
from fractions import Fraction as F

from roc_auc import (auc_pairwise, auc_ranks, auc_sorted, hanley_mcneil_se, mann_whitney_u,
                     mid_ranks, roc_curve, trapezoid)


def test_worked_example_without_ties() -> None:
    s = [0.9, 0.8, 0.7, 0.6, 0.55, 0.5, 0.4, 0.3]
    y = [1, 1, 0, 1, 0, 1, 0, 0]
    assert auc_sorted(s, y) == auc_pairwise(s, y) == auc_ranks(s, y) == F(13, 16)


def test_worked_example_with_ties() -> None:
    s = [3, 2, 2, 1, 2, 1, 0]
    y = [1, 1, 1, 1, 0, 0, 0]
    assert mid_ranks(s) == [7, 5, 5, F(5, 2), 5, F(5, 2), 1]
    assert mann_whitney_u(s, y) == F(19, 2)
    assert roc_curve(s, y) == [(0, 0), (0, F(1, 4)), (F(1, 3), F(3, 4)), (F(2, 3), 1), (1, 1)]
    assert auc_sorted(s, y) == auc_pairwise(s, y) == auc_ranks(s, y) == F(19, 24)
    assert trapezoid(roc_curve(s, y)) == F(19, 24)


def test_sorted_equals_pairwise_exactly_with_ties() -> None:
    r = random.Random(1)
    for _ in range(4000):
        n = r.randint(2, 16)
        y = [r.randint(0, 1) for _ in range(n)]
        if 0 not in y or 1 not in y:
            continue
        levels = r.choice((2, 3, 5, 1000))
        s = [r.randrange(levels) for _ in range(n)]
        a = auc_pairwise(s, y)
        assert auc_sorted(s, y) == a
        assert auc_ranks(s, y) == a
        assert trapezoid(roc_curve(s, y)) == a


def test_reversal_and_monotone_invariance() -> None:
    r = random.Random(4)
    for _ in range(1000):
        n = r.randint(2, 12)
        y = [r.randint(0, 1) for _ in range(n)]
        if 0 not in y or 1 not in y:
            continue
        s = [r.randint(-4, 4) for _ in range(n)]
        a = auc_sorted(s, y)
        assert auc_sorted([-v for v in s], y) == 1 - a
        assert auc_sorted([v ** 3 + 7 for v in s], y) == a
        assert auc_sorted(s, [1 - v for v in y]) == 1 - a


def test_constant_score_gives_one_half() -> None:
    assert auc_sorted([0.3] * 5, [1, 0, 0, 1, 0]) == F(1, 2)


def test_hanley_mcneil_se_shrinks_with_n() -> None:
    a = 0.8
    assert hanley_mcneil_se(a, 100, 100) < hanley_mcneil_se(a, 10, 10)
    assert hanley_mcneil_se(0.5, 50, 50) > 0
