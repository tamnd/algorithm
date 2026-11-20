# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ironing/. The authors are listed in prov/Y8ZAS3.jsonl.

"""Ironing of the virtual values of a discrete value distribution.

A distribution is a list of (value, probability) pairs with distinct values and positive
probabilities that sum to 1, as ints or Fractions. The revenue curve has the points (0, 0) and
(q_k, s_k q_k) with q_k = Pr[v >= s_k]. The virtual value of s_k is the slope of the curve on the
quantile interval of s_k, and the ironed virtual value is the slope of the concave hull there.
"""

from fractions import Fraction
from typing import Sequence

Dist = Sequence[tuple]


def normalize(dist: Dist):
    """Return (values, probs) sorted by value, as Fractions, after checking the input."""
    pairs = sorted((Fraction(v), Fraction(p)) for v, p in dist)
    values = [v for v, _ in pairs]
    probs = [p for _, p in pairs]
    if not pairs or len(set(values)) != len(values):
        raise ValueError("the support must be nonempty with distinct values")
    if any(p <= 0 for p in probs) or sum(probs) != 1:
        raise ValueError("the probabilities must be positive and sum to 1")
    return values, probs


def revenue_curve(dist: Dist):
    """Return the points (q, R) from (0, 0) to (1, s_1), in increasing order of q."""
    values, probs = normalize(dist)
    pts = [(Fraction(0), Fraction(0))]
    q = Fraction(0)
    for s, f in zip(reversed(values), reversed(probs)):
        q += f
        pts.append((q, s * q))
    return pts


def concave_hull(pts):
    """Return the indices of the vertices of the upper concave hull of points sorted by q."""
    hull = []
    for k, (x, y) in enumerate(pts):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = pts[hull[-2]], pts[hull[-1]]
            if (y2 - y1) * (x - x1) <= (y - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(k)
    return hull


def virtual_values(dist: Dist):
    """Return the virtual values of the support values, in increasing order of value."""
    pts = revenue_curve(dist)
    slopes = [(pts[j][1] - pts[j - 1][1]) / (pts[j][0] - pts[j - 1][0]) for j in range(1, len(pts))]
    return list(reversed(slopes))


def iron(dist: Dist):
    """Return (ironed virtual values, ironed intervals).

    The ironed values are in increasing order of value. An ironed interval is a pair (lo, hi) of
    value indices, lo < hi, such that one hull segment spans the values s_lo, ..., s_hi, so they
    share one ironed virtual value. Inside the interval the revenue curve lies on or below the hull.
    """
    pts = revenue_curve(dist)  # @line L1
    K = len(pts) - 1
    hull = concave_hull(pts)  # @line L2
    slope = [None] * (K + 1)
    intervals = []
    for a, b in zip(hull, hull[1:]):  # @line L3
        m = (pts[b][1] - pts[a][1]) / (pts[b][0] - pts[a][0])
        for j in range(a + 1, b + 1):  # @line L4
            slope[j] = m
        if b - a >= 2:
            # curve point j belongs to value index K - j; the segment covers points a + 1 .. b
            intervals.append((K - b, K - (a + 1)))  # @line L5
    return list(reversed(slope[1:])), sorted(intervals)  # @line L6
