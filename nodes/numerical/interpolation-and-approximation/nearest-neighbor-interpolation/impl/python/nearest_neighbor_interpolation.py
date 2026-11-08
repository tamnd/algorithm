# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-neighbor-interpolation/. The authors are listed in prov/JNZ01E.jsonl.

"""Nearest-neighbor interpolation in one dimension and, by brute force, in d dimensions."""

from typing import Sequence


def nn_interpolate(x: Sequence, y: Sequence, t):
    """Return the value y[k] of a node x[k] nearest to t; a tie goes to the left node.

    Precondition: x strictly increasing, len(x) == len(y) >= 1. A point t
    outside [x[0], x[n]] is clamped to the nearest end node.
    Cost: Theta(log n) comparisons.
    """
    n = len(x) - 1
    if t <= x[0]:
        return y[0]
    if t >= x[n]:
        return y[n]
    if n == 0:  # @line L1
        return y[0]
    lo, hi = 0, n  # @line L2
    while hi - lo > 1:  # @line L3
        mid = lo + (hi - lo) // 2  # @line L4
        if x[mid] <= t:  # @line L5
            lo = mid
        else:
            hi = mid
    if t - x[lo] <= x[lo + 1] - t:  # @line L6
        return y[lo]
    return y[lo + 1]  # @line L7


def nn_interpolate_nd(points: Sequence[Sequence], values: Sequence, q: Sequence):
    """Return the value of a point nearest to q in the Euclidean norm (lowest index on a tie).

    Brute force: Theta(N d) for N points in dimension d.
    """
    if not points:
        raise ValueError("no data points")
    best, best_d = 0, None
    for i, p in enumerate(points):
        d2 = sum((a - b) * (a - b) for a, b in zip(p, q))
        if best_d is None or d2 < best_d:
            best, best_d = i, d2
    return values[best]
