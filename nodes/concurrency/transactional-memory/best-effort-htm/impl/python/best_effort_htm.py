# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-effort-htm/. The authors are listed in prov/W7DBTZ.jsonl.
"""Running an atomic block on best-effort HTM, with a fallback lock.

`atomic` is a generator for one simulated processor. It tries the block as
a hardware transaction up to `tries` times. Inside the transaction it reads
the fallback lock, so that a thread that takes the lock aborts it. After an
abort without the RETRY bit (capacity, interrupt, or an explicit abort other
than "lock busy"), or after the last try, it takes the lock with
compare-and-swap and runs the block without a transaction.

A block is a generator function `body(view)`: it reads and writes shared
memory only by `view.load(a)` and `view.store(a, v)`, yields after each
access, and returns its result. The same block runs on both paths.

Precondition: the lock address holds 0 (free) or 1 (taken), and no other
code writes it. Cost: at most `tries` hardware attempts and one run under
the lock; each step is one access in the model.
"""

from __future__ import annotations

from htmsim import EXPLICIT, RETRY, Abort, explicit_code

LOCK_BUSY = 0xFF   # the explicit abort code for "the fallback lock is taken"


class View:
    """The accesses a block may make; the HTM decides if they are transactional."""

    def __init__(self, htm, p: int) -> None:
        self.htm = htm
        self.p = p

    def load(self, a):
        return self.htm.load(self.p, a)

    def store(self, a, v) -> None:
        self.htm.store(self.p, a, v)


def atomic(htm, p: int, lock, body, tries: int = 3, log: list | None = None):
    """Run body atomically on processor p; return (result, path)."""
    view = View(htm, p)
    for _ in range(tries):
        yield (lambda: htm.mem[lock] == 0)      # wait while the lock is taken
        htm.begin(p)
        try:
            if htm.load(p, lock) != 0:          # the lock joins the read set
                htm.abort(p, LOCK_BUSY)
            yield
            result = yield from body(view)
            htm.commit(p)
        except Abort as abort:
            if log is not None:
                log.append(abort.status)
            busy = abort.status & EXPLICIT and explicit_code(abort.status) == LOCK_BUSY
            give_up = not (abort.status & RETRY) and not busy
            yield
            if give_up:
                break                           # retrying will not help
            continue
        yield
        return result, "htm"
    while not htm.cas(p, lock, 0, 1):           # the fallback path
        yield (lambda: htm.mem[lock] == 0)
    yield
    result = yield from body(view)
    htm.store(p, lock, 0)
    yield
    return result, "lock"
