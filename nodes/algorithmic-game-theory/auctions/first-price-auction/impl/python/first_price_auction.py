# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/first-price-auction/. The authors are listed in prov/VEN1KY.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction, float]


def first_price_auction(
    bids: Sequence[Number], reserve: Number = 0
) -> tuple[int | None, Number]:
    """Run a first-price sealed-bid auction with a reserve price.

    A bid can win only if it is at least the reserve. The highest such bid
    wins, a tie goes to the smallest index, and the winner pays its own bid.
    Return the 0-based winner and the price, or (None, 0) if no bid reaches
    the reserve. Losers pay 0.
    """
    winner: int | None = None  # @line L1
    for i in range(len(bids)):  # @line L2
        if bids[i] >= reserve and (winner is None or bids[i] > bids[winner]):  # @line L3
            winner = i  # @line L3
    if winner is None:  # @line L4
        return None, 0  # @line L4
    return winner, bids[winner]  # @line L5


def equilibrium_bid(value: Fraction, n: int, a: int = 1) -> Fraction:
    """Symmetric equilibrium bid for n bidders with values of CDF F(v) = v^a on [0, 1].

    The bid is E[Y | Y < v] for Y the highest of the other n - 1 values, which
    is a(n - 1) v / (a(n - 1) + 1). For a = 1 (uniform values) it is (n - 1) v / n.
    """
    k = a * (n - 1)
    return Fraction(k, k + 1) * value


def interim_utility(value: Fraction, target: Fraction, n: int, a: int = 1) -> Fraction:
    """Expected utility of a bidder of the given value who bids as type target in [0, 1].

    The others bid equilibrium_bid, which is increasing, so the bid wins when
    all n - 1 other values are below target, with probability target^(a(n - 1)).
    """
    return (value - equilibrium_bid(target, n, a)) * target ** (a * (n - 1))
