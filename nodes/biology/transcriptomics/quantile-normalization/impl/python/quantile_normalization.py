# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantile-normalization/. The authors are listed in prov/C7FM0S.jsonl.
"""Quantile normalization (Bolstad, Irizarry, Astrand and Speed 2003).

x is a list of rows, one row per gene and one column per sample. Sort each
column, average the sorted columns position by position to get the target
t[1] <= ... <= t[n], and give each entry the target value at its rank in its
column. Entries that tie in a column get the mean of the target values over
the ranks of the tie, so that the result does not depend on how the sort
orders them. Packages treat ties in other ways; this is one fixed choice.
"""

from __future__ import annotations

from typing import List, Sequence


def _check(x: Sequence[Sequence[float]]) -> int:
    if not x:
        raise ValueError("need at least one gene")
    m = len(x[0])
    if m == 0 or any(len(row) != m for row in x):
        raise ValueError("every gene needs the same positive number of samples")
    return m


def target_distribution(x: Sequence[Sequence[float]]) -> List[float]:
    """The mean, over the samples, of the i-th smallest value, for i = 1..n."""
    m = _check(x)
    n = len(x)
    cols = [sorted(row[j] for row in x) for j in range(m)]  # @line L1
    return [sum(cols[j][i] for j in range(m)) / m for i in range(n)]  # @line L2


def normalize_to_target(x: Sequence[Sequence[float]], target: Sequence[float]) -> List[List[float]]:
    """Give each entry the target value at its rank in its column (ties share the mean)."""
    m = _check(x)
    n = len(x)
    t = sorted(target)
    if len(t) != n:
        raise ValueError("the target needs one value per gene")
    prefix = [0.0]
    for v in t:
        prefix.append(prefix[-1] + v)
    out = [[0.0] * m for _ in range(n)]
    for j in range(m):  # @line L3
        order = sorted(range(n), key=lambda g: x[g][j])
        a = 0
        while a < n:  # @line L4
            b = a
            while b + 1 < n and x[order[b + 1]][j] == x[order[a]][j]:
                b += 1
            value = t[a] if a == b else (prefix[b + 1] - prefix[a]) / (b - a + 1)  # @line L5
            for r in range(a, b + 1):
                out[order[r]][j] = value
            a = b + 1
    return out  # @line L6


def quantile_normalize(x: Sequence[Sequence[float]]) -> List[List[float]]:
    """Quantile normalization of the columns of x."""
    return normalize_to_target(x, target_distribution(x))
