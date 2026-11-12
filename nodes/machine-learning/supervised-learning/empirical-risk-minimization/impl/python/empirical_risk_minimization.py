# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-risk-minimization/. The authors are listed in prov/CNMDNK.jsonl.

"""Empirical risk minimization (ERM): return a hypothesis with the least mean loss on
the sample. Two forms: brute force over a finite class, and a sort and sweep ERM for
one dimensional thresholds under the 0-1 loss."""

from fractions import Fraction


def zero_one(prediction, label):
    return 0 if prediction == label else 1


def empirical_risk(h, sample, loss=zero_one):
    """L_S(h) = (1/n) sum_i loss(h(x_i), y_i), as an exact fraction."""
    return Fraction(sum(loss(h(x), y) for x, y in sample), len(sample))


def erm_finite(hypotheses, sample, loss=zero_one):
    """Brute force ERM over a finite class. Ties go to the first hypothesis in the list.
    Returns (index, risk). Cost: |H| n loss evaluations."""
    best, best_risk = None, None  # @line L1
    for i, h in enumerate(hypotheses):  # @line L2
        r = empirical_risk(h, sample, loss)  # @line L3
        if best_risk is None or r < best_risk:  # @line L4
            best, best_risk = i, r
    return best, best_risk  # @line L5


def threshold(t):
    """h_t(x) = 1 when x >= t, else 0. t may be float('inf') (the all-0 hypothesis)."""
    return lambda x: 1 if x >= t else 0


def erm_threshold(sample):
    """ERM over {h_t : t real or +infinity} under the 0-1 loss, in O(n log n) time.

    Sort the points. A threshold at the k-th smallest distinct value labels the points
    below it 0 and the others 1. Sweep k and keep the count of errors.
    Returns (t, number of errors)."""
    pts = sorted(sample)  # @line L6
    n = len(pts)
    errors = sum(1 for _, y in pts if y == 0)  # @line L7: t = smallest x, all predicted 1
    best_t = pts[0][0] if n else float("inf")  # @line L8
    best = errors
    i = 0
    while i < n:  # @line L9
        x = pts[i][0]
        while i < n and pts[i][0] == x:  # @line L10: move the points equal to x below the cut
            errors += 1 if pts[i][1] == 1 else -1
            i += 1
        t = pts[i][0] if i < n else float("inf")  # @line L11
        if errors < best:  # @line L12
            best, best_t = errors, t
    return best_t, best  # @line L13


def memorizer(sample, default=0):
    """The rule that returns the training label on a seen point and `default` elsewhere.
    It is an ERM over the class of all functions: its empirical risk is 0 when no point
    has two labels."""
    table = {x: y for x, y in sample}
    return lambda x: table.get(x, default)
