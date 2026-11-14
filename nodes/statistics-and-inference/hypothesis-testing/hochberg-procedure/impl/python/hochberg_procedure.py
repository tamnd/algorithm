# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochberg-procedure/. The authors are listed in prov/T4RCRV.jsonl.
"""Hochberg's step-up procedure for m hypotheses.

Sort the p-values, p_(1) <= ... <= p_(m). Find the largest k with
p_(k) <= alpha / (m - k + 1) and reject H_(1), ..., H_(k). The adjusted p-value of
H_(k) is min over j >= k of min(1, (m - j + 1) p_(j)). The family-wise error rate is
at most alpha when the Simes inequality holds for the true nulls, for example under
independence or MTP2 dependence; it can exceed alpha under negative dependence.
The code works with floats or with fractions.Fraction.
"""

from collections.abc import Sequence


def hochberg(p: Sequence, alpha) -> tuple[list[bool], list]:
    """Return (reject, adjusted) in the original order of p."""
    m = len(p)
    if m == 0:
        return [], []
    if any(not 0 <= v <= 1 for v in p):
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1]")
    order = sorted(range(m), key=lambda i: p[i])  # @line L1
    k = m  # number of rejections; ranks are 1-based here
    while k >= 1 and (m - k + 1) * p[order[k - 1]] > alpha:  # @line L2
        k -= 1  # @line L3
    reject = [False] * m
    for r in range(k):  # @line L4
        reject[order[r]] = True
    adjusted = [0] * m
    running = 1
    for r in range(m - 1, -1, -1):  # @line L5
        running = min(running, (m - r) * p[order[r]])  # @line L6
        adjusted[order[r]] = running  # @line L7
    return reject, adjusted  # @line L8
