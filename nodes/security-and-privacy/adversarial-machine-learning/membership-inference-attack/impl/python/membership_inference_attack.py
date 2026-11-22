# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/membership-inference-attack/. The authors are listed in prov/52KYBB.jsonl.

"""Membership inference with shadow models (Shokri et al. 2017), as an abstract model on synthetic data.

The target and shadow models are logistic regressions from mlkit, trained on Gaussian
blobs that the tests draw from a fixed seed. The attack model is one threshold on the
confidence of the true label, fitted on the shadow models. Nothing here queries a real
model or reads a real data set. Labels are 0 and 1.
"""

import math
from typing import Sequence

from mlkit import Data, dot, sigmoid, train_logistic

Model = tuple[list[float], float]


def confidence(model: Model, x: Sequence[float], y: int) -> float:
    """The probability that the logistic model gives the true label y of x. Cost O(d)."""
    w, b = model
    p = sigmoid(dot(w, x) + b)
    return p if y == 1 else 1.0 - p


def best_threshold(scores_in: Sequence[float], scores_out: Sequence[float]) -> tuple[float, float]:
    """The threshold tau that maximizes TPR - FPR for the rule "member iff score >= tau", and that value.

    The candidates are the scores and +infinity (which says "member" for nothing). Ties
    in the advantage go to the largest tau. Precondition: both lists are nonempty.
    Cost O(m log m) for m scores.
    """
    pts = sorted([(s, 1) for s in scores_in] + [(s, 0) for s in scores_out], reverse=True)
    n_in, n_out = len(scores_in), len(scores_out)
    best_tau, best_key = math.inf, 0  # key = (TPR - FPR) n_in n_out, an exact integer
    tp = fp = 0
    i = 0
    while i < len(pts):
        s = pts[i][0]
        while i < len(pts) and pts[i][0] == s:  # every point with score s passes tau = s
            tp += pts[i][1]
            fp += 1 - pts[i][1]
            i += 1
        key = tp * n_out - fp * n_in
        if key > best_key:
            best_tau, best_key = s, key
    return best_tau, best_key / (n_in * n_out)


def rates(scores_in: Sequence[float], scores_out: Sequence[float], tau: float) -> tuple[float, float]:
    """(TPR, FPR) of the rule "member iff score >= tau". Cost O(m)."""
    tpr = sum(1 for s in scores_in if s >= tau) / len(scores_in)
    fpr = sum(1 for s in scores_out if s >= tau) / len(scores_out)
    return tpr, fpr


def tpr_at_fpr(scores_in: Sequence[float], scores_out: Sequence[float], alpha: float) -> float:
    """The largest TPR of a threshold rule whose FPR is at most alpha. Cost O(m log m)."""
    pts = sorted([(s, 1) for s in scores_in] + [(s, 0) for s in scores_out], reverse=True)
    n_in, n_out = len(scores_in), len(scores_out)
    best = 0.0
    tp = fp = 0
    i = 0
    while i < len(pts):
        s = pts[i][0]
        while i < len(pts) and pts[i][0] == s:
            tp += pts[i][1]
            fp += 1 - pts[i][1]
            i += 1
        if fp / n_out <= alpha:
            best = max(best, tp / n_in)
    return best


def shadow_attack(shadow_sets: Sequence[Data], steps: int, lr: float, l2: float) -> float:
    """Fit the attack threshold on shadow models; each shadow set is split into its first half (in) and second half (out).

    The shadow models use the same training procedure as the target. Precondition: each
    set has at least 2 points. Cost O(k steps m d) for k shadow sets of m points.
    """
    scores_in: list[float] = []
    scores_out: list[float] = []
    for data in shadow_sets:  # @line L1
        half = len(data) // 2
        inside, outside = data[:half], data[half:]
        g = train_logistic(inside, steps, lr, l2)  # @line L2
        scores_in += [confidence(g, x, y) for x, y in inside]  # @line L3
        scores_out += [confidence(g, x, y) for x, y in outside]
    tau, _ = best_threshold(scores_in, scores_out)  # @line L4
    return tau


def infer(target: Model, tau: float, x: Sequence[float], y: int) -> bool:
    """The attack decision on the record (x, y): member iff the target's confidence is at least tau. Cost O(d)."""
    return confidence(target, x, y) >= tau  # @line L5
