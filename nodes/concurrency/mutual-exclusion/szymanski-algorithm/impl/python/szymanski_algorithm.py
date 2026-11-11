# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/szymanski-algorithm/. The authors are listed in prov/PMKEEH.jsonl.
"""Szymanski's n-process mutual exclusion algorithm with linear wait (1988).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Processes
are numbered 0 to n - 1. flag[i] takes the values 0 to 4:

    0  in the remainder section
    1  wants to enter
    2  in the waiting room, waits for the others to come in
    3  in the doorway of the waiting room
    4  door_in is closed; on the way to (or in) the critical section

Each "await for all j" reads one flag at a time, in increasing order of
j, and waits on each flag until the condition holds for it. Each "for
some j" test reads the flags one at a time in increasing order.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, R, W


def make(n: int) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes."""

    def lock(i: int) -> Iterator:
        v = yield W(("flag", i), 1)  # @line L1
        v = yield DOOR  # the doorway is the write flag[i] = 1
        for j in range(n):
            if j != i:
                while True:
                    f = yield R(("flag", j))  # @line L2
                    if f < 3:
                        break
        v = yield W(("flag", i), 3)  # @line L3
        seen = False
        for j in range(n):
            if j != i:
                f = yield R(("flag", j))
                if f == 1:  # @line L4
                    seen = True
                    break
        if seen:
            v = yield W(("flag", i), 2)  # @line L5
            found = False
            while not found:
                for j in range(n):
                    if j != i:
                        f = yield R(("flag", j))
                        if f == 4:  # @line L6
                            found = True
                            break
        v = yield W(("flag", i), 4)  # @line L7
        for j in range(i):
            while True:
                f = yield R(("flag", j))  # @line L8
                if f < 2:
                    break

    def unlock(i: int) -> Iterator:
        for j in range(i + 1, n):
            while True:
                f = yield R(("flag", j))  # @line L9
                if f < 2 or f == 4:
                    break
        v = yield W(("flag", i), 0)  # @line L10

    return lock, unlock, {("flag", i): 0 for i in range(n)}
