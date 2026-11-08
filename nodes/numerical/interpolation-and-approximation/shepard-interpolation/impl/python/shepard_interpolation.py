# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shepard-interpolation/. The authors are listed in prov/GAEMZW.jsonl.

"""Shepard interpolation (inverse distance weighting).

Points are tuples of coordinates, all of the same dimension d >= 1.
With an even power p and Fraction coordinates and values, the global
method is exact rational arithmetic, because only squared distances
are used.
"""

import math


def _dist2(a, b):
    return sum((u - v) * (u - v) for u, v in zip(a, b))


def _inv_pow(d2, p):
    # d^(-p) computed from d^2; exact for even integer p
    if isinstance(p, int) and p % 2 == 0:
        return 1 / d2 ** (p // 2)
    return 1 / math.sqrt(d2) ** p


def shepard(points, values, x, p=2, radius=None):
    """Return the Shepard interpolant at x.

    p is the power of the inverse distance (p > 0; p > 1 for a smooth
    interpolant). If radius is given, the local Franke-Little weights
    ((R - d)_+ / (R d))^2 are used instead of d^(-p); then a ValueError
    is raised when no data point lies within the radius.
    If x coincides with data points, the mean of their values is returned.
    """
    if len(points) == 0 or len(points) != len(values):
        raise ValueError("need equally many points and values, at least one")
    if p <= 0:
        raise ValueError("p must be positive")
    num = 0
    den = 0
    hits = []
    for xi, yi in zip(points, values):
        d2 = _dist2(x, xi)                               # @line L1
        if d2 == 0:                                      # @line L2
            hits.append(yi)
            continue
        if hits:
            continue
        if radius is None:
            w = _inv_pow(d2, p)                          # @line L3
        else:
            d = math.sqrt(d2)
            if d >= radius:
                continue
            w = ((radius - d) / (radius * d)) ** 2
        num += w * yi
        den += w
    if hits:
        return sum(hits) / len(hits)
    if den == 0:
        raise ValueError("no data point within the radius")
    return num / den                                     # @line L4


def shepard_weights(points, x, p=2):
    """Return the normalized global weights w_i(x), summing to 1."""
    raw = []
    for xi in points:
        d2 = _dist2(x, xi)
        if d2 == 0:
            hit = [1 if _dist2(x, xj) == 0 else 0 for xj in points]
            k = sum(hit)
            return [h / k if h else 0 for h in hit]
        raw.append(_inv_pow(d2, p))
    s = sum(raw)
    return [w / s for w in raw]
