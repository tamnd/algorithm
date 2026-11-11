# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/livelock/. The authors are listed in prov/92X6MQ.jsonl.
"""A polite entry protocol that livelocks, and its randomized fix.

Two processes share the flags ('flag', 0) and ('flag', 1). A process raises
its flag and looks at the flag of the other process. If that flag is down it
enters. If it is up, the process is polite: it lowers its own flag and tries
again. Two processes that move in lock step repeat this forever.

The fix: after it lowers its flag, the process flips a coin and waits 0 or 1
units of UNIT local steps before it tries again. The mark 'retreat' counts
the collisions.
"""

from __future__ import annotations

from typing import Iterator

INIT = {("flag", 0): False, ("flag", 1): False}
UNIT = 3  # one attempt takes three steps: raise, look, lower


def enter(me: int, randomized: bool) -> Iterator:
    other = 1 - me
    while True:
        yield ("write", ("flag", me), True)
        if not (yield ("read", ("flag", other))):
            return
        yield ("write", ("flag", me), False)
        yield ("mark", "retreat")
        if randomized:
            d = (yield ("coin", 2)) * UNIT
            while d > 0:
                yield ("mark", "wait")
                d -= 1


def leave(me: int) -> Iterator:
    yield ("write", ("flag", me), False)


def client(randomized: bool, rounds: int | None = 1):
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from enter(pid, randomized)
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from leave(pid)
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make


def collisions_before_first_entry(log: list) -> int:
    """The number of retreats of process 0 before the first entry of any process."""
    k = 0
    for entry in log:
        if entry[1] == "cs":
            return k
        if entry[0] == 0 and entry[1] == "retreat":
            k += 1
    return k
