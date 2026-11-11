# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/last-writer-wins/. The authors are listed in prov/SZ23RT.jsonl.

"""The last-writer-wins rule for one replicated value.

Each write gets a stamp (timestamp, replica id). A replica keeps the write with
the largest stamp it has seen; the id breaks ties. Two clock sources:

- "physical": the replica's own clock, real time plus a fixed skew;
- "lamport": a Lamport clock, which is at least one more than any stamp the
  replica has seen, so a write made after seeing another write wins over it.
"""

import heapq
import random
from typing import Callable

Stamp = tuple[int, int]  # (timestamp, replica id)


def lww_merge(a: tuple[Stamp, object] | None, b: tuple[Stamp, object] | None) -> tuple[Stamp, object] | None:
    """Keep the (stamp, value) pair with the larger stamp."""
    if a is None:
        return b
    if b is None:
        return a
    return a if a[0] >= b[0] else b


class Replica:
    def __init__(self, rid: int, skew: int = 0, clock: str = "physical") -> None:
        self.rid = rid
        self.skew = skew
        self.clock = clock
        self.lamport = 0
        self.last = -10 ** 9
        self.cell: tuple[Stamp, object] | None = None

    def stamp(self, real_time: int) -> Stamp:
        if self.clock == "physical":
            # a replica never gives two of its writes the same timestamp
            self.last = max(real_time + self.skew, self.last + 1)
            return (self.last, self.rid)
        self.lamport += 1
        return (self.lamport, self.rid)

    def write(self, value: object, real_time: int) -> tuple[Stamp, object]:
        w = (self.stamp(real_time), value)
        self.cell = lww_merge(self.cell, w)
        return w

    def receive(self, w: tuple[Stamp, object]) -> None:
        self.lamport = max(self.lamport, w[0][0])
        self.cell = lww_merge(self.cell, w)

    def value(self) -> object:
        return None if self.cell is None else self.cell[1]


class Net:
    """Broadcast of each write to all other replicas, with seeded delays."""

    def __init__(self, replicas: list[Replica], seed: int, delay: tuple[int, int] = (1, 20)) -> None:
        self.replicas = replicas
        self.rng = random.Random(seed)
        self.delay = delay
        self.heap: list = []
        self.seq = 0
        self.now = 0

    def at(self, t: int, fn: Callable[[], None]) -> None:
        heapq.heappush(self.heap, (t, self.seq, fn))
        self.seq += 1

    def write(self, rid: int, value: object, t: int) -> None:
        def go() -> None:
            w = self.replicas[rid].write(value, self.now)
            for r in self.replicas:
                if r.rid != rid:
                    self.at(self.now + self.rng.randint(*self.delay), lambda r=r: r.receive(w))
        self.at(t, go)

    def run(self) -> None:
        while self.heap:
            t, _, fn = heapq.heappop(self.heap)
            self.now = t
            fn()


def concurrent_run() -> list[Replica]:
    """Replicas 0 and 1 write at the same real time; neither has seen the other."""
    reps = [Replica(i) for i in range(3)]
    net = Net(reps, 0)
    net.write(0, "cart = {book}", 10)
    net.write(1, "cart = {pen}", 10)
    net.run()
    return reps


def skew_run(clock: str) -> list[Replica]:
    """Replica 0's clock runs 100 ahead. It writes "a" at real time 10. Replica 1
    receives it at time 15 and writes "b" at real time 20, after it has seen "a"."""
    reps = [Replica(0, skew=100, clock=clock), Replica(1, clock=clock)]
    net = Net(reps, 0, delay=(5, 5))
    net.write(0, "a", 10)
    net.write(1, "b", 20)
    net.run()
    return reps
