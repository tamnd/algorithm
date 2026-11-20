# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vickrey-auction/. The authors are listed in prov/3GCYFC.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction, float]


def vickrey_auction(
    bids: Sequence[Number], reserve: Number = 0
) -> tuple[int | None, Number]:
    """Run a second-price sealed-bid auction with a reserve price.

    A bid can win only if it is at least the reserve. The highest such bid
    wins, and a tie goes to the smallest index. The winner pays the larger of
    the reserve and the highest bid of the other bidders. Return the 0-based
    index of the winner and the price, or (None, 0) if no bid reaches the
    reserve. Losers pay 0.
    """
    winner: int | None = None
    second: Number = reserve  # @line L1
    for i in range(len(bids)):  # @line L2
        b = bids[i]
        if b >= reserve and (winner is None or b > bids[winner]):  # @line L3
            if winner is not None:  # @line L4
                second = bids[winner]  # @line L4
            winner = i  # @line L5
        else:
            second = max(second, b)  # @line L6
    if winner is None:  # @line L7
        return None, 0  # @line L7
    return winner, second  # @line L8


def utility(value: Number, bids: Sequence[Number], i: int, reserve: Number = 0) -> Number:
    """Quasilinear utility of bidder i with the given value when the bids are bids."""
    winner, price = vickrey_auction(bids, reserve)
    if winner != i:
        return 0
    return value - price
