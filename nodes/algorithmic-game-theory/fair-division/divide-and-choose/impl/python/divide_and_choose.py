# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-choose/. The authors are listed in prov/EWY1RW.jsonl.

from fractions import Fraction

from agtcake import Oracle

Piece = list[tuple[Fraction, Fraction]]

HALF = Fraction(1, 2)


def divide_and_choose(oracle: Oracle, cutter: int = 0, chooser: int = 1) -> dict[int, Piece]:
    """Divide [0, 1] between two agents. The cutter cuts, the chooser chooses.

    Returns a dict from each agent to its piece. The chooser takes the left
    piece when it values the two pieces equally.
    """
    x = oracle.cut_query(cutter, 0, HALF)  # @line L1
    left: Piece = [(Fraction(0), x)]
    right: Piece = [(x, Fraction(1))]
    if oracle.eval_query(chooser, 0, x) >= HALF:  # @line L2
        return {chooser: left, cutter: right}  # @line L3
    return {cutter: left, chooser: right}  # @line L4
