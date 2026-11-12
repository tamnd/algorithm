# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aging/. The authors are listed in prov/1CN15A.jsonl.

"""Aging for nonpreemptive priority scheduling on one CPU.

A smaller number is a higher priority, and 0 is the highest. A process with
base priority p that has waited w time units in the ready queue has the
effective priority max(0, p - floor(w / A)), where A is the aging period.
Ties go to the earlier arrival, then to the smaller index. period=None turns
aging off, which gives plain static priority scheduling.
"""


def effective_priority(base: int, waited, period) -> int:
    """The aged priority: one level higher for each full period of waiting."""
    if period is None:
        return base
    return max(0, base - int(waited // period))


def choose(ready: list, now, arrival: list, priority: list, period) -> int:
    """The ready process with the least (aged priority, arrival, index)."""
    return min(ready, key=lambda i: (effective_priority(priority[i], now - arrival[i], period),
                                     arrival[i], i))


def schedule_with_aging(arrival: list, burst: list, priority: list, period=None) -> list:
    """Return the start time of each process.

    Each process runs once, to completion. At each moment when the CPU is free,
    the scheduler takes the ready process chosen by `choose`.
    Cost: O(n^2) time, since each decision scans the ready processes.
    """
    n = len(arrival)
    order = sorted(range(n), key=lambda i: (arrival[i], i))
    start = [None] * n
    k, t, ready = 0, 0, []
    while k < n or ready:
        if not ready and t < arrival[order[k]]:
            t = arrival[order[k]]
        while k < n and arrival[order[k]] <= t:
            ready.append(order[k])
            k += 1
        i = choose(ready, t, arrival, priority, period)
        ready.remove(i)
        start[i] = t
        t = t + burst[i]
    return start


def wait_bound(i: int, arrival: list, burst: list, priority: list, period) -> object:
    """An upper bound on the wait of process i under aging.

    After p_i * A units of waiting, i has priority 0, and from then on only the
    process that is running and processes with priority 0 that arrived before i
    can go first.
    """
    earlier = sum(burst[j] for j in range(len(arrival)) if (arrival[j], j) < (arrival[i], i))
    return priority[i] * period + max(burst) + earlier
