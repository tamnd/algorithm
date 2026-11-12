# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-learning/. The authors are listed in prov/1ASVXZ.jsonl.
"""The generic ensemble template and three exact facts about combining predictors:
the Condorcet majority probability, the variance of an average of correlated predictors
(ESL Eq. 15.1), and the ambiguity decomposition of Krogh and Vedelsby.

Data model: a training set is a list of (x, y) pairs. A learner maps a training set to a
predictor. make_set(j, S, members) builds the training set of member j, and may look at the
earlier members (as in boosting) or not (as in bagging).
"""

from fractions import Fraction
from math import comb
from typing import Callable, Sequence


def ensemble(s: Sequence, learners: Sequence[Callable], make_set: Callable, combine: Callable) -> Callable:
    members: list = []
    for j, learner in enumerate(learners):  # @line L1
        s_j = make_set(j, s, members)  # @line L2
        members.append(learner(s_j))  # @line L3
    return lambda x: combine([f(x) for f in members])  # @line L4


def majority_correct(m: int, p: Fraction) -> Fraction:
    """P(more than half of m independent voters are right), each right with probability p."""
    return sum(comb(m, k) * p ** k * (1 - p) ** (m - k) for k in range(m // 2 + 1, m + 1))


def condorcet_step(m: int, p: Fraction) -> Fraction:
    """The exact gain from m to m + 2 voters, for odd m: C(m, (m-1)/2) (p (1-p))^((m+1)/2) (2p - 1)."""
    return comb(m, (m - 1) // 2) * (p * (1 - p)) ** ((m + 1) // 2) * (2 * p - 1)


def variance_of_average(sigma2: float, rho: float, m: int) -> float:
    """Var((X_1 + ... + X_m)/m) when each X_j has variance sigma2 and each pair has correlation rho."""
    return rho * sigma2 + (1 - rho) * sigma2 / m


def variance_from_covariance(cov: Sequence[Sequence[float]]) -> float:
    m = len(cov)
    return sum(sum(row) for row in cov) / (m * m)


def ambiguity(preds: Sequence[float], weights: Sequence[float], y: float) -> tuple[float, float, float]:
    """Return (ensemble error, weighted member error, ambiguity) for a convex combination.
    Krogh and Vedelsby: ensemble error = weighted member error - ambiguity."""
    fbar = sum(w * f for w, f in zip(weights, preds))
    err = (fbar - y) ** 2
    member = sum(w * (f - y) ** 2 for w, f in zip(weights, preds))
    amb = sum(w * (f - fbar) ** 2 for w, f in zip(weights, preds))
    return err, member, amb
