# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weiszfelds-algorithm/. The authors are listed in prov/5VREF5.jsonl.

"""Weiszfeld's algorithm for the geometric median, with the Vardi-Zhang step.

Points are tuples of numbers in any fixed dimension d. Weights are positive.
The method is numerical, so the iterates are floats. When an iterate is equal
to a data point, the step of Vardi and Zhang (which is Kuhn's descent step)
either moves away from that point or proves that the point is the median.
"""

import math

Point = tuple


def _norm(v) -> float:
    return math.sqrt(sum(c * c for c in v))


def weber_cost(points, y, weights=None) -> float:
    """The weighted sum of Euclidean distances from y to the points."""
    if weights is None:
        weights = [1] * len(points)
    return sum(w * math.dist(p, y) for p, w in zip(points, weights))


def data_point_is_median(points, k: int, weights=None) -> bool:
    """Kuhn's test: points[k] is a median iff |R| <= (weight at points[k]).

    R is the weighted sum of the unit vectors from points[k] toward the
    other points. Copies of points[k] add their weights to the right side.
    """
    if weights is None:
        weights = [1] * len(points)
    a = points[k]
    d = len(a)
    eta = 0.0
    r = [0.0] * d
    for p, w in zip(points, weights):
        dist = math.dist(p, a)
        if dist == 0.0:
            eta += w
            continue
        for j in range(d):
            r[j] += w * (p[j] - a[j]) / dist
    return _norm(r) <= eta


def weiszfeld(points, weights=None, start=None, tol: float = 1e-12, max_iter: int = 100000) -> Point:
    """Approximate the point that minimizes the weighted sum of distances.

    The iteration starts at `start`, or at the weighted centroid. It stops
    when an iterate is a data point that passes Kuhn's test, when the step is
    at most tol * (1 + |y|), or after max_iter steps.
    """
    pts = [tuple(float(c) for c in p) for p in points]
    n = len(pts)
    if n == 0:
        raise ValueError("no points")
    d = len(pts[0])
    w = [1.0] * n if weights is None else [float(x) for x in weights]
    if len(w) != n or any(x <= 0 for x in w):
        raise ValueError("weights must be positive, one per point")
    if start is None:
        total = sum(w)
        start = [sum(wi * p[j] for p, wi in zip(pts, w)) / total for j in range(d)]
    y = [float(c) for c in start]  # @line L1
    for _ in range(max_iter):  # @line L2
        s = 0.0  # @line L3
        t = [0.0] * d
        r = [0.0] * d
        eta = 0.0
        for p, wi in zip(pts, w):  # @line L4
            dist = math.dist(p, y)
            if dist == 0.0:  # @line L5
                eta += wi
                continue
            s += wi / dist  # @line L6
            for j in range(d):
                t[j] += wi * p[j] / dist
                r[j] += wi * (p[j] - y[j]) / dist
        rn = _norm(r)  # @line L7
        if rn <= eta:  # @line L8
            return tuple(y)
        lam = eta / rn  # @line L9
        new = [(1.0 - lam) * t[j] / s + lam * y[j] for j in range(d)]
        step = math.dist(new, y)
        y = new  # @line L10
        if step <= tol * (1.0 + _norm(y)):  # @line L11
            return tuple(y)
    return tuple(y)  # @line L12
