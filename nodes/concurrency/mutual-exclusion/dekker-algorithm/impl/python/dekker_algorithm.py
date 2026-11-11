# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dekker-algorithm/. The authors are listed in prov/D4K719.jsonl.
"""Dekker's two-process mutual exclusion algorithm, as reported by Dijkstra.

This is the usual modern form with two flags and a turn variable (the
form of Dijkstra's account and of the textbooks), not the original
ALGOL text with jumps. The entry and exit sections are generators that
yield one shared memory step at a time to the interleaving explorer (see
explorer.py). Shared memory: flag[0], flag[1] and turn, all atomic
read/write registers.
"""
from __future__ import annotations

from typing import Iterator

from explorer import R, W

MEM = {("flag", 0): False, ("flag", 1): False, "turn": 0}
HOME = {("flag", 0): 0, ("flag", 1): 1, "turn": 0}


def lock(i: int) -> Iterator:
    """Entry section of process i, for i in {0, 1}."""
    j = 1 - i
    v = yield W(("flag", i), True)  # @line L1
    while True:
        f = yield R(("flag", j))  # @line L2
        if not f:
            break
        t = yield R("turn")  # @line L3
        if t == j:
            v = yield W(("flag", i), False)  # @line L4
            while True:
                t = yield R("turn")  # @line L5
                if t != j:
                    break
            v = yield W(("flag", i), True)  # @line L6


def unlock(i: int) -> Iterator:
    """Exit section of process i: give the turn away, then lower the flag."""
    v = yield W("turn", 1 - i)  # @line L7
    v = yield W(("flag", i), False)  # @line L8


def no_turn_lock(i: int) -> Iterator:
    """A wrong variant without the turn: raise the flag and wait while the other flag is up."""
    j = 1 - i
    v = yield W(("flag", i), True)
    while True:
        f = yield R(("flag", j))
        if not f:
            break


def no_turn_unlock(i: int) -> Iterator:
    v = yield W(("flag", i), False)
