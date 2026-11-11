# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ticket-lock/. The authors are listed in prov/B01V2J.jsonl.
"""The ticket lock with proportional backoff, for the explorer in interleave.py.

Shared words: 'next' (the next ticket to hand out) and 'serving' (the ticket
that may enter). Both start at 0. Each function is a generator that yields one
shared memory step at a time. With wrap = M the counters count modulo M, as a
fixed width hardware counter does; this is correct when M > n. The waiting
loop costs one remote reference in the CC model for each change of 'serving'
while the process waits, so at most n + 2 remote references per passage.
"""

from __future__ import annotations

from typing import Iterator

INIT = {"next": 0, "serving": 0}


def _fetch_and_increment_mod(m: int):
    def f(mem, pid):
        return [(mem["next"], {"next": (mem["next"] + 1) % m})]
    return f


def ticket_acquire(base: int = 0, wrap: int | None = None) -> Iterator:
    """Take a ticket, then wait until it is served. Returns the ticket."""
    if wrap is None:
        my = yield ("faa", "next", 1)  # @line L1
    else:
        my = yield ("atomic", _fetch_and_increment_mod(wrap), None)  # @line L1
    yield ("mark", "doorway")
    while True:  # @line L2
        s = yield ("read", "serving")  # @line L3
        if s == my:  # @line L4
            return my
        d = base * ((my - s) % wrap if wrap else my - s)  # @line L5
        del s  # the old value plays no part later; dropping it keeps the state space small
        while d > 0:
            yield ("mark", "backoff")
            d -= 1


def ticket_release(my: int, wrap: int | None = None) -> Iterator:
    """Serve the next ticket. Only the holder writes 'serving'."""
    yield ("write", "serving", (my + 1) % wrap if wrap else my + 1)  # @line L6


def client(base: int = 0, rounds: int | None = 1, wrap: int | None = None):
    """A process factory: each process runs `rounds` passages (None means forever)."""
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            my = yield from ticket_acquire(base, wrap)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from ticket_release(my, wrap)
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
