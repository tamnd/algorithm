# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-virtual-time/. The authors are listed in prov/9E7NPE.jsonl.

"""Mattern's GVT algorithm with two cuts and message colours (JPDC 1993), on a
seeded simulator of an optimistic simulation.

Each logical process (LP) i holds a heap of unprocessed timestamps; its local
virtual time LVT_i is the least of them. An LP takes its least event at time t
and schedules one new event with timestamp t + k (k >= 1), on itself or as a
message to another LP. A message that arrives with a timestamp below LVT_i is
a straggler; it lowers LVT_i, as a rollback does. The rollback work itself is
not modelled, since only timestamps matter for GVT.

The true GVT at a moment is the least timestamp of all unprocessed events and
of all messages in transit. A controller computes an estimate in rounds. Round
r has colour r: a process that has passed the first cut of round r tags its
messages r, and messages with tag r - 1 are the white messages of the round.

  cut 1: each LP takes the colour r, sets tmin = inf, and reports how many
         white messages it sent to each LP.
  cut 2: LP j waits until it has received every white message sent to it, then
         reports min(LVT_j, tmin_j), where tmin_j is the least timestamp of the
         messages it sent with colour r.
  The estimate is the least report.
"""

import heapq
import random
from collections import defaultdict

INF = float("inf")


class System:
    def __init__(self, n: int, seed: int, end: int = 200, p_remote: float = 0.6) -> None:
        self.n, self.end, self.p_remote = n, end, p_remote
        self.rng = random.Random(seed)
        self.heap: list[list[int]] = [[] for _ in range(n)]
        for i in range(n):
            for _ in range(3):
                heapq.heappush(self.heap[i], self.rng.randrange(0, 5))
        self.colour = [0] * n
        self.sent = defaultdict(int)  # (colour, src, dst) -> count
        self.recd = defaultdict(int)  # (colour, dst) -> count
        self.tmin = [INF] * n
        self.wait: dict[int, int] = {}  # LP -> white messages it must still see, in cut 2
        self.q: list = []  # (real time, seq, kind, data)
        self.seq = 0
        self.in_transit: dict[int, int] = {}  # seq -> timestamp
        self.round = 0
        self.acks: dict[int, dict] = {}
        self.reports: dict[int, float] = {}
        self.estimates: list[tuple[float, float]] = []  # (real time, estimate)
        self.start_gvt: list[float] = []  # true GVT when each round starts
        self.now = 0.0

    def push(self, t: float, kind: str, data: tuple) -> int:
        heapq.heappush(self.q, (t, self.seq, kind, data))
        self.seq += 1
        return self.seq - 1

    def lvt(self, i: int) -> float:
        return self.heap[i][0] if self.heap[i] else INF

    def true_gvt(self) -> float:
        return min([self.lvt(i) for i in range(self.n)] + list(self.in_transit.values()), default=INF)

    # --- the simulation -------------------------------------------------------

    def step(self, i: int) -> None:
        if self.heap[i] and self.heap[i][0] <= self.end:
            t = heapq.heappop(self.heap[i])
            ts = t + self.rng.randint(1, 6)
            if self.rng.random() < self.p_remote:
                dst = self.rng.choice([j for j in range(self.n) if j != i])
                c = self.colour[i]
                self.sent[(c, i, dst)] += 1  # @line L2
                self.tmin[i] = min(self.tmin[i], ts)  # @line L3
                s = self.push(self.now + self.rng.uniform(0.1, 8.0), "msg", (dst, ts, c))
                self.in_transit[s] = ts
            else:
                heapq.heappush(self.heap[i], ts)
        self.push(self.now + self.rng.uniform(0.2, 1.5), "step", (i,))

    def on_msg(self, s: int, dst: int, ts: int, c: int) -> None:
        del self.in_transit[s]
        heapq.heappush(self.heap[dst], ts)
        self.recd[(c, dst)] += 1
        self.check_wait(dst)

    # --- the GVT algorithm ----------------------------------------------------

    def ctrl(self, dst: int, kind: str, data: tuple) -> None:
        self.push(self.now + self.rng.uniform(0.1, 3.0), kind, (dst,) + data)

    def start_round(self) -> None:
        self.round += 1
        self.acks, self.reports = {}, {}
        self.start_gvt.append(self.true_gvt())  # for the tests only
        for j in range(self.n):
            self.ctrl(j, "cut1", (self.round,))

    def on_cut1(self, j: int, r: int) -> None:
        self.colour[j] = r  # @line L1
        self.tmin[j] = INF
        counts = {k: self.sent[(r - 1, j, k)] for k in range(self.n)}
        self.ctrl(j, "ack1", (counts,))

    def on_ack1(self, j: int, counts: dict) -> None:
        self.acks[j] = counts
        if len(self.acks) == self.n:
            r = self.round
            for k in range(self.n):
                total = sum(self.acks[i][k] for i in range(self.n))
                self.ctrl(k, "cut2", (r, total))

    def on_cut2(self, k: int, r: int, total: int) -> None:
        self.wait[k] = total  # @line L4
        self.check_wait(k)

    def check_wait(self, k: int) -> None:
        if k in self.wait and self.recd[(self.round - 1, k)] >= self.wait[k]:
            del self.wait[k]
            self.ctrl(k, "rep", (min(self.lvt(k), self.tmin[k]),))  # @line L5

    def on_rep(self, k: int, value: float) -> None:
        self.reports[k] = value
        if len(self.reports) == self.n:
            est = min(self.reports.values())  # @line L6
            self.estimates.append((self.now, est))
            self.push(self.now + self.rng.uniform(1.0, 5.0), "go", ())

    def run(self, rounds: int, check: bool = True) -> list[tuple[float, float]]:
        for i in range(self.n):
            self.push(self.rng.uniform(0, 1), "step", (i,))
        self.push(2.0, "go", ())
        best = -INF  # the largest estimate so far
        while self.q and self.round <= rounds:
            self.now, s, kind, data = heapq.heappop(self.q)
            if kind == "step":
                self.step(*data)
            elif kind == "msg":
                self.on_msg(s, *data)
            elif kind == "go":
                if self.round == rounds:
                    break
                self.start_round()
            elif kind == "cut1":
                self.on_cut1(*data)
            elif kind == "ack1":
                self.on_ack1(*data)
            elif kind == "cut2":
                self.on_cut2(*data)
            elif kind == "rep":
                self.on_rep(*data)
            if self.estimates:
                best = max(best, self.estimates[-1][1])
            if check:
                assert self.true_gvt() >= best, (self.now, self.true_gvt(), best)
        return self.estimates
