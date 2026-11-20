# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/all-pay-auction/. The authors are listed in prov/HC5JY0.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction, float]


def all_pay_auction(bids: Sequence[Number]) -> tuple[int | None, list[Number]]:
    """Run a sealed-bid all-pay auction.

    The highest bid wins, a tie goes to the smallest index, and every bidder
    pays its own bid, win or lose. Return the 0-based winner (None if there
    are no bids) and the list of payments.
    """
    if not bids:
        return None, []
    winner = 0  # @line L1
    for i in range(1, len(bids)):  # @line L2
        if bids[i] > bids[winner]:  # @line L3
            winner = i  # @line L3
    payments = [bids[i] for i in range(len(bids))]  # @line L4
    return winner, payments  # @line L5


def equilibrium_bid(value: Fraction, n: int) -> Fraction:
    """Symmetric equilibrium bid (n - 1) v^n / n for n bidders with values uniform on [0, 1]."""
    return Fraction(n - 1, n) * value**n


def interim_utility(value: Fraction, target: Fraction, n: int) -> Fraction:
    """Expected utility of a bidder of the given value who bids as type target in [0, 1].

    The others bid equilibrium_bid, which is increasing, so the bid wins with
    probability target^(n - 1), and the bid is paid in every case.
    """
    return value * target ** (n - 1) - equilibrium_bid(target, n)
