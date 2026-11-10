# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chang-roberts/. The authors are listed in prov/YMKAJR.jsonl.

"""Chang-Roberts leader election on an asynchronous unidirectional ring.

Process i holds the identifier ids[i] and sends only to process (i + 1) mod n.
All processes start at once. The run is a deterministic simulation: a seeded
scheduler picks the next message to deliver. The schedules "random", "first",
"last" and "slow" keep each channel FIFO; "any" and "lifo" do not, because the
algorithm does not need FIFO channels.

Cost: the elect messages are the sum, over all identifiers, of the number of
hops to the next larger identifier (n hops for the largest). That is at most
n (n + 1) / 2, and n H_n on average over random orders. The announcement adds
exactly n messages.
"""

import random
from collections import deque

SCHEDULES = ("random", "first", "last", "slow", "any", "lifo")


class Process:
    """The local state of one process."""

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.status = "unknown"  # @line L2
        self.leader: int | None = None
        self.done = False

    def start(self) -> list[tuple[str, int]]:
        return [("elect", self.uid)]  # @line L1

    def receive(self, msg: tuple[str, int]) -> list[tuple[str, int]]:
        kind, v = msg
        if kind == "elect":  # @line L3
            if v > self.uid:  # @line L4
                return [("elect", v)]
            if v == self.uid:  # @line L5
                self.status = "leader"  # @line L6
                self.leader = v
                return [("leader", v)]  # @line L7
            return []  # @line L8
        assert kind == "leader"  # @line L9
        if v != self.uid:  # @line L10
            self.status = "non-leader"
            self.leader = v
            self.done = True
            return [("leader", v)]  # @line L11
        self.done = True  # @line L12
        return []


def _pick(chans: list[deque], schedule: str, rng: random.Random, slow: int) -> tuple[int, int]:
    """Return (channel, position) of the next message to deliver."""
    full = [c for c in range(len(chans)) if chans[c]]
    if schedule == "first":
        return full[0], 0
    if schedule == "last":
        return full[-1], 0
    if schedule == "slow":
        others = [c for c in full if c != slow]
        return (rng.choice(others) if others else slow), 0
    if schedule == "any":
        c = rng.choice(full)
        return c, rng.randrange(len(chans[c]))
    if schedule == "lifo":
        c = max(full, key=lambda k: chans[k][-1][0])
        return c, len(chans[c]) - 1
    return rng.choice(full), 0


def chang_roberts(ids: list[int], schedule: str = "random", seed: int = 0) -> dict:
    """Run the algorithm on the ring ids[0] -> ids[1] -> ... -> ids[0].

    Returns the statuses, the leader id known at each process, the index of
    the leader, and the numbers of elect and leader messages.
    """
    n = len(ids)
    if len(set(ids)) != n:
        raise ValueError("identifiers must be distinct")
    if schedule not in SCHEDULES:
        raise ValueError("unknown schedule")
    rng = random.Random(seed)
    slow = rng.randrange(n)
    procs = [Process(u) for u in ids]
    chans: list[deque] = [deque() for _ in range(n)]
    count = {"elect": 0, "leader": 0}
    stamp = 0

    def send(i: int, msgs: list[tuple[str, int]]) -> None:
        nonlocal stamp
        for m in msgs:
            chans[i].append((stamp, m))
            stamp += 1
            count[m[0]] += 1

    for i in range(n):
        send(i, procs[i].start())
    while any(chans):
        c, k = _pick(chans, schedule, rng, slow)
        _, m = chans[c][k]
        del chans[c][k]
        j = (c + 1) % n
        send(j, procs[j].receive(m))
    leaders = [i for i in range(n) if procs[i].status == "leader"]
    return {
        "status": [p.status for p in procs],
        "known": [p.leader for p in procs],
        "done": [p.done for p in procs],
        "leaders": leaders,
        "elect": count["elect"],
        "announce": count["leader"],
    }


def hops_to_larger(ids: list[int]) -> list[int]:
    """For each process, the number of hops its identifier travels."""
    n = len(ids)
    out = []
    for i in range(n):
        d = 1
        while d < n and ids[(i + d) % n] < ids[i]:
            d += 1
        out.append(d)
    return out
