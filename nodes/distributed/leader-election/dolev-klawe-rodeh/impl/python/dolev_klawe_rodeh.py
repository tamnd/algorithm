# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dolev-klawe-rodeh/. The authors are listed in prov/2S8HY8.jsonl.

"""Dolev-Klawe-Rodeh extrema finding on an asynchronous unidirectional ring.

Process i holds ids[i] and sends only to process (i + 1) mod n over a FIFO
channel. Messages are typed: <one, x> carries the value of an active process,
<two, y> carries the value of the active process before it, and <found, w>
tells every process the maximum w. The process whose identifier is w becomes
the leader. A seeded scheduler picks the next channel to deliver from.

Cost: exactly 2 n R + n messages of types one and two, where R is the number
of phases with two or more active processes, R <= floor(lg n), and n found
messages.
"""

import random
from collections import deque

SCHEDULES = ("random", "first", "last", "slow")


class Process:
    """The local state of one process."""

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.active = True  # @line L1
        self.max = uid
        self.left: int | None = None
        self.status = "unknown"
        self.finder = False
        self.known: int | None = None

    def start(self) -> list[tuple[str, int]]:
        return [("one", self.max)]  # @line L2

    def receive(self, msg: tuple[str, int]) -> list[tuple[str, int]]:
        kind, x = msg
        if kind == "one":  # @line L3
            if not self.active:  # @line L4
                return [msg]
            if x == self.max:  # @line L5
                self.finder = True
                self.active = False
                return [("found", x)]
            self.left = x  # @line L6
            return [("two", x)]
        if kind == "two":  # @line L7
            if not self.active:  # @line L8
                return [msg]
            if self.left > self.max and self.left > x:  # @line L9
                self.max = self.left
                return [("one", self.max)]
            self.active = False  # @line L10
            return []
        self.known = x  # @line L11
        self.status = "leader" if x == self.uid else "non-leader"  # @line L12
        if self.finder:  # @line L13
            return []
        return [msg]


def dolev_klawe_rodeh(ids: list[int], schedule: str = "random", seed: int = 0) -> dict:
    """Run the algorithm on the ring ids[0] -> ids[1] -> ... -> ids[0]."""
    n = len(ids)
    if len(set(ids)) != n:
        raise ValueError("identifiers must be distinct")
    if schedule not in SCHEDULES:
        raise ValueError("unknown schedule")
    rng = random.Random(seed)
    slow = rng.randrange(n)
    procs = [Process(u) for u in ids]
    chans: list[deque] = [deque() for _ in range(n)]
    count = {"one": 0, "two": 0, "found": 0}

    def send(i: int, msgs: list[tuple[str, int]]) -> None:
        for m in msgs:
            chans[i].append(m)
            count[m[0]] += 1

    for i in range(n):
        send(i, procs[i].start())
    while any(chans):
        full = [c for c in range(n) if chans[c]]
        if schedule == "first":
            c = full[0]
        elif schedule == "last":
            c = full[-1]
        elif schedule == "slow":
            others = [k for k in full if k != slow]
            c = rng.choice(others) if others else slow
        else:
            c = rng.choice(full)
        m = chans[c].popleft()
        j = (c + 1) % n
        send(j, procs[j].receive(m))
    return {
        "status": [p.status for p in procs],
        "known": [p.known for p in procs],
        "finder": [i for i in range(n) if procs[i].finder],
        "leaders": [i for i in range(n) if procs[i].status == "leader"],
        "one": count["one"],
        "two": count["two"],
        "found": count["found"],
    }


def franklin_rounds(ids: list[int]) -> int:
    """Rounds with two or more candidates when each round keeps local maxima.

    This is the number of rounds of Franklin's bidirectional algorithm on the
    same ring; Dolev-Klawe-Rodeh keeps the same values in each phase.
    """
    vals = list(ids)
    r = 0
    while len(vals) >= 2:
        k = len(vals)
        vals = [vals[j] for j in range(k) if vals[j] > max(vals[j - 1], vals[(j + 1) % k])]
        r += 1
    return r
