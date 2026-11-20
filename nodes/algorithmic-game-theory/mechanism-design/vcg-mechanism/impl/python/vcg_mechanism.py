# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vcg-mechanism/. The authors are listed in prov/SH7M6B.jsonl.

"""The Vickrey-Clarke-Groves mechanism with Clarke pivot payments.

The outcome set is a finite list. A valuation is a dict from outcome to a number (int or
Fraction). The mechanism takes the reported valuations, picks an outcome of maximum
reported welfare (the first one in the list on ties), and charges each agent the loss of
welfare that its presence causes to the others. A positive payment is paid by the agent.
"""

from fractions import Fraction
from itertools import product
from typing import Callable, Hashable, Sequence

Outcome = Hashable
Valuation = dict


def welfare(valuations: Sequence[Valuation], o: Outcome, skip: int | None = None) -> Fraction:
    """Return the sum of v_j(o) over the agents j other than skip."""
    return sum((Fraction(v[o]) for j, v in enumerate(valuations) if j != skip), Fraction(0))


def best_outcome(outcomes: Sequence[Outcome], valuations: Sequence[Valuation], skip: int | None = None):
    """Return (o, w): the first outcome of maximum welfare of the agents other than skip, and that welfare."""
    best, best_w = None, None
    for o in outcomes:
        w = welfare(valuations, o, skip)
        if best_w is None or w > best_w:
            best, best_w = o, w
    return best, best_w


def vcg(outcomes: Sequence[Outcome], valuations: Sequence[Valuation]):
    """Run VCG with the Clarke pivot rule. Return (x, payments), payments as Fractions."""
    if not outcomes:
        raise ValueError("the outcome set is empty")
    total = {o: welfare(valuations, o) for o in outcomes}  # @line L1
    x = outcomes[0]
    for o in outcomes:  # @line L2
        if total[o] > total[x]:
            x = o
    payments = []
    for i, v in enumerate(valuations):  # @line L3
        w_without = max(total[o] - Fraction(v[o]) for o in outcomes)  # @line L4
        payments.append(w_without - (total[x] - Fraction(v[x])))  # @line L5
    return x, payments  # @line L6


def groves(outcomes: Sequence[Outcome], valuations: Sequence[Valuation], h: Sequence[Callable]):
    """Run a Groves mechanism: the VCG outcome, and p_i = h_i(v_-i) - sum over j != i of v_j(x).

    h[i] is called with the list of the reports of the other agents (agent i removed), so it
    cannot depend on the report of agent i. With h_i(v_-i) = max over o of the welfare of the
    others, this is vcg().
    """
    x, _ = best_outcome(outcomes, valuations)
    payments = []
    for i in range(len(valuations)):
        others = [v for j, v in enumerate(valuations) if j != i]
        payments.append(Fraction(h[i](others)) - welfare(valuations, x, skip=i))
    return x, payments


def utility(v: Valuation, x: Outcome, p) -> Fraction:
    """The quasilinear utility v(x) - p."""
    return Fraction(v[x]) - Fraction(p)


# Combinatorial auctions: m items 0..m-1 and n bidders 0..n-1. An allocation is a tuple a of
# length m, where a[j] is the bidder that gets item j, or -1 if item j stays unsold.


def allocations(n: int, m: int) -> list[tuple]:
    """All (n + 1)^m allocations of m items to n bidders, the empty allocation first."""
    return list(product(range(-1, n), repeat=m))


def bundle(a: tuple, i: int) -> frozenset:
    """The set of items that allocation a gives to bidder i."""
    return frozenset(j for j, b in enumerate(a) if b == i)


def xor_value(bids: dict, s: frozenset) -> Fraction:
    """The value of bundle s for XOR bids {bundle: value}: the best bid inside s, or 0."""
    return max((Fraction(w) for t, w in bids.items() if t <= s), default=Fraction(0))


def auction_valuations(xor_bids: Sequence[dict], m: int) -> tuple[list, list]:
    """Turn XOR bids of n bidders on m items into (outcomes, valuations) for vcg()."""
    n = len(xor_bids)
    outs = allocations(n, m)
    vals = [{a: xor_value(b, bundle(a, i)) for a in outs} for i, b in enumerate(xor_bids)]
    return outs, vals


def single_item(values: Sequence) -> tuple[list, list]:
    """One item and n bidders. Outcome i means that bidder i wins."""
    n = len(values)
    outs = list(range(n))
    vals = [{o: (Fraction(values[i]) if o == i else Fraction(0)) for o in outs} for i in range(n)]
    return outs, vals
