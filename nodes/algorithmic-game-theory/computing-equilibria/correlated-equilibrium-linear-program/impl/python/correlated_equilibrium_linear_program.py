# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/correlated-equilibrium-linear-program/. The authors are listed in prov/V535CJ.jsonl.
"""A correlated equilibrium of a finite game in normal form, by one linear program.

The game is a pair (sizes, pay) as in the shared helper agtgame; players maximize. The LP
has one variable p(s) >= 0 per pure profile s, one inequality per player i and ordered pair
j != l of its strategies, and the equation sum_s p(s) = 1. Its feasible set is exactly the
set of correlated equilibria. The LP is solved exactly, in Fraction, by the shared helper
agtlp.
"""

from fractions import Fraction

from agtgame import profiles
from agtlp import lp_max


def _replace(s, i, a):
    return s[:i] + (a,) + s[i + 1:]


def ce_constraints(game):
    """Return (S, rows, labels): the profiles in a fixed order, and one row per incentive
    constraint, as a list of coefficients over S, with the label (i, j, l) of the row.

    The row (i, j, l) reads sum_{s: s_i = j} p(s) (u_i(l, s_-i) - u_i(s)) <= 0.
    """
    sizes, pay = game
    S = profiles(sizes)
    rows, labels = [], []
    for i, k in enumerate(sizes):  # @line L2
        for j in range(k):
            for l in range(k):
                if l == j:
                    continue
                row = [pay[_replace(s, i, l)][i] - pay[s][i] if s[i] == j else Fraction(0) for s in S]  # @line L3
                rows.append(row)
                labels.append((i, j, l))
    return S, rows, labels


def correlated_equilibrium_lp(game, weight=None):
    """Return (p, value): a correlated equilibrium p (a dict from profiles to Fraction, with
    the profiles of probability 0 left out) that maximizes sum_s weight(s) p(s), and that
    maximum.

    weight is a function from profiles to numbers; the default is the social welfare
    sum_i u_i(s). Pass weight=lambda s: 0 for any correlated equilibrium.

    Precondition: a finite game with at least one strategy per player. Cost: one LP with
    |S| variables and sum_i k_i (k_i - 1) + 1 constraints; the exact simplex method used
    here takes an exponential number of pivots in the worst case.
    """
    sizes, pay = game
    if weight is None:
        weight = lambda s: sum(pay[s], Fraction(0))
    S, rows, _ = ce_constraints(game)  # @line L1
    A_eq = [[1] * len(S)]  # @line L4
    c = [Fraction(weight(s)) for s in S]
    status, x, value, _ = lp_max(c, rows, [0] * len(rows), A_eq, [1])  # @line L5
    if status != "optimal":
        raise AssertionError("the CE polytope is nonempty and bounded")
    p = {s: q for s, q in zip(S, x) if q != 0}  # @line L6
    return p, value
