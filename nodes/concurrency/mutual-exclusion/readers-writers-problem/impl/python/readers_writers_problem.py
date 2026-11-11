# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/readers-writers-problem/. The authors are listed in prov/GNF11S.jsonl.

"""Three semaphore solutions of the readers-writers problem, as procsim models.

  policy 1  Courtois, Heymans and Parnas (1971), Problem 1, readers priority:
            readcount and the semaphores mutex and w. Writers can starve.
  policy 2  Courtois, Heymans and Parnas (1971), Problem 2, writers priority:
            readcount, writecount and the semaphores mutex 1, mutex 2,
            mutex 3, w and r. Readers can starve.
  policy 3  a fair solution with a turnstile (as in Downey, The Little Book
            of Semaphores): turnstile, roomEmpty, and a light switch for the
            readers. It is starvation free when the turnstile is a FIFO
            (strong) semaphore, and not when it is weak.

All semaphores start at 1. Each process runs its protocol `rounds` times; the
read and the write are each a start step and an end step.

Precondition: rounds >= 1. Cost: the exhaustive searches in the tests visit a
few thousand states.
"""

from typing import Iterator

from procsim import Sim


def _start(kind: str):
    def f(s: Sim) -> None:
        s.v[kind] += 1
        if kind == "reading":
            s.v["reads"] += 1
            for w in s.v["queued_writers"](s):
                s.v["bypass"][w] += 1
        else:
            s.v["writes"] += 1
            s.v["bypass"][s.current] = 0
    return f


def _end(kind: str):
    def f(s: Sim) -> None:
        s.v[kind] -= 1
    return f


def _add(var: str, d: int):
    def f(s: Sim) -> int:
        s.v[var] += d
        return s.v[var]
    return f


# Policy 1: readers priority (Courtois, Heymans and Parnas, Problem 1).
def reader_1(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "mutex")
        rc = yield ("atomic", _add("readcount", 1))
        if rc == 1:
            yield ("P", "w")
        yield ("V", "mutex")
        yield ("atomic", _start("reading"))
        yield ("atomic", _end("reading"))
        yield ("P", "mutex")
        rc = yield ("atomic", _add("readcount", -1))
        if rc == 0:
            yield ("V", "w")
        yield ("V", "mutex")


def writer_1(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "w")
        yield ("atomic", _start("writing"))
        yield ("atomic", _end("writing"))
        yield ("V", "w")


# Policy 2: writers priority (Courtois, Heymans and Parnas, Problem 2).
def reader_2(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "mutex3")
        yield ("P", "r")
        yield ("P", "mutex1")
        rc = yield ("atomic", _add("readcount", 1))
        if rc == 1:
            yield ("P", "w")
        yield ("V", "mutex1")
        yield ("V", "r")
        yield ("V", "mutex3")
        yield ("atomic", _start("reading"))
        yield ("atomic", _end("reading"))
        yield ("P", "mutex1")
        rc = yield ("atomic", _add("readcount", -1))
        if rc == 0:
            yield ("V", "w")
        yield ("V", "mutex1")


def writer_2(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "mutex2")
        wc = yield ("atomic", _add("writecount", 1))
        if wc == 1:
            yield ("P", "r")
        yield ("V", "mutex2")
        yield ("P", "w")
        yield ("atomic", _start("writing"))
        yield ("atomic", _end("writing"))
        yield ("V", "w")
        yield ("P", "mutex2")
        wc = yield ("atomic", _add("writecount", -1))
        if wc == 0:
            yield ("V", "r")
        yield ("V", "mutex2")


# Policy 3: a turnstile in front of everyone.
def reader_3(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "turnstile")
        yield ("V", "turnstile")
        yield ("P", "mutex")  # the light switch: the first reader in locks the room
        rc = yield ("atomic", _add("readcount", 1))
        if rc == 1:
            yield ("P", "roomEmpty")
        yield ("V", "mutex")
        yield ("atomic", _start("reading"))
        yield ("atomic", _end("reading"))
        yield ("P", "mutex")  # the last reader out unlocks it
        rc = yield ("atomic", _add("readcount", -1))
        if rc == 0:
            yield ("V", "roomEmpty")
        yield ("V", "mutex")


def writer_3(sim: Sim, me: str, rounds: int) -> Iterator[tuple]:
    for _ in range(rounds):
        yield ("P", "turnstile")
        yield ("P", "roomEmpty")
        yield ("atomic", _start("writing"))
        yield ("atomic", _end("writing"))
        yield ("V", "turnstile")
        yield ("V", "roomEmpty")


PROGRAMS = {1: (reader_1, writer_1), 2: (reader_2, writer_2), 3: (reader_3, writer_3)}
SEMAPHORES = {1: ("mutex", "w"), 2: ("mutex1", "mutex2", "mutex3", "w", "r"),
              3: ("turnstile", "roomEmpty", "mutex")}


def _queued_writers(s: Sim) -> list[str]:
    """Writers of policy 3 that hold the turnstile or wait in its FIFO queue."""
    out = []
    for name, p in s.procs.items():
        if name.startswith("w") and p.op in (("_granted", "turnstile"), ("P", "roomEmpty"),
                                             ("_granted", "roomEmpty")):
            out.append(name)
    return out


def build(policy: int, readers: int, writers: int, rounds: int = 1,
          writer_rounds: int = 0, fifo: bool = False) -> Sim:
    """Readers r0, r1, ... and writers w0, w1, ...; writer_rounds = 0 means rounds."""
    reader, writer = PROGRAMS[policy]
    s = Sim()
    for name in ("readcount", "writecount", "reading", "writing", "reads", "writes"):
        s.v[name] = 0
    s.v["bypass"] = {f"w{j}": 0 for j in range(writers)}
    s.v["queued_writers"] = _queued_writers
    for name in SEMAPHORES[policy]:
        s.semaphore(name, 1, fifo=fifo)
    for i in range(readers):
        s.spawn(f"r{i}", reader, rounds)
    for j in range(writers):
        s.spawn(f"w{j}", writer, writer_rounds or rounds)
    return s


def exclusion(s: Sim):
    """The safety property: a writer is alone."""
    if s.v["writing"] > 1 or (s.v["writing"] == 1 and s.v["reading"] > 0):
        return f"{s.v['writing']} writing and {s.v['reading']} reading"
    return None
