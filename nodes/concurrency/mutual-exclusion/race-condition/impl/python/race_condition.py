# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/race-condition/. The authors are listed in prov/TVHXNT.jsonl.
"""Race conditions and data races, shown with the interleaving explorer.

Each process is a generator that yields one shared memory step at a time
(see explorer.py). A plain read is R(a) and a plain write is W(a, v). An
atomic load is ("faa", a, 0) and an atomic store is ("xchg", a, v): each is
one indivisible step that the explorer treats as an atomic operation.

``outcomes`` runs every interleaving and returns the set of final values.
``data_race`` looks for a reachable state in which two processes are about
to make conflicting accesses to the same address and one of them is plain.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import Explorer, R, W

PLAIN = ("r", "w")


def increment() -> Iterator:
    """counter++ as a plain read and a plain write: two separate steps."""
    v = yield R("c")
    v = yield W("c", v + 1)


def atomic_rw_increment() -> Iterator:
    """counter++ as an atomic load and an atomic store: no data race, still a race condition."""
    v = yield ("faa", "c", 0)
    x = yield ("xchg", "c", v + 1)


def faa_increment() -> Iterator:
    """counter++ as one fetch-and-add: correct."""
    v = yield ("faa", "c", 1)


def locked_increment() -> Iterator:
    """counter++ inside a critical section guarded by a test-and-set lock."""
    while True:
        held = yield ("tas", "lock")
        if held == 0:
            break
    v = yield R("c")
    x = yield W("c", v + 1)
    x = yield ("xchg", "lock", 0)


def withdraw(amount: int = 100) -> Iterator:
    """Check the balance, then take the money. Every access is atomic."""
    b = yield ("faa", "bal", 0)
    if b >= amount:
        x = yield ("xchg", "bal", b - amount)
        x = yield ("faa", "paid", amount)


def set_done() -> Iterator:
    """A plain write of the same value: a data race, but no race condition."""
    x = yield W("done", True)


def outcomes(makes: list[Callable], mem: dict, addrs: list) -> set:
    """The final values of addrs over all interleavings in which every process finishes."""
    ex = Explorer(makes, mem).explore()
    out = set()
    for s in ex.states:
        if all(r[1] is None for r in s[1]):
            out.add(tuple(ex.value(s, a) for a in addrs))
    return out


def _conflict(a: tuple, b: tuple) -> bool:
    if a[1] != b[1]:
        return False
    if a[0] not in PLAIN and b[0] not in PLAIN:
        return False
    return a[0] != "r" or b[0] != "r"


def data_race(makes: list[Callable], mem: dict) -> tuple | None:
    """A state and two processes whose next steps form a data race, or None.

    Two accesses conflict if they touch the same address and at least one
    writes. In a sequentially consistent run, two conflicting accesses that
    are both enabled in the same state are not ordered by happens-before,
    so the program has a data race if one of them is plain.
    """
    ex = Explorer(makes, mem).explore()
    for u, s in enumerate(ex.states):
        ops = [r[1] for r in s[1]]
        for p in range(len(ops)):
            for q in range(p + 1, len(ops)):
                if ops[p] is not None and ops[q] is not None and _conflict(ops[p], ops[q]):
                    return u, p, q, ops[p], ops[q]
    return None


def schedule(makes: list[Callable], mem: dict, order: list[int], addr: str) -> object:
    """The value at addr after the processes take steps in the given order."""
    ex = Explorer(makes, mem)
    return ex.value(ex.run(order), addr)
