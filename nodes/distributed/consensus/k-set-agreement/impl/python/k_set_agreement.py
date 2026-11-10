# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-set-agreement/. The authors are listed in prov/16H2HE.jsonl.

"""Two algorithms for k-set agreement with crash failures.

min_of_first: Chaudhuri's asynchronous algorithm for f < k. Each process sends
its input to all, waits for n - f values (its own included) and decides the
smallest. The decisions are among the f + 1 smallest inputs.

flood_min: the synchronous algorithm. Each process floods the smallest value
it has seen for floor(f / k) + 1 rounds and decides it.

Both come with a simulator in which crashed processes can stop in the middle
of a broadcast.
"""

from __future__ import annotations

import random
from typing import Optional


def min_of_first(values: list[int], heard: list[list[int]], f: int) -> list[Optional[int]]:
    """Decisions of the asynchronous algorithm, given for each process the senders it hears first.

    heard[p] lists senders in the order their values reach p (p's own value first).
    A process that hears fewer than n - f values does not decide (None).
    """
    n = len(values)
    out: list[Optional[int]] = []
    for p in range(n):
        got = heard[p][: n - f]  # @line L2
        out.append(min(values[q] for q in got) if len(got) == n - f else None)  # @line L3
    return out


def async_run(values: list[int], f: int, seed: int, crashes: dict[int, int]) -> list[Optional[int]]:
    """Message-passing run with a random scheduler.

    crashes maps a process to the number of its sends before it stops (at most f entries).
    A crashed process decides only if it got n - f values before its crash time.
    """
    n = len(values)
    rng = random.Random(seed)
    inflight: list[tuple[int, int]] = []  # (sender, receiver)
    heard: list[list[int]] = [[p] for p in range(n)]
    for p in range(n):  # @line L1
        targets = [q for q in range(n) if q != p]
        rng.shuffle(targets)
        k = crashes.get(p, len(targets))
        inflight += [(p, q) for q in targets[:k]]
    crash_after = {p: rng.randrange(0, n) for p in crashes}  # deliveries a crashed process handles
    rng.shuffle(inflight)
    for s, r in inflight:
        if r in crashes and len(heard[r]) > crash_after[r]:
            continue  # r has crashed and takes no more steps
        heard[r].append(s)
    return min_of_first(values, heard, f)


def flood_min(values: list[int], f: int, k: int, crashes: dict[int, tuple[int, frozenset]],
              rounds: Optional[int] = None) -> dict[int, int]:
    """Synchronous FloodMin. crashes[p] = (round r, receivers that get p's round r message).

    A process that crashes in round r sends nothing after round r and decides nothing.
    Returns the decisions of the processes that do not crash.
    """
    n = len(values)
    if rounds is None:
        rounds = f // k + 1
    x = list(values)
    alive = set(range(n))
    for r in range(1, rounds + 1):  # @line L4
        inbox: dict[int, list[int]] = {p: [] for p in range(n)}
        for p in sorted(alive):
            if p in crashes and crashes[p][0] == r:
                targets = crashes[p][1]
            else:
                targets = frozenset(range(n))
            for q in targets:
                inbox[q].append(x[p])
        alive -= {p for p in crashes if crashes[p][0] == r}
        for p in alive:
            x[p] = min([x[p]] + inbox[p])
    return {p: x[p] for p in alive}  # @line L5
