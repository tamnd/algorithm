# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simultaneous-ascending-auction/. The authors are listed in prov/427AF8.jsonl.

from fractions import Fraction
from typing import Callable, Sequence, Union

Number = Union[int, Fraction]
Valuation = Callable[[frozenset], Number]


def all_bundles(m: int) -> list[frozenset]:
    """All subsets of range(m), in the order of their bit masks."""
    return [frozenset(j for j in range(m) if mask >> j & 1) for mask in range(1 << m)]


def demand(v: Valuation, prices: Sequence[Number], bundles: Sequence[frozenset], held: frozenset) -> frozenset:
    """A bundle that maximizes v(S) - sum of prices over S.

    Among the best bundles, prefer one that contains the held items, then the
    first in the order of bundles. This is the tie rule of a straightforward
    bidder.
    """
    best, best_key = None, None
    for s in bundles:
        key = (v(s) - sum(prices[j] for j in s), held <= s)
        if best_key is None or key > best_key:
            best, best_key = s, key
    return best


def simultaneous_ascending_auction(
    valuations: Sequence[Valuation], m: int, epsilon: Number
) -> tuple[list[frozenset], list[Number], int]:
    """Simultaneous ascending auction with straightforward bidders.

    There are m items, numbered 0 to m - 1, and valuations[i] maps a
    frozenset of items to the value of bidder i, with value 0 for the empty
    set. Every price starts at 0. In each round, each bidder i faces the
    price p_j for an item j it holds and p_j + epsilon for any other item,
    picks a demanded bundle T with the tie rule of demand(), and bids on the
    items of T that it does not hold. A bid cannot be withdrawn. For each
    item with new bids, the bidder with the smallest index becomes the
    standing high bidder, and the price rises by epsilon. The auction stops
    after a round with no new bid. Return (bundles held, prices, rounds).
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    bundles = all_bundles(m)
    prices: list[Number] = [0] * m  # @line L1
    holder: list[int | None] = [None] * m  # @line L1
    rounds = 0
    while True:  # @line L2
        rounds += 1
        new_bids: list[list[int]] = [[] for _ in range(m)]
        for i, v in enumerate(valuations):  # @line L3
            held = frozenset(j for j in range(m) if holder[j] == i)  # @line L4
            personal = [prices[j] if j in held else prices[j] + epsilon for j in range(m)]  # @line L4
            target = demand(v, personal, bundles, held)  # @line L5
            for j in target - held:  # @line L6
                new_bids[j].append(i)  # @line L6
        if not any(new_bids):  # @line L7
            break  # @line L7
        for j in range(m):  # @line L8
            if new_bids[j]:  # @line L8
                holder[j] = min(new_bids[j])  # @line L9
                prices[j] = prices[j] + epsilon  # @line L9
    held_by = [frozenset(j for j in range(m) if holder[j] == i) for i in range(len(valuations))]
    return held_by, prices, rounds  # @line L10
