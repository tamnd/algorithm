# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ransac/. The authors are listed in prov/648BZZ.jsonl.
"""RANSAC (random sample consensus), Fischler and Bolles 1981.

The loop is generic: it takes a minimal solver and a residual function. The
default model is a line in the plane, a x + b y + c = 0 with a^2 + b^2 = 1, fit
from s = 2 points, with the point-to-line distance as the residual. The number
of trials adapts to the best consensus set found so far:
k = ceil(log(1 - p) / log(1 - w^s)).
Standard library only. Cost: O(k (C + n)) for k trials, n data items and a
solver of cost C.
"""

import math
import random


def line_through(sample):
    """The line through two points, as (a, b, c) with a^2 + b^2 = 1, or None if they coincide."""
    (x1, y1), (x2, y2) = sample
    a, b = y1 - y2, x2 - x1
    nrm = math.hypot(a, b)
    if nrm == 0.0:
        return None
    a, b = a / nrm, b / nrm
    return canonical_line((a, b, -(a * x1 + b * y1)))


def canonical_line(line):
    """Fix the sign of (a, b, c): the first nonzero of a, b is positive."""
    a, b, c = line
    if a < 0 or (a == 0 and b < 0):
        return (-a, -b, -c)
    return (a, b, c)


def point_line_distance(line, pt):
    a, b, c = line
    return abs(a * pt[0] + b * pt[1] + c)


def fit_line_lsq(points, weights=None):
    """Total least squares line: minimizes the sum of (weighted) squared distances."""
    if weights is None:
        weights = [1.0] * len(points)
    sw = sum(weights)
    if len(points) < 2 or sw <= 0.0:
        return None
    mx = sum(w * p[0] for w, p in zip(weights, points)) / sw
    my = sum(w * p[1] for w, p in zip(weights, points)) / sw
    sxx = sum(w * (p[0] - mx) ** 2 for w, p in zip(weights, points))
    syy = sum(w * (p[1] - my) ** 2 for w, p in zip(weights, points))
    sxy = sum(w * (p[0] - mx) * (p[1] - my) for w, p in zip(weights, points))
    if sxx == 0.0 and syy == 0.0:
        return None
    theta = 0.5 * math.atan2(2.0 * sxy, sxx - syy)  # direction of the largest spread
    a, b = -math.sin(theta), math.cos(theta)
    return canonical_line((a, b, -(a * mx + b * my)))


def ransac_trials(p, w, s):
    """Smallest k with 1 - (1 - w^s)^k >= p, for 0 < p < 1 and 0 <= w <= 1."""
    q = w ** s
    if q >= 1.0:
        return 1
    if q <= 0.0:
        return math.inf
    return math.ceil(math.log(1.0 - p) / math.log1p(-q))


def ransac(data, threshold, rng=None, s=2, p=0.99, max_trials=10000,
           fit_minimal=line_through, residual=point_line_distance, refit=fit_line_lsq):
    """Return (model, inliers, trials).

    model is the refit of the best consensus set (or the sampled model if the
    refit fails), inliers is the sorted list of indices of the best consensus
    set, and trials is the number of samples drawn. Returns (None, [], trials)
    if no sample gives a model.
    """
    rng = rng if rng is not None else random.Random()
    n = len(data)
    if n < s:
        return None, [], 0
    best, best_inl, k, t = None, [], max_trials, 0  # @line L1
    while t < k:  # @line L2
        t += 1  # @line L3
        idx = rng.sample(range(n), s)  # @line L4
        theta = fit_minimal([data[i] for i in idx])  # @line L5
        if theta is None:  # @line L6
            continue
        inl = [i for i in range(n) if residual(theta, data[i]) <= threshold]  # @line L7
        if len(inl) > len(best_inl):  # @line L8
            best, best_inl = theta, inl  # @line L9
            w = len(best_inl) / n  # @line L10
            k = min(max_trials, ransac_trials(p, w, s))  # @line L11
    if best is None:  # @line L12
        return None, [], t
    model = refit([data[i] for i in best_inl]) if refit is not None else None  # @line L13
    return (model if model is not None else best), best_inl, t  # @line L14


def consensus_size(model, data, threshold, residual=point_line_distance):
    return sum(1 for x in data if residual(model, x) <= threshold)
