# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-lock/. The authors are listed in prov/RBPQNE.jsonl.
"""The tournament lock: a binary tree of two-process Peterson locks.

This is the tree of Peterson and Fischer (1977) with Peterson's 1981
two-process algorithm at each node, as textbooks present it. Peterson and
Fischer used a two-process algorithm of their own at the nodes.

The entry and exit sections are generators that yield one shared memory
step at a time to the interleaving explorer (see explorer.py). The tree is
stored as a heap: node 1 is the root, node x has children 2x and 2x + 1,
and process i starts at leaf i + size, where size is the smallest power of
two that is at least n. A process that comes to node x from child 2x + s
plays side s of the Peterson lock at x.
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

    With fence=True, a full fence follows each write of turn, which is what
    the algorithm needs on TSO hardware such as x86.
    """
    size = 1
    while size < n:
        size *= 2

    def lock(i: int) -> Iterator:
        first = True
        for x, s in path(i, size):  # @line L1
            v = yield W(("flag", x, s), True)  # @line L2
            v = yield W(("turn", x), 1 - s)  # @line L3
            if fence:
                v = yield FENCE
            if first:
                first = False
                v = yield DOOR  # the doorway is L2 and L3 at the lowest node
            while True:  # @line L4
                f = yield R(("flag", x, 1 - s))  # @line L5
                if not f:
                    break
                t = yield R(("turn", x))  # @line L6
                if t != 1 - s:
                    break

    def unlock(i: int) -> Iterator:
        for x, s in reversed(path(i, size)):  # @line L7
            v = yield W(("flag", x, s), False)  # @line L8

    mem: dict = {}
    for x in range(1, size):
        mem[("flag", x, 0)] = False
        mem[("flag", x, 1)] = False
        mem[("turn", x)] = 0
    return lock, unlock, mem
