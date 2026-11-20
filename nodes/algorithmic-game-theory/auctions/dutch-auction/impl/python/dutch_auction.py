# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dutch-auction/. The authors are listed in prov/6N55V9.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction, float]


def dutch_auction(
    stops: Sequence[Number], top: Number, delta: Number, reserve: Number = 0
) -> tuple[int | None, Number]:
    """Run a descending clock auction with a fixed decrement.

    The clock starts at top and falls by delta, and it never goes below the
    reserve. stops[i] is the price at which bidder i accepts: bidder i stops
    the clock at the first level p with stops[i] >= p. If several bidders
    accept at the same level, the smallest index wins. The winner pays the
    level. Return the 0-based winner and the price, or (None, 0) if the clock
    passes the reserve with no acceptance. The level is computed as
    top - k * delta, so floats do not accumulate rounding error.
    """
    if delta <= 0:
        raise ValueError("delta must be positive")
    k = 0
    price = top  # @line L1
    while price >= reserve:  # @line L2
        accepting = [i for i in range(len(stops)) if stops[i] >= price]  # @line L3
        if accepting:  # @line L4
            return accepting[0], price  # @line L4
        k += 1
        price = top - k * delta  # @line L5
    return None, 0  # @line L6
