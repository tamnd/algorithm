# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-persuasion/. The authors are listed in prov/7DNF62.jsonl.

"""Optimal Bayesian persuasion with finite states and actions, by linear programming.

prior[w] is the prior probability of state w. receiver[w][a] and sender[w][a] are the
utilities of the receiver and the sender when the state is w and the receiver takes action
a. By the revelation principle for persuasion, it is enough to consider schemes whose
signals are action recommendations that the receiver is willing to follow. The variables are
z(w, a) = Pr[state w and recommendation a], and the problem is one LP, solved exactly in
Fraction by agtlp. Ties of the receiver are broken in favor of the sender, as usual.
"""

from fractions import Fraction

from agtlp import lp_max


def optimal_scheme(prior, receiver, sender):
    """Return (value, scheme) where scheme[w][a] = Pr[recommend a | state w]."""
    S, A = len(prior), len(receiver[0])
    prior = [Fraction(p) for p in prior]
    if any(p < 0 for p in prior) or sum(prior) != 1:
        raise ValueError("prior must be a probability vector")
    var = {(w, a): w * A + a for w in range(S) for a in range(A)}  # @line L1
    nv = S * A
    A_eq, b_eq = [], []
    for w in range(S):  # @line L2
        row = [Fraction(0)] * nv
        for a in range(A):
            row[var[w, a]] = Fraction(1)
        A_eq.append(row)
        b_eq.append(prior[w])
    A_ub, b_ub = [], []
    for a in range(A):  # @line L3
        for b in range(A):
            if b != a:
                row = [Fraction(0)] * nv
                for w in range(S):
                    # Obedience written as  sum_w z(w, a) (u_R(w, b) - u_R(w, a)) <= 0.
                    row[var[w, a]] = Fraction(receiver[w][b]) - Fraction(receiver[w][a])
                A_ub.append(row)
                b_ub.append(Fraction(0))
    c = [Fraction(sender[w][a]) for w in range(S) for a in range(A)]  # @line L4
    status, z, value, _ = lp_max(c, A_ub, b_ub, A_eq, b_eq)
    assert status == "optimal"  # the scheme that reveals nothing is always feasible
    scheme = []
    for w in range(S):  # @line L5
        if prior[w] > 0:
            scheme.append([z[var[w, a]] / prior[w] for a in range(A)])
        else:
            scheme.append([Fraction(int(a == 0)) for a in range(A)])
    return value, scheme  # @line L6


def receiver_action(belief, receiver, sender):
    """Best action of the receiver at a belief, with ties broken in favor of the sender."""
    S, A = len(belief), len(receiver[0])

    def key(a):
        return (sum(belief[w] * Fraction(receiver[w][a]) for w in range(S)),
                sum(belief[w] * Fraction(sender[w][a]) for w in range(S)))

    return max(range(A), key=key)


def sender_value(belief, receiver, sender):
    """The sender's expected utility when the receiver holds this belief and acts on it."""
    a = receiver_action(belief, receiver, sender)
    return sum(Fraction(belief[w]) * Fraction(sender[w][a]) for w in range(len(belief)))


def posteriors(prior, scheme):
    """The signal probabilities and posteriors induced by a scheme, one per signal used."""
    S, A = len(prior), len(scheme[0])
    out = []
    for a in range(A):
        p = sum(Fraction(prior[w]) * scheme[w][a] for w in range(S))
        if p > 0:
            out.append((a, p, [Fraction(prior[w]) * scheme[w][a] / p for w in range(S)]))
    return out
