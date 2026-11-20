# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automated-mechanism-design/. The authors are listed in prov/JG4KT0.jsonl.

"""Automated mechanism design by linear programming, after Conitzer and Sandholm.

The setting is finite. Agent i has a list of types types[i]. The prior is a dict from type
profiles (tuples) to probabilities, so the types may be correlated. outcomes is a list, and
value[i][s][o] is the value of agent i of type s for outcome o. Utilities are quasilinear.

A randomized mechanism gives, for each reported profile t, a lottery x(t, o) over the
outcomes and a payment p_i(t) from each agent. The designer maximizes the expectation of

    g[o] + a * (sum of the agents' values of o) + b * (sum of the payments)

under incentive constraints ic ("bic" or "dsic") and participation constraints ir
("interim", "ex_post" or "none"). With payments=False all payments are 0. Everything is
one linear program, solved exactly in Fraction by agtlp.
"""

from fractions import Fraction
from itertools import product

from agtlp import lp_max


def profiles(types):
    """All type profiles, in the order of itertools.product."""
    return list(product(*types))


def _deviate(t, i, s):
    return t[:i] + (s,) + t[i + 1:]


def design(types, prior, outcomes, value, g=None, a=0, b=1, ic="bic", ir="interim", payments=True):
    """Return (status, objective value, mechanism) of an optimal randomized mechanism.

    mechanism maps each profile t to (lottery, pay), where lottery[j] is the probability of
    outcomes[j] and pay[i] is the payment of agent i. status is the one of the LP.
    """
    if ic not in ("bic", "dsic") or ir not in ("interim", "ex_post", "none"):
        raise ValueError("unknown constraint type")
    n, m = len(types), len(outcomes)
    g = [Fraction(0)] * m if g is None else [Fraction(v) for v in g]
    a, b = Fraction(a), Fraction(b)
    prof = profiles(types)
    pr = {t: Fraction(prior.get(t, 0)) for t in prof}
    # Variables: x(t, o) for every t and o, then p_i(t) = plus - minus if there are payments.
    xi = {}  # @line L1
    for t in prof:
        for j in range(m):
            xi[t, j] = len(xi)
    pi = {}
    if payments:
        for t in prof:
            for i in range(n):
                pi[t, i] = (len(xi) + 2 * len(pi), len(xi) + 2 * len(pi) + 1)
    nv = len(xi) + 2 * len(pi)

    def utility(i, s, t, weight, row):
        # Add weight * (utility of agent i of true type s when the report profile is t).
        for j, o in enumerate(outcomes):
            row[xi[t, j]] += weight * Fraction(value[i][s][o])
        if payments:
            plus, minus = pi[t, i]
            row[plus] -= weight
            row[minus] += weight

    A_ub, b_ub, A_eq, b_eq = [], [], [], []

    def at_least_zero(row):
        A_ub.append([-v for v in row])
        b_ub.append(Fraction(0))

    for t in prof:  # @line L2
        row = [Fraction(0)] * nv
        for j in range(m):
            row[xi[t, j]] = Fraction(1)
        A_eq.append(row)
        b_eq.append(Fraction(1))
    for i in range(n):  # @line L3
        for s in types[i]:
            for r in types[i]:
                if r == s:
                    continue
                if ic == "bic":
                    row = [Fraction(0)] * nv
                    for t in prof:
                        if t[i] == s and pr[t] != 0:
                            utility(i, s, t, pr[t], row)
                            utility(i, s, _deviate(t, i, r), -pr[t], row)
                    at_least_zero(row)
                else:
                    for t in prof:
                        if t[i] == s:
                            row = [Fraction(0)] * nv
                            utility(i, s, t, Fraction(1), row)
                            utility(i, s, _deviate(t, i, r), Fraction(-1), row)
                            at_least_zero(row)
    if ir != "none":  # @line L4
        for i in range(n):
            for s in types[i]:
                if ir == "interim":
                    row = [Fraction(0)] * nv
                    for t in prof:
                        if t[i] == s and pr[t] != 0:
                            utility(i, s, t, pr[t], row)
                    at_least_zero(row)
                else:
                    for t in prof:
                        if t[i] == s:
                            row = [Fraction(0)] * nv
                            utility(i, s, t, Fraction(1), row)
                            at_least_zero(row)
    c = [Fraction(0)] * nv  # @line L5
    for t in prof:
        for j, o in enumerate(outcomes):
            welfare = sum((Fraction(value[i][t[i]][o]) for i in range(n)), Fraction(0))
            c[xi[t, j]] += pr[t] * (g[j] + a * welfare)
        if payments:
            for i in range(n):
                plus, minus = pi[t, i]
                c[plus] += pr[t] * b
                c[minus] -= pr[t] * b
    status, x, val, _ = lp_max(c, A_ub, b_ub, A_eq, b_eq)
    if status != "optimal":
        return status, None, None
    mech = {}  # @line L6
    for t in prof:
        lottery = [x[xi[t, j]] for j in range(m)]
        if payments:
            pay = [x[pi[t, i][0]] - x[pi[t, i][1]] for i in range(n)]
        else:
            pay = [Fraction(0)] * n
        mech[t] = (lottery, pay)
    return status, val, mech
