# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peak-ewma/. The authors are listed in prov/MD9K0X.jsonl.

"""Peak EWMA load balancing, after Finagle's PeakEwma and its p2c balancer.

Each backend keeps a cost c (a latency estimate), the time s of its last
update and its number of pending requests p. A sample x at time t with
x > c sets c = x at once (the peak rule). A smaller sample is mixed in with
the weight w = exp(-(t - s) / tau), which depends on the time since the last
update, not on the number of samples. Reading the load first decays c toward
0 by the same weight. The load is c * (p + 1), or a large penalty plus p if
there is no sample yet but requests are pending.

pick() draws two different backends with the caller's random.Random and
keeps the one with the smaller load (power of two choices). Time is an
explicit argument; nothing reads a real clock. Cost: O(1) per pick and per
response, Theta(n) space.
"""

import math
import random
from typing import List, Optional, Tuple

PENALTY = float((2 ** 63 - 1) >> 16)  # Finagle: Long.MaxValue >> 16 nanoseconds


class PeakEwma:
    def __init__(self, n: int, tau: float = 10.0, start: float = 0.0) -> None:
        if tau <= 0:
            raise ValueError("tau must be positive")
        self.tau = tau
        self.c = [0.0] * n
        self.s = [start] * n
        self.p = [0] * n

    def observe(self, j: int, x: float, t: float) -> None:
        dt = max(t - self.s[j], 0.0)  # @line L1
        self.s[j] = max(self.s[j], t)
        if x > self.c[j]:  # @line L2
            self.c[j] = x  # @line L3
        else:
            w = math.exp(-dt / self.tau)  # @line L4
            self.c[j] = self.c[j] * w + x * (1.0 - w)  # @line L5

    def load(self, j: int, t: float) -> float:
        self.observe(j, 0.0, t)  # @line L6
        if self.c[j] == 0.0 and self.p[j] != 0:  # @line L7
            return PENALTY + self.p[j]
        return self.c[j] * (self.p[j] + 1)  # @line L8

    def pick(self, t: float, rng: random.Random) -> int:
        n = len(self.c)
        if n == 1:
            i = 0
        else:
            i = rng.randrange(n)  # @line L9
            k = rng.randrange(n - 1)
            if k >= i:
                k += 1
            if self.load(k, t) < self.load(i, t):  # @line L10
                i = k
        self.p[i] += 1  # @line L11
        return i

    def done(self, j: int, t0: float, t: float) -> None:
        if self.p[j] <= 0:
            raise ValueError("no pending request on this backend")
        self.p[j] -= 1  # @line L12
        self.observe(j, max(t - t0, 0.0), t)  # @line L13


def decayed_peak(samples: List[Tuple[float, float]], t: float, tau: float) -> float:
    """max of x * exp(-(t - u) / tau) over the samples (u, x) with u <= t; 0 if none."""
    return max([x * math.exp(-(t - u) / tau) for u, x in samples if u <= t] + [0.0])


def trace(events: List[Tuple[str, int, float, float]], n: int, tau: float = 10.0) -> List[float]:
    """Run ('obs', j, x, t) and ('read', j, 0, t) events; return the cost after each."""
    pe = PeakEwma(n, tau)
    out: List[float] = []
    for kind, j, x, t in events:
        if kind == "obs":
            pe.observe(j, x, t)
        else:
            pe.load(j, t)
        out.append(pe.c[j])
    return out


def pick_counts(pe: PeakEwma, rng: random.Random, picks: int, t: float) -> List[int]:
    """Counts of picks at a fixed time when no request ends."""
    counts = [0] * len(pe.c)
    for _ in range(picks):
        counts[pe.pick(t, rng)] += 1
    return counts


def first_time_cheaper(spike: float, rival_load: float, tau: float) -> Optional[float]:
    """Time after a spike at which spike * exp(-t / tau) falls below rival_load."""
    if rival_load <= 0:
        return None
    return tau * math.log(spike / rival_load) if spike > rival_load else 0.0
