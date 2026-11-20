# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moulin-mechanism/. The authors are listed in prov/ZZQA5X.jsonl.
"""The Moulin mechanism (Moulin 1999, Moulin and Shenker 2001).

The input is a set of players, their bids, and a cost-sharing method xi. The method maps a
set S of players to the share xi(i, S) of each i in S. The mechanism starts with all players,
drops every player whose bid is below its share, and repeats with the smaller set until all
remaining players can pay. It serves the final set S and charges xi(i, S). If xi is
cross-monotonic (no share rises when the set grows), the mechanism is group strategyproof.

The method is given as a function from a frozenset S to a dict {i: xi(i, S)}. Shares and bids
should be Fraction or int, so that the comparison b_i < xi(i, S) is exact.

Three cross-monotonic methods are included as examples: equal split of a fixed cost, the
Shapley value of an airport game, and the Shapley value of a weighted coverage cost.
"""

from fractions import Fraction


def moulin(players, bids, xi):
    """Return (served, payments): the served set as a frozenset and a dict of payments."""
    players = list(players)
    served = frozenset(players)  # @line L1
    while True:  # @line L2
        shares = xi(served)
        drop = {i for i in served if bids[i] < shares[i]}  # @line L3
        served = served - drop  # @line L4
        if not drop:  # @line L5
            break
    payments = {i: (shares[i] if i in served else Fraction(0)) for i in players}  # @line L6
    return served, payments  # @line L7


def equal_split(total):
    """Equal split of a fixed cost: C(S) = total for nonempty S, xi(i, S) = total / |S|."""
    total = Fraction(total)

    def xi(S):
        return {i: total / len(S) for i in S}

    return xi


def airport_shapley(lengths):
    """The Shapley value of the airport game C(S) = max of lengths[i] over i in S.

    Each segment of the runway is split equally among the players of S that need it."""
    lengths = {i: Fraction(r) for i, r in lengths.items()}

    def xi(S):
        order = sorted(S, key=lambda i: (lengths[i], i))
        out, acc, prev = {}, Fraction(0), Fraction(0)
        for k, i in enumerate(order):
            acc += (lengths[i] - prev) / (len(order) - k)
            prev = lengths[i]
            out[i] = acc
        return out

    return xi


def coverage_shapley(covers, weights):
    """The Shapley value of the coverage cost C(S) = total weight of the elements covered by S.

    covers[i] is the set of elements that player i needs; each element's weight is split
    equally among the players of S that need it."""
    weights = {e: Fraction(w) for e, w in weights.items()}

    def xi(S):
        count = {}
        for i in S:
            for e in covers[i]:
                count[e] = count.get(e, 0) + 1
        return {i: sum((weights[e] / count[e] for e in covers[i]), Fraction(0)) for i in S}

    return xi


def coverage_cost(covers, weights, S):
    """C(S) for the coverage cost."""
    needed = set()
    for i in S:
        needed |= set(covers[i])
    return sum((Fraction(weights[e]) for e in needed), Fraction(0))
