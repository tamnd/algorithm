# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-membership-attack/. The authors are listed in prov/CGYJMS.jsonl.

"""The likelihood ratio membership attack (LiRA) of Carlini et al. (2022), as an abstract model on synthetic data.

The target and shadow models are logistic regressions from mlkit, trained on Gaussian
blobs that the tests draw from a fixed seed. For each record the attack fits one
Gaussian to the logit-scaled confidence of the shadow models that trained on the
record and one to those that did not, and tests membership by the ratio of the two
densities at the target's value. Nothing here queries a real model or reads a real
data set. Labels are 0 and 1.
"""

import math
import random
from typing import Optional, Sequence

from mlkit import Data, dot, train_logistic

Model = tuple[list[float], float]


def logit_confidence(model: Model, x: Sequence[float], y: int) -> float:
    """phi = ln(c / (1 - c)) for the confidence c of the true label y of x.

    For a logistic model c = sigmoid(s z) with z = w.x + b and s = 2 y - 1, so phi = s z
    exactly, with no rounding of c near 0 or 1. Cost O(d).
    """
    w, b = model
    return (2 * y - 1) * (dot(w, x) + b)


def gaussian_fit(values: Sequence[float]) -> tuple[float, float]:
    """(mean, population variance) of the values. Precondition: at least one value. Cost O(r) for r values."""
    mu = math.fsum(values) / len(values)
    return mu, math.fsum((v - mu) ** 2 for v in values) / len(values)


def log_normal(t: float, mu: float, var: float) -> float:
    """ln of the density of N(mu, var) at t. Precondition: var > 0. Cost O(1)."""
    return -0.5 * math.log(2.0 * math.pi * var) - (t - mu) ** 2 / (2.0 * var)


def online_score(
    phi: float,
    in_vals: Sequence[float],
    out_vals: Sequence[float],
    var_in: Optional[float] = None,
    var_out: Optional[float] = None,
    floor: float = 1e-6,
) -> float:
    """Lambda = ln N(phi; mu_in, var_in) - ln N(phi; mu_out, var_out), the log likelihood ratio of membership.

    The means come from in_vals and out_vals. A variance that is not given is fitted
    from the same values; every variance is raised to at least floor. Precondition: both
    lists are nonempty and floor > 0. Cost O(r) for r values.
    """
    mu_in, v_in = gaussian_fit(in_vals)
    mu_out, v_out = gaussian_fit(out_vals)
    v_in = max(v_in if var_in is None else var_in, floor)
    v_out = max(v_out if var_out is None else var_out, floor)
    return log_normal(phi, mu_in, v_in) - log_normal(phi, mu_out, v_out)


def offline_score(phi: float, out_vals: Sequence[float], var_out: Optional[float] = None, floor: float = 1e-6) -> float:
    """Pr[Z <= phi] for Z ~ N(mu_out, var_out): the one-sided test of the offline attack, with no IN models.

    Precondition: out_vals is nonempty and floor > 0. Cost O(r) for r values.
    """
    mu, v = gaussian_fit(out_vals)
    v = max(v if var_out is None else var_out, floor)
    return 0.5 * (1.0 + math.erf((phi - mu) / math.sqrt(2.0 * v)))


def train_shadows(pool: Data, pairs: int, rng: random.Random, steps: int, lr: float, l2: float) -> tuple[list[Model], list[list[bool]]]:
    """Train 2 pairs shadow models; in each pair one model trains on a random half of the pool and the other on the rest.

    Returns the models and, for each model, the mask of the pool records it trained on.
    So every record is IN for exactly half of the models. Precondition: the pool has an
    even number m >= 2 of records. Cost O(pairs steps m d).
    """
    m = len(pool)
    models: list[Model] = []
    masks: list[list[bool]] = []
    for _ in range(pairs):  # @line L1
        half = set(rng.sample(range(m), m // 2))
        for side in (True, False):
            mask = [(i in half) == side for i in range(m)]
            models.append(train_logistic([pool[i] for i in range(m) if mask[i]], steps, lr, l2))
            masks.append(mask)
    return models, masks


def lira_scores(
    target: Model,
    shadows: Sequence[Model],
    masks: Sequence[Sequence[bool]],
    pool: Data,
    global_variance: bool,
    floor: float = 1e-6,
) -> list[float]:
    """The online score Lambda of the target on every pool record, with the given shadow models.

    With global_variance, one IN variance and one OUT variance are the means of the
    per-record variances over all records, as in the fixed variance variant of Carlini
    et al.; else each record has its own. Precondition: every record is IN for at least
    one shadow and OUT for at least one. Cost O(k m d) for k shadows and m records.
    """
    ins: list[list[float]] = []
    outs: list[list[float]] = []
    for i, (x, y) in enumerate(pool):
        phis = [logit_confidence(g, x, y) for g in shadows]  # @line L2
        ins.append([p for p, mk in zip(phis, masks) if mk[i]])
        outs.append([p for p, mk in zip(phis, masks) if not mk[i]])
    v_in: Optional[float] = None
    v_out: Optional[float] = None
    if global_variance:  # @line L3
        v_in = math.fsum(gaussian_fit(v)[1] for v in ins) / len(ins)
        v_out = math.fsum(gaussian_fit(v)[1] for v in outs) / len(outs)
    scores = []
    for i, (x, y) in enumerate(pool):
        phi = logit_confidence(target, x, y)  # @line L4
        scores.append(online_score(phi, ins[i], outs[i], v_in, v_out, floor))  # @line L5
    return scores


def decide(score: float, t: float) -> bool:
    """Member iff the log likelihood ratio is at least the cut t. Cost O(1)."""
    return score >= t  # @line L6


def tpr_at_fpr(scores_in: Sequence[float], scores_out: Sequence[float], alpha: float) -> float:
    """The largest TPR of a rule "member iff score >= t" whose FPR is at most alpha. Cost O(r log r) for r scores."""
    pts = sorted([(s, 1) for s in scores_in] + [(s, 0) for s in scores_out], reverse=True)
    best = 0.0
    tp = fp = 0
    i = 0
    while i < len(pts):
        s = pts[i][0]
        while i < len(pts) and pts[i][0] == s:
            tp += pts[i][1]
            fp += 1 - pts[i][1]
            i += 1
        if fp / len(scores_out) <= alpha:
            best = max(best, tp / len(scores_in))
    return best


def best_advantage(scores_in: Sequence[float], scores_out: Sequence[float]) -> float:
    """max over cuts t of TPR - FPR for "member iff score >= t", and 0 for the cut above every score. Cost O(r log r)."""
    pts = sorted([(s, 1) for s in scores_in] + [(s, 0) for s in scores_out], reverse=True)
    n_in, n_out = len(scores_in), len(scores_out)
    best = 0
    tp = fp = 0
    i = 0
    while i < len(pts):
        s = pts[i][0]
        while i < len(pts) and pts[i][0] == s:
            tp += pts[i][1]
            fp += 1 - pts[i][1]
            i += 1
        best = max(best, tp * n_out - fp * n_in)
    return best / (n_in * n_out)
