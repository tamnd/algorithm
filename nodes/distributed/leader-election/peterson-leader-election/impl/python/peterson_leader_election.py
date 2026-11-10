# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-leader-election/. The authors are listed in prov/M6ANZC.jsonl.

"""Peterson's leader election on an asynchronous unidirectional ring.

This is the form of Lynch, Section 15.1.3 (PetersonLeader). Process i holds
ids[i] and sends only to process (i + 1) mod n. Channels are FIFO, as the
algorithm needs. A seeded scheduler picks the next channel to deliver from:
"random", "first", "last", or "slow" (one process is served only when nothing
else can move). Schedule "sync" runs lock-step rounds of one hop each.

Each phase with at least two active processes sends exactly 2n messages, and
there are at most floor(lg n) such phases. The last phase sends n messages,
and the announcement n more.
"""

import random
from collections import deque

SCHEDULES = ("random", "first", "last", "slow", "sync")


class Process:
    """The local state of one process."""

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.mode = "active"  # @line L1
        self.tid = uid
        self.status = "unknown"
        self.waiting = "first"
        self.v1: int | None = None
        self.phase = 1
        self.leader: int | None = None

    def start(self) -> list[tuple[str, int]]:
        return [("tid", self.tid)]  # @line L2

    def receive(self, msg: tuple[str, int]) -> list[tuple[str, int]]:
        kind, v = msg
        if kind == "leader":  # @line L12
            if self.status == "leader":
                return []
            self.status = "non-leader"  # @line L13
            self.leader = v
            return [msg]
        if self.mode == "relay":  # @line L3
            return [msg]  # @line L4
        if self.waiting == "first":  # @line L5
            if v == self.tid:  # @line L6
                self.status = "leader"
                self.leader = self.uid
                return [("leader", self.uid)]
            self.v1 = v  # @line L7
            self.waiting = "second"
            return [("tid", v)]
        self.waiting = "first"  # @line L8
        if self.v1 > max(self.tid, v):  # @line L9
            self.tid = self.v1  # @line L10
            self.phase += 1
            return [("tid", self.tid)]
        self.mode = "relay"  # @line L11
        return []


def peterson(ids: list[int], schedule: str = "random", seed: int = 0) -> dict:
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
    count = {"tid": 0, "leader": 0}
    rounds = 0
    elected_round = None

    def send(i: int, msgs: list[tuple[str, int]]) -> None:
        for m in msgs:
            chans[i].append(m)
            count[m[0]] += 1

    def deliver(c: int) -> None:
        nonlocal elected_round
        m = chans[c].popleft()
        j = (c + 1) % n
        before = procs[j].status
        send(j, procs[j].receive(m))
        if before != "leader" and procs[j].status == "leader":
            elected_round = rounds

    for i in range(n):
        send(i, procs[i].start())
    while any(chans):
        rounds += 1
        full = [c for c in range(n) if chans[c]]
        if schedule == "sync":
            sizes = {c: len(chans[c]) for c in full}
            for c in full:
                for _ in range(sizes[c]):
                    deliver(c)
        elif schedule == "first":
            deliver(full[0])
        elif schedule == "last":
            deliver(full[-1])
        elif schedule == "slow":
            others = [c for c in full if c != slow]
            deliver(rng.choice(others) if others else slow)
        else:
            deliver(rng.choice(full))
    return {
        "status": [p.status for p in procs],
        "known": [p.leader for p in procs],
        "tid": [p.tid for p in procs],
        "leaders": [i for i in range(n) if procs[i].status == "leader"],
        "elect": count["tid"],
        "announce": count["leader"],
        "phases": max(p.phase for p in procs),
        "elected_round": elected_round if schedule == "sync" else None,
    }


def phases_with_two_or_more(ids: list[int]) -> int:
    """The number R of phases in which at least two processes are active.

    The survivors of a phase are the successors of the active processes whose
    temporary id is larger than the ids of both active neighbours.
    """
    act = list(ids)  # temporary ids of the active processes, in ring order
    r = 0
    while len(act) >= 2:
        k = len(act)
        act = [act[i - 1] for i in range(k) if act[i - 1] > max(act[i - 2], act[i])]
        r += 1
    return r
