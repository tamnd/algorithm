# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-lamport-snapshot/. The authors are listed in prov/32HBY1.jsonl.

"""The Chandy and Lamport snapshot algorithm on a seeded discrete event
simulator of a bank: n processes hold money and send transfers to each other.

Channels join every ordered pair of processes. With fifo=True each channel
delivers in send order; with fifo=False a later message may overtake an
earlier one, and the algorithm can then record an inconsistent state.
"""

import heapq
import random
from dataclasses import dataclass, field
from typing import Callable

DelayFn = Callable[[int, int, tuple, random.Random], float]


def uniform_delay(lo: float, hi: float) -> DelayFn:
    return lambda src, dst, msg, rng: rng.uniform(lo, hi)


@dataclass
class Proc:
    balance: int
    log: list = field(default_factory=list)  # ("send", mid, dst) or ("recv", mid, src)
    recorded: bool = False
    k: int = 0  # number of events before the recording
    saved: int = 0  # the recorded balance
    recording: dict = field(default_factory=dict)  # src -> still recording?
    chan: dict = field(default_factory=dict)  # src -> list of (mid, amount)


class Bank:
    def __init__(self, balances: list[int], fifo: bool, delay: DelayFn, seed: int) -> None:
        self.n = len(balances)
        self.p = [Proc(b) for b in balances]
        self.fifo = fifo
        self.delay = delay
        self.rng = random.Random(seed)
        self.q: list = []
        self.seq = 0
        self.last: dict = {}  # (src, dst) -> last delivery time, for FIFO
        self.mid = 0
        self.markers = 0

    def push(self, t: float, kind: str, data: tuple) -> None:
        heapq.heappush(self.q, (t, self.seq, kind, data))
        self.seq += 1

    def send(self, now: float, src: int, dst: int, msg: tuple) -> None:
        t = now + self.delay(src, dst, msg, self.rng)
        if self.fifo:
            t = max(t, self.last.get((src, dst), t))
            self.last[(src, dst)] = t
        self.push(t, "deliver", (src, dst, msg))

    def transfer(self, now: float, src: int, dst: int, amount: int) -> None:
        pr = self.p[src]
        pr.balance -= amount
        pr.log.append(("send", self.mid, dst))
        self.send(now, src, dst, ("app", self.mid, amount))
        self.mid += 1

    def record(self, now: float, i: int) -> None:
        pr = self.p[i]
        pr.recorded, pr.k, pr.saved = True, len(pr.log), pr.balance  # @line L1
        for j in range(self.n):
            if j != i:
                self.send(now, i, j, ("marker",))  # @line L2
                self.markers += 1
                pr.recording[j] = True
                pr.chan[j] = []

    def on_deliver(self, now: float, src: int, dst: int, msg: tuple) -> None:
        pr = self.p[dst]
        if msg[0] == "marker":
            if not pr.recorded:  # @line L3
                self.record(now, dst)  # @line L4
            pr.recording[src] = False  # @line L5
            return
        _, mid, amount = msg
        pr.balance += amount
        pr.log.append(("recv", mid, src))
        if pr.recorded and pr.recording[src]:
            pr.chan[src].append((mid, amount))  # @line L6

    def run(self, initiator: int, t_init: float, ticks: int = 0, horizon: float = 0.0, script: list | None = None) -> None:
        for i in range(self.n):
            for _ in range(ticks):
                self.push(self.rng.uniform(0, horizon), "tick", (i,))
        for t, src, dst, amount in script or []:
            self.push(t, "scripted", (src, dst, amount))
        self.push(t_init, "init", (initiator,))
        while self.q:
            now, _, kind, data = heapq.heappop(self.q)
            if kind == "init":
                if not self.p[data[0]].recorded:
                    self.record(now, data[0])
            elif kind == "tick":
                i = data[0]
                if self.p[i].balance > 0:
                    dst = self.rng.choice([j for j in range(self.n) if j != i])
                    self.transfer(now, i, dst, self.rng.randint(1, self.p[i].balance))
            elif kind == "scripted":
                self.transfer(now, *data)
            else:
                self.on_deliver(now, *data)

    # --- checks -------------------------------------------------------------

    def cut(self) -> tuple[int, ...]:
        return tuple(pr.k for pr in self.p)

    def is_consistent(self) -> bool:
        sends = {e[1] for pr in self.p for e in pr.log[: pr.k] if e[0] == "send"}
        return all(e[1] in sends for pr in self.p for e in pr.log[: pr.k] if e[0] == "recv")

    def in_transit(self) -> dict:
        """The messages the cut says are in a channel: sent inside, received outside."""
        sent = {}
        for i, pr in enumerate(self.p):
            for e in pr.log[: pr.k]:
                if e[0] == "send":
                    sent[e[1]] = (i, e[2])
        got = {e[1] for pr in self.p for e in pr.log[: pr.k] if e[0] == "recv"}
        out: dict = {}
        for mid, ch in sent.items():
            if mid not in got:
                out.setdefault(ch, set()).add(mid)
        return out

    def recorded_channels(self) -> dict:
        out: dict = {}
        for j, pr in enumerate(self.p):
            for i, msgs in pr.chan.items():
                if msgs:
                    out[(i, j)] = {mid for mid, _ in msgs}
        return out

    def recorded_total(self) -> int:
        return sum(pr.saved for pr in self.p) + sum(a for pr in self.p for msgs in pr.chan.values() for _, a in msgs)
