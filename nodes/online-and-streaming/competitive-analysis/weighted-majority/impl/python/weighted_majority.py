# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-majority/. The authors are listed in prov/PJZVZH.jsonl.

"""Weighted majority (Littlestone and Warmuth) with exact rational weights.

predictions[t][i] is the bit that expert i predicts in round t, and
outcomes[t] is the true bit. The factor beta is a Fraction with 0 <= beta < 1.
"""

import random
from fractions import Fraction
from typing import Callable


def weighted_majority(
    predictions: list[list[int]], outcomes: list[int], beta: Fraction = Fraction(1, 2)
) -> tuple[list[int], list[Fraction]]:
    """Run deterministic weighted majority. Return its predictions and the final weights.

    Ties (equal weight on 0 and 1) predict 1. Cost: O(n) per round.
    """
    if not 0 <= beta < 1:
        raise ValueError("beta must be in [0, 1)")
    if len(predictions) != len(outcomes):
        raise ValueError("one outcome per round is needed")
    n = len(predictions[0]) if predictions else 0
    w = [Fraction(1)] * n  # @line L1
    said: list[int] = []
    for f, y in zip(predictions, outcomes):  # @line L2
        if len(f) != n:  # @line L3
            raise ValueError("each round needs one prediction per expert")
        w1 = sum((w[i] for i in range(n) if f[i] == 1), Fraction(0))  # @line L4
        w0 = sum((w[i] for i in range(n) if f[i] != 1), Fraction(0))
        said.append(1 if w1 >= w0 else 0)  # @line L5
        # @line L6: the outcome y is revealed here
        for i in range(n):  # @line L7
            if f[i] != y:
                w[i] *= beta
    return said, w


def mistakes(said: list[int], outcomes: list[int]) -> int:
    return sum(1 for a, y in zip(said, outcomes) if a != y)


def expert_mistakes(predictions: list[list[int]], outcomes: list[int]) -> list[int]:
    n = len(predictions[0]) if predictions else 0
    return [sum(1 for f, y in zip(predictions, outcomes) if f[i] != y) for i in range(n)]


def against_adversary(n_experts: int, rounds: int, advice: Callable[[int], list[int]],
                      beta: Fraction = Fraction(1, 2)) -> tuple[list[list[int]], list[int]]:
    """Build the sequence on which an adaptive adversary makes WM err in every round.

    advice(t) gives the expert predictions of round t; the outcome is the
    opposite of the prediction of weighted majority. Cost: O(n) per round.
    """
    w = [Fraction(1)] * n_experts
    preds: list[list[int]] = []
    outs: list[int] = []
    for t in range(rounds):
        f = advice(t)
        w1 = sum((w[i] for i in range(n_experts) if f[i] == 1), Fraction(0))
        w0 = sum((w[i] for i in range(n_experts) if f[i] != 1), Fraction(0))
        y = 0 if w1 >= w0 else 1
        for i in range(n_experts):
            if f[i] != y:
                w[i] *= beta
        preds.append(f)
        outs.append(y)
    return preds, outs


def randomized_weighted_majority(
    losses: list[list[Fraction]], beta: Fraction = Fraction(1, 2)
) -> tuple[Fraction, list[list[Fraction]]]:
    """Randomized weighted majority for losses in [0, 1].

    In round t the expert i is chosen with probability w_i / W, and after the
    losses are seen each weight is multiplied by 1 - (1 - beta) * loss, which
    is between beta**loss and 1. Return the expected total loss and the
    probability vectors. Cost: O(n) per round.
    """
    if not 0 < beta < 1:
        raise ValueError("beta must be in (0, 1)")
    n = len(losses[0]) if losses else 0
    w = [Fraction(1)] * n
    total = Fraction(0)
    probs: list[list[Fraction]] = []
    for row in losses:
        if len(row) != n or any(not 0 <= x <= 1 for x in row):
            raise ValueError("each round needs n losses in [0, 1]")
        s = sum(w, Fraction(0))
        p = [x / s for x in w]
        probs.append(p)
        total += sum((pi * li for pi, li in zip(p, row)), Fraction(0))
        w = [wi * (1 - (1 - beta) * li) for wi, li in zip(w, row)]
    return total, probs


def sample_choices(probs: list[list[Fraction]], rng: random.Random) -> list[int]:
    """Draw the expert of each round from the probability vectors."""
    out = []
    for p in probs:
        out.append(rng.choices(range(len(p)), [float(x) for x in p])[0])
    return out
