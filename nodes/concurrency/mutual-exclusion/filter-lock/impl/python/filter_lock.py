# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-lock/. The authors are listed in prov/5JN2ZF.jsonl.
"""The filter lock: Peterson's n-process algorithm (Peterson 1981).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Processes
are numbered 0 to n - 1. There are n - 1 levels; level[i] is the level
that process i has reached (0 when it does not try), and victim[l] is the
process that came to level l last. Process i writes only level[i]; the
victim registers have many writers.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, FENCE, R, W


def make(n: int, fence: bool = False) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes.

    With fence=True, a full fence follows each write of victim, which is
    what the algorithm needs on TSO hardware such as x86.
    """

    def lock(i: int) -> Iterator:
        for lev in range(1, n):  # @line L1
            v = yield W(("level", i), lev)  # @line L2
            v = yield W(("victim", lev), i)  # @line L3
            if fence:
                v = yield FENCE
            if lev == 1:
                v = yield DOOR  # the doorway is L2 and L3 of level 1
            while True:  # @line L4
                vic = yield R(("victim", lev))  # @line L5
                if vic != i:
                    break
                blocked = False
                for k in range(n):
                    if k != i:
                        lk = yield R(("level", k))  # @line L6
                        if lk >= lev:
                            blocked = True
                            break
                if not blocked:  # @line L7
                    break

    def unlock(i: int) -> Iterator:
        v = yield W(("level", i), 0)  # @line L8

    mem: dict = {("level", i): 0 for i in range(n)}
    for lev in range(1, n):
        mem[("victim", lev)] = 0
    return lock, unlock, mem
