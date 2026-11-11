# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semaphore/. The authors are listed in prov/AHWX4C.jsonl.
"""Semaphores for the explorer in interleave.py, and Morris's starvation-free mutex.

A semaphore s uses three words: ('val', s), ('blocked', s) and ('woken', s).

- P(s): if the value is positive, decrement it; otherwise join the blocked
  processes and wait until a V wakes this process.
- V(s): if some process is blocked, wake one of them; otherwise increment.

A weak semaphore wakes any blocked process (each choice is a branch for the
explorer). A strong semaphore keeps the blocked processes in FIFO order and
wakes the first. In both kinds, a process that calls V and then P cannot pass
a process that was blocked at the time of the V.

lock_cv_P() and lock_cv_V() build a counting semaphore from a mutex and a
condition variable, in the usual way.
"""

from __future__ import annotations

from typing import Iterator


def declare(mem: dict, s: str, value: int, strong: bool = False) -> dict:
    mem[("val", s)] = value
    mem[("blocked", s)] = () if strong else frozenset()
    mem[("woken", s)] = frozenset()
    return mem


def P(s: str) -> Iterator:
    v, b, w = ("val", s), ("blocked", s), ("woken", s)

    def _enter(mem, pid):
        if mem[v] > 0:
            return [(True, {v: mem[v] - 1})]
        blocked = mem[b] + (pid,) if isinstance(mem[b], tuple) else mem[b] | {pid}
        return [(False, {b: blocked})]

    if not (yield ("atomic", _enter, None)):
        # wait until a V names this process
        yield ("atomic", lambda mem, pid: [(None, {w: mem[w] - {pid}})], lambda mem, pid: pid in mem[w])


def V(s: str) -> Iterator:
    v, b, w = ("val", s), ("blocked", s), ("woken", s)

    def _signal(mem, pid):
        blocked = mem[b]
        if not blocked:
            return [(None, {v: mem[v] + 1})]
        if isinstance(blocked, tuple):  # strong: wake the first
            return [(None, {b: blocked[1:], w: mem[w] | {blocked[0]}})]
        return [(None, {b: blocked - {q}, w: mem[w] | {q}}) for q in sorted(blocked)]

    yield ("atomic", _signal, None)


def naive_mutex(strong: bool, rounds: int | None):
    """P(mutex); critical section; V(mutex)."""
    init = declare({}, "mutex", 1, strong)

    def make(pid):
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from P("mutex")
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from V("mutex")
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make, init


def morris(rounds: int | None):
    """Morris (1979): mutual exclusion without starvation from three weak semaphores."""
    init = {"room1": 0, "room2": 0}
    declare(init, "mutex", 1)
    declare(init, "t1", 1)
    declare(init, "t2", 0)

    def make(pid):
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from P("mutex")
            r = yield ("read", "room1")
            yield ("write", "room1", r + 1)
            yield from V("mutex")
            yield from P("t1")  # the first door
            r = yield ("read", "room2")
            yield ("write", "room2", r + 1)
            yield from P("mutex")
            r = yield ("read", "room1")
            yield ("write", "room1", r - 1)
            if r - 1 == 0:  # the last one in room 1 closes the first door, opens the second
                yield from V("mutex")
                yield from V("t2")
            else:
                yield from V("mutex")
                yield from V("t1")
            yield from P("t2")  # the second door
            r = yield ("read", "room2")
            yield ("write", "room2", r - 1)
            yield ("mark", "cs")
            yield ("mark", "exit")
            if r - 1 == 0:  # the last one out of room 2 opens the first door again
                yield from V("t1")
            else:
                yield from V("t2")
            del r
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make, init


# ---------------------------------------------- from a mutex and a condition variable
def lock_cv_init(k: int) -> dict:
    return {"m": False, "count": k, "waiting": frozenset()}


def _acquire_m():
    return ("atomic", lambda mem, pid: [(None, {"m": True})], lambda mem, pid: not mem["m"])


def lock_cv_P() -> Iterator:
    yield _acquire_m()
    while (yield ("read", "count")) == 0:
        # wait: release m and sleep in one step; after a signal, take m again
        yield ("atomic", lambda mem, pid: [(None, {"m": False, "waiting": mem["waiting"] | {pid}})], None)
        yield ("atomic", lambda mem, pid: [(None, {"m": True})], lambda mem, pid: pid not in mem["waiting"] and not mem["m"])
    c = yield ("read", "count")
    yield ("write", "count", c - 1)
    yield ("write", "m", False)


def lock_cv_V() -> Iterator:
    yield _acquire_m()
    c = yield ("read", "count")
    yield ("write", "count", c + 1)

    def _signal(mem, pid):  # wake one waiter, any of them
        if not mem["waiting"]:
            return [(None, {})]
        return [(None, {"waiting": mem["waiting"] - {q}}) for q in sorted(mem["waiting"])]

    yield ("atomic", _signal, None)
    yield ("write", "m", False)


def guarded(P_op, V_op, rounds: int | None = 1):
    """A process that uses a semaphore to guard a section that is marked 'cs'."""
    def make(pid):
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            yield from P_op()
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from V_op()
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make
