# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transactional-lock-elision/. The authors are listed in prov/70FJV6.jsonl.
"""Transactional lock elision on the best-effort HTM model of htmsim.py.

`elide` is a generator for one simulated processor. It runs a critical
section `body` as a hardware transaction that reads the lock but does not
write it, so threads that touch different data run in parallel. After a
bounded number of failed tries, or an abort that a retry will not fix, it
takes the lock for real.

Two switches exist only to show what goes wrong without them:
  subscribe=False  the transaction does not read the lock (unsafe);
  wait=False       a retry does not wait for the lock to be free first
                   (safe, but it causes the lemming effect).

A body is a generator function `body(view)` that accesses shared memory
only by `view.load(a)` and `view.store(a, v)` and yields after each access.

Precondition: the lock word holds 0 (free) or 1 (taken); only `elide` and
`hold_lock` write it. Cost: at most `tries` hardware attempts and one run
under the lock, each of O(length of body) steps.
"""

from __future__ import annotations

from htmsim import EXPLICIT, RETRY, Abort, explicit_code

BUSY = 0xFF   # explicit abort code: the lock was held


class View:
    """The accesses a body may make; the HTM decides if they are transactional."""

    def __init__(self, htm, p: int) -> None:
        self.htm = htm
        self.p = p

    def load(self, a):
        return self.htm.load(self.p, a)

    def store(self, a, v) -> None:
        self.htm.store(self.p, a, v)


def elide(htm, p: int, lock, body, tries: int = 3, subscribe: bool = True,
          wait: bool = True, stats: dict | None = None):
    """Run body as if under lock, on processor p; return (result, path)."""
    view = View(htm, p)
    for _ in range(tries):  # @line L1
        if wait:
            yield (lambda: htm.mem[lock] == 0)  # @line L2
        else:
            yield
        htm.begin(p)  # @line L3
        try:
            if subscribe and htm.load(p, lock) != 0:  # @line L4
                htm.abort(p, BUSY)  # @line L4
            yield
            result = yield from body(view)  # @line L5
            htm.commit(p)  # @line L6
        except Abort as abort:  # @line L7
            if stats is not None:
                stats["aborts"] = stats.get("aborts", 0) + 1
            busy = bool(abort.status & EXPLICIT) and explicit_code(abort.status) == BUSY
            give_up = not (abort.status & RETRY) and not busy  # @line L8
            yield
            if give_up:
                break  # @line L8
            continue
        yield
        return result, "htm"  # @line L6
    while not htm.cas(p, lock, 0, 1):  # @line L9
        yield (lambda: htm.mem[lock] == 0)  # @line L9
    yield
    if stats is not None:
        stats["locked"] = stats.get("locked", 0) + 1
    result = yield from body(view)  # @line L10
    htm.store(p, lock, 0)  # @line L11
    yield
    return result, "lock"  # @line L11


def hold_lock(htm, p: int, lock, body):
    """A thread that always takes the lock, for example because its critical
    section makes a system call that would abort a transaction."""
    while not htm.cas(p, lock, 0, 1):
        yield (lambda: htm.mem[lock] == 0)
    yield
    result = yield from body(View(htm, p))
    htm.store(p, lock, 0)
    yield
    return result, "lock"
