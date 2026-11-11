# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stamp-benchmark-suite/. The authors are listed in prov/A9KZDJ.jsonl.
"""Three toy workloads in the spirit of STAMP, on the HTM model of htmsim.py.

THIS IS NOT STAMP. The real suite is a set of C programs with real data
structures and inputs. These generators only copy the shape of the
transactions of three of its applications, so that the effect of that
shape on a best-effort HTM can be seen in a few lines:

  kmeans_like     many short transactions that update one of K shared
                  cluster records; contention depends on K.
  vacation_like   sessions that reserve several items of a shared table
                  in one medium transaction, with a capacity check.
  labyrinth_like  each transaction claims a whole path of grid cells if
                  all are free; long paths exceed the write buffer.

Every transaction runs with transactional lock elision (`atomic`): a few
hardware tries that read the lock, then the lock. Statistics go into a
dict given by the caller.

A thread is a generator for the scheduler of sched.py. A body accesses
memory only by view.load and view.store and yields after each access.

Precondition: the memory holds the lock "L" = 0 and the addresses that
the workload uses. Cost: each transaction takes O(size of its body)
steps per try, and at most `tries` tries plus one run under the lock.
"""

from __future__ import annotations

from htmsim import CAPACITY, CONFLICT, EXPLICIT, RETRY, Abort, explicit_code

LOCK = "L"
BUSY = 0xFF


class View:
    def __init__(self, htm, p: int) -> None:
        self.htm = htm
        self.p = p

    def load(self, a):
        return self.htm.load(self.p, a)

    def store(self, a, v) -> None:
        self.htm.store(self.p, a, v)


def _count(stats: dict, key: str) -> None:
    stats[key] = stats.get(key, 0) + 1


def atomic(htm, p: int, body, stats: dict, tries: int = 3):
    """Run body with lock elision on LOCK; return its result."""
    view = View(htm, p)
    for _ in range(tries):
        yield (lambda: htm.mem[LOCK] == 0)
        htm.begin(p)
        try:
            if htm.load(p, LOCK) != 0:
                htm.abort(p, BUSY)
            yield
            result = yield from body(view)
            htm.commit(p)
        except Abort as abort:
            s = abort.status
            busy = bool(s & EXPLICIT) and explicit_code(s) == BUSY
            _count(stats, "capacity" if s & CAPACITY else "conflict" if s & CONFLICT
                   else "busy" if busy else "other")
            yield
            if not (s & RETRY) and not busy:
                break
            continue
        _count(stats, "htm")
        yield
        return result
    while not htm.cas(p, LOCK, 0, 1):
        yield (lambda: htm.mem[LOCK] == 0)
    yield
    result = yield from body(view)
    htm.store(p, LOCK, 0)
    _count(stats, "lock")
    yield
    return result


# -- kmeans_like ----------------------------------------------------------------

def kmeans_memory(k: int) -> dict:
    mem = {LOCK: 0}
    for c in range(k):
        mem[("n", c)] = 0
        mem[("sum", c)] = 0
    return mem


def kmeans_like(htm, p: int, points: list[int], k: int, stats: dict):
    """Add each point to cluster point % k (a stand-in for the nearest
    center): one short transaction of 2 reads and 2 writes per point."""
    for x in points:
        c = x % k

        def body(v, c=c, x=x):
            n = v.load(("n", c))
            yield
            s = v.load(("sum", c))
            yield
            v.store(("n", c), n + 1)
            yield
            v.store(("sum", c), s + x)
            yield

        yield from atomic(htm, p, body, stats)


# -- vacation_like --------------------------------------------------------------

def vacation_memory(items: int, capacity: int, threads: int) -> dict:
    mem = {LOCK: 0}
    for i in range(items):
        mem[("free", i)] = capacity
    for p in range(threads):
        mem[("booked", p)] = 0
    return mem


def vacation_like(htm, p: int, sessions: list[list[int]], stats: dict, results: list):
    """Each session reserves all its items or none (if one is sold out)."""
    for wanted in sessions:

        def body(v, wanted=wanted):
            free = []
            for i in wanted:
                free.append(v.load(("free", i)))
                yield
            if min(free) == 0:
                return False
            for i, f in zip(wanted, free):
                v.store(("free", i), f - 1)
                yield
            b = v.load(("booked", p))
            yield
            v.store(("booked", p), b + len(wanted))
            yield
            return True

        ok = yield from atomic(htm, p, body, stats)
        results.append((p, tuple(wanted), ok))


# -- labyrinth_like -------------------------------------------------------------

def labyrinth_memory(cells: int) -> dict:
    mem = {LOCK: 0}
    for i in range(cells):
        mem[("cell", i)] = 0
    return mem


def labyrinth_like(htm, p: int, paths: list[list[int]], stats: dict, results: list):
    """Claim each path (a list of cells) for p if every cell is free."""
    for path in paths:

        def body(v, path=path):
            for i in path:
                taken = v.load(("cell", i))
                yield
                if taken:
                    return False
            for i in path:
                v.store(("cell", i), p + 1)
                yield
            return True

        ok = yield from atomic(htm, p, body, stats)
        results.append((p, tuple(path), ok))
