# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truetime/. The authors are listed in prov/SPFG5M.jsonl.

"""TrueTime and the commit rules of Spanner (Corbett et al., OSDI 2012,
Sections 3 and 4.1.2), in a deterministic simulator.

Each server has a local clock C(t) = t + e(t) with |e(t)| <= eps. TT.now()
returns [C(t) - eps, C(t) + eps], which holds the real time t. A read-write
transaction T has a start event (the client sends the commit request) and a
commit event (the data becomes visible).

  Start rule:   s <- TT.now().latest, read after the request reaches the leader
  Commit wait:  the leader makes the data visible only once TT.after(s) holds,
                that is, once TT.now().earliest > s

External consistency: if T1 commits before T2 starts (in real time), then
s1 < s2. The checker below tests it for every pair.
"""

import math
import random
from dataclasses import dataclass
from typing import Callable


@dataclass
class Server:
    eps: float
    err: Callable[[float], float]  # e(t), with |e(t)| <= eps and t + e(t) increasing

    def clock(self, t: float) -> float:
        return t + self.err(t)

    def now(self, t: float) -> tuple[float, float]:
        c = self.clock(t)
        return c - self.eps, c + self.eps  # @line L1

    def after(self, s: float, t: float) -> bool:
        return self.now(t)[0] > s  # @line L2

    def first_after(self, s: float, t: float) -> float:
        """The first real time >= t at which TT.after(s) holds (bisection; C is increasing)."""
        if self.after(s, t):
            return t
        lo, hi = t, t + 1.0
        while not self.after(s, hi):
            hi += 1.0
        for _ in range(80):
            mid = (lo + hi) / 2
            if self.after(s, mid):
                hi = mid
            else:
                lo = mid
        return hi


def sine_server(rng: random.Random, eps: float) -> Server:
    a = rng.uniform(-eps, eps)
    b = rng.uniform(0.01, 0.5)
    phase = rng.uniform(0, 2 * math.pi)
    return Server(eps, lambda t, a=a, b=b, p=phase: a * math.sin(b * t + p))


def fixed_server(eps: float, e: float) -> Server:
    return Server(eps, lambda t, e=e: e)


@dataclass
class Txn:
    name: str
    start: float  # real time of the start event
    leader: int
    s: float = 0.0  # commit timestamp
    commit: float = 0.0  # real time of the commit event


def execute(txns: list[Txn], servers: list[Server], delay: float, work: float, commit_wait: bool) -> list[Txn]:
    """Each request reaches its leader `delay` after the start, the leader needs
    `work` to prepare, then picks s and (with commit wait) waits."""
    for tx in txns:
        srv = servers[tx.leader]
        arrive = tx.start + delay
        tx.s = srv.now(arrive)[1]  # @line L3
        ready = arrive + work
        tx.commit = srv.first_after(tx.s, ready) if commit_wait else ready  # @line L4
    return txns


def violations(txns: list[Txn]) -> list[tuple[str, str]]:
    """Pairs (T1, T2) with commit(T1) < start(T2) but s1 >= s2."""
    return [(a.name, b.name) for a in txns for b in txns if a.commit < b.start and not a.s < b.s]
