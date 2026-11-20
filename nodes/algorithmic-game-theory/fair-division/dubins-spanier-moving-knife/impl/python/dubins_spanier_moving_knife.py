# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dubins-spanier-moving-knife/. The authors are listed in prov/RTDGDA.jsonl.

from fractions import Fraction

from agtcake import Oracle

Piece = list[tuple[Fraction, Fraction]]


def dubins_spanier(oracle: Oracle) -> dict[int, Piece]:
    """The Dubins-Spanier moving knife, run with cut queries.

    A knife that moves from the left end stops at the first point where
    some remaining agent values the piece to its left at 1/n. That point is
    the least of the agents' 1/n marks, so one cut query per remaining agent
    and round finds it. Ties go to the agent with the smallest index.
    """
    n = oracle.n
    share = Fraction(1, n)
    alloc: dict[int, Piece] = {}
    a = Fraction(0)  # @line L1
    rest = list(range(n))
    while len(rest) > 1:  # @line L2
        marks = {i: oracle.cut_query(i, a, share) for i in rest}  # @line L3
        h = min(rest, key=lambda i: (marks[i], i))  # @line L4
        alloc[h] = [(a, marks[h])]  # @line L5
        rest.remove(h)
        a = marks[h]
    alloc[rest[0]] = [(a, Fraction(1))]  # @line L6
    return alloc
