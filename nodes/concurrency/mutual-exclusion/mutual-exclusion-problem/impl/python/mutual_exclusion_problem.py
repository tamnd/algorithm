# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-problem/. The authors are listed in prov/0XYD33.jsonl.
"""Checks for the requirements of the mutual exclusion problem, and three failed attempts.

A lock is a pair of generator functions lock(i) and unlock(i): the entry
section and the exit section of process i. Each yields one shared memory
step at a time (see explorer.py). ``check`` runs every interleaving of n
clients, each looping remainder, entry, critical, exit, and reports which
requirements hold.
"""
from __future__ import annotations

from typing import Callable, Iterator

from explorer import DOOR, PASSDOOR, START, Explorer, R, W, procs

TWO = {("flag", 0): False, ("flag", 1): False, "turn": 0, "busy": False}


def one_flag_lock(i: int) -> Iterator:
    """Wait until the lock is free, then take it: the read and the write can be split."""
    while True:
        b = yield R("busy")
        if not b:
            break
    v = yield W("busy", True)


def one_flag_unlock(i: int) -> Iterator:
    v = yield W("busy", False)


def alternation_lock(i: int) -> Iterator:
    """Strict alternation: wait for your turn."""
    while True:
        t = yield R("turn")
        if t == i:
            break


def alternation_unlock(i: int) -> Iterator:
    v = yield W("turn", 1 - i)


def two_flags_lock(i: int) -> Iterator:
    """Raise your flag, then wait until the other flag is down."""
    v = yield W(("flag", i), True)
    while True:
        f = yield R(("flag", 1 - i))
        if not f:
            break


def flag_unlock(i: int) -> Iterator:
    v = yield W(("flag", i), False)


def peterson_lock(i: int) -> Iterator:
    """Peterson's algorithm, a correct solution, for comparison."""
    j = 1 - i
    v = yield W(("flag", i), True)
    v = yield W("turn", j)
    v = yield DOOR
    while True:
        f = yield R(("flag", j))
        if not f:
            break
        t = yield R("turn")
        if t != j:
            break


def check(lock: Callable, unlock: Callable, mem: dict, n: int = 2, rounds: int = -1) -> dict:
    """Which requirements hold for n clients that each run ``rounds`` times (forever if < 0).

    The result has mutual_exclusion, deadlock_free, starvation_free, the
    bypass bound counted from the start of the entry section and from the
    end of the doorway (64 means unbounded), the number of states, and a
    bad schedule if mutual exclusion fails.
    """
    ex = Explorer(procs(lock, unlock, n, rounds), mem).explore()
    out = {"states": len(ex.states), "mutual_exclusion": ex.bad is None, "bad": ex.bad}
    if ex.bad is None:
        out["deadlock_free"] = ex.deadlock() is None
        out["starvation_free"] = all(ex.starvation(p) is None for p in range(n))
        out["bypass_from_start"] = max(ex.bypass(p, START) for p in range(n))
        out["bypass_from_door"] = max(ex.bypass(p, PASSDOOR) for p in range(n))
        out["fcfs"] = all(ex.fcfs(p) for p in range(n))
    return out


def stuck_run(lock: Callable, unlock: Callable, mem: dict, order: list[int]) -> tuple:
    """The state after the given schedule of two clients that loop forever."""
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    return ex, ex.run(order)
