# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-buffer-problem/. The authors are listed in prov/3ZSHF1.jsonl.

"""Solutions of the bounded buffer (producer-consumer) problem, as procsim models.

The buffer is a circular array of `capacity` slots with an in index and an out
index. A put reads the in index, writes the slot and moves the index, in three
steps; a take does the same with the out index. A put into a full slot or a
take from an empty slot records an error, which the invariant reports.

  semaphores   empty = capacity, full = 0, mutex = 1 (Dijkstra):
               producer P(empty) P(mutex) put V(mutex) V(full),
               consumer P(full) P(mutex) take V(mutex) V(empty).
               swapped=True makes the producer do P(mutex) before P(empty),
               which can deadlock; mutex=False drops the mutex, which is
               safe only for one producer and one consumer.
  monitor      a mutex and the conditions notFull and notEmpty, with a while
               loop or (wrongly, for Mesa semantics) an if around each wait.
  sleep        count, sleep and wakeup without a lock (Tanenbaum's example),
               which can lose a wakeup and deadlock.

Precondition: capacity >= 1; the producers make as many items as the
consumers take. Cost: O(1) synchronization operations per item; the tests
search a few thousand states.
"""

from typing import Iterator

from procsim import Sim


def _read(var: str):
    def f(s: Sim):
        return s.v[var]
    return f


def _store(item):
    def f(s: Sim) -> None:
        i = s.v["in"]
        if s.v["slots"][i] is not None:
            s.v["error"] = s.v["error"] or f"{s.current} overwrites slot {i}"
        s.v["slots"][i] = item
    return f


def _load(s: Sim):
    j = s.v["out"]
    x = s.v["slots"][j]
    if x is None:
        s.v["error"] = s.v["error"] or f"{s.current} takes from empty slot {j}"
    s.v["slots"][j] = None
    s.v["got"].append(x)
    return x


def _move(var: str, old: int):
    def f(s: Sim) -> None:
        s.v[var] = (old + 1) % len(s.v["slots"])
    return f


def put(item) -> Iterator[tuple]:
    """Three steps: read the in index, write the slot, move the index."""
    i = yield ("atomic", _read("in"))
    yield ("atomic", _store(item))
    yield ("atomic", _move("in", i))


def take() -> Iterator[tuple]:
    j = yield ("atomic", _read("out"))
    x = yield ("atomic", _load)
    yield ("atomic", _move("out", j))
    return x


# The semaphore solution.
def sem_producer(sim: Sim, me: str, items: int, swapped: bool, mutex: bool) -> Iterator[tuple]:
    for k in range(items):
        if swapped:
            yield ("P", "mutex")
            yield ("P", "empty")
        else:
            yield ("P", "empty")
            if mutex:
                yield ("P", "mutex")
        yield from put((me, k))
        if mutex:
            yield ("V", "mutex")
        yield ("V", "full")


def sem_consumer(sim: Sim, me: str, items: int, swapped: bool, mutex: bool) -> Iterator[tuple]:
    for _ in range(items):
        yield ("P", "full")
        if mutex:
            yield ("P", "mutex")
        yield from take()
        if mutex:
            yield ("V", "mutex")
        yield ("V", "empty")


# The monitor solution.
def _count(s: Sim) -> int:
    return s.v["count"]


def _add(d: int):
    def f(s: Sim) -> None:
        s.v["count"] += d
    return f


def mon_producer(sim: Sim, me: str, items: int, loop: bool) -> Iterator[tuple]:
    cap = len(sim.v["slots"])
    for k in range(items):
        yield ("lock", "m")
        if loop:
            while (yield ("atomic", _count)) == cap:
                yield ("wait", "notFull")
        elif (yield ("atomic", _count)) == cap:
            yield ("wait", "notFull")
        yield from put((me, k))
        yield ("atomic", _add(1))
        yield ("signal", "notEmpty")
        yield ("unlock", "m")


def mon_consumer(sim: Sim, me: str, items: int, loop: bool) -> Iterator[tuple]:
    for _ in range(items):
        yield ("lock", "m")
        if loop:
            while (yield ("atomic", _count)) == 0:
                yield ("wait", "notEmpty")
        elif (yield ("atomic", _count)) == 0:
            yield ("wait", "notEmpty")
        yield from take()
        yield ("atomic", _add(-1))
        yield ("signal", "notFull")
        yield ("unlock", "m")


# Sleep and wakeup with an unprotected count (the lost wakeup).
def _bump(d: int):
    def f(s: Sim) -> int:
        s.v["count"] += d
        return s.v["count"]
    return f


def sleep_producer(sim: Sim, me: str, items: int) -> Iterator[tuple]:
    cap = len(sim.v["slots"])
    for k in range(items):
        if (yield ("atomic", _count)) == cap:
            yield ("sleep",)
        yield from put((me, k))
        if (yield ("atomic", _bump(1))) == 1:
            yield ("wakeup", "c0")


def sleep_consumer(sim: Sim, me: str, items: int) -> Iterator[tuple]:
    cap = len(sim.v["slots"])
    for _ in range(items):
        if (yield ("atomic", _count)) == 0:
            yield ("sleep",)
        yield from take()
        if (yield ("atomic", _bump(-1))) == cap - 1:
            yield ("wakeup", "p0")


def build(kind: str, capacity: int, producers: int = 1, consumers: int = 1, items: int = 2,
          swapped: bool = False, mutex: bool = True, loop: bool = True, mode: str = "mesa") -> Sim:
    """Producers p0, p1, ... make `items` items each; the consumers c0, c1, ... share
    the same total, split as evenly as possible."""
    s = Sim()
    s.v.update(slots=[None] * capacity, got=[], error=None, count=0)
    s.v["in"] = s.v["out"] = 0
    total = producers * items
    shares = [total // consumers + (1 if c < total % consumers else 0) for c in range(consumers)]
    if kind == "semaphores":
        s.semaphore("empty", capacity)
        s.semaphore("full", 0)
        s.semaphore("mutex", 1)
        for p in range(producers):
            s.spawn(f"p{p}", sem_producer, items, swapped, mutex)
        for c in range(consumers):
            s.spawn(f"c{c}", sem_consumer, shares[c], swapped, mutex)
    elif kind == "monitor":
        s.mutex("m")
        s.cond("notFull", "m", mode)
        s.cond("notEmpty", "m", mode)
        for p in range(producers):
            s.spawn(f"p{p}", mon_producer, items, loop)
        for c in range(consumers):
            s.spawn(f"c{c}", mon_consumer, shares[c], loop)
    elif kind == "sleep":
        assert producers == 1 and consumers == 1
        s.spawn("p0", sleep_producer, items)
        s.spawn("c0", sleep_consumer, items)
    else:
        raise ValueError(kind)
    return s


def no_error(s: Sim):
    """The safety property: no slot is overwritten and no empty slot is taken."""
    return s.v["error"]
