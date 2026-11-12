# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-fair-scheduling/. The authors are listed in prov/PSY7PJ.jsonl.

"""Proportional fair scheduling (Jalali, Padovani and Pankaj, VTC 2000).

In each slot the base station learns the rate r_i that each user could get
now, and serves the user with the largest r_i / R_i, where R_i is an
exponentially weighted average of the rate that user i has received, with
time constant t_c. Max-rate and round robin are given for comparison.
"""

import math
import random


class ProportionalFair:
    def __init__(self, n: int, tc: float, r0: float = 1.0) -> None:
        if tc <= 1:
            raise ValueError("t_c must be more than 1 slot")
        if r0 <= 0:
            raise ValueError("the averages must start positive")
        self.n = n
        self.tc = tc
        self.avg = [r0] * n  # R_i, positive so that r_i / R_i is defined

    def choose(self, rates: list) -> int:
        best = 0  # @line L1
        for i in range(1, self.n):
            if rates[i] * self.avg[best] > rates[best] * self.avg[i]:
                best = i
        return best

    def update(self, rates: list, served: int) -> None:
        b = 1.0 / self.tc
        for i in range(self.n):  # @line L3
            if i == served:  # @line L4
                self.avg[i] = (1 - b) * self.avg[i] + b * rates[i]
            else:  # @line L5
                self.avg[i] = (1 - b) * self.avg[i]

    def step(self, rates: list) -> int:
        """One slot: choose a user, serve it and update the averages."""
        i = self.choose(rates)
        self.update(rates, i)  # @line L2
        return i


def rayleigh_rates(rng: random.Random, snr: list) -> list:
    """Shannon rate log2(1 + snr * h) with Rayleigh fading, h ~ Exp(1)."""
    return [math.log2(1 + s * rng.expovariate(1.0)) for s in snr]


def run(policy: str, snr: list, slots: int, seed: int, tc: float = 100.0):
    """Return (throughput per user, fraction of slots per user) for one of
    the policies "pf", "max-rate" and "round-robin" on a seeded channel."""
    rng = random.Random(seed)
    n = len(snr)
    pf = ProportionalFair(n, tc)
    got = [0.0] * n
    slots_of = [0] * n
    for t in range(slots):
        r = rayleigh_rates(rng, snr)
        if policy == "pf":
            i = pf.step(r)
        elif policy == "max-rate":
            i = max(range(n), key=lambda k: r[k])
        elif policy == "round-robin":
            i = t % n
        else:
            raise ValueError(policy)
        got[i] += r[i]
        slots_of[i] += 1
    return [g / slots for g in got], [s / slots for s in slots_of]


def sum_log(throughputs: list) -> float:
    """Sum of log throughputs; a starved user gives minus infinity."""
    return sum(math.log(x) if x > 0 else -math.inf for x in throughputs)
