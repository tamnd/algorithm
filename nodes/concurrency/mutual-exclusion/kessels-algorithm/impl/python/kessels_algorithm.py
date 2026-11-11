# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kessels-algorithm/. The authors are listed in prov/F0CXA1.jsonl.
"""Kessels' algorithm (Kessels 1982): two-process arbitration without a
register that both processes write, and the binary tree of such nodes for
n processes.

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). The tree is
stored as a heap: node 1 is the root and node x has the children 2x and
2x + 1. Process i starts at leaf i + size, where size is the smallest
power of two that is at least n, and it plays side s at node x when it
comes from child 2x + s. For n = 2 the tree is one node, and process i
plays side i: this is the two-process algorithm.

At node x, side s writes only b[x][s] and t[x][s]. The two t registers
together act as Peterson's turn: turn = t[x][0] xor t[x][1], and side s
waits while the other side has its b up and turn = s.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, FENCE, R, W


def path(i: int, size: int) -> list:
    """The (node, side) pairs from the leaf of process i up to the root."""
    out, leaf = [], i + size
    while leaf > 1:
        out.append((leaf // 2, leaf % 2))
        leaf //= 2
    return out


def make(n: int, fence: bool = False) -> tuple[Callable, Callable, dict]:
    """Return (lock, unlock, initial memory) for n >= 2 processes.

    With fence=True, a full fence follows each write in the entry section.
    On TSO hardware such as x86 the algorithm needs both: without the first
    one, the read of t at L3 can pass the write of b at L2.
    """
    size = 1
    while size < n:
        size *= 2

    def lock(i: int) -> Iterator:
        first = True
        for x, s in path(i, size):  # @line L1
            v = yield W(("b", x, s), True)  # @line L2
            if fence:
                v = yield FENCE
            o = yield R(("t", x, 1 - s))  # @line L3
            mine = o if s == 0 else 1 - o  # @line L4
            v = yield W(("t", x, s), mine)  # @line L5
            if fence:
                v = yield FENCE
            if first:
                first = False
                v = yield DOOR  # the doorway is L2 to L5 at the lowest node
            while True:  # @line L6
                f = yield R(("b", x, 1 - s))  # @line L7
                if not f:
                    break
                o = yield R(("t", x, 1 - s))  # @line L8
                if (s == 0 and mine != o) or (s == 1 and mine == o):  # @line L9
                    break

    def unlock(i: int) -> Iterator:
        for x, s in reversed(path(i, size)):  # @line L10
            v = yield W(("b", x, s), False)  # @line L11

    mem: dict = {}
    for x in range(1, size):
        for s in (0, 1):
            mem[("b", x, s)] = False
            mem[("t", x, s)] = 0
    return lock, unlock, mem
