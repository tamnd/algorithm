# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/franklin/. The authors are listed in prov/PG80TJ.jsonl.

"""Franklin's leader election on an asynchronous bidirectional ring.

Process i holds ids[i] and has two local ports, 0 and 1. In an oriented ring
port 0 leads to process i + 1; flip[i] = True swaps the ports of process i.
The algorithm treats both ports alike, so it works on non-oriented rings.
Channels are FIFO. A seeded scheduler picks the next channel to deliver from.

Each round with two or more active processes sends exactly 2n messages; at
most floor(lg n) such rounds happen. The last round sends 2n messages and the
announcement n more.
"""

import random
from collections import deque

SCHEDULES = ("random", "first", "last", "slow")


class Process:
    """The local state of one process."""

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.active = True  # @line L1
        self.status = "unknown"
        self.leader: int | None = None
        self.round = 1
        self.buf: list[deque] = [deque(), deque()]

    def start(self) -> list[tuple[int, tuple]]:
        return [(p, ("val", self.uid)) for p in (0, 1)]  # @line L2

    def receive(self, port: int, msg: tuple) -> list[tuple[int, tuple]]:
        kind, v = msg
        if kind == "leader":  # @line L11
            if self.status == "leader":
                return []
            self.status = "non-leader"  # @line L12
            self.leader = v
            return [(1 - port, msg)]
        if not self.active:  # @line L3
            return [(1 - port, msg)]
        self.buf[port].append(v)  # @line L4
        if not (self.buf[0] and self.buf[1]):
            return []
        a, b = self.buf[0].popleft(), self.buf[1].popleft()  # @line L5
        if a == self.uid:  # @line L6
            self.status = "leader"
            self.leader = self.uid
            return [(0, ("leader", self.uid))]
        if self.uid > max(a, b):  # @line L7
            self.round += 1  # @line L8
            return [(p, ("val", self.uid)) for p in (0, 1)]
        self.active = False  # @line L9
        out = []
        for p in (0, 1):  # @line L10
            while self.buf[p]:
                out.append((1 - p, ("val", self.buf[p].popleft())))
        return out


def franklin(
    ids: list[int],
    schedule: str = "random",
    seed: int = 0,
    flip: list[bool] | None = None,
) -> dict:
    """Run the algorithm and return the statuses and the message counts."""
    n = len(ids)
    if len(set(ids)) != n:
        raise ValueError("identifiers must be distinct")
    if schedule not in SCHEDULES:
        raise ValueError("unknown schedule")
    flip = flip or [False] * n
    rng = random.Random(seed)
    procs = [Process(u) for u in ids]

    def direction(i: int, p: int) -> int:
        return 1 if (p == 0) != flip[i] else -1

    def port_towards(j: int, d: int) -> int:
        return 0 if direction(j, 0) == d else 1

    keys = [(i, d) for i in range(n) for d in (1, -1)]
    slow = rng.choice(keys)
    chans: dict[tuple[int, int], deque] = {k: deque() for k in keys}
    count = {"val": 0, "leader": 0}

    def send(i: int, out: list[tuple[int, tuple]]) -> None:
        for p, m in out:
            chans[(i, direction(i, p))].append(m)
            count[m[0]] += 1

    for i in range(n):
        send(i, procs[i].start())
    while any(chans.values()):
        full = [k for k in keys if chans[k]]
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
        i, d = c
        j = (i + d) % n
        send(j, procs[j].receive(port_towards(j, -d), m))
    return {
        "status": [p.status for p in procs],
        "known": [p.leader for p in procs],
        "leaders": [i for i in range(n) if procs[i].status == "leader"],
        "elect": count["val"],
        "announce": count["leader"],
        "rounds": max(p.round for p in procs),
    }


def rounds_with_two_or_more(ids: list[int]) -> int:
    """The number of rounds in which at least two processes are active."""
    vals = list(ids)
    r = 0
    while len(vals) >= 2:
        k = len(vals)
        vals = [vals[j] for j in range(k) if vals[j] > max(vals[j - 1], vals[(j + 1) % k])]
        r += 1
    return r
