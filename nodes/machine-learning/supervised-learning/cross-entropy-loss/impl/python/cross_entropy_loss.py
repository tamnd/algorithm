# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-entropy-loss/. The authors are listed in prov/0EGAS8.jsonl.
"""Softmax cross-entropy loss with a stable log-sum-exp, and its gradient p - y."""

import math


def log_sum_exp(z: list[float]) -> float:
    """Return log(sum(exp(z_j))) without overflow: shift by the maximum first."""
    if not z:
        raise ValueError("empty score vector")
    m = max(z)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(v - m) for v in z))


def softmax(z: list[float]) -> list[float]:
    """Probabilities exp(z_j) / sum exp(z_i), computed after a shift by max(z)."""
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def log_softmax(z: list[float]) -> list[float]:
    lse = log_sum_exp(z)
    return [v - lse for v in z]


def cross_entropy(z: list[float], y: int) -> float:
    """Loss of the scores z (logits) for the true class y: log-sum-exp(z) - z[y]."""
    return log_sum_exp(z) - z[y]


def cross_entropy_soft(z: list[float], q: list[float]) -> float:
    """Loss against a target distribution q: -sum_j q_j log p_j with p = softmax(z)."""
    lp = log_softmax(z)
    return -sum(qj * lj for qj, lj in zip(q, lp) if qj > 0)


def cross_entropy_grad(z: list[float], q: list[float]) -> list[float]:
    """Gradient of cross_entropy_soft with respect to z: p - q (q sums to 1)."""
    p = softmax(z)
    return [pj - qj for pj, qj in zip(p, q)]


def one_hot(y: int, k: int) -> list[float]:
    return [1.0 if j == y else 0.0 for j in range(k)]


def mean_cross_entropy(scores: list[list[float]], labels: list[int]) -> float:
    """Empirical risk: the mean loss over n examples."""
    if len(scores) != len(labels) or not scores:
        raise ValueError("need the same positive number of score vectors and labels")
    return sum(cross_entropy(z, y) for z, y in zip(scores, labels)) / len(scores)


def entropy(q: list[float]) -> float:
    return -sum(a * math.log(a) for a in q if a > 0)


def kl_divergence(q: list[float], p: list[float]) -> float:
    total = 0.0
    for a, b in zip(q, p):
        if a > 0:
            if b == 0:
                return math.inf
            total += a * math.log(a / b)
    return total
