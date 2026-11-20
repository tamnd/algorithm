# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marginal-contribution-nets/. The authors are listed in prov/J0TAYV.jsonl.
"""Marginal contribution nets (MC-nets): a TU game written as a list of rules.

A rule is a triple (P, Q, x). P is the set of positive literals, Q the set of negative
literals and x the value. The rule applies to a coalition S if P is a subset of S and Q does
not meet S. The value v(S) is the sum of x over the rules that apply to S. P must be nonempty
and disjoint from Q, so that no rule applies to the empty coalition and v(empty set) = 0.
Players are 0 to n - 1. Values may be ints or Fractions, and the indices come out exact.
"""

from fractions import Fraction
from itertools import combinations
from math import factorial

Rule = tuple[frozenset, frozenset, object]


def make_rule(pos, neg, x) -> Rule:
    """Build a rule and check that it is valid."""
    P, Q = frozenset(pos), frozenset(neg)
    if not P:
        raise ValueError("a rule needs at least one positive literal")
    if P & Q:
        raise ValueError("a player cannot be both a positive and a negative literal")
    return (P, Q, x)


def value(rules: list[Rule], S) -> object:
    """v(S): the sum of the values of the rules that apply to S."""
    S = frozenset(S)
    total = 0  # @line L1
    for P, Q, x in rules:  # @line L2
        if P <= S and not (Q & S):  # @line L3
            total += x
    return total  # @line L4


def shapley(rules: list[Rule], n: int) -> list[Fraction]:
    """The Shapley value of every player, in time linear in the size of the rules."""
    phi = [Fraction(0)] * n  # @line L5
    for P, Q, x in rules:  # @line L6
        a, b = len(P), len(Q)
        for i in P:  # @line L7
            phi[i] += Fraction(x) * factorial(a - 1) * factorial(b) / factorial(a + b)  # @line L8
        for j in Q:  # @line L9
            phi[j] -= Fraction(x) * factorial(a) * factorial(b - 1) / factorial(a + b)  # @line L10
    return phi  # @line L11


def banzhaf(rules: list[Rule], n: int) -> list[Fraction]:
    """The raw Banzhaf value of every player: the mean of v(S + i) - v(S) over the 2^(n-1) sets S."""
    beta = [Fraction(0)] * n  # @line L12
    for P, Q, x in rules:  # @line L13
        share = Fraction(x) / 2 ** (len(P) + len(Q) - 1)  # @line L14
        for i in P:  # @line L15
            beta[i] += share
        for j in Q:  # @line L16
            beta[j] -= share
    return beta  # @line L17


def from_game(n: int, v) -> list[Rule]:
    """Rules with no negative literals for any game v, from its Harsanyi dividends.

    The dividend of T is the sum over S in T of (-1)^(|T| - |S|) v(S). The game is the sum of
    dividend(T) times the unanimity game of T, so the rule (T, empty set, dividend(T)) for each
    nonempty T with a nonzero dividend gives back v. The output can have 2^n - 1 rules.
    """
    rules = []
    for r in range(1, n + 1):
        for T in combinations(range(n), r):
            d = 0
            for k in range(r + 1):
                for S in combinations(T, k):
                    d += (-1) ** (r - k) * v(frozenset(S))
            if d != 0:
                rules.append(make_rule(T, (), d))
    return rules
