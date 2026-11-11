# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-mutex-algorithm/. The authors are listed in prov/EYD54X.jsonl.
"""Dijkstra's n-process mutual exclusion algorithm (CACM, 1965).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). The names
follow Dijkstra's paper: b[i] is false while process i takes part (it is
true in the remainder section), c[i] is false while process i claims the
critical section, and k is the number of the process that has the turn.
Each test in the paper reads one register per step here: the test
"if b[k]" at L5 reads k and then b[k].
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import R, W


def make(n: int) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes."""

    def lock(i: int) -> Iterator:
        v = yield W(("b", i), False)  # @line L1
        while True:  # @line L2
            k = yield R("k")
            if k != i:  # @line L3
                v = yield W(("c", i), True)  # @line L4
                k = yield R("k")
                bk = yield R(("b", k))  # @line L5
                if bk:
                    v = yield W("k", i)  # @line L6
            else:  # @line L7
                v = yield W(("c", i), False)  # @line L8
                ok = True
                for j in range(n):  # @line L9
                    if j != i:
                        cj = yield R(("c", j))
                        if not cj:  # @line L10
                            ok = False
                            break
                if ok:
                    return  # @line L11

    def unlock(i: int) -> Iterator:
        v = yield W(("c", i), True)  # @line L12
        v = yield W(("b", i), True)  # @line L13

    mem: dict = {}
    for i in range(n):
        mem[("b", i)] = True
        mem[("c", i)] = True
    mem["k"] = 0
    return lock, unlock, mem
