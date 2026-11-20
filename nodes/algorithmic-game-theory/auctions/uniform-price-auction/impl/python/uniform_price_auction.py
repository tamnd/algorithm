# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-price-auction/. The authors are listed in prov/6TRC5Q.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]

HIGHEST_LOSING = "highest-losing"
LOWEST_WINNING = "lowest-winning"


def uniform_price_auction(
    bids: Sequence[Sequence[Number]], k: int, rule: str = HIGHEST_LOSING
) -> tuple[list[int], Number, list[Number]]:
    """Sell k identical units at one price.

    bids[i] is the list of marginal bids of bidder i: bids[i][j] is what
    bidder i offers for its (j + 1)-th unit. Each list must be nonincreasing.
    The k highest marginal bids win one unit each. A tie between equal bids
    goes to the smaller bidder index, then to the smaller unit index, which
    for a nonincreasing list is the same as the earlier unit.

    With rule HIGHEST_LOSING the price is the highest losing bid, or 0 if
    every bid wins. With rule LOWEST_WINNING the price is the lowest winning
    bid, or 0 if no bid wins. Every unit sold costs the same price.

    Return (units, price, payments): units[i] is the number of units of
    bidder i and payments[i] = units[i] * price.
    """
    if k < 0:
        raise ValueError("k must be nonnegative")
    if rule not in (HIGHEST_LOSING, LOWEST_WINNING):
        raise ValueError("unknown price rule")
    for row in bids:
        for j in range(1, len(row)):
            if row[j] > row[j - 1]:
                raise ValueError("marginal bids must be nonincreasing")
    entries = [(row[j], i, j) for i, row in enumerate(bids) for j in range(len(row))]  # @line L1
    entries.sort(key=lambda e: (-e[0], e[1], e[2]))  # @line L2
    sold = min(k, len(entries))  # @line L3
    units = [0] * len(bids)
    for _, i, _ in entries[:sold]:  # @line L4
        units[i] += 1  # @line L4
    price: Number = 0
    if rule == HIGHEST_LOSING:  # @line L5
        if len(entries) > k:  # @line L5
            price = entries[k][0]  # @line L5
    elif sold > 0:  # @line L6
        price = entries[sold - 1][0]  # @line L6
    payments = [u * price for u in units]  # @line L7
    return units, price, payments  # @line L7


def utility(
    values: Sequence[Number], bids: Sequence[Sequence[Number]], i: int, k: int,
    rule: str = HIGHEST_LOSING,
) -> Number:
    """Quasilinear utility of bidder i whose true marginal values are values.

    The bidder gets values[0] + ... + values[u - 1] for u units and pays
    u times the price.
    """
    units, _, payments = uniform_price_auction(bids, k, rule)
    return sum(values[:units[i]]) - payments[i]
