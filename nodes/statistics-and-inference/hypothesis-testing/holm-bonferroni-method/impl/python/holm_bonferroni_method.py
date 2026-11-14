# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/holm-bonferroni-method/. The authors are listed in prov/7A4AQ3.jsonl.
"""Holm's step-down procedure for m hypotheses.

Sort the p-values, p_(1) <= ... <= p_(m), and reject H_(1), H_(2), ... while
p_(k) <= alpha / (m - k + 1); stop at the first failure. The adjusted p-value of
H_(k) is max over j <= k of min(1, (m - j + 1) p_(j)). The procedure controls the
family-wise error rate strongly at alpha under any dependence. The code works with
floats or with fractions.Fraction; with Fractions every result is exact.
"""

from collections.abc import Sequence


def holm(p: Sequence, alpha) -> tuple[list[bool], list]:
    """Return (reject, adjusted) in the original order of p."""
    m = len(p)
    if m == 0:
        return [], []
    if any(not 0 <= v <= 1 for v in p):
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1]")
    order = sorted(range(m), key=lambda i: p[i])  # @line L1
    reject = [False] * m
    k = 0  # 0-based rank, so the threshold is alpha / (m - k)
    while k < m and p[order[k]] * (m - k) <= alpha:  # @line L2
        reject[order[k]] = True  # @line L3
        k += 1  # @line L4
    adjusted = [0] * m
    running = 0
    for k, i in enumerate(order):  # @line L5
        running = max(running, min(1, (m - k) * p[i]))  # @line L6
        adjusted[i] = running  # @line L7
    return reject, adjusted  # @line L8
