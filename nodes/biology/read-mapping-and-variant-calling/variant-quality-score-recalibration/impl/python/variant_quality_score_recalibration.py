# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variant-quality-score-recalibration/. The authors are listed in prov/DTZA1Z.jsonl.
"""A small version of variant quality score recalibration (VQSR).

Each call is a vector of annotation values (for example QD, FS and MQ). A
Gaussian mixture with diagonal covariances is fitted by EM to the calls that
lie in a training set of trusted variants. A second mixture is fitted to the
calls that the first model scores worst. The score of a call is the log
ratio ln p+(x) - ln p-(x) of the two densities (GATK calls it VQSLOD). The
filter threshold is the largest score that keeps at least the target share
of the truth-set calls.

Left out: the Bayesian (variational) mixture of GATK with its priors on the
means and covariances, full covariances, the separate SNP and indel models,
the annotation transforms, and the several tranches written to the VCF.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence, Tuple

Vector = Sequence[float]
Mixture = Tuple[List[float], List[List[float]], List[List[float]]]  # weights, means, variances

VAR_FLOOR = 1e-3


def _lse(xs: Sequence[float]) -> float:
    m = max(xs)
    if m == -math.inf:
        return m
    return m + math.log(sum(math.exp(x - m) for x in xs))


def _log_normal(x: Vector, mean: Vector, var: Vector) -> float:
    return -0.5 * sum(math.log(2 * math.pi * v) + (a - m) ** 2 / v for a, m, v in zip(x, mean, var))


def log_density(mix: Mixture, x: Vector) -> float:
    """ln p(x) under the mixture."""
    w, mu, var = mix
    return _lse([math.log(w[k]) + _log_normal(x, mu[k], var[k]) for k in range(len(w)) if w[k] > 0])


def log_likelihood(mix: Mixture, data: Sequence[Vector]) -> float:
    return sum(log_density(mix, x) for x in data)


def fit_gmm(data: Sequence[Vector], k: int, rng: random.Random, iters: int = 100,
            tol: float = 1e-9, trace: List[float] = None) -> Mixture:
    """A k-component diagonal Gaussian mixture fitted by EM, started from k random points."""
    n, d = len(data), len(data[0])
    if n < k:
        raise ValueError("need at least k points")
    mean_all = [sum(x[j] for x in data) / n for j in range(d)]
    var_all = [max(VAR_FLOOR, sum((x[j] - mean_all[j]) ** 2 for x in data) / n) for j in range(d)]
    mix: Mixture = ([1.0 / k] * k, [list(data[i]) for i in rng.sample(range(n), k)],
                    [list(var_all) for _ in range(k)])
    prev = -math.inf
    for _ in range(iters):
        w, mu, var = mix
        resp = []  # E step: the posterior share of each component in each point
        total = 0.0
        for x in data:
            lp = [math.log(w[c]) + _log_normal(x, mu[c], var[c]) if w[c] > 0 else -math.inf for c in range(k)]
            z = _lse(lp)
            total += z
            resp.append([math.exp(v - z) for v in lp])
        if trace is not None:
            trace.append(total)
        if total - prev < tol * max(1.0, abs(total)):
            break
        prev = total
        nk = [sum(r[c] for r in resp) for c in range(k)]  # M step
        new_w, new_mu, new_var = [], [], []
        for c in range(k):
            if nk[c] < 1e-12:
                new_w.append(0.0)
                new_mu.append(mu[c])
                new_var.append(var[c])
                continue
            m = [sum(r[c] * x[j] for r, x in zip(resp, data)) / nk[c] for j in range(d)]
            v = [max(VAR_FLOOR, sum(r[c] * (x[j] - m[j]) ** 2 for r, x in zip(resp, data)) / nk[c])
                 for j in range(d)]
            new_w.append(nk[c] / n)
            new_mu.append(m)
            new_var.append(v)
        mix = (new_w, new_mu, new_var)
    return mix


def vqsr(calls: Sequence[Vector], training: Sequence[bool], truth: Sequence[bool], sensitivity: float,
         k_pos: int = 3, k_neg: int = 2, bad_share: float = 0.1, seed: int = 0):
    """(scores, threshold, passed) for every call."""
    rng = random.Random(seed)
    pos = fit_gmm([x for x, t in zip(calls, training) if t], k_pos, rng)  # @line L1
    lp = [log_density(pos, x) for x in calls]  # @line L2
    n_bad = max(k_neg, int(bad_share * len(calls)))
    worst = sorted(range(len(calls)), key=lambda i: lp[i])[:n_bad]  # @line L3
    neg = fit_gmm([calls[i] for i in worst], k_neg, rng)  # @line L4
    scores = [lp[i] - log_density(neg, calls[i]) for i in range(len(calls))]  # @line L5
    threshold = tranche_threshold([s for s, t in zip(scores, truth) if t], sensitivity)  # @line L6
    passed = [s >= threshold for s in scores]  # @line L7
    return scores, threshold, passed  # @line L8


def tranche_threshold(truth_scores: Sequence[float], sensitivity: float) -> float:
    """The largest t such that at least the share sensitivity of truth_scores is >= t."""
    if not truth_scores or not 0 < sensitivity <= 1:
        raise ValueError("need truth scores and 0 < sensitivity <= 1")
    s = sorted(truth_scores, reverse=True)
    need = math.ceil(sensitivity * len(s) - 1e-12)
    return s[need - 1]
