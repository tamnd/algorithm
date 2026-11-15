# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-click-model/. The authors are listed in prov/56VCGX.jsonl.
"""The position-based click model (PBM) and its EM fit.

A result d shown at rank r (0-based) is clicked with probability
gamma[r] * alpha[d]: the user examines rank r with probability gamma[r],
is attracted by d with probability alpha[d], and the two events are
independent. Clicks at different ranks are independent.

The EM fit works on aggregated counts: n[(d, r)] impressions of d at r
and c[(d, r)] clicks among them.
"""

import math


def simulate(rankings, alpha, gamma, rng):
    """Return one 0/1 click vector for each ranking."""
    return [[1 if rng.random() < gamma[r] * alpha[d] else 0 for r, d in enumerate(ranking)] for ranking in rankings]


def aggregate(rankings, clicks):
    """Return (n, c), the impressions and clicks of each (document, rank) pair."""
    n, c = {}, {}
    for ranking, vec in zip(rankings, clicks):
        for r, (d, k) in enumerate(zip(ranking, vec)):
            n[(d, r)] = n.get((d, r), 0) + 1
            c[(d, r)] = c.get((d, r), 0) + k
    return n, c


def log_likelihood(n, c, alpha, gamma):
    total = 0.0
    for key, m in n.items():
        d, r = key
        p = gamma[r] * alpha[d]
        k = c[key]
        if k:
            total += k * math.log(p)
        if m - k:
            total += (m - k) * math.log(1.0 - p)
    return total


def em_step(n, c, alpha, gamma):
    """One EM iteration. The parameters must lie strictly inside (0, 1)."""
    exam, attr = {}, {}
    n_rank, n_doc = {}, {}
    for key, m in n.items():
        d, r = key
        k = c[key]
        g, a = gamma[r], alpha[d]
        skip = 1.0 - g * a
        # Expected numbers of examinations and attractions: a click has both,
        # a non-click has E = 1 with g (1 - a) / skip and A = 1 with a (1 - g) / skip.
        exam[r] = exam.get(r, 0.0) + k + (m - k) * g * (1.0 - a) / skip
        attr[d] = attr.get(d, 0.0) + k + (m - k) * a * (1.0 - g) / skip
        n_rank[r] = n_rank.get(r, 0) + m
        n_doc[d] = n_doc.get(d, 0) + m
    new_gamma = {r: exam[r] / n_rank[r] for r in exam}
    new_alpha = {d: attr[d] / n_doc[d] for d in attr}
    return new_alpha, new_gamma


def fit(n, c, iterations=500, start=0.5):
    """Run EM from alpha = gamma = start. Return (alpha, gamma, history),
    where history holds the log likelihood before each step and at the end."""
    alpha = {d: start for d, _ in n}
    gamma = {r: start for _, r in n}
    history = [log_likelihood(n, c, alpha, gamma)]
    for _ in range(iterations):
        alpha, gamma = em_step(n, c, alpha, gamma)
        history.append(log_likelihood(n, c, alpha, gamma))
    return alpha, gamma, history
