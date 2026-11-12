# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/confusion-matrix/. The authors are listed in prov/WPW65B.jsonl.
"""The confusion matrix with true labels in rows and predicted labels in columns, and the
metrics read from it: accuracy, balanced accuracy, Cohen's kappa and the Matthews
correlation coefficient (binary and the multiclass form). Ratios are exact Fractions."""

from fractions import Fraction
from math import sqrt


def confusion_matrix(y_true: list, y_pred: list, labels: list | None = None) -> list[list[int]]:
    """C[i][j] = number of examples whose true label is labels[i] and predicted label is labels[j]."""
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    index = {lab: i for i, lab in enumerate(labels)}
    k = len(labels)
    c = [[0] * k for _ in range(k)]
    for t, p in zip(y_true, y_pred):
        c[index[t]][index[p]] += 1
    return c


def total(c: list[list[int]]) -> int:
    return sum(sum(row) for row in c)


def row_sums(c: list[list[int]]) -> list[int]:
    """True class counts (support)."""
    return [sum(row) for row in c]


def col_sums(c: list[list[int]]) -> list[int]:
    """Predicted class counts."""
    return [sum(c[i][j] for i in range(len(c))) for j in range(len(c))]


def one_vs_rest_counts(c: list[list[int]], j: int) -> tuple[int, int, int, int]:
    """(TP, FP, FN, TN) for class j treated as the positive class."""
    n = total(c)
    tp = c[j][j]
    fp = col_sums(c)[j] - tp
    fn = row_sums(c)[j] - tp
    return tp, fp, fn, n - tp - fp - fn


def accuracy(c: list[list[int]]) -> Fraction:
    return Fraction(sum(c[i][i] for i in range(len(c))), total(c))


def balanced_accuracy(c: list[list[int]]) -> Fraction:
    """Mean recall over the classes that occur in the true labels (rows with a nonzero sum)."""
    recalls = [Fraction(c[i][i], s) for i, s in enumerate(row_sums(c)) if s > 0]
    return sum(recalls, Fraction(0)) / len(recalls)


def cohen_kappa(c: list[list[int]]) -> Fraction | None:
    """(p_o - p_e) / (1 - p_e); None when p_e = 1, where kappa is undefined."""
    n = total(c)
    p_o = accuracy(c)
    p_e = Fraction(sum(r * q for r, q in zip(row_sums(c), col_sums(c))), n * n)
    if p_e == 1:
        return None
    return (p_o - p_e) / (1 - p_e)


def mcc_parts(c: list[list[int]]) -> tuple[int, int, int]:
    """Numerator and the two factors under the square root of the multiclass MCC (Gorodkin)."""
    s = total(c)
    tr = sum(c[i][i] for i in range(len(c)))
    t, p = row_sums(c), col_sums(c)
    num = tr * s - sum(pk * tk for pk, tk in zip(p, t))
    return num, s * s - sum(pk * pk for pk in p), s * s - sum(tk * tk for tk in t)


def mcc(c: list[list[int]]) -> float:
    """Matthews correlation coefficient; 0 when the denominator is 0 (the scikit-learn convention)."""
    num, a, b = mcc_parts(c)
    if a == 0 or b == 0:
        return 0.0
    return num / sqrt(a * b)


def mcc_binary(tp: int, fp: int, fn: int, tn: int) -> float:
    """Matthews (1975): (TP TN - FP FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)), 0 if a factor is 0."""
    d = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    if d == 0:
        return 0.0
    return (tp * tn - fp * fn) / sqrt(d)


def transpose(c: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*c)]
