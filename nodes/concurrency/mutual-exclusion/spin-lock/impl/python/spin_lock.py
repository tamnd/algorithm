# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spin-lock/. The authors are listed in prov/S4E1T8.jsonl.
"""Spin locks for the interleaving explorer in interleave.py.

The main lock is test-and-test-and-set with exponential backoff (TTAS-BO).
The module also has the plain test-and-set lock (TAS) and test-and-test-and-set
without backoff (TTAS), for comparison, and the spin then block rule.

Each lock word holds False (free) or True (held). Each function is a
generator that yields one shared memory step at a time (see interleave.py).
Cost: in the CC model a waiter of TAS makes one remote reference per step;
a waiter of TTAS makes one remote reference per change of the lock word.
"""

from __future__ import annotations

from typing import Iterator


def spin_lock_acquire(lock: str = "L", min_delay: int = 1, max_delay: int = 4) -> Iterator:
    """TTAS-BO acquire. The backoff length is a coin in [0, delay)."""
    delay = min_delay  # @line L1
    while True:  # @line L2
        while (yield ("read", lock)):  # @line L3
            pass
        if not (yield ("tas", lock)):  # @line L4
            return
        d = yield ("coin", delay)  # @line L5
        while d > 0:
            yield ("mark", "backoff")
            d -= 1
        delay = min(2 * delay, max_delay)  # @line L6


def spin_lock_release(lock: str = "L") -> Iterator:
    """Release: one write."""
    yield ("write", lock, False)  # @line L7


def tas_acquire(lock: str = "L") -> Iterator:
    """Plain test-and-set lock: apply test-and-set until it returns False."""
    while (yield ("tas", lock)):
        pass


def ttas_acquire(lock: str = "L") -> Iterator:
    """Test-and-test-and-set without backoff."""
    while True:
        while (yield ("read", lock)):
            pass
        if not (yield ("tas", lock)):
            return


def client(acquire, release=spin_lock_release, rounds: int | None = 1):
    """A process factory: each process runs `rounds` passages (None means forever)."""
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from acquire()
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from release()
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make


def spin_then_block(wait: float, switch: float, threshold: float) -> float:
    """Cost of a waiter that spins up to `threshold` time units, then blocks at cost `switch`.

    The lock becomes free after `wait` time units. Spinning costs one unit
    per time unit. The optimal offline cost is min(wait, switch).
    """
    if wait <= threshold:
        return wait
    return threshold + switch
