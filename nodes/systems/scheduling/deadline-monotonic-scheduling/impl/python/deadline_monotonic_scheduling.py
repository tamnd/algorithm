# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadline-monotonic-scheduling/. The authors are listed in prov/RQ7EFJ.jsonl.

"""Deadline-monotonic priorities and Audsley's optimal priority assignment.

A task is (C, T, D): worst-case execution time, period and relative deadline.
Times are integers. Release is synchronous unless offsets are given.
"""

import heapq
from fractions import Fraction
from math import ceil, lcm


def deadline_monotonic_order(tasks):
    """Task indices from the highest priority to the lowest: shortest D first, ties by index."""
    return sorted(range(len(tasks)), key=lambda i: (tasks[i][2], i))  # @line L1


def simulate(tasks, order, horizon, offsets=None):
    """Preemptive fixed priorities on one processor; returns (task, release, finish) of each job."""
    rank = {i: k for k, i in enumerate(order)}
    offsets = offsets or [0] * len(tasks)
    jobs = []
    for i, (c, t, _) in enumerate(tasks):
        for r in range(offsets[i], horizon, t):
            jobs.append((r, i, c))
    jobs.sort()
    left = [c for _, _, c in jobs]
    ready, out, now, nxt = [], [], 0, 0
    while nxt < len(jobs) or ready:  # @line L2
        if not ready:
            now = max(now, jobs[nxt][0])
        while nxt < len(jobs) and jobs[nxt][0] <= now:  # @line L3
            heapq.heappush(ready, (rank[jobs[nxt][1]], jobs[nxt][0], nxt))
            nxt += 1
        k = ready[0][2]  # @line L4
        run = left[k] if nxt == len(jobs) else min(left[k], jobs[nxt][0] - now)  # @line L5
        now += run
        left[k] -= run
        if left[k] == 0:  # @line L6
            heapq.heappop(ready)
            out.append((jobs[k][1], jobs[k][0], now))
    return out


def deadline_monotonic_scheduling(tasks, horizon=None):
    """Run DM over the hyperperiod; return the list of (task, release) that miss."""
    if horizon is None:
        horizon = lcm(*(t for _, t, _ in tasks))
    out = simulate(tasks, deadline_monotonic_order(tasks), horizon)
    return [(i, r) for i, r, f in out if f - r > tasks[i][2]]


def worst_response_time(tasks, i, higher):
    """Exact worst-case response time of task i below the set `higher`, for any D (busy period analysis).

    Returns None when the utilization of `higher` and i exceeds 1.
    """
    level = [tasks[j] for j in higher] + [tasks[i]]
    if sum(Fraction(c, t) for c, t, _ in level) > 1:
        return None
    c, t, _ = tasks[i]
    length = sum(cj for cj, _, _ in level)
    while True:
        nxt = sum(ceil(Fraction(length, tj)) * cj for cj, tj, _ in level)
        if nxt == length:
            break
        length = nxt
    worst = 0
    for q in range(ceil(Fraction(length, t))):
        w = (q + 1) * c
        while True:
            nxt = (q + 1) * c + sum(ceil(Fraction(w, tasks[j][1])) * tasks[j][0] for j in higher)
            if nxt == w:
                break
            w = nxt
        worst = max(worst, w - q * t)
    return worst


def audsley_optimal_priority_assignment(tasks):
    """Audsley's algorithm: fill the priority levels from the lowest one up.

    At each level, pick a task that meets its deadline when all other
    unassigned tasks have higher priority. Returns the order from the highest
    priority to the lowest, or None when no fixed-priority order works.
    """
    unassigned = list(range(len(tasks)))
    lowest_first = []
    while unassigned:
        for i in unassigned:
            others = [j for j in unassigned if j != i]
            r = worst_response_time(tasks, i, others)
            if r is not None and r <= tasks[i][2]:
                lowest_first.append(i)
                unassigned.remove(i)
                break
        else:
            return None
    return lowest_first[::-1]
