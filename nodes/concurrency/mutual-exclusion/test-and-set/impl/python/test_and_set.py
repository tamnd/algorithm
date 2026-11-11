# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/test-and-set/. The authors are listed in prov/JZT9EK.jsonl.
"""Two uses of the test-and-set bit, for the explorer in interleave.py.

1. Wait-free consensus for two processes: each process announces its
   input in its own register, then applies test-and-set to the word 'T'.
   The winner decides its own input; the loser decides the input of the
   other process.
2. The test-and-set lock: apply test-and-set to 'L' until it returns False.
"""

from __future__ import annotations

from typing import Iterator

CONSENSUS_INIT = {"T": False, ("reg", 0): None, ("reg", 1): None}
LOCK_INIT = {"L": False}


def consensus(inputs: tuple):
    """Process p proposes inputs[p] and records its decision as an operation in the history."""
    inputs = tuple(inputs)

    def make(p: int) -> Iterator:
        v = inputs[p]
        yield ("mark", "inv", ("propose", v))
        yield ("write", ("reg", p), v)  # announce
        lost = yield ("tas", "T")
        if not lost:
            d = v  # the winner decides its own input
        else:
            d = yield ("read", ("reg", 1 - p))  # the loser decides the winner's input
        yield ("mark", "res", d)
    return make


def decisions(history) -> dict:
    return {pid: res for pid, _, _, res, _ in history}


def tas_lock_acquire() -> Iterator:
    while (yield ("tas", "L")):
        pass


def tas_lock_release() -> Iterator:
    yield ("write", "L", False)


def lock_client(rounds: int | None = 1):
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from tas_lock_acquire()
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from tas_lock_release()
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
