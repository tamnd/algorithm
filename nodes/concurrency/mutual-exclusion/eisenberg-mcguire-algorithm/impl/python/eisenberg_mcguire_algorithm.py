# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisenberg-mcguire-algorithm/. The authors are listed in prov/Y50GY4.jsonl.
"""The Eisenberg-McGuire n-process mutual exclusion algorithm (CACM, 1972).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Processes
are numbered 0 to n - 1. flag[i] is IDLE, WAITING or ACTIVE; turn is the
process with the highest priority. All arithmetic on process numbers is
mod n. The final test of a round reads turn once into a local t and then
reads flag[t]; the paper writes this test as one expression.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, FENCE, R, W

IDLE, WAITING, ACTIVE = 0, 1, 2


def make(n: int, fence: bool = False) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes.

    With fence=True, a full fence follows each write of flag[i] in the
    entry section, for machines with store buffers (TSO).
    """

    def lock(i: int) -> Iterator:
        first = True
        while True:  # @line L1
            v = yield W(("flag", i), WAITING)  # @line L2
            if first:
                first = False
                v = yield DOOR  # the doorway is the first write flag[i] = WAITING
            if fence:
                v = yield FENCE
            j = yield R("turn")  # @line L3
            while j != i:  # @line L4
                f = yield R(("flag", j))  # @line L5
                if f != IDLE:
                    j = yield R("turn")
                else:
                    j = (j + 1) % n
            v = yield W(("flag", i), ACTIVE)  # @line L6
            if fence:
                v = yield FENCE
            clash = False
            for j in range(n):  # @line L7
                if j != i:
                    f = yield R(("flag", j))
                    if f == ACTIVE:  # @line L8
                        clash = True
                        break
            if clash:
                continue
            t = yield R("turn")  # @line L9
            if t == i:
                break
            ft = yield R(("flag", t))
            if ft == IDLE:  # @line L10
                break
        v = yield W("turn", i)  # @line L11

    def unlock(i: int) -> Iterator:
        t = yield R("turn")
        j = (t + 1) % n  # @line L12
        while True:
            f = yield R(("flag", j))  # @line L13
            if f != IDLE:
                break
            j = (j + 1) % n
        v = yield W("turn", j)  # @line L14
        v = yield W(("flag", i), IDLE)  # @line L15

    mem: dict = {("flag", i): IDLE for i in range(n)}
    mem["turn"] = 0
    return lock, unlock, mem
