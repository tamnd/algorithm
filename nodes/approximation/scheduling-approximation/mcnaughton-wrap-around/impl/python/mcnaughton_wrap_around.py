# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcnaughton-wrap-around/. The authors are listed in prov/FQ9V3K.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]
Piece = tuple[int, int, Fraction, Fraction]  # (job, machine, start, end)


def mcnaughton_wrap_around(p: list[Number], m: int) -> tuple[Fraction, list[Piece]]:
    """McNaughton's wrap-around rule for P|pmtn|C_max.

    Fill machine 0 from time 0 up to C* = max(max p_j, sum p_j / m), then go on
    with machine 1 from time 0, and so on. A job that does not fit in the rest
    of a machine is split: its first part ends the machine, its second part
    starts the next machine at time 0. Precondition: m >= 1, every p[j] >= 0.
    Returns (C*, pieces), with exact fractions. The schedule is optimal.
    Cost: O(n + m) time; at most m - 1 jobs are split.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    if not p:
        return Fraction(0), []
    c = max(Fraction(max(p)), Fraction(sum(p), m))  # @line L1
    i, t = 0, Fraction(0)  # @line L2
    pieces: list[Piece] = []
    for j in range(len(p)):  # @line L3
        r = Fraction(p[j])  # @line L4
        while r > 0:  # @line L5
            d = min(r, c - t)  # @line L6
            pieces.append((j, i, t, t + d))  # @line L7
            t, r = t + d, r - d  # @line L8
            if t == c:  # @line L9
                i, t = i + 1, Fraction(0)
    return c, pieces  # @line L10
