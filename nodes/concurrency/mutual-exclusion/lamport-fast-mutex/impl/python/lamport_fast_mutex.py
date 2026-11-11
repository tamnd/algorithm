# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-fast-mutex/. The authors are listed in prov/HZ54V5.jsonl.
"""Lamport's fast mutual exclusion algorithm (1987).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Process i
uses the name i + 1 in the shared registers x and y, so that 0 can mean
"free" in y. Each process has a boolean register b[i]. Without contention
a process makes 5 writes and 2 reads in one passage.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import R, W


def make(n: int) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes."""

    def lock(i: int) -> Iterator:
        me = i + 1
        while True:  # @line L1
            v = yield W(("b", i), True)  # @line L2
            v = yield W("x", me)  # @line L3
            y = yield R("y")
            if y != 0:  # @line L4
                v = yield W(("b", i), False)  # @line L5
                while True:
                    y = yield R("y")  # @line L6
                    if y == 0:
                        break
                continue  # @line L7
            v = yield W("y", me)  # @line L8
            x = yield R("x")
            if x != me:  # @line L9
                v = yield W(("b", i), False)  # @line L10
                for j in range(n):
                    while True:
                        f = yield R(("b", j))  # @line L11
                        if not f:
                            break
                y = yield R("y")
                if y != me:  # @line L12
                    while True:
                        y = yield R("y")  # @line L13
                        if y == 0:
                            break
                    continue  # @line L14
            break  # @line L15

    def unlock(i: int) -> Iterator:
        v = yield W("y", 0)  # @line L16
        v = yield W(("b", i), False)  # @line L17

    mem = {("b", i): False for i in range(n)}
    mem["x"] = 0
    mem["y"] = 0
    return lock, unlock, mem
