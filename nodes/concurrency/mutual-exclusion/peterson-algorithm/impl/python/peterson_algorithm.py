# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-algorithm/. The authors are listed in prov/SA5BTH.jsonl.
"""Peterson's two-process mutual exclusion algorithm (Peterson 1981).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Shared
memory: flag[0], flag[1] and turn, all atomic read/write registers.
``lock_fenced`` adds a full fence between the doorway and the waiting
loop, which is what the algorithm needs on TSO hardware such as x86.
"""
from __future__ import annotations

from typing import Iterator

from explorer import DOOR, FENCE, R, W

MEM = {("flag", 0): False, ("flag", 1): False, "turn": 0}
HOME = {("flag", 0): 0, ("flag", 1): 1, "turn": 0}


def lock(i: int) -> Iterator:
    """Entry section of process i, for i in {0, 1}."""
    j = 1 - i
    v = yield W(("flag", i), True)  # @line L1
    v = yield W("turn", j)  # @line L2
    v = yield DOOR
    while True:  # @line L3
        f = yield R(("flag", j))  # @line L4
        if not f:
            break
        t = yield R("turn")  # @line L5
        if t != j:
            break


def unlock(i: int) -> Iterator:
    """Exit section of process i."""
    v = yield W(("flag", i), False)  # @line L6


def lock_fenced(i: int) -> Iterator:
    """The entry section with a full fence after the doorway (for TSO)."""
    j = 1 - i
    v = yield W(("flag", i), True)
    v = yield W("turn", j)
    v = yield FENCE
    v = yield DOOR
    while True:
        f = yield R(("flag", j))
        if not f:
            break
        t = yield R("turn")
        if t != j:
            break
