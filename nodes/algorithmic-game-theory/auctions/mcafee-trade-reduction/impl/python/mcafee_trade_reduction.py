# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcafee-trade-reduction/. The authors are listed in prov/AMA27A.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def mcafee_trade_reduction(
    buyer_bids: Sequence[Number], seller_asks: Sequence[Number]
) -> tuple[list[int], list[int], Number, Number]:
    """Run McAfee's double auction with trade reduction.

    Each buyer wants one unit and bids buyer_bids[i]. Each seller has one unit
    and asks seller_asks[j]. Buyers are ranked by bid, highest first, and
    sellers by ask, lowest first; a tie goes to the smaller index. Let k be
    the number of efficient trades, the largest k with b(k) >= s(k).

    If both a (k + 1)-th buyer and a (k + 1)-th seller exist and the price
    p0 = (b(k + 1) + s(k + 1)) / 2 lies in [s(k), b(k)], the top k buyers and
    sellers trade at p0. Otherwise only the top k - 1 pairs trade: each of
    those buyers pays b(k) and each of those sellers receives s(k), and the
    auctioneer keeps the difference.

    Return (buyers, sellers, buyer_price, seller_price), with the 0-based
    indices of the buyers and sellers who trade, in rank order.
    """
    buyers = sorted(range(len(buyer_bids)), key=lambda i: (-buyer_bids[i], i))  # @line L1
    sellers = sorted(range(len(seller_asks)), key=lambda j: (seller_asks[j], j))  # @line L1
    b = [buyer_bids[i] for i in buyers]
    s = [seller_asks[j] for j in sellers]
    k = 0  # @line L2
    while k < min(len(b), len(s)) and b[k] >= s[k]:  # @line L2
        k += 1  # @line L2
    if k == 0:  # @line L3
        return [], [], 0, 0  # @line L3
    if k < len(b) and k < len(s):  # @line L4
        p0 = Fraction(b[k] + s[k], 2)  # @line L4
        if s[k - 1] <= p0 <= b[k - 1]:  # @line L5
            return buyers[:k], sellers[:k], p0, p0  # @line L6
    return buyers[:k - 1], sellers[:k - 1], b[k - 1], s[k - 1]  # @line L7


def buyer_utility(value: Number, bids: Sequence[Number], asks: Sequence[Number], i: int) -> Number:
    """Utility of buyer i with the given value under the reports bids and asks."""
    buyers, _, price, _ = mcafee_trade_reduction(bids, asks)
    return value - price if i in buyers else 0


def seller_utility(cost: Number, bids: Sequence[Number], asks: Sequence[Number], j: int) -> Number:
    """Utility of seller j with the given cost under the reports bids and asks."""
    _, sellers, _, price = mcafee_trade_reduction(bids, asks)
    return price - cost if j in sellers else 0
