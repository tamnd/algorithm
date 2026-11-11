# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fischer-algorithm/. The authors are listed in prov/DRQ896.jsonl.
"""Fischer's timed mutual exclusion algorithm, and a small timed simulator.

Process i (names 1 to n) runs the algorithm one atomic step at a time.
Time is an integer. A process must take its next step in a time window
that its last step fixes:

    after the read of x = 0, the write x = i comes at most step_max later;
    after the write, the check of x comes at least delay later (and at
    most step_max after that);
    every other step comes at most step_max later, except that a process
    may stay in the remainder or the critical section for any time.

Several steps may happen at the same time, in any order. ``search``
tries all timed runs of n processes for small numbers, and ``replay``
checks one given timed run.
"""
from __future__ import annotations

from collections import deque

REM, AWAIT, WRITE, DELAY, CS, EXIT = "rem", "await", "write", "delay", "cs", "exit"


def step(i: int, pc: str, x: int) -> tuple[str, int]:
    """One atomic step of process i at the program counter pc; returns (next pc, new x)."""
    if pc == REM:
        return AWAIT, x
    if pc == AWAIT:
        if x == 0:  # @line L2
            return WRITE, x
        return AWAIT, x
    if pc == WRITE:
        return DELAY, i  # @line L3
    if pc == DELAY:
        if x == i:  # @line L5
            return CS, x
        return AWAIT, x  # @line L1
    if pc == CS:
        return EXIT, x
    return REM, 0  # @line L6


def window(pc: str, step_max: int, delay: int) -> tuple[int, int | None]:
    """The allowed gap before the next step of a process at pc; None means no bound."""
    if pc == DELAY:
        return delay, delay + step_max  # @line L4
    if pc in (REM, CS):
        return 0, None
    return 0, step_max


def search(n: int, step_max: int, delay: int, limit: int = 200000) -> tuple[int, list | None]:
    """Try all timed runs; return (number of states, a run with two processes in the CS or None).

    The time in the remainder and the critical section is cut at
    delay + step_max + 1, which keeps the search finite.
    A run is a list of (time, process index, program counter before the step).
    """
    top = delay + step_max + 1
    s0 = (0, tuple((REM, 0) for _ in range(n)))
    parent: dict = {s0: None}
    queue = deque([s0])
    while queue:
        s = queue.popleft()
        x, ps = s
        for p, (pc, t) in enumerate(ps):
            if t != 0:
                continue
            pc2, x2 = step(p + 1, pc, x)
            lo, hi = window(pc2, step_max, delay)
            for g in range(lo, (top if hi is None else hi) + 1):
                new = list(ps)
                new[p] = (pc2, g)
                m = min(tt for _, tt in new)
                s2 = (x2, tuple((a, b - m) for a, b in new))
                if s2 in parent:
                    continue
                parent[s2] = (s, p, pc, m)
                if len(parent) > limit:
                    raise RuntimeError("too many states")
                if sum(a == CS for a, _ in s2[1]) > 1:
                    return len(parent), _trace(parent, s2)
                queue.append(s2)
    return len(parent), None


def _trace(parent: dict, s: tuple) -> list:
    back = []
    while parent[s] is not None:
        s, p, pc, m = parent[s]
        back.append((p, pc, m))
    run, now = [], 0
    for p, pc, m in reversed(back):
        run.append((now, p, pc))
        now += m
    return run


def replay(n: int, step_max: int, delay: int, events: list) -> tuple:
    """Check a timed run given as (time, process index) pairs in time order.

    Each step must be in the window of its process, and no process may be
    late. Returns (x, program counters, windows relative to the last time).
    """
    x, pcs = 0, [REM] * n
    lo, hi = [0] * n, [None] * n
    now = 0
    for t, p in events:
        assert t >= now and lo[p] <= t, (t, p)
        assert all(h is None or t <= h for h in hi), (t, p)
        now = t
        pcs[p], x = step(p + 1, pcs[p], x)
        a, b = window(pcs[p], step_max, delay)
        lo[p], hi[p] = t + a, None if b is None else t + b
    rel = tuple((max(lo[q] - now, 0), None if hi[q] is None else hi[q] - now) for q in range(n))
    return x, tuple(pcs), rel
