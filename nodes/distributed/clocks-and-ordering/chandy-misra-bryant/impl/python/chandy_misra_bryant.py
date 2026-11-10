# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-bryant/. The authors are listed in prov/ASK6PS.jsonl.

"""The Chandy, Misra and Bryant null message protocol on a closed network of
FIFO single server queues, and the sequential simulation it must match.

Station i has a fixed list of output stations. A job that arrives at i at time
a leaves at dep = max(a, last departure of i) + s, where the service time s is
a pure function of (job, visit) and s >= L >= 1. It then arrives at the next
station at time dep. So the departures of a station strictly increase, and
every link carries strictly increasing timestamps.

Arrivals at a station are taken in the order of the key (ts, source station,
job). Jobs that start at a station arrive at time 0 from source -1.
"""

import heapq
import random
from collections import deque
from dataclasses import dataclass, field

INF = float("inf")


def service(job: int, visit: int, lookahead: int) -> int:
    return lookahead + (job * 7 + visit * 13 + (job * visit) % 5) % 4


def route(outs: list[int], job: int, visit: int) -> int:
    return outs[(job * 31 + visit * 17 + job * visit) % len(outs)]


def sequential(outs: list[list[int]], start: list[int], lookahead: int, end: int) -> list[list[tuple]]:
    """start[job] = first station. Returns the processed arrivals of each station."""
    n = len(outs)
    last = [0] * n
    visits = [0] * len(start)
    done: list[list[tuple]] = [[] for _ in range(n)]
    q = [(0, -1, job, st) for job, st in enumerate(start)]
    heapq.heapify(q)
    while q:
        ts, src, job, st = heapq.heappop(q)
        done[st].append((ts, src, job))
        dep = max(ts, last[st]) + service(job, visits[job], lookahead)
        last[st] = dep
        nxt = route(outs[st], job, visits[job])
        visits[job] += 1
        if dep <= end:
            heapq.heappush(q, (dep, st, job, nxt))
    return done


@dataclass
class Station:
    ins: list[int]
    outs: list[int]
    queue: dict = field(default_factory=dict)  # source -> deque of (ts, src, job, visit)
    lb: dict = field(default_factory=dict)  # source -> earliest possible ts of the next message
    last: int = 0
    sent_null: dict = field(default_factory=dict)  # destination -> last null value sent
    done: list = field(default_factory=list)


class CMB:
    def __init__(self, outs: list[list[int]], start: list[int], lookahead: int, end: int, seed: int, nulls: bool = True) -> None:
        n = len(outs)
        ins = [[j for j in range(n) if i in outs[j]] for i in range(n)]
        self.st = [Station(ins[i], outs[i]) for i in range(n)]
        for s in self.st:
            for j in s.ins + [-1]:
                s.queue[j] = deque()
                s.lb[j] = 0
            s.lb[-1] = INF  # the start jobs are all known
        for job, i in enumerate(start):
            self.st[i].queue[-1].append((0, -1, job, 0))
        self.L, self.end, self.nulls = lookahead, end, nulls
        self.rng = random.Random(seed)
        self.transit: list = []  # (arrive step, seq, dst, src, msg)
        self.link_last: dict = {}
        self.seq = self.step = self.null_count = 0

    def post(self, src: int, dst: int, msg: tuple) -> None:
        t = self.step + self.rng.randint(1, 4)
        t = max(t, self.link_last.get((src, dst), t))  # FIFO links
        self.link_last[(src, dst)] = t
        self.transit.append((t, self.seq, dst, src, msg))
        self.seq += 1

    def deliver(self, dst: int, src: int, msg: tuple) -> None:
        s = self.st[dst]
        if msg[0] == "null":
            s.lb[src] = max(s.lb[src], msg[1])  # @line L6
        else:
            _, ts, job, visit = msg
            s.queue[src].append((ts, src, job, visit))
            s.lb[src] = ts + 1  # links carry strictly increasing timestamps

    def safe_head(self, i: int):
        """The queued arrival with the least key, if no link can still bring a smaller one."""
        s = self.st[i]
        heads = [q[0] for q in s.queue.values() if q]
        if not heads:
            return None
        h = min(heads)  # @line L1
        for j, q in s.queue.items():
            if not q and (s.lb[j], j) < (h[0], h[1]):  # @line L2
                return None
        return h

    def t_in(self, i: int) -> float:
        """A lower bound on the timestamp of every future arrival at station i."""
        s = self.st[i]
        return min((q[0][0] if q else s.lb[j]) for j, q in s.queue.items())

    def work(self, i: int) -> bool:
        s = self.st[i]
        moved = False
        while True:
            h = self.safe_head(i)
            if h is None or h[0] > self.end:
                break
            ts, src, job, visit = s.queue[h[1]].popleft()
            s.done.append((ts, src, job))  # @line L3
            dep = max(ts, s.last) + service(job, visit, self.L)
            s.last = dep
            if dep <= self.end:
                self.post(i, route(s.outs, job, visit), ("job", dep, job, visit + 1))  # @line L4
            moved = True
        if self.nulls:
            v = min(max(self.t_in(i), s.last) + self.L, self.end + 1)  # @line L5
            for k in s.outs:
                if v > s.sent_null.get(k, -1):
                    s.sent_null[k] = v
                    self.post(i, k, ("null", v))
                    self.null_count += 1
                    moved = True
        return moved

    def run(self, max_steps: int = 100000) -> str:
        """Return "done" when every arrival up to `end` is taken, else "deadlock"."""
        while self.step < max_steps:
            self.step += 1
            ready = sorted((m for m in self.transit if m[0] <= self.step), key=lambda m: m[1])
            self.transit = [m for m in self.transit if m[0] > self.step]
            for _, _, dst, src, msg in ready:
                self.deliver(dst, src, msg)
            moved = bool(ready)
            for i in self.rng.sample(range(len(self.st)), len(self.st)):
                moved |= self.work(i)
            if not moved and not self.transit:
                left = any(q and q[0][0] <= self.end for s in self.st for q in s.queue.values())
                return "deadlock" if left else "done"
        raise RuntimeError("step limit")

    def result(self) -> list[list[tuple]]:
        return [s.done for s in self.st]
