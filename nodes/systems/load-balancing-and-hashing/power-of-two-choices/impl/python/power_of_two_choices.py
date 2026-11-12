# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-of-two-choices/. The authors are listed in prov/FH6PZB.jsonl.

"""The power of two choices: each ball samples d bins and joins the least loaded.

greedy places m balls by the d-choice rule of Azar, Broder, Karlin and Upfal.
always_go_left is the asymmetric rule of Vocking. supermarket simulates the
queueing model of Mitzenmacher, and supermarket_tail and expected_time give
its fixed point.
"""

import random
from fractions import Fraction


def choose(loads: list[int], d: int, rng: random.Random) -> int:
    """Sample d bins independently and uniformly; return the least loaded one.

    A tie goes to the bin sampled first.
    """
    n = len(loads)
    best = rng.randrange(n)  # @line L1
    for _ in range(d - 1):  # @line L2
        b = rng.randrange(n)  # @line L3
        if loads[b] < loads[best]:  # @line L4
            best = b
    return best


def place(loads: list[int], d: int, rng: random.Random) -> int:
    """TWO-CHOICE-PLACE: add one job to the least loaded of d sampled bins."""
    best = choose(loads, d, rng)
    loads[best] += 1  # @line L5
    return best  # @line L6


def greedy(n: int, m: int, d: int, rng: random.Random) -> list[int]:
    """Place m balls into n bins with d choices each. Return the loads."""
    if n < 1 or d < 1:
        raise ValueError("need n >= 1 and d >= 1")
    loads = [0] * n
    for _ in range(m):
        place(loads, d, rng)
    return loads


def always_go_left(n: int, m: int, d: int, rng: random.Random) -> list[int]:
    """Vocking's rule: split the bins into d groups of n/d bins, sample one bin
    in each group, join the least loaded, and break a tie toward the leftmost group."""
    if n % d:
        raise ValueError("n must be a multiple of d")
    size = n // d
    loads = [0] * n
    for _ in range(m):
        best = rng.randrange(size)
        for g in range(1, d):
            b = g * size + rng.randrange(size)
            if loads[b] < loads[best]:
                best = b
        loads[best] += 1
    return loads


def supermarket(n: int, lam: float, d: int, steps: int, burn: int, rng: random.Random) -> list[float]:
    """Simulate the supermarket model: n FIFO servers of rate 1, Poisson arrivals
    of rate lam * n, and each arrival joins the shortest of d sampled queues.

    The chain is uniformized: each step is an arrival with probability
    lam / (lam + 1), else a service event at a uniform server (no effect if it is
    idle). Return the time average of s_i, the fraction of queues with at least
    i jobs, for i = 0, 1, 2, ... after burn steps.
    """
    q = [0] * n
    count = [n]  # count[i] = number of queues with at least i jobs
    acc: list[float] = []
    p_arrival = lam / (lam + 1)
    for t in range(burn + steps):
        if rng.random() < p_arrival:
            j = choose(q, d, rng)
            q[j] += 1
            if q[j] == len(count):
                count.append(0)
            count[q[j]] += 1
        else:
            j = rng.randrange(n)
            if q[j] > 0:
                count[q[j]] -= 1
                q[j] -= 1
        if t >= burn:
            while len(acc) < len(count):
                acc.append(0.0)
            for i, c in enumerate(count):
                acc[i] += c
    return [a / (steps * n) for a in acc]


def supermarket_tail(lam: Fraction, d: int, i: int) -> Fraction:
    """The fixed point s_i = lam^((d^i - 1)/(d - 1)) of the supermarket model
    (s_i = lam^i when d = 1)."""
    e = i if d == 1 else (d ** i - 1) // (d - 1)
    return lam ** e


def is_fixed_point(lam: Fraction, d: int, levels: int) -> bool:
    """Check that the tail s_i is a fixed point of the limit equations
    ds_i/dt = lam (s_{i-1}^d - s_i^d) - (s_i - s_{i+1}), with s_0 = 1."""
    s = [supermarket_tail(lam, d, i) for i in range(levels + 2)]
    return s[0] == 1 and all(lam * (s[i - 1] ** d - s[i] ** d) == s[i] - s[i + 1] for i in range(1, levels + 1))


def expected_time(lam: float, d: int, terms: int = 200) -> float:
    """Expected time in the system at the fixed point, by Little's law:
    sum over i >= 1 of s_i / lam."""
    if d == 1:
        return 1 / (1 - lam)
    total = 0.0
    for i in range(1, terms + 1):
        e = (d ** i - 1) // (d - 1)
        term = lam ** (e - 1)
        total += term
        if term < 1e-18:
            break
    return total
