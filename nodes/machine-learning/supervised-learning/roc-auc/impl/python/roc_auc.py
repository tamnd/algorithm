# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roc-auc/. The authors are listed in prov/D427XN.jsonl.
"""The ROC curve of a real-valued score and its area. auc_sorted is the O(n log n) method:
sort by decreasing score and add one trapezoid per group of tied scores (Fawcett 2006,
Algorithm 2). auc_ranks is the Mann-Whitney form U / (n+ n-) with mid-ranks. auc_pairwise
is the O(n+ n-) definition: the fraction of (positive, negative) pairs ranked correctly,
ties counted as 1/2. All three return exact Fractions. Labels are 1 (positive) or 0."""

from fractions import Fraction


def _counts(labels: list[int]) -> tuple[int, int]:
    pos = sum(1 for y in labels if y == 1)
    neg = len(labels) - pos
    if pos == 0 or neg == 0:
        raise ValueError("AUC needs at least one positive and one negative example")
    return pos, neg


def roc_curve(scores: list[float], labels: list[int]) -> list[tuple[Fraction, Fraction]]:
    """(FPR, TPR) points from (0, 0) to (1, 1), one per distinct threshold, highest first."""
    pos, neg = _counts(labels)
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    pts = [(Fraction(0), Fraction(0))]
    tp = fp = i = 0
    while i < len(order):
        s = scores[order[i]]
        while i < len(order) and scores[order[i]] == s:
            if labels[order[i]] == 1:
                tp += 1
            else:
                fp += 1
            i += 1
        pts.append((Fraction(fp, neg), Fraction(tp, pos)))
    return pts


def auc_sorted(scores: list[float], labels: list[int]) -> Fraction:
    """Sort once; for each tie group with tp_g positives and fp_g negatives add the trapezoid
    fp_g * (tp_before + tp_g / 2); divide by n+ n-."""
    pos, neg = _counts(labels)
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    area2 = 0  # twice the area in count units, so it stays an integer
    tp = i = 0
    while i < len(order):
        s = scores[order[i]]
        tp_g = fp_g = 0
        while i < len(order) and scores[order[i]] == s:
            if labels[order[i]] == 1:
                tp_g += 1
            else:
                fp_g += 1
            i += 1
        area2 += fp_g * (2 * tp + tp_g)
        tp += tp_g
    return Fraction(area2, 2 * pos * neg)


def mid_ranks(scores: list[float]) -> list[Fraction]:
    """Ranks 1..n in increasing order of score; a tie group gets the mean of its ranks."""
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [Fraction(0)] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j < len(order) and scores[order[j]] == scores[order[i]]:
            j += 1
        r = Fraction(i + 1 + j, 2)  # mean of the ranks i+1, ..., j
        for t in range(i, j):
            ranks[order[t]] = r
        i = j
    return ranks


def mann_whitney_u(scores: list[float], labels: list[int]) -> Fraction:
    """U = (sum of the mid-ranks of the positives) - n+ (n+ + 1) / 2."""
    pos, _ = _counts(labels)
    r = mid_ranks(scores)
    return sum((r[i] for i, y in enumerate(labels) if y == 1), Fraction(0)) - Fraction(pos * (pos + 1), 2)


def auc_ranks(scores: list[float], labels: list[int]) -> Fraction:
    pos, neg = _counts(labels)
    return mann_whitney_u(scores, labels) / (pos * neg)


def auc_pairwise(scores: list[float], labels: list[int]) -> Fraction:
    """The definition: mean over all (positive, negative) pairs of [s+ > s-] + [s+ = s-] / 2."""
    pos, neg = _counts(labels)
    sp = [s for s, y in zip(scores, labels) if y == 1]
    sn = [s for s, y in zip(scores, labels) if y != 1]
    twice = sum(2 if a > b else 1 if a == b else 0 for a in sp for b in sn)
    return Fraction(twice, 2 * pos * neg)


def trapezoid(points: list[tuple[Fraction, Fraction]]) -> Fraction:
    return sum(((x1 - x0) * (y0 + y1) / 2 for (x0, y0), (x1, y1) in zip(points, points[1:])), Fraction(0))


def hanley_mcneil_se(a: float, n_pos: int, n_neg: int) -> float:
    """Approximate standard error of an AUC estimate (Hanley and McNeil 1982)."""
    q1 = a / (2 - a)
    q2 = 2 * a * a / (1 + a)
    var = (a * (1 - a) + (n_pos - 1) * (q1 - a * a) + (n_neg - 1) * (q2 - a * a)) / (n_pos * n_neg)
    return var ** 0.5
