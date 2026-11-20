# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-in-range-mechanism/. The authors are listed in prov/HD9BNP.jsonl.

"""A maximal-in-range mechanism for small combinatorial auctions.

An allocation is a tuple owner, where owner[j] is the bidder who gets item j, or None.
A valuation is a dict from frozenset of items to a number. The mechanism maximizes the
reported welfare exactly over a fixed range of allocations, which does not depend on the
bids, and charges VCG payments computed over the same range. The range used here gives all
items to one bidder, or gives each bidder at most one item. All arithmetic is exact.
"""

from fractions import Fraction
from itertools import product
from typing import Mapping, Sequence

Allocation = tuple


def bundle(owner: Allocation, i: int) -> frozenset:
    """The set of items that the allocation gives to bidder i."""
    return frozenset(j for j, o in enumerate(owner) if o == i)


def value(valuation: Mapping, owner: Allocation, i: int) -> Fraction:
    """Value of bidder i for its bundle under the allocation."""
    return Fraction(valuation[bundle(owner, i)])


def grand_or_single_range(n: int, m: int) -> list:
    """All grand-bundle allocations, then all allocations with at most one item per bidder."""
    rng = [tuple([i] * m) for i in range(n)]
    for owner in product([None] + list(range(n)), repeat=m):
        taken = [o for o in owner if o is not None]
        if len(taken) == len(set(taken)) and owner not in rng:
            rng.append(owner)
    return rng


def all_allocations(n: int, m: int) -> list:
    """Every allocation of m items to n bidders, some items possibly unassigned."""
    return list(product([None] + list(range(n)), repeat=m))


def maximal_in_range(rng: Sequence[Allocation], bids: Sequence[Mapping]):
    """Run the mechanism on the fixed range rng. Return (x, payments)."""
    if not rng:
        raise ValueError("the range must not be empty")
    n = len(bids)
    total = {o: sum((value(bids[i], o, i) for i in range(n)), Fraction(0)) for o in rng}  # @line L1
    x = rng[0]
    for o in rng:  # @line L2
        if total[o] > total[x]:
            x = o
    payments = []
    for i in range(n):  # @line L3
        best_without = max(total[o] - value(bids[i], o, i) for o in rng)  # @line L4
        payments.append(best_without - (total[x] - value(bids[i], x, i)))  # @line L5
    return x, payments  # @line L6


def welfare(valuations: Sequence[Mapping], owner: Allocation) -> Fraction:
    """True welfare of an allocation."""
    return sum((value(v, owner, i) for i, v in enumerate(valuations)), Fraction(0))
