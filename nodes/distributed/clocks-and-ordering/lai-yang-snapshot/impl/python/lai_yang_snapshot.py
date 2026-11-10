# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lai-yang-snapshot/. The authors are listed in prov/HRAZCB.jsonl.

"""The Lai and Yang snapshot algorithm on a seeded discrete event simulator of
a bank. Channels need not be FIFO: every message has its own random delay.

Every process starts white and turns red when it records its state. Each
message carries the colour of its sender at the send. A white process that
receives a red message records its state first, then takes the message. Each
process keeps the white messages it sent and received; the state of channel
(i, j) is the white messages i sent to j minus the white messages j received
before it recorded.

So that every process records, a process that turns red sends a red message
with no money on each outgoing channel. Lai and Yang assume instead that the
program sends such messages itself.
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
    log: list = field(default_factory=list)
    red: bool = False
    k: int = 0
    saved: int = 0
    white_sent: dict = field(default_factory=dict)  # dst -> {mid: amount}
    white_recd: dict = field(default_factory=dict)  # src -> {mid: amount}, before recording
    snap_recd: dict = field(default_factory=dict)  # copy of white_recd at the recording


class Bank:
    def __init__(self, balances: list[int], delay: DelayFn, seed: int) -> None:
        self.n = len(balances)
        self.p = [Proc(b) for b in balances]
        self.delay = delay
        self.rng = random.Random(seed)
        self.q: list = []
        self.seq = 0
        self.mid = 0

    def push(self, t: float, kind: str, data: tuple) -> None:
        heapq.heappush(self.q, (t, self.seq, kind, data))
        self.seq += 1

    def send(self, now: float, src: int, dst: int, amount: int) -> None:
        pr = self.p[src]
        colour = "red" if pr.red else "white"  # @line L1
        if amount:
            pr.balance -= amount
            pr.log.append(("send", self.mid, dst))
        if colour == "white":
            pr.white_sent.setdefault(dst, {})[self.mid] = amount  # @line L2
        msg = (colour, self.mid, amount)
        self.mid += 1
        self.push(now + self.delay(src, dst, msg, self.rng), "deliver", (src, dst, msg))

    def record(self, now: float, i: int) -> None:
        pr = self.p[i]
        pr.red, pr.k, pr.saved = True, len(pr.log), pr.balance  # @line L3
        pr.snap_recd = {s: dict(m) for s, m in pr.white_recd.items()}
        for j in range(self.n):
            if j != i:
                self.send(now, i, j, 0)  # a red message with no money

    def on_deliver(self, now: float, src: int, dst: int, msg: tuple) -> None:
        colour, mid, amount = msg
        pr = self.p[dst]
        if colour == "red" and not pr.red:
            self.record(now, dst)  # @line L4
        if amount:
            pr.balance += amount
            pr.log.append(("recv", mid, src))
        if colour == "white" and not pr.red:
            pr.white_recd.setdefault(src, {})[mid] = amount  # @line L5

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
                if not self.p[data[0]].red:
                    self.record(now, data[0])
            elif kind == "tick":
                i = data[0]
                if self.p[i].balance > 0:
                    dst = self.rng.choice([j for j in range(self.n) if j != i])
                    self.send(now, i, dst, self.rng.randint(1, self.p[i].balance))
            elif kind == "scripted":
                self.send(now, *data)
            else:
                self.on_deliver(now, *data)

    def channel_states(self) -> dict:
        """State of (i, j) = white sent by i to j minus white received by j before it recorded."""
        out = {}
        for i, pi in enumerate(self.p):
            for j, sent in pi.white_sent.items():
                got = self.p[j].snap_recd.get(i, {})
                left = {mid: a for mid, a in sent.items() if mid not in got and a}  # @line L6
                if left:
                    out[(i, j)] = left
        return out

    # --- checks -------------------------------------------------------------

    def is_consistent(self) -> bool:
        sends = {e[1] for pr in self.p for e in pr.log[: pr.k] if e[0] == "send"}
        return all(e[1] in sends for pr in self.p for e in pr.log[: pr.k] if e[0] == "recv")

    def in_transit(self) -> dict:
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

    def recorded_total(self) -> int:
        return sum(pr.saved for pr in self.p) + sum(sum(m.values()) for m in self.channel_states().values())
