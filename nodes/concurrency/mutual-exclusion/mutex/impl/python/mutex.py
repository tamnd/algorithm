# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutex/. The authors are listed in prov/CKW457.jsonl.
"""A mutex: its sequential specification and futex-based implementations.

``MutexSpec`` is the abstract type: lock, unlock and trylock with an owner.
The generator functions are the three-state mutex of Drepper, "Futexes Are
Tricky" (mutex3, "Mutex, Take 3"), his first attempt (mutex, "Take 1"), and
a broken variant whose waiters never mark the mutex as contended, so that
unlock never wakes them. Each yields one atomic step at a time to the
interleaving explorer (see explorer.py). The futex calls are modelled as
in Linux: futex_wait(a, v) sleeps only if the word at a still holds v,
and futex_wake(a, 1) wakes at most one sleeper.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import Explorer, procs

FREE, LOCKED, CONTENDED = 0, 1, 2


class MutexSpec:
    """The sequential specification of a non-reentrant mutex with an owner."""

    def __init__(self) -> None:
        self.owner: int | None = None

    def trylock(self, p: int) -> bool:
        if self.owner is None:
            self.owner = p
            return True
        if self.owner == p:
            raise RuntimeError("relock by the owner: a non-reentrant mutex deadlocks here")
        return False

    def lock(self, p: int) -> bool:
        """True if p now holds the mutex; False means p must wait (the call blocks)."""
        return self.trylock(p)

    def unlock(self, p: int) -> None:
        if self.owner != p:
            raise RuntimeError("unlock by a process that does not hold the mutex")
        self.owner = None


def mutex3_lock(i: int) -> Iterator:
    """Drepper's mutex3: 0 free, 1 locked, 2 locked with possible waiters."""
    c = yield ("cas", "val", FREE, LOCKED)
    if c != FREE:
        if c != CONTENDED:
            c = yield ("xchg", "val", CONTENDED)
        while c != FREE:
            r = yield ("futex_wait", "val", CONTENDED)
            c = yield ("xchg", "val", CONTENDED)


def mutex3_unlock(i: int) -> Iterator:
    old = yield ("dec", "val")
    if old != LOCKED:
        v = yield ("w", "val", FREE)
        r = yield ("futex_wake", "val", 1)


def mutex3_trylock(i: int) -> Iterator:
    c = yield ("cas", "val", FREE, LOCKED)
    return c == FREE


def take1_lock(i: int) -> Iterator:
    """Drepper's first attempt: a counter of lockers; correct but slow."""
    while True:
        c = yield ("faa", "val", 1)
        if c == 0:
            break
        r = yield ("futex_wait", "val", c + 1)


def take1_unlock(i: int) -> Iterator:
    v = yield ("w", "val", 0)
    r = yield ("futex_wake", "val", 1)


def broken_lock(i: int) -> Iterator:
    """Waiters sleep on value 1 and never write 2, so unlock never knows about them."""
    c = yield ("cas", "val", FREE, LOCKED)
    while c != FREE:
        r = yield ("futex_wait", "val", LOCKED)
        c = yield ("cas", "val", FREE, LOCKED)


def lost_wakeups(ex: Explorer) -> list[int]:
    """States in which some process sleeps on the futex and every other process is idle.

    No process can wake the sleeper from such a state: it waits for a
    futex_wake that nobody will call.
    """
    out = []
    for u, s in enumerate(ex.states):
        recs = s[1]
        if any(r[6] is not None for r in recs) and all(r[6] is not None or r[2] in "RF" for r in recs):
            out.append(u)
    return out


def check(lock: Callable, unlock: Callable, n: int, rounds: int) -> dict:
    ex = Explorer(procs(lock, unlock, n, rounds), {"val": FREE}).explore()
    out = {"states": len(ex.states), "mutual_exclusion": ex.bad is None}
    if ex.bad is None:
        out["lost_wakeups"] = len(lost_wakeups(ex))
        out["starvation_free"] = all(ex.starvation(p) is None for p in range(n))
    return out


def solo_calls(lock: Callable, unlock: Callable) -> dict:
    """The atomic operations and futex calls of one lock and one unlock with no contention."""
    ex = Explorer(procs(lock, unlock, 1, 1), {"val": FREE})
    s, count = ex.s0, {"atomic": 0, "plain": 0, "futex": 0}
    while True:
        moves = ex.succ(s)
        if not moves:
            return count
        _, label, s, _, _ = moves[0]
        if label[0].startswith("futex"):
            count["futex"] += 1
        elif label[0] in ("r", "w"):
            count["plain"] += 1
        elif label[0] in ("cas", "xchg", "faa", "dec", "tas"):
            count["atomic"] += 1
