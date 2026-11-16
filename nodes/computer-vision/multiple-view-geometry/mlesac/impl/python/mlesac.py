# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mlesac/. The authors are listed in prov/3GWPBP.jsonl.
"""MLESAC (maximum likelihood estimation sample consensus), Torr and Zisserman 2000.

The RANSAC loop with a likelihood score. A residual e has the mixture density
    gamma * N(e; 0, sigma^2) + (1 - gamma) / v,
Gaussian inliers with known sigma and uniform outliers on a range of size v.
For each hypothesis, a few EM steps from gamma = 1/2 estimate the mixing weight
gamma only; the model of least negative log-likelihood wins. The default model
is a line in the plane, a x + b y + c = 0 with a^2 + b^2 = 1, from s = 2 points.
The final model is a weighted least squares refit with the posterior inlier
probabilities as weights (a choice of this code). Standard library only.
Cost: O(k (C + m n)) for k trials, m EM steps and n data items.
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


def fit_line_weighted(points, weights):
    """Weighted total least squares line, or None if the weights or the spread vanish."""
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


def gauss(e, sigma):
    return math.exp(-0.5 * (e / sigma) ** 2) / (math.sqrt(2.0 * math.pi) * sigma)


def mixture_nll(residuals, gamma, sigma, v):
    """Negative log-likelihood of the residuals under the mixture."""
    return -sum(math.log(gamma * gauss(e, sigma) + (1.0 - gamma) / v) for e in residuals)


def em_mixing(residuals, sigma, v, steps=5, gamma=0.5):
    """EM for the mixing weight only, from the given start, for a fixed number of steps."""
    g = [gauss(e, sigma) for e in residuals]
    u = 1.0 / v
    for _ in range(steps):
        gamma = sum(gamma * gi / (gamma * gi + (1.0 - gamma) * u) for gi in g) / len(g)
    return gamma


def mlesac(data, sigma, v, rng=None, s=2, p=0.99, max_trials=10000, em_steps=5,
           fit_minimal=line_through, residual=point_line_distance, refit=fit_line_weighted):
    """Return (model, gamma, nll, trials).

    nll is the negative log-likelihood of the best sampled model, gamma its
    estimated inlier fraction, and model the weighted refit with the posterior
    inlier probabilities (or the sampled model if the refit fails). Returns
    (None, 0.0, inf, trials) if no sample gives a model.
    """
    rng = rng if rng is not None else random.Random()
    n = len(data)
    if n < s:
        return None, 0.0, math.inf, 0
    u = 1.0 / v
    best, best_nll, best_gamma, k, t = None, math.inf, 0.0, max_trials, 0  # @line L1
    while t < k:  # @line L2
        t += 1  # @line L3
        idx = rng.sample(range(n), s)  # @line L4
        theta = fit_minimal([data[i] for i in idx])  # @line L5
        if theta is None:  # @line L6
            continue
        g = [gauss(residual(theta, x), sigma) for x in data]  # @line L7
        gamma = 0.5  # @line L8
        for _ in range(em_steps):  # @line L9
            z = [gamma * gi / (gamma * gi + (1.0 - gamma) * u) for gi in g]  # @line L10
            gamma = sum(z) / n  # @line L11
        nll = -sum(math.log(gamma * gi + (1.0 - gamma) * u) for gi in g)  # @line L12
        if nll < best_nll:  # @line L13
            best, best_nll, best_gamma = theta, nll, gamma  # @line L14
            k = min(max_trials, ransac_trials(p, gamma, s))  # @line L15
    if best is None:  # @line L16
        return None, 0.0, math.inf, t
    g = [gauss(residual(best, x), sigma) for x in data]  # @line L17
    z = [best_gamma * gi / (best_gamma * gi + (1.0 - best_gamma) * u) for gi in g]
    model = refit(data, z) if refit is not None else None
    return (model if model is not None else best), best_gamma, best_nll, t  # @line L18
