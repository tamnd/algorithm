# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benjamini-hochberg-procedure/. The authors are listed in prov/MA7Z7G.jsonl.
"""The Benjamini-Hochberg linear step-up procedure.

Sort the p-values, p_(1) <= ... <= p_(m), find the largest k with
p_(k) <= k q / m, and reject H_(1), ..., H_(k). For independent null p-values
(independent of each other and of the non-null ones) the false discovery rate is
at most (m_0 / m) q, with equality when the null p-values are uniform. Comparisons
are done as m p <= k q, so that floats and fractions.Fraction give the same
decisions and the adjusted p-values agree with the rejections.

Two implementations: bh sorts (Theta(m log m)); bh_linear counts p-values in m
buckets and needs no sort (Theta(m)).
"""

import math
from collections.abc import Sequence


def _check(p: Sequence, q) -> None:
    if any(not 0 <= v <= 1 for v in p):
        raise ValueError("p-values must lie in [0, 1]")
    if not 0 < q <= 1:
        raise ValueError("q must lie in (0, 1]")


def bh(p: Sequence, q) -> tuple[list[bool], list]:
    """Return (reject, adjusted) in the original order of p."""
    m = len(p)
    if m == 0:
        return [], []
    _check(p, q)
    order = sorted(range(m), key=lambda i: p[i])  # @line L1
    k = m
    while k >= 1 and m * p[order[k - 1]] > k * q:  # @line L2
        k -= 1  # @line L3
    reject = [False] * m
    for r in range(k):  # @line L4
        reject[order[r]] = True
    adjusted = [0] * m
    running = 1
    for r in range(m - 1, -1, -1):  # @line L5
        running = min(running, m * p[order[r]] / (r + 1))  # @line L6
        adjusted[order[r]] = running  # @line L7
    return reject, adjusted  # @line L8


def bh_linear(p: Sequence, q) -> list[bool]:
    """The same rejections as bh, found by counting in Theta(m) time without sorting.

    Bucket b holds the p-values whose smallest k with m p <= k q is b. Then
    #{i : p_i <= k q / m} is the prefix sum up to k, and BH's k is the largest k
    whose prefix sum is at least k.
    """
    m = len(p)
    if m == 0:
        return []
    _check(p, q)
    count = [0] * (m + 2)
    bucket = [0] * m
    for i, v in enumerate(p):
        b = max(1, math.ceil(m * v / q))  # first guess, corrected below for rounding
        while b > 1 and m * v <= (b - 1) * q:
            b -= 1
        while b <= m and m * v > b * q:
            b += 1
        bucket[i] = min(b, m + 1)  # m + 1 means "never at most k q / m"
        count[bucket[i]] += 1
    k, cum = 0, 0
    for j in range(1, m + 1):
        cum += count[j]
        if cum >= j:
            k = j
    return [bucket[i] <= k for i in range(m)]
