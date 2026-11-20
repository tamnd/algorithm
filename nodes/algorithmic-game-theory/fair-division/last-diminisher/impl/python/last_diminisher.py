# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/last-diminisher/. The authors are listed in prov/VJGVJA.jsonl.

from fractions import Fraction

from agtcake import Oracle

Piece = list[tuple[Fraction, Fraction]]


def last_diminisher(oracle: Oracle) -> dict[int, Piece]:
    """Banach-Knaster last diminisher for the n agents of the oracle.

    Each agent i gets one interval, worth at least 1/n to it. In each round
    the first remaining agent cuts a piece worth 1/n to it, and each later
    agent trims the piece when it is worth more than 1/n to that agent.
    """
    n = oracle.n
    share = Fraction(1, n)
    alloc: dict[int, Piece] = {}
    a = Fraction(0)  # @line L1
    rest = list(range(n))
    while len(rest) > 1:  # @line L2
        holder = rest[0]  # @line L3
        x = oracle.cut_query(holder, a, share)
        for j in rest[1:]:  # @line L4
            if oracle.eval_query(j, a, x) > share:  # @line L5
                x = oracle.cut_query(j, a, share)  # @line L6
                holder = j
        alloc[holder] = [(a, x)]  # @line L7
        rest.remove(holder)
        a = x
    alloc[rest[0]] = [(a, Fraction(1))]  # @line L8
    return alloc
