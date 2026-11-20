# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/english-auction/. The authors are listed in prov/6F235Y.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction, float]


def english_auction(
    thresholds: Sequence[Number], delta: Number, start: Number = 0
) -> tuple[int | None, Number]:
    """Run an ascending clock auction with a fixed increment.

    thresholds[i] is the highest price at which bidder i stays in. The clock
    starts at start (the reserve) and rises by delta. At each step the active
    bidders whose threshold is at least the next price stay in. When one
    bidder is left it wins at the current price. When all remaining bidders
    leave at the same step, the smallest index among them wins at the price
    they last accepted. Return the 0-based winner and the price, or (None, 0)
    if no threshold reaches start.
    """
    if delta <= 0:
        raise ValueError("delta must be positive")
    active = [i for i in range(len(thresholds)) if thresholds[i] >= start]  # @line L1
    price = start  # @line L1
    if not active:  # @line L2
        return None, 0  # @line L2
    while len(active) >= 2:  # @line L3
        staying = [i for i in active if thresholds[i] >= price + delta]  # @line L4
        if not staying:  # @line L5
            return active[0], price  # @line L5
        active = staying  # @line L6
        price = price + delta  # @line L6
    return active[0], price  # @line L7


def utility(value: Number, thresholds: Sequence[Number], i: int, delta: Number, start: Number = 0) -> Number:
    """Quasilinear utility of bidder i with the given value under these thresholds."""
    winner, price = english_auction(thresholds, delta, start)
    if winner != i:
        return 0
    return value - price
