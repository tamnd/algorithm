# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clh-lock/. The authors are listed in prov/RHBQNE.jsonl.
"""The CLH queue lock, for the explorer in interleave.py.

There are n + 1 queue nodes. Node i has one word ('locked', i). Process p
starts with node p, and node n is the dummy node that 'tail' points to at
the start; it holds False, so the first process enters at once. On release a
process gives its node to its successor and takes the node of its
predecessor for the next passage. In the DSM model node i lives with process
i, and the dummy node with process 0 (see home(n)).
"""

from __future__ import annotations

from typing import Iterator


def init(n: int) -> dict:
    mem: dict = {"tail": n}
    for i in range(n + 1):
        mem[("locked", i)] = False
    return mem


def home(n: int) -> dict:
    h = {("locked", i): i for i in range(n)}
    h[("locked", n)] = 0
    h["tail"] = 0
    return h


def clh_acquire(my: int) -> Iterator:
    """Mark the own node busy, swap it into the tail, spin on the predecessor node. Returns pred."""
    yield ("write", ("locked", my), True)  # @line L1
    pred = yield ("swap", "tail", my)  # @line L2
    yield ("mark", "doorway")
    while (yield ("read", ("locked", pred))):  # @line L3
        pass
    return pred


def clh_release(my: int) -> Iterator:
    """Free the own node; the successor spins on it."""
    yield ("write", ("locked", my), False)  # @line L4


def client(rounds: int | None = 1):
    """A process factory: each process runs `rounds` passages (None means forever)."""
    def make(pid: int) -> Iterator:
        my = pid
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            pred = yield from clh_acquire(my)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from clh_release(my)
            my = pred  # @line L5
            del pred
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
