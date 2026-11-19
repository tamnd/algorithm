# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-risk-training/. The authors are listed in prov/1GGJMF.jsonl.

"""The risk of minimum risk training (Shen et al. 2016) and its gradient.

For one source sentence x with the reference y*, the model gives the log
probabilities log P(y | x; theta) of the candidates y in a subset S(x),
usually drawn by sampling from the model. The distribution over the subset is

    Q(y) = P(y | x)^alpha / sum_{y' in S} P(y' | x)^alpha,

with the sharpness alpha, and the risk is R = sum_y Q(y) Delta(y, y*).
The derivative of R with respect to log P(y | x) is

    alpha Q(y) (Delta(y, y*) - R),

and the chain rule through log P(y | x; theta) gives the gradient for the
parameters. The log probabilities and the losses are given (outputs of a
network and of a metric such as 1 - sentence BLEU); this module does not
train a network.
"""

import math
from typing import List, Sequence, Tuple

from nlslog import softmax


def risk_and_gradient(logp: Sequence[float], loss: Sequence[float],
                      alpha: float) -> Tuple[float, List[float], List[float]]:
    """Return (R, Q, g) for one sentence, where g[k] = dR / d logp[k]."""
    if len(logp) == 0 or len(logp) != len(loss):
        raise ValueError("logp and loss must be non-empty and of the same length")
    if not alpha > 0:
        raise ValueError("alpha must be positive")
    s = [alpha * x for x in logp]  # @line L1
    q = softmax(s)  # @line L2
    r = math.fsum(qk * dk for qk, dk in zip(q, loss))  # @line L3
    g = [alpha * qk * (dk - r) for qk, dk in zip(q, loss)]  # @line L4
    return r, q, g  # @line L5


def corpus_risk(batch: Sequence[Tuple[Sequence[float], Sequence[float]]],
                alpha: float) -> Tuple[float, List[List[float]]]:
    """Return the sum of the sentence risks and the gradients for each sentence."""
    total, grads = 0.0, []
    for logp, loss in batch:  # @line L6
        r, _, g = risk_and_gradient(logp, loss, alpha)
        total += r
        grads.append(g)
    return total, grads  # @line L7


def dedupe(samples: Sequence[Sequence[str]]) -> List[Tuple[str, ...]]:
    """Return the distinct candidates in the order of their first appearance.

    S(x) is a set: a candidate drawn twice counts once in Q.
    """
    seen, out = set(), []
    for y in samples:
        t = tuple(y)
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out
