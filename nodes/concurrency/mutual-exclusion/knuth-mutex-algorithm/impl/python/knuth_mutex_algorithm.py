# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-mutex-algorithm/. The authors are listed in prov/YTPF2R.jsonl.
"""Knuth's n-process mutual exclusion algorithm (CACM, 1966).

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). Processes
are numbered 0 to n - 1 here; Knuth numbers them 1 to N. control[i] is 0
(idle), 1 (waiting) or 2 (claiming); k is the process with the highest
priority. The scan at L3 goes from k down to i, cyclically:
k, k - 1, ..., 0, n - 1, ..., i + 1, and stops at i.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, R, W


def make(n: int) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes."""

    def lock(i: int) -> Iterator:
        first = True
        while True:  # @line L1
            v = yield W(("control", i), 1)  # @line L2
            if first:
                first = False
                v = yield DOOR  # the doorway is the first write control[i] = 1
            while True:
                j = yield R("k")  # @line L3
                blocked = False
                while j != i:
                    c = yield R(("control", j))  # @line L4
                    if c != 0:
                        blocked = True  # @line L5
                        break
                    j = (j - 1) % n
                if not blocked:
                    break
            v = yield W(("control", i), 2)  # @line L6
            ok = True
            for j in range(n - 1, -1, -1):  # @line L7
                if j != i:
                    c = yield R(("control", j))
                    if c == 2:  # @line L8
                        ok = False
                        break
            if ok:
                break  # @line L9
        v = yield W("k", i)  # @line L10

    def unlock(i: int) -> Iterator:
        v = yield W("k", (i - 1) % n)  # @line L11
        v = yield W(("control", i), 0)  # @line L12

    mem: dict = {("control", i): 0 for i in range(n)}
    mem["k"] = 0
    return lock, unlock, mem
