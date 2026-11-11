# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcs-lock/. The authors are listed in prov/YFEJH1.jsonl.
"""The MCS list-based queue lock, for the explorer in interleave.py.

Process p owns the queue node p, with the words ('next', p) and
('locked', p). The word 'tail' holds the process at the end of the queue,
or None. In the DSM model the node of p lives with p (see home(n)).
"""

from __future__ import annotations

from typing import Iterator

NIL = None


def init(n: int) -> dict:
    mem: dict = {"tail": NIL}
    for p in range(n):
        mem[("next", p)] = NIL
        mem[("locked", p)] = False
    return mem


def home(n: int) -> dict:
    h = {("next", p): p for p in range(n)}
    h.update({("locked", p): p for p in range(n)})
    h["tail"] = 0
    return h


def mcs_acquire(me: int) -> Iterator:
    """Join the queue with fetch-and-store, link behind the predecessor, spin on the own node."""
    yield ("write", ("next", me), NIL)  # @line L1
    pred = yield ("swap", "tail", me)  # @line L2
    yield ("mark", "doorway")
    if pred is not NIL:  # @line L3
        yield ("write", ("locked", me), True)  # @line L4
        yield ("write", ("next", pred), me)  # @line L5
        del pred
        while (yield ("read", ("locked", me))):  # @line L6
            pass


def mcs_release(me: int) -> Iterator:
    """Hand the lock to the successor, or empty the queue with compare-and-swap."""
    succ = yield ("read", ("next", me))  # @line L7
    if succ is NIL:
        if (yield ("cas", "tail", me, NIL)):  # @line L8
            return
        while succ is NIL:  # @line L9
            succ = yield ("read", ("next", me))
    yield ("write", ("locked", succ), False)  # @line L10


def client(rounds: int | None = 1):
    """A process factory: each process runs `rounds` passages (None means forever)."""
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from mcs_acquire(pid)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from mcs_release(pid)
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
