# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/demange-gale-sotomayor-auction/. The authors are listed in prov/RZZ6FP.jsonl.
"""The Demange-Gale-Sotomayor exact auction for unit-demand bidders.

Bidders are 0, ..., n - 1 and items are 0, ..., m - 1. values[i][j] is the nonnegative integer
value of bidder i for item j. A bidder buys at most one item and pays its price, so her utility
for item j at prices p is values[i][j] - p[j], and 0 for no item. The auction raises the price
of every item of a minimal overdemanded set by one unit until no set is overdemanded. It ends
at the minimum Walrasian (competitive equilibrium) price vector.
"""

from fractions import Fraction
from typing import Optional

NONE = -1  # the null option: no item


def demand(values: list[list[int]], prices: list[Fraction], i: int) -> set[int]:
    """Return the demand set of bidder i: the items of maximum utility, plus NONE when that
    maximum is at most 0."""
    best = max([Fraction(0)] + [values[i][j] - prices[j] for j in range(len(prices))])
    out = {j for j in range(len(prices)) if values[i][j] - prices[j] == best}
    if best <= 0:
        out.add(NONE)
    return out


def _max_matching(bidders, items, dem, match_of_item=None):
    """Augmenting path matching of the given bidders into the given items along demand edges.
    Returns (bidder -> item, item -> bidder)."""
    item_set = set(items)
    mi = {} if match_of_item is None else dict(match_of_item)
    mb = {b: j for j, b in mi.items()}

    def augment(b, seen):
        for j in sorted(dem[b]):
            if j in item_set and j not in seen:
                seen.add(j)
                if j not in mi or augment(mi[j], seen):
                    mi[j] = b
                    mb[b] = j
                    return True
        return False

    for b in bidders:
        if b not in mb:
            augment(b, set())
    return mb, mi


def _has_overdemanded_subset(S, required, dem):
    """True if some subset of the items S is overdemanded, by Hall's theorem: the bidders whose
    demand lies inside S cannot all be matched into S."""
    inside = [b for b in required if dem[b] <= S]
    mb, _ = _max_matching(inside, S, dem)
    return len(mb) < len(inside)


def dgs_auction(values: list[list[int]], trace: Optional[list] = None):
    """Run the exact auction. Return (prices, assignment): prices is a list of Fraction (all
    integers), and assignment[i] is the item of bidder i or NONE.

    If trace is a list, each round appends (prices before the round, the set S raised).
    """
    n = len(values)
    m = len(values[0]) if n else 0
    for row in values:
        if len(row) != m or any(not isinstance(x, int) or x < 0 for x in row):
            raise ValueError("values must be an n by m table of nonnegative integers")
    prices = [Fraction(0)] * m  # @line L1
    while True:  # @line L2
        dem = [demand(values, prices, i) for i in range(n)]  # @line L3
        required = [i for i in range(n) if NONE not in dem[i]]
        mb, mi = _max_matching(required, range(m), dem)  # @line L4
        if len(mb) == len(required):  # @line L5
            break
        # Items reachable by alternating paths from an unmatched required bidder.
        start = next(b for b in required if b not in mb)  # @line L6
        reach_items, stack, seen_b = set(), [start], {start}
        while stack:
            b = stack.pop()
            for j in dem[b]:
                if j != NONE and j not in reach_items:
                    reach_items.add(j)
                    nb = mi.get(j)
                    if nb is not None and nb not in seen_b:
                        seen_b.add(nb)
                        stack.append(nb)
        S = set(reach_items)
        for j in sorted(reach_items):  # @line L7
            if _has_overdemanded_subset(S - {j}, required, dem):
                S.discard(j)
        if trace is not None:
            trace.append((list(prices), frozenset(S)))
        for j in S:  # @line L8
            prices[j] += 1
    # Extend the matching so that every item with a positive price is sold.
    mi = dict(mi)
    for j0 in range(m):  # @line L9
        if prices[j0] == 0 or j0 in mi:
            continue
        # Breadth-first search over alternating paths j0 - b1 - j1 - b2 - ... that end at a free
        # bidder or at a matched item of price 0.
        parent = {("item", j0): None}
        queue = [("item", j0)]
        end = None
        while queue and end is None:
            node = queue.pop(0)
            kind, x = node
            if kind == "item":
                for b in range(n):
                    if x in dem[b] and mi.get(x) != b and ("bid", b) not in parent:
                        parent[("bid", b)] = node
                        if b not in mb:
                            end = ("bid", b)
                            break
                        queue.append(("bid", b))
            else:
                j = mb[x]
                if ("item", j) not in parent:
                    parent[("item", j)] = node
                    if prices[j] == 0:
                        end = ("item", j)
                        break
                    queue.append(("item", j))
        if end is None:
            raise AssertionError("no alternating path; the prices are not Walrasian")
        node = end
        if node[0] == "item":  # the path ends at an item of price 0, which becomes unsold
            del mi[node[1]]
            node = parent[node]
        while node is not None:  # node is a bidder; give it the item before it on the path
            b = node[1]
            j = parent[node][1]
            mb[b] = j
            mi[j] = b
            node = parent[parent[node]]
    assignment = [mb.get(i, NONE) for i in range(n)]  # @line L10
    return prices, assignment
