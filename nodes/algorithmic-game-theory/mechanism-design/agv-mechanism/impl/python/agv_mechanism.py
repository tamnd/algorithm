# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/agv-mechanism/. The authors are listed in prov/KNJ3AG.jsonl.

"""The AGV (d'Aspremont-Gerard-Varet) expected externality mechanism.

An instance has n >= 2 agents. Agent i has a finite list of types types[i] and an
independent prior probs[i], a dict from type to Fraction. There is a finite list of
outcomes. value[i][t][o] is the value of agent i of type t for outcome o. The
payment p_i is paid by agent i; a negative payment is a transfer to the agent.
"""

from fractions import Fraction
from itertools import product


def efficient_outcome(outcomes, value, profile):
    """Return the first outcome, in list order, that maximizes the reported welfare."""
    best, best_w = None, None
    for o in outcomes:
        w = sum(Fraction(value[i][t][o]) for i, t in enumerate(profile))
        if best_w is None or w > best_w:
            best, best_w = o, w
    return best


def expected_externalities(types, probs, outcomes, value):
    """Return h, with h[i][t] the expected welfare of the others when agent i reports t.

    The others report their true types, drawn from the prior, and the outcome is the
    efficient one. One pass over all type profiles fills every h[i][t].
    """
    n = len(types)
    h = [{t: Fraction(0) for t in types[i]} for i in range(n)]  # @line L1
    for t in product(*types):  # @line L2
        o = efficient_outcome(outcomes, value, t)  # @line L3
        vals = [Fraction(value[j][t[j]][o]) for j in range(n)]
        total = sum(vals)
        for i in range(n):  # @line L4
            pr = Fraction(1)
            for j in range(n):
                if j != i:
                    pr *= Fraction(probs[j][t[j]])
            h[i][t[i]] += pr * (total - vals[i])  # @line L5
    return h


def agv_payments(h, bids):
    """Return the AGV payments for the reported profile, given the table h."""
    n = len(bids)
    if n < 2:
        raise ValueError("the AGV mechanism needs at least two agents")
    payments = []
    for i in range(n):  # @line L7
        others = sum(h[j][bids[j]] for j in range(n) if j != i)
        payments.append(others / (n - 1) - h[i][bids[i]])  # @line L8
    return payments


def agv(types, probs, outcomes, value, bids):
    """Run the AGV mechanism on the reports bids. Return (outcome, payments)."""
    h = expected_externalities(types, probs, outcomes, value)
    o = efficient_outcome(outcomes, value, bids)  # @line L6
    return o, agv_payments(h, bids)  # @line L9


def interim_utility(types, probs, outcomes, value, i, true_type, report):
    """Expected utility of agent i of type true_type who reports report, when the
    others report their true types drawn from the prior. Exact, in Fraction."""
    n = len(types)
    h = expected_externalities(types, probs, outcomes, value)
    total = Fraction(0)
    others = [types[j] for j in range(n) if j != i]
    for rest in product(*others):
        prof = list(rest[:i]) + [report] + list(rest[i:])
        pr = Fraction(1)
        for j in range(n):
            if j != i:
                pr *= Fraction(probs[j][prof[j]])
        o = efficient_outcome(outcomes, value, prof)
        pay = agv_payments(h, prof)[i]
        total += pr * (Fraction(value[i][true_type][o]) - pay)
    return total
