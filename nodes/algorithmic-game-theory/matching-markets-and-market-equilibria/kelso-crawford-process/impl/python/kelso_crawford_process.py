# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kelso-crawford-process/. The authors are listed in prov/AYJGGA.jsonl.
"""The Kelso-Crawford ascending process, in the auction form with personalized prices.

Bidders (firms) are 0, ..., n - 1 and items (workers) are 0, ..., m - 1. Each bidder i has a
valuation values[i], a function from a frozenset of items to a number, with value 0 for the
empty set. Items have no preferences except for money, so an item goes to the bidder who bids
for it last. A bidder sees the price p[j] for an item she holds and p[j] + delta for any other
item. In each turn she picks a demanded bundle that keeps all her items and takes the new items
of that bundle, whose prices rise by delta. The process ends when no bidder wants to change.
When every valuation has gross substitutes, a demanded bundle that keeps her items always exists.
"""

from fractions import Fraction
from itertools import combinations
from typing import Callable, Optional

Valuation = Callable[[frozenset], object]
NONE = -1  # an item that no bidder holds


def bundles(m: int):
    """All subsets of range(m), by size and then in lexicographic order."""
    for k in range(m + 1):
        for c in combinations(range(m), k):
            yield frozenset(c)


def demand(v: Valuation, prices, m: int) -> list[frozenset]:
    """All bundles of maximum utility v(S) - sum of prices over S."""
    best, out = None, []
    for S in bundles(m):
        u = v(S) - sum((prices[j] for j in S), Fraction(0))
        if best is None or u > best:
            best, out = u, [S]
        elif u == best:
            out.append(S)
    return out


def kelso_crawford(values: list[Valuation], m: int, delta=None, trace: Optional[list] = None):
    """Run the process. Return (prices, owner): prices[j] is a Fraction and owner[j] is the
    bidder who holds item j, or NONE. delta defaults to 1 / (m + 1), which makes the final
    allocation optimal when all values are integers.

    If trace is a list, each bid appends (bidder, the new items, the prices after the bid).
    Raise ValueError if some bidder has no demanded bundle that keeps her items, which can
    happen only when her valuation does not have gross substitutes.
    """
    n = len(values)
    if m < 0:
        raise ValueError("m must be nonnegative")
    delta = Fraction(1, m + 1) if delta is None else Fraction(delta)
    if delta <= 0:
        raise ValueError("delta must be positive")
    prices = [Fraction(0)] * m  # @line L1
    owner = [NONE] * m
    while True:  # @line L2
        changed = False  # @line L3
        for i in range(n):  # @line L4
            X = frozenset(j for j in range(m) if owner[j] == i)  # @line L5
            q = [prices[j] if j in X else prices[j] + delta for j in range(m)]  # @line L6
            keep = [S for S in demand(values[i], q, m) if X <= S]  # @line L7
            if not keep:
                raise ValueError("bidder %d has no demanded bundle that keeps her items" % i)
            S = keep[0]
            new = sorted(S - X)
            for j in new:  # @line L8
                prices[j] += delta
                owner[j] = i
                changed = True
            if new and trace is not None:
                trace.append((i, new, list(prices)))
        if not changed:  # @line L9
            break
    return prices, owner  # @line L10


def allocation(owner: list[int], n: int) -> list[frozenset]:
    """The bundle of each bidder."""
    return [frozenset(j for j, o in enumerate(owner) if o == i) for i in range(n)]
