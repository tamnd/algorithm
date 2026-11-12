# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/confusion-matrix/. The authors are listed in prov/WPW65B.jsonl.

import random
from fractions import Fraction

from confusion_matrix import (accuracy, balanced_accuracy, cohen_kappa, confusion_matrix, mcc,
                              mcc_binary, mcc_parts, one_vs_rest_counts, transpose)


def test_layout_rows_are_true_labels() -> None:
    c = confusion_matrix([0, 0, 1, 1, 1], [0, 1, 1, 1, 0])
    assert c == [[1, 1], [1, 2]]
    tn, fp, fn, tp = c[0][0], c[0][1], c[1][0], c[1][1]
    assert (tp, fp, fn, tn) == one_vs_rest_counts(c, 1)


def test_imbalanced_all_negative() -> None:
    c = [[95, 0], [5, 0]]
    assert accuracy(c) == Fraction(19, 20)
    assert balanced_accuracy(c) == Fraction(1, 2)
    assert cohen_kappa(c) == 0
    assert mcc(c) == 0.0


def test_binary_example() -> None:
    c = [[45, 5], [10, 40]]  # rows: true negative, true positive
    assert accuracy(c) == Fraction(17, 20)
    assert cohen_kappa(c) == Fraction(7, 10)
    assert abs(mcc(c) - 0.703526) < 1e-6
    assert abs(mcc(c) - mcc_binary(40, 5, 10, 45)) < 1e-12


def test_three_class_example() -> None:
    c = [[8, 1, 1], [2, 3, 1], [0, 1, 3]]
    assert accuracy(c) == Fraction(7, 10)
    assert balanced_accuracy(c) == Fraction(41, 60)
    assert cohen_kappa(c) == Fraction(13, 25)
    assert mcc_parts(c) == (130, 250, 248)
    assert abs(mcc(c) - 0.522093) < 1e-6


def test_multiclass_mcc_reduces_to_matthews_exactly() -> None:
    r = random.Random(5)
    for _ in range(3000):
        tp, fp, fn, tn = (r.randint(0, 30) for _ in range(4))
        if tp + fp + fn + tn == 0:
            continue
        num, a, b = mcc_parts([[tn, fp], [fn, tp]])
        assert num == 2 * (tp * tn - fp * fn)
        assert a * b == 4 * (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
        assert abs(mcc([[tn, fp], [fn, tp]]) - mcc_binary(tp, fp, fn, tn)) < 1e-12


def test_transpose_invariance() -> None:
    r = random.Random(8)
    for _ in range(500):
        k = r.randint(2, 4)
        c = [[r.randint(0, 9) for _ in range(k)] for _ in range(k)]
        if sum(map(sum, c)) == 0:
            continue
        t = transpose(c)
        assert accuracy(t) == accuracy(c)
        assert cohen_kappa(t) == cohen_kappa(c)
        assert abs(mcc(t) - mcc(c)) < 1e-12


def test_kappa_and_mcc_ranges() -> None:
    r = random.Random(11)
    for _ in range(2000):
        k = r.randint(2, 4)
        y = [r.randrange(k) for _ in range(r.randint(1, 30))]
        p = [r.randrange(k) for _ in y]
        c = confusion_matrix(y, p, list(range(k)))
        kap = cohen_kappa(c)
        assert kap is None or kap <= 1
        assert -1 - 1e-12 <= mcc(c) <= 1 + 1e-12
    perfect = confusion_matrix([0, 1, 2, 2], [0, 1, 2, 2])
    assert cohen_kappa(perfect) == 1 and abs(mcc(perfect) - 1) < 1e-12
