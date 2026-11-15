# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ia-select/. The authors are listed in prov/PXB2Y2.jsonl.
"""IA-Select (Agrawal, Gollapudi, Halverson and Ieong, 2009).

The objective of a set S of documents is

    P(S | q) = sum over c of P(c | q) * (1 - prod over d in S of (1 - V(d | q, c))),

the probability that at least one document of S satisfies the user, when
the user's intent c is drawn from P(c | q) and the documents satisfy
independently given c. IA-Select adds documents one by one. It keeps
U(c), the probability that intent c is the intent and is not yet
satisfied, starting from P(c | q), and picks the document with the largest
gain sum over c of U(c) V(d | q, c), which is the exact increase of
P(S | q). Ties go to the smaller id.
"""

from itertools import combinations


def objective(selected, p_cat, value):
    """P(S | q) for the documents in selected."""
    total = 0.0
    for c, p in p_cat.items():
        miss = 1.0
        for d in selected:
            miss *= 1.0 - value[d].get(c, 0.0)
        total += p * (1.0 - miss)
    return total


def ia_select_steps(docs, p_cat, value, k):
    """Return the list of (document, gain at the time it was picked)."""
    for d in docs:
        for c, v in value[d].items():
            if c not in p_cat or not 0.0 <= v <= 1.0:
                raise ValueError("V(d | q, c) must lie in [0, 1] for a known category")
    u = dict(p_cat)  # @line L1
    rest = sorted(set(docs))
    chosen = []  # @line L2
    while rest and len(chosen) < k:  # @line L3
        best, best_gain = None, None
        for d in rest:  # @line L4
            gain = sum(u[c] * v for c, v in value[d].items())  # @line L5
            if best_gain is None or gain > best_gain:  # ties keep the smaller id
                best, best_gain = d, gain
        chosen.append((best, best_gain))  # @line L6
        rest.remove(best)
        for c, v in value[best].items():  # @line L7
            u[c] *= 1.0 - v  # @line L8
    return chosen  # @line L9


def ia_select(docs, p_cat, value, k):
    """Return the documents that IA-Select picks, in order."""
    return [d for d, _ in ia_select_steps(docs, p_cat, value, k)]


def best_subset(docs, p_cat, value, k):
    """The exact optimum over all subsets of size min(k, |docs|), by enumeration."""
    size = min(k, len(docs))
    best, best_val = (), -1.0
    for s in combinations(sorted(docs), size):
        v = objective(s, p_cat, value)
        if v > best_val:
            best, best_val = s, v
    return list(best), best_val
