# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sjf-optimality/. The authors are listed in prov/137WN4.jsonl.

"""Exact checks of the optimality of shortest-job-first for mean waiting time.

All functions work on integer or Fraction times on one CPU. Brute force runs in
O(n! * n) time, so use n <= 8.
"""

from itertools import permutations


def total_waiting(order: list, burst: list) -> object:
    """Total waiting time when all processes arrive at 0 and run in this order."""
    t = 0
    total = 0
    for i in order:
        total += t
        t += burst[i]
    return total


def sjf_order(burst: list) -> list:
    """Indices in order of nondecreasing burst, ties by index."""
    return sorted(range(len(burst)), key=lambda i: (burst[i], i))


def formula(burst: list) -> object:
    """sum over k of (n - k) * b_(k) for the bursts sorted increasingly (k from 1)."""
    b = sorted(burst)
    n = len(b)
    return sum((n - k) * b[k - 1] for k in range(1, n + 1))


def best_nonpreemptive(arrival: list, burst: list) -> object:
    """Least total waiting over all nonpreemptive schedules, idle time allowed.

    Some optimal schedule starts each job as early as its order allows, so it
    suffices to try every order.
    """
    best = None
    for order in permutations(range(len(burst))):
        t, total = 0, 0
        for i in order:
            t = max(t, arrival[i])
            total += t - arrival[i]
            t += burst[i]
        best = total if best is None else min(best, total)
    return best


def preemptive_waiting(arrival: list, burst: list, slices: list) -> object:
    """Total waiting of a preemptive schedule given as one job index per unit slot.

    Slot s is [s, s + 1); None means idle. Integer bursts only.
    """
    left = list(burst)
    done = [None] * len(burst)
    for s, j in enumerate(slices):
        if j is None:
            continue
        assert s >= arrival[j] and left[j] > 0
        left[j] -= 1
        if left[j] == 0:
            done[j] = s + 1
    assert all(x == 0 for x in left)
    return sum(c - a - b for c, a, b in zip(done, arrival, burst))


def srpt_slices(arrival: list, burst: list) -> list:
    """Unit-step SRPT, used as the preemptive optimum with arrivals."""
    left = list(burst)
    out = []
    t = 0
    while any(left):
        ready = [j for j in range(len(burst)) if arrival[j] <= t and left[j] > 0]
        if not ready:
            out.append(None)
        else:
            j = min(ready, key=lambda j: (left[j], j))
            left[j] -= 1
            out.append(j)
        t += 1
    return out
