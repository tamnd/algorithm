# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preemptive-ransac/. The authors are listed in prov/86C9V2.jsonl.
"""Preemptive RANSAC, Nister 2003 (Algorithm 1 of the paper).

A fixed number M of hypotheses is generated first. The observations are put in
random order and scored one at a time; after observation i only the f(i) best
hypotheses (by accumulated score) stay, with the preemption function
f(i) = floor(M * 2^(-floor(i / B))). The run ends when one hypothesis is left
or the observations are used up. The total work is fixed in advance, which
suits real-time systems.

The score of one observation is the truncated quadratic cost min(r^2, T^2)
(a choice of this code; lower is better). The model is a line in the plane,
a x + b y + c = 0 with a^2 + b^2 = 1, from 2 points. Standard library only.
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
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return (a, b, -(a * x1 + b * y1))


def point_line_distance(line, pt):
    a, b, c = line
    return abs(a * pt[0] + b * pt[1] + c)


def preemption(i, M, B):
    """f(i) = floor(M 2^(-floor(i/B)))."""
    return M >> (i // B)


def total_scorings(N, M, B):
    """M scorings for the first observation, then f(i) for i = 2, 3, ... until i > N or f(i) <= 1."""
    total = M
    for i in range(2, N + 1):
        f = preemption(i, M, B)
        if f <= 1:
            break
        total += min(f, M)
    return total


def make_hypotheses(data, M, rng, s=2, fit_minimal=line_through, max_tries=None):
    hyps = []
    if len(data) < s:
        return hyps
    tries = 0
    max_tries = max_tries if max_tries is not None else 10 * M
    while len(hyps) < M and tries < max_tries:
        tries += 1
        h = fit_minimal(rng.sample(data, s))
        if h is not None:
            hyps.append(h)
    return hyps


def preemptive_ransac(data, threshold, M=500, B=100, rng=None, s=2, hypotheses=None,
                      residual=point_line_distance):
    """Return (best_hypothesis, its accumulated cost, number of scorings)."""
    rng = rng if rng is not None else random.Random()
    t2 = threshold * threshold

    def rho(x, h):
        return min(residual(h, x) ** 2, t2)

    obs = list(data)
    rng.shuffle(obs)  # @line L1
    hyps = list(hypotheses) if hypotheses is not None else make_hypotheses(data, M, rng, s)  # @line L2
    if not hyps or not obs:
        return None, math.inf, 0
    M = len(hyps)
    scored = [(rho(obs[0], h), j) for j, h in enumerate(hyps)]  # @line L3
    count = len(scored)
    i = 2
    while True:  # @line L4
        f = preemption(i, M, B)
        if i > len(obs) or f <= 1:  # @line L5
            cost, j = min(scored)
            return hyps[j], cost, count
        if f < len(scored):  # @line L6
            scored = sorted(scored)[:f]
        scored = [(c + rho(obs[i - 1], hyps[j]), j) for c, j in scored]  # @line L7
        count += len(scored)
        i += 1  # @line L8
