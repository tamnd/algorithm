# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/response-time-analysis/. The authors are listed in prov/62Y3C2.jsonl.

"""Response-time analysis for preemptive fixed priorities on one processor.

A task is (C, T, D): worst-case execution time, period or minimum
inter-arrival time, and relative deadline with D <= T. The list of tasks is in
priority order: index 0 has the highest priority. Times are int or Fraction.
"""

import heapq
from math import lcm


def _ceil_div(a, b):
    """The exact ceiling of a / b for int or Fraction values, with b > 0."""
    return -(-a // b)


def response_time(tasks, i, blocking=0):
    """Worst-case response time of task i, or None when it exceeds the deadline D_i.

    Solves R = C_i + B_i + sum over j < i of ceil(R / T_j) C_j by fixed-point
    iteration from R = C_i + B_i.
    """
    c, _, d = tasks[i]
    r = c + blocking  # @line L1
    while True:  # @line L2
        nxt = c + blocking + sum(_ceil_div(r, tj) * cj for cj, tj, _ in tasks[:i])  # @line L3
        if nxt > d:  # @line L4
            return None
        if nxt == r:  # @line L5
            return r
        r = nxt  # @line L6


def response_time_analysis(tasks, blocking=None):
    """Return the list of worst-case response times (None for a task that can miss)."""
    if blocking is None:
        blocking = [0] * len(tasks)
    return [response_time(tasks, i, blocking[i]) for i in range(len(tasks))]


def schedulable(tasks):
    return all(r is not None for r in response_time_analysis(tasks))


def simulate(tasks, offsets, horizon):
    """Preemptive fixed priorities, jobs released in [0, horizon) at offset + k T.

    Returns a list of (task, release, finish) for every job; jobs run to the end.
    """
    jobs = []
    for i, (c, t, _) in enumerate(tasks):
        r = offsets[i]
        while r < horizon:
            jobs.append((r, i, c))
            r += t
    jobs.sort()
    left = [c for _, _, c in jobs]
    ready, out, now, nxt = [], [], 0, 0
    while nxt < len(jobs) or ready:
        if not ready:
            now = max(now, jobs[nxt][0])
        while nxt < len(jobs) and jobs[nxt][0] <= now:
            heapq.heappush(ready, (jobs[nxt][1], jobs[nxt][0], nxt))
            nxt += 1
        k = ready[0][2]
        run = left[k] if nxt == len(jobs) else min(left[k], jobs[nxt][0] - now)
        now += run
        left[k] -= run
        if left[k] == 0:
            heapq.heappop(ready)
            out.append((jobs[k][1], jobs[k][0], now))
    return out


def critical_instant_response(tasks, i):
    """Response time of the first job of task i when all tasks release at time 0."""
    horizon = max(t for _, t, _ in tasks[: i + 1])
    while True:
        first = [f for task, r, f in simulate(tasks[: i + 1], [0] * (i + 1), horizon) if task == i and r == 0]
        if first[0] <= horizon:
            return first[0]
        horizon *= 2


def hyperperiod(tasks):
    return lcm(*(t for _, t, _ in tasks))
