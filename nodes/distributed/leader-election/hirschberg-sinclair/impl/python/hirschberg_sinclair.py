# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-sinclair/. The authors are listed in prov/41MZQ5.jsonl.

"""Hirschberg-Sinclair leader election on a bidirectional ring.

Process i holds ids[i] and has two local ports, 0 and 1. In an oriented ring
port 0 leads to process i + 1; flip[i] = True swaps the two ports of process
i, which gives a non-oriented ring. The algorithm only uses "the other port"
and "the same port", so it works in both cases.

The run is a deterministic simulation. Schedule "sync" delivers all messages
in transit in lock-step rounds (one round per hop). The other schedules are
asynchronous: a seeded scheduler picks the next message, FIFO per channel for
"random", "first", "last", and in any order for "any".

Cost: at most 8 n (1 + ceil(lg n)) election messages and n announcement
messages. In the synchronous mode the leader knows after
2 (2^L - 1) + n rounds, L = ceil(lg n).
"""

import random
from collections import deque

SCHEDULES = ("sync", "random", "first", "last", "any")


class Process:
    """The local state of one process."""

    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.phase = 0  # @line L1
        self.status = "unknown"
        self.leader: int | None = None
        self.replies = 0

    def start(self) -> list[tuple[int, tuple]]:
        return [(p, ("out", self.uid, 1)) for p in (0, 1)]  # @line L2

    def receive(self, port: int, msg: tuple) -> list[tuple[int, tuple]]:
        other = 1 - port
        kind, v = msg[0], msg[1]
        if kind == "out":  # @line L3
            h = msg[2]
            if v > self.uid and h > 1:  # @line L4
                return [(other, ("out", v, h - 1))]
            if v > self.uid and h == 1:  # @line L5
                return [(port, ("in", v))]
            if v == self.uid and self.status == "unknown":  # @line L6
                self.status = "leader"
                self.leader = v
                return [(0, ("leader", v))]
            return []  # @line L7
        if kind == "in":  # @line L8
            if v != self.uid:  # @line L9
                return [(other, ("in", v))]
            self.replies += 1  # @line L10
            if self.replies == 2:  # @line L11
                self.phase += 1
                self.replies = 0
                return [(p, ("out", self.uid, 2**self.phase)) for p in (0, 1)]
            return []
        if v != self.uid:  # @line L12
            self.status = "non-leader"  # @line L13
            self.leader = v
            return [(other, ("leader", v))]
        return []


def hirschberg_sinclair(
    ids: list[int],
    schedule: str = "random",
    seed: int = 0,
    flip: list[bool] | None = None,
) -> dict:
    """Run the algorithm and return statuses, counts and the time of election."""
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

    chans: dict[tuple[int, int], deque] = {(i, d): deque() for i in range(n) for d in (1, -1)}
    count = {"out": 0, "in": 0, "leader": 0}
    elected_at: int | None = None
    now = 0

    def send(i: int, out: list[tuple[int, tuple]]) -> None:
        for p, m in out:
            chans[(i, direction(i, p))].append(m)
            count[m[0]] += 1

    def deliver(c: tuple[int, int], m: tuple) -> None:
        nonlocal elected_at
        i, d = c
        j = (i + d) % n
        q = port_towards(j, -d)
        before = procs[j].status
        send(j, procs[j].receive(q, m))
        if before != "leader" and procs[j].status == "leader":
            elected_at = now

    for i in range(n):
        send(i, procs[i].start())
    while any(chans.values()):
        now += 1
        if schedule == "sync":
            batch = [(c, chans[c].popleft()) for c in sorted(chans) for _ in range(len(chans[c]))]
            for c, m in batch:
                deliver(c, m)
            continue
        full = sorted(c for c in chans if chans[c])
        if schedule == "first":
            c, k = full[0], 0
        elif schedule == "last":
            c, k = full[-1], 0
        elif schedule == "any":
            c = rng.choice(full)
            k = rng.randrange(len(chans[c]))
        else:
            c, k = rng.choice(full), 0
        m = chans[c][k]
        del chans[c][k]
        deliver(c, m)
    return {
        "status": [p.status for p in procs],
        "known": [p.leader for p in procs],
        "leaders": [i for i in range(n) if procs[i].status == "leader"],
        "elect": count["out"] + count["in"],
        "announce": count["leader"],
        "phases": max(p.phase for p in procs),
        "elected_at": elected_at,
        "steps": now,
    }
