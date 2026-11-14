# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-median-of-squares/. The authors are listed in prov/0GC0T5.jsonl.

import random
from fractions import Fraction


def coverage(n):
    """h = floor(n/2) + 1, the number of residuals the fit must cover."""
    return n // 2 + 1


def best_intercept(s, x, y, h):
    """For a fixed slope s: the intercept that minimises the h-th smallest
    |y - s x - a|, and the half-width of the narrowest window of h values
    of z = y - s x. O(n log n)."""
    z = sorted(yi - s * xi for xi, yi in zip(x, y))  # @line L7
    best = None
    for i in range(len(z) - h + 1):  # @line L8
        w = z[i + h - 1] - z[i]
        if best is None or w < best[0]:
            best = (w, i)
    w, i = best
    return (z[i] + z[i + h - 1]) / 2, w / 2  # @line L9


def lms_line(x, y):
    """Exact least median of squares line for simple regression.

    The best slope is among the pairwise slopes (or any slope if all x are
    equal), so try each one with its best intercept. O(n^3 log n) time.
    Returns (slope, intercept, objective) with objective = the h-th smallest
    squared residual.
    """
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    n = len(x)
    if n < 2:
        raise ValueError("need at least two points")
    h = coverage(n)  # @line L1
    slopes = {(y[j] - y[i]) / (x[j] - x[i])  # @line L2
              for i in range(n) for j in range(i + 1, n) if x[i] != x[j]}
    if not slopes:
        slopes = {Fraction(0)}
    best = None
    for s in sorted(slopes):  # @line L3
        a, r = best_intercept(s, x, y, h)  # @line L4
        if best is None or r < best[2]:  # @line L5
            best = (s, a, r)
    s, a, r = best
    return s, a, r * r  # @line L6


def lms_random(x, y, trials, rng=None):
    """PROGRESS-style approximation: slopes through random pairs of points,
    each with its best intercept. O(trials * n log n) time."""
    rng = rng or random.Random(0)
    x = [Fraction(v) for v in x]
    y = [Fraction(v) for v in y]
    n = len(x)
    h = coverage(n)
    best = None
    for _ in range(trials):
        i, j = rng.sample(range(n), 2)
        if x[i] == x[j]:
            continue
        s = (y[j] - y[i]) / (x[j] - x[i])
        a, r = best_intercept(s, x, y, h)
        if best is None or r < best[2]:
            best = (s, a, r)
    if best is None:
        raise ValueError("no pair with different x was drawn")
    s, a, r = best
    return s, a, r * r


def hth_squared_residual(s, a, x, y):
    """The objective of the line y = a + s x."""
    r = sorted((Fraction(yi) - a - s * Fraction(xi)) ** 2 for xi, yi in zip(x, y))
    return r[coverage(len(x)) - 1]
