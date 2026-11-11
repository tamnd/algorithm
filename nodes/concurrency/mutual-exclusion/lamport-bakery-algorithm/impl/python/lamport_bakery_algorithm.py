# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-bakery-algorithm/. The authors are listed in prov/XJ2MAW.jsonl.
"""Lamport's bakery algorithm for n processes (Lamport 1974).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Process i
writes only choosing[i] and number[i]; all other accesses are reads.
Processes are numbered 0 to n - 1, and ties of tickets go to the smaller
number. ``make(n, choosing=False)`` builds the wrong variant without the
choosing flags, for the tests.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, FENCE, R, W


def make(n: int, choosing: bool = True, fence: bool = False) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n processes.

    With fence=True, a full fence follows L1 and L4, which is what the
    algorithm needs on TSO hardware such as x86.
    """

    def lock(i: int) -> Iterator:
        if choosing:
            v = yield W(("choosing", i), True)  # @line L1
        if fence:
            v = yield FENCE
        m = 0
        for j in range(n):
            if j != i:
                t = yield R(("number", j))  # @line L2
                m = max(m, t)
        mine = m + 1
        v = yield W(("number", i), mine)  # @line L3
        if choosing:
            v = yield W(("choosing", i), False)  # @line L4
        if fence:
            v = yield FENCE
        v = yield DOOR
        for j in range(n):  # @line L5
            if j == i:
                continue
            while choosing:
                c = yield R(("choosing", j))  # @line L6
                if not c:
                    break
            while True:
                t = yield R(("number", j))  # @line L7
                if t == 0 or (t, j) > (mine, i):
                    break

    def unlock(i: int) -> Iterator:
        v = yield W(("number", i), 0)  # @line L8

    mem: dict = {}
    for i in range(n):
        mem[("choosing", i)] = False
        mem[("number", i)] = 0
    return lock, unlock, mem


def safe_domain(mem: dict, top: int) -> dict:
    """Values that a read may return when it overlaps a write (safe registers), cut at top."""
    return {a: ((False, True) if a[0] == "choosing" else tuple(range(top + 1))) for a in mem}
