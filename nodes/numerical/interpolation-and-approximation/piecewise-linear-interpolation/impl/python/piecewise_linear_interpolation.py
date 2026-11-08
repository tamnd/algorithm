# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piecewise-linear-interpolation/. The authors are listed in prov/CR12BK.jsonl.

"""Piecewise linear interpolation through sorted data points."""

from typing import Sequence


def pl_interpolate(x: Sequence, y: Sequence, t):
    """Return s(t), the broken line through (x[j], y[j]), at x[0] <= t <= x[n].

    Precondition: x is strictly increasing, len(x) == len(y) >= 1.
    Cost: Theta(log n) comparisons and O(1) arithmetic operations.
    Works with float or Fraction; with Fraction the result is exact.
    """
    n = len(x) - 1
    if not x[0] <= t <= x[n]:
        raise ValueError("t is outside [x[0], x[n]]")
    if n == 0:  # @line L1
        return y[0]
    lo, hi = 0, n  # @line L2
    while hi - lo > 1:  # @line L3
        mid = lo + (hi - lo) // 2  # @line L4
        if x[mid] <= t:  # @line L5
            lo = mid
        else:
            hi = mid
    lam = (t - x[lo]) / (x[lo + 1] - x[lo])  # @line L6
    return (1 - lam) * y[lo] + lam * y[lo + 1]  # @line L7


def pl_interpolate_sorted(x: Sequence, y: Sequence, ts: Sequence) -> list:
    """Evaluate s at the sorted points ts by one merge-like sweep.

    Cost: Theta(n + m) for n + 1 nodes and m queries.
    """
    out, j, n = [], 0, len(x) - 1
    for t in ts:
        if not x[0] <= t <= x[n]:
            raise ValueError("t is outside [x[0], x[n]]")
        if n == 0:
            out.append(y[0])
            continue
        while j < n - 1 and x[j + 1] <= t:
            j += 1
        lam = (t - x[j]) / (x[j + 1] - x[j])
        out.append((1 - lam) * y[j] + lam * y[j + 1])
    return out
