# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anderson-lock/. The authors are listed in prov/SV4NZH.jsonl.
"""Anderson's array-based queue lock, for the explorer in interleave.py.

This is the form given by Mellor-Crummey and Scott (1991): a slot array with
one entry for each process, and a counter next_slot. The process with place 0
mod n subtracts n from the counter, so the counter stays bounded.

Shared words: 'next_slot' and ('slot', i) for i in 0 .. n - 1. Slot 0 starts
as HAS_LOCK and the others as MUST_WAIT. Use init(n) to build the memory and
lines(n, padded) to put the slots on separate cache lines or on one line.
"""

from __future__ import annotations

from typing import Iterator

HAS_LOCK = True
MUST_WAIT = False


def init(n: int) -> dict:
    mem = {"next_slot": 0}
    for i in range(n):
        mem[("slot", i)] = HAS_LOCK if i == 0 else MUST_WAIT
    return mem


def lines(n: int, padded: bool) -> dict:
    """Cache lines: one line for each slot (padded) or one line for all slots (false sharing)."""
    return {("slot", i): (("line", i) if padded else "slots") for i in range(n)}


def home(n: int) -> dict:
    """DSM placement: slot i lives with process i, the counter with process 0."""
    h = {("slot", i): i for i in range(n)}
    h["next_slot"] = 0
    return h


def anderson_acquire(n: int) -> Iterator:
    """Take a place in the array and wait on its slot. Returns the place."""
    place = yield ("faa", "next_slot", 1)  # @line L1
    yield ("mark", "doorway")
    if place % n == 0:  # @line L2
        yield ("faa", "next_slot", -n)
    place = place % n  # @line L3
    while (yield ("read", ("slot", place))) == MUST_WAIT:  # @line L4
        pass
    yield ("write", ("slot", place), MUST_WAIT)  # @line L5
    return place


def anderson_release(n: int, place: int) -> Iterator:
    """Give the lock to the next place."""
    yield ("write", ("slot", (place + 1) % n), HAS_LOCK)  # @line L6


def client(n: int, rounds: int | None = 1):
    """A process factory: each process runs `rounds` passages (None means forever)."""
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            place = yield from anderson_acquire(n)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from anderson_release(n, place)
            del place
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
