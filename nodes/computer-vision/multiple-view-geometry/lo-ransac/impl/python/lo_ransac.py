# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lo-ransac/. The authors are listed in prov/BQXMXZ.jsonl.
"""LO-RANSAC (locally optimized RANSAC), Chum, Matas and Kittler 2003,
with the local optimization of Lebeda, Matas and Chum 2012.

The RANSAC loop, plus a local optimization step that runs each time a model
from a minimal sample has more inliers than every earlier minimal-sample model.
The step refits on the inliers at a wider threshold, then several times draws a
larger non-minimal sample from the inliers, fits it by least squares and
iterates least squares while the threshold shrinks from m * eps to eps. The
best model of the step can replace the best model so far, and the number of
trials is updated from its inlier count. The model is a line in the plane,
a x + b y + c = 0 with a^2 + b^2 = 1, from s = 2 points; the least squares
fit is total least squares with unit weights (a choice of this code).
Standard library only.
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
    """Total least squares line through the points, or None if fewer than 2 or all equal."""
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


def inliers(model, data, eps):
    return [i for i, x in enumerate(data) if point_line_distance(model, x) <= eps]


def local_opt(model, inl, data, eps, rng, m_theta=math.sqrt(2.0), reps=10, iters=4, s_is=8):
    """Return (model, inliers) of the best model found by the local optimization."""
    best, best_inl = model, inl  # @line L16
    cand = fit_line_lsq([data[i] for i in inliers(model, data, m_theta * eps)])  # @line L17
    if cand is not None:
        c_inl = inliers(cand, data, eps)
        if len(c_inl) > len(best_inl):
            best, best_inl = cand, c_inl
    size = max(2, min(s_is, len(inl) // 2))
    delta = (m_theta * eps - eps) / (iters - 1)
    for _ in range(reps):  # @line L18
        sub = rng.sample(inl, min(size, len(inl)))  # @line L19
        cand = fit_line_lsq([data[i] for i in sub])  # @line L20
        if cand is None:
            continue
        cand = fit_line_lsq([data[i] for i in inliers(cand, data, eps)]) or cand  # @line L21
        thr = m_theta * eps
        for _ in range(iters):  # @line L22
            c_inl = inliers(cand, data, eps)  # @line L23
            if len(c_inl) > len(best_inl):
                best, best_inl = cand, c_inl
            nxt = fit_line_lsq([data[i] for i in inliers(cand, data, thr)])  # @line L24
            if nxt is None:
                break
            cand = nxt
            thr -= delta  # @line L25
        c_inl = inliers(cand, data, eps)
        if len(c_inl) > len(best_inl):
            best, best_inl = cand, c_inl
    return best, best_inl  # @line L26


def lo_ransac(data, eps, rng=None, s=2, p=0.99, max_trials=10000, **lo_args):
    """Return (model, inliers, trials, lo_runs)."""
    rng = rng if rng is not None else random.Random()
    n = len(data)
    if n < s:
        return None, [], 0, 0
    lo_runs = 0
    best, best_inl, n_s, k, t = None, [], 0, max_trials, 0  # @line L1
    while t < k:  # @line L2
        t += 1  # @line L3
        idx = rng.sample(range(n), s)  # @line L4
        theta = line_through([data[i] for i in idx])  # @line L5
        if theta is None:  # @line L6
            continue
        inl = inliers(theta, data, eps)  # @line L7
        if len(inl) > n_s:  # @line L8
            n_s = len(inl)  # @line L9
            lo_runs += 1
            lo_model, lo_inl = local_opt(theta, inl, data, eps, rng, **lo_args)  # @line L10
            if len(lo_inl) > len(best_inl):  # @line L11
                best, best_inl = lo_model, lo_inl  # @line L12
                k = min(max_trials, ransac_trials(p, len(best_inl) / n, s))  # @line L13
    if best is None:  # @line L14
        return None, [], t, lo_runs
    return best, best_inl, t, lo_runs  # @line L15
