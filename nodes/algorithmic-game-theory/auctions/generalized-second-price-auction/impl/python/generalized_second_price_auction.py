# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-second-price-auction/. The authors are listed in prov/ATPJNQ.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def gsp(
    bids: Sequence[Number], ctrs: Sequence[Number], reserve: Number = 0
) -> tuple[list[int], list[Number]]:
    """Run the generalized second-price auction for ranked ad slots.

    ctrs[s] is the click-through rate of slot s, with ctrs nonincreasing.
    Only bids of at least the reserve take part. They are ranked by bid,
    highest first, with ties to the smaller index, and the s-th ranked
    bidder gets slot s. It pays per click the next bid in the ranking, or the
    reserve if there is no next bid. Return (winners, prices): winners[s] is
    the 0-based bidder index in slot s, and prices[s] is its price per click.
    """
    ranked = sorted((i for i in range(len(bids)) if bids[i] >= reserve), key=lambda i: (-bids[i], i))  # @line L1
    filled = min(len(ctrs), len(ranked))  # @line L2
    winners: list[int] = []
    prices: list[Number] = []
    for s in range(filled):  # @line L3
        winners.append(ranked[s])  # @line L4
        if s + 1 < len(ranked):  # @line L5
            prices.append(bids[ranked[s + 1]])  # @line L5
        else:  # @line L6
            prices.append(reserve)  # @line L6
    return winners, prices  # @line L7


def utility(value: Number, bids: Sequence[Number], ctrs: Sequence[Number], i: int, reserve: Number = 0) -> Number:
    """Utility of bidder i per unit of time: ctr of its slot times value minus price."""
    winners, prices = gsp(bids, ctrs, reserve)
    for s, w in enumerate(winners):
        if w == i:
            return ctrs[s] * (value - prices[s])
    return 0


def revenue(bids: Sequence[Number], ctrs: Sequence[Number], reserve: Number = 0) -> Number:
    """Total payment of all bidders per unit of time."""
    winners, prices = gsp(bids, ctrs, reserve)
    return sum(ctrs[s] * prices[s] for s in range(len(winners)))


def vcg_payments(values: Sequence[Number], ctrs: Sequence[Number]) -> tuple[list[int], list[Number]]:
    """VCG outcome of the position auction with reported values.

    Rank by value as in gsp. The bidder in slot s pays the externality
    sum over t >= s of (ctrs[t] - ctrs[t + 1]) * v(t + 1), where v(t + 1)
    is the value ranked t + 1 (0 if it does not exist) and ctrs past the
    last slot are 0. Return (winners, total payments per slot).
    """
    ranked = sorted(range(len(values)), key=lambda i: (-values[i], i))
    k = min(len(ctrs), len(ranked))
    alpha = list(ctrs[:k]) + [0]
    v = [values[i] for i in ranked] + [0]
    pay = [sum((alpha[t] - alpha[t + 1]) * v[t + 1] for t in range(s, k)) for s in range(k)]
    return ranked[:k], pay


def eos_bids(values: Sequence[Number], ctrs: Sequence[Number]) -> list[Number]:
    """The bidder-optimal locally envy-free equilibrium of Edelman, Ostrovsky and Schwarz.

    The bidder ranked j >= 2 bids the VCG payment of slot j - 1 divided by
    ctrs[j - 1], the bidder ranked first bids its value, and bidders ranked
    below the first loser bid their values. Click-through rates must be
    positive.
    """
    ranked = sorted(range(len(values)), key=lambda i: (-values[i], i))
    _, pay = vcg_payments(values, ctrs)
    bids: list[Number] = [0] * len(values)
    for j, i in enumerate(ranked):
        if j == 0 or j > len(pay):
            bids[i] = values[i]
        else:
            bids[i] = Fraction(pay[j - 1]) / ctrs[j - 1]
    return bids
