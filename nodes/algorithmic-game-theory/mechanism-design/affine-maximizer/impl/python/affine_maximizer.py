# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-maximizer/. The authors are listed in prov/P44K0N.jsonl.

"""An affine maximizer with Clarke-style payments.

The range is a finite list of outcomes. A bid is a dict from outcome to a number (int or
Fraction). The mechanism picks the first outcome of the range with the largest affine score
c(o) + w_1 b_1(o) + ... + w_n b_n(o), and charges agent i the amount
(H_i - (S(x) - w_i b_i(x))) / w_i, where H_i is the best score of the others alone.
A positive payment is paid by the agent. All arithmetic is exact.
"""

from fractions import Fraction
from typing import Hashable, Mapping, Sequence

Outcome = Hashable


def affine_score(o: Outcome, bids: Sequence[Mapping], weights: Sequence, constants: Mapping, skip: int | None = None) -> Fraction:
    """Return c(o) plus the sum of w_j b_j(o) over the agents j other than skip."""
    s = Fraction(constants.get(o, 0))
    for j, (w, b) in enumerate(zip(weights, bids)):
        if j != skip:
            s += Fraction(w) * Fraction(b[o])
    return s


def affine_maximizer(outcomes: Sequence[Outcome], bids: Sequence[Mapping], weights: Sequence, constants: Mapping | None = None):
    """Run the affine maximizer with positive weights. Return (x, payments)."""
    if not outcomes:
        raise ValueError("the range must not be empty")
    if len(weights) != len(bids) or any(Fraction(w) <= 0 for w in weights):
        raise ValueError("need one positive weight per agent")
    constants = constants or {}
    score = {o: affine_score(o, bids, weights, constants) for o in outcomes}  # @line L1
    x = outcomes[0]
    for o in outcomes:  # @line L2
        if score[o] > score[x]:
            x = o
    payments = []
    for i, (w, b) in enumerate(zip(weights, bids)):  # @line L3
        h_i = max(score[o] - Fraction(w) * Fraction(b[o]) for o in outcomes)  # @line L4
        payments.append((h_i - (score[x] - Fraction(w) * Fraction(b[x]))) / Fraction(w))  # @line L5
    return x, payments  # @line L6


def utility(value: Mapping, x: Outcome, payment) -> Fraction:
    """Quasilinear utility of an agent with valuation value for outcome x and payment."""
    return Fraction(value[x]) - Fraction(payment)
