# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/msac/. The authors are listed in prov/S7R7BT.jsonl.
"""MSAC (M-estimator sample consensus), Torr and Zisserman 2000.

The RANSAC loop with a different score: a model costs
C(theta) = sum_i min(r_i^2, T^2), a truncated quadratic, and the model of least
cost wins. Inliers still pay their squared residual, so among models with the
same number of inliers the one that fits them more tightly wins. The default
model is a line in the plane, a x + b y + c = 0 with a^2 + b^2 = 1, from s = 2
points. Standard library only. Cost: O(k (C + n)) for k trials, n data items
and a solver of cost C.
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
    a, b, c = line
    if a < 0 or (a == 0 and b < 0):
        return (-a, -b, -c)
    return (a, b, c)


def point_line_distance(line, pt):
    a, b, c = line
    return abs(a * pt[0] + b * pt[1] + c)


def fit_line_lsq(points):
    """Total least squares line through the points, or None if they coincide."""
    if len(points) < 2:
        return None
    m = len(points)
    mx = sum(p[0] for p in points) / m
    my = sum(p[1] for p in points) / m
    sxx = sum((p[0] - mx) ** 2 for p in points)
    syy = sum((p[1] - my) ** 2 for p in points)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points)
    if sxx == 0.0 and syy == 0.0:
        return None
    theta = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    a, b = -math.sin(theta), math.cos(theta)
    return canonical_line((a, b, -(a * mx + b * my)))


def ransac_trials(p, w, s):
    """Smallest k with 1 - (1 - w^s)^k >= p."""
    q = w ** s
    if q >= 1.0:
        return 1
    if q <= 0.0:
        return math.inf
    return math.ceil(math.log(1.0 - p) / math.log1p(-q))


def msac_cost(model, data, threshold, residual=point_line_distance):
    """The truncated quadratic cost sum_i min(r_i^2, T^2)."""
    t2 = threshold * threshold
    return sum(min(residual(model, x) ** 2, t2) for x in data)


def msac(data, threshold, rng=None, s=2, p=0.99, max_trials=10000,
         fit_minimal=line_through, residual=point_line_distance, refit=fit_line_lsq):
    """Return (model, inliers, cost, trials).

    cost is the truncated quadratic cost of the best sampled model, inliers
    the sorted indices with residual at most threshold for that model, and
    model the least squares refit on those inliers (or the sampled model if
    the refit fails). Returns (None, [], inf, trials) if no sample gives a model.
    """
    rng = rng if rng is not None else random.Random()
    n = len(data)
    if n < s:
        return None, [], math.inf, 0
    t2 = threshold * threshold
    best, best_cost, best_inl, k, t = None, math.inf, [], max_trials, 0  # @line L1
    while t < k:  # @line L2
        t += 1  # @line L3
        idx = rng.sample(range(n), s)  # @line L4
        theta = fit_minimal([data[i] for i in idx])  # @line L5
        if theta is None:  # @line L6
            continue
        r2 = [residual(theta, x) ** 2 for x in data]  # @line L7
        cost = sum(min(e, t2) for e in r2)  # @line L8
        if cost < best_cost:  # @line L9
            best, best_cost = theta, cost  # @line L10
            best_inl = [i for i in range(n) if r2[i] <= t2]  # @line L11
            k = min(max_trials, ransac_trials(p, len(best_inl) / n, s))  # @line L12
    if best is None:  # @line L13
        return None, [], math.inf, t
    model = refit([data[i] for i in best_inl]) if refit is not None else None  # @line L14
    return (model if model is not None else best), best_inl, best_cost, t  # @line L15
