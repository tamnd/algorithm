# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/precision-and-recall/. The authors are listed in prov/1ZSBS6.jsonl.
"""Precision, recall and F-beta from counts, micro, macro and weighted averaging over the
classes of a confusion matrix, the precision-recall curve of a score, and three different
summaries of that curve: average precision (the step sum, the one this page computes), the
trapezoid area, and the 11-point interpolated average precision. All values are Fractions.
A ratio 0/0 is replaced by zero_division (default 0)."""

from fractions import Fraction


def _ratio(a: int, b: int, zero_division: Fraction) -> Fraction:
    return Fraction(a, b) if b else zero_division


def precision(tp: int, fp: int, zero_division: Fraction = Fraction(0)) -> Fraction:
    return _ratio(tp, tp + fp, zero_division)


def recall(tp: int, fn: int, zero_division: Fraction = Fraction(0)) -> Fraction:
    return _ratio(tp, tp + fn, zero_division)


def f_beta(tp: int, fp: int, fn: int, beta: Fraction = Fraction(1),
           zero_division: Fraction = Fraction(0)) -> Fraction:
    """(1 + b^2) TP / ((1 + b^2) TP + b^2 FN + FP), the weighted harmonic mean of P and R."""
    b2 = Fraction(beta) ** 2
    den = (1 + b2) * tp + b2 * fn + fp
    return (1 + b2) * tp / den if den else zero_division


def per_class_counts(c: list[list[int]]) -> list[tuple[int, int, int]]:
    """(TP, FP, FN) for each class of a confusion matrix with true labels in rows."""
    k = len(c)
    out = []
    for j in range(k):
        tp = c[j][j]
        fp = sum(c[i][j] for i in range(k)) - tp
        fn = sum(c[j]) - tp
        out.append((tp, fp, fn))
    return out


def averaged(c: list[list[int]], average: str, beta: Fraction = Fraction(1),
             zero_division: Fraction = Fraction(0)) -> tuple[Fraction, Fraction, Fraction]:
    """(precision, recall, F-beta) with average in {'micro', 'macro', 'weighted'}."""
    counts = per_class_counts(c)
    if average == "micro":
        tp = sum(t for t, _, _ in counts)
        fp = sum(f for _, f, _ in counts)
        fn = sum(f for _, _, f in counts)
        return (precision(tp, fp, zero_division), recall(tp, fn, zero_division),
                f_beta(tp, fp, fn, beta, zero_division))
    scores = [(precision(tp, fp, zero_division), recall(tp, fn, zero_division),
               f_beta(tp, fp, fn, beta, zero_division)) for tp, fp, fn in counts]
    if average == "macro":
        w = [Fraction(1, len(c))] * len(c)
    elif average == "weighted":
        support = [tp + fn for tp, _, fn in counts]
        w = [Fraction(s, sum(support)) for s in support]
    else:
        raise ValueError("average must be 'micro', 'macro' or 'weighted'")
    return tuple(sum((wi * s[m] for wi, s in zip(w, scores)), Fraction(0)) for m in range(3))


def pr_curve(scores: list[float], labels: list[int]) -> list[tuple[Fraction, Fraction]]:
    """(recall, precision) at each distinct threshold, from the highest score down.
    Examples with equal scores enter together. labels are 1 (positive) or 0."""
    pos = sum(labels)
    if pos == 0:
        raise ValueError("recall is undefined without positive examples")
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    points, tp, fp, i = [], 0, 0, 0
    while i < len(order):
        s = scores[order[i]]
        while i < len(order) and scores[order[i]] == s:
            if labels[order[i]] == 1:
                tp += 1
            else:
                fp += 1
            i += 1
        points.append((Fraction(tp, pos), Fraction(tp, tp + fp)))
    return points


def average_precision(scores: list[float], labels: list[int]) -> Fraction:
    """AP = sum_n (R_n - R_{n-1}) P_n over the distinct thresholds, with R_0 = 0. No interpolation."""
    ap, prev_r = Fraction(0), Fraction(0)
    for r, p in pr_curve(scores, labels):
        ap += (r - prev_r) * p
        prev_r = r
    return ap


def trapezoid_pr_area(scores: list[float], labels: list[int]) -> Fraction:
    """Area under the straight-line interpolation of the PR points, starting at (0, 1). A contrast only."""
    pts = [(Fraction(0), Fraction(1))] + pr_curve(scores, labels)
    return sum(((r1 - r0) * (p0 + p1) / 2 for (r0, p0), (r1, p1) in zip(pts, pts[1:])), Fraction(0))


def interpolated_precision(points: list[tuple[Fraction, Fraction]], r: Fraction) -> Fraction:
    """max precision over the points with recall >= r (0 if there is none)."""
    return max((p for rr, p in points if rr >= r), default=Fraction(0))


def eleven_point_ap(scores: list[float], labels: list[int]) -> Fraction:
    """Mean interpolated precision at recall 0, 0.1, ..., 1. A contrast only."""
    pts = pr_curve(scores, labels)
    return sum((interpolated_precision(pts, Fraction(i, 10)) for i in range(11)), Fraction(0)) / 11
