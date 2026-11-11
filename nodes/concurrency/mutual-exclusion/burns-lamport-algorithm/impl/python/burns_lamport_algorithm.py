# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burns-lamport-algorithm/. The authors are listed in prov/XQXAGT.jsonl.
"""The one-bit n-process mutual exclusion algorithm of Burns and Lamport.

This is the form in Lamport (1986), part II. The entry and exit sections
are generators that yield one shared memory step at a time to the
interleaving explorer (see explorer.py). Processes are numbered 0 to
n - 1, and process i owns one boolean register x[i], false at the start.
A process gives way to every lower process and waits for every higher
process.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, R, W


def make(n: int) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes."""

    def lock(i: int) -> Iterator:
        first = True
        while True:  # @line L1
            v = yield W(("x", i), True)  # @line L2
            if first:
                first = False
                v = yield DOOR  # marks the first write of x[i] = true in this passage
            blocked = -1
            for j in range(i):  # @line L3
                f = yield R(("x", j))
                if f:  # @line L4
                    blocked = j
                    break
            if blocked >= 0:
                v = yield W(("x", i), False)  # @line L5
                while True:
                    f = yield R(("x", blocked))  # @line L6
                    if not f:
                        break
                continue  # @line L7
            break
        for j in range(i + 1, n):  # @line L8
            while True:
                f = yield R(("x", j))  # @line L9
                if not f:
                    break

    def unlock(i: int) -> Iterator:
        v = yield W(("x", i), False)  # @line L10

    return lock, unlock, {("x", i): False for i in range(n)}
