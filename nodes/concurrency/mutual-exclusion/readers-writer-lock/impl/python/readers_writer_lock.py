# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/readers-writer-lock/. The authors are listed in prov/ZZ28W3.jsonl.
"""Three readers-writer locks with different policies, for the explorer in interleave.py.

Both readers and writers mark their critical section with 'cs'; the tests
check that a writer is never inside together with any other process.

- reader preference: the first solution of Courtois, Heymans and Parnas
  (1971), with a weak semaphore 'wrt' and a counter guarded by 'mutex'.
- writer preference: a monitor style lock. Each operation on the words
  'readers', 'writer' and 'waiting' is one atomic step, as it would be under
  the monitor lock; a blocked call is a guarded step.
- fair: a ticket lock shared by readers and writers. A reader passes the
  ticket on as soon as it has registered, so consecutive readers share the
  lock; a writer keeps the ticket until it leaves. Tickets count modulo
  WRAP, which is safe when WRAP exceeds the number of processes.
"""

from __future__ import annotations

from typing import Iterator

WRAP = 4


def P(s: str):
    """Semaphore wait as one guarded atomic step (a weak semaphore)."""
    return ("atomic", lambda mem, pid: [(None, {s: mem[s] - 1})], lambda mem, pid: mem[s] > 0)


def V(s: str):
    return ("atomic", lambda mem, pid: [(None, {s: mem[s] + 1})], None)


def _when(cond, change):
    return ("atomic", lambda mem, pid: [(None, change(mem))], lambda mem, pid: cond(mem))


def _process(acquire, release, rounds):
    def make(pid: int) -> Iterator:
        i = 0
        while rounds is None or i < rounds:
            yield ("mark", "try")
            t = yield from acquire()
            yield ("mark", "cs")
            yield ("mark", "exit")
            yield from release(t)
            del t
            yield ("mark", "rem")
            if rounds is not None:
                i += 1
    return make


# ------------------------------------------------ reader preference
RP_INIT = {"mutex": 1, "wrt": 1, "rc": 0}


def rp_read_acquire() -> Iterator:
    yield P("mutex")
    rc = yield ("faa", "rc", 1)
    if rc == 0:  # the first reader locks out the writers
        yield P("wrt")
    yield V("mutex")


def rp_read_release(_t=None) -> Iterator:
    yield P("mutex")
    rc = yield ("faa", "rc", -1)
    if rc == 1:  # the last reader lets the writers in
        yield V("wrt")
    yield V("mutex")


def rp_write_acquire() -> Iterator:
    yield P("wrt")


def rp_write_release(_t=None) -> Iterator:
    yield V("wrt")


# ------------------------------------------------ writer preference
WP_INIT = {"readers": 0, "writer": False, "waiting": 0}


def wp_read_acquire() -> Iterator:
    yield _when(lambda m: not m["writer"] and m["waiting"] == 0, lambda m: {"readers": m["readers"] + 1})


def wp_read_release(_t=None) -> Iterator:
    yield _when(lambda m: True, lambda m: {"readers": m["readers"] - 1})


def wp_write_acquire() -> Iterator:
    yield _when(lambda m: True, lambda m: {"waiting": m["waiting"] + 1})
    yield _when(lambda m: not m["writer"] and m["readers"] == 0, lambda m: {"writer": True, "waiting": m["waiting"] - 1})


def wp_write_release(_t=None) -> Iterator:
    yield _when(lambda m: True, lambda m: {"writer": False})


def wp_upgrade() -> Iterator:
    """A reader that holds the lock asks to become the writer: wait until it is the only reader."""
    yield _when(lambda m: not m["writer"] and m["readers"] == 1, lambda m: {"writer": True, "readers": 0})


# ------------------------------------------------ fair (ticket order)
FAIR_INIT = {"next": 0, "serving": 0, "readers": 0}


def _take_ticket():
    return ("atomic", lambda mem, pid: [(mem["next"], {"next": (mem["next"] + 1) % WRAP})], None)


def fair_read_acquire() -> Iterator:
    t = yield _take_ticket()
    yield ("mark", "doorway")
    while (yield ("read", "serving")) != t:
        pass
    yield ("faa", "readers", 1)
    yield ("write", "serving", (t + 1) % WRAP)  # the next in line may be a reader too


def fair_read_release(_t=None) -> Iterator:
    yield ("faa", "readers", -1)


def fair_write_acquire() -> Iterator:
    t = yield _take_ticket()
    yield ("mark", "doorway")
    while (yield ("read", "serving")) != t:
        pass
    while (yield ("read", "readers")) != 0:
        pass
    return t


def fair_write_release(t) -> Iterator:
    yield ("write", "serving", (t + 1) % WRAP)


POLICIES = {
    "reader preference": (RP_INIT, (rp_read_acquire, rp_read_release), (rp_write_acquire, rp_write_release)),
    "writer preference": (WP_INIT, (wp_read_acquire, wp_read_release), (wp_write_acquire, wp_write_release)),
    "fair": (FAIR_INIT, (fair_read_acquire, fair_read_release), (fair_write_acquire, fair_write_release)),
}


def system(policy: str, roles: str, rounds: int | None = 1):
    """Processes for a string of roles such as 'rrw' (two readers, one writer). Returns (procs, init)."""
    init, reader, writer = POLICIES[policy]
    procs = [_process(*(reader if r == "r" else writer), rounds) for r in roles]
    return procs, init
