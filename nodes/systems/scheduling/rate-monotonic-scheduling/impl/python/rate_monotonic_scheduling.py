# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rate-monotonic-scheduling/. The authors are listed in prov/JM2GFC.jsonl.

"""Rate-monotonic scheduling on one preemptive processor, with exact arithmetic.

A task is a tuple (C, T) or (C, T, D) or (C, T, D, O): the worst-case
execution time C, the period T, the relative deadline D (default T) and the
offset O of the first release (default 0). Times are int or Fraction.
"""

import heapq
from fractions import Fraction
from math import lcm, prod


def _params(task):
    c, p = task[0], task[1]
    d = task[2] if len(task) > 2 else p
    o = task[3] if len(task) > 3 else 0
    return c, p, d, o


def hyperperiod(tasks):
    """The least common multiple of the periods. The periods must be integers."""
    return lcm(*(task[1] for task in tasks))


def rate_monotonic_order(tasks):
    """Task indices from the highest priority to the lowest: shortest period first, ties by index."""
    return sorted(range(len(tasks)), key=lambda i: (tasks[i][1], i))


def fixed_priority_schedule(tasks, order, horizon):
    """Simulate preemptive fixed priorities for the jobs released in [0, horizon).

    Returns (pieces, jobs). pieces is a list of (start, end, task index).
    jobs is a list of dicts with the keys task, release, deadline, finish.
    Each job runs to completion, also after its deadline.
    """
    rank = {i: k for k, i in enumerate(order)}  # @line L1
    jobs = []  # @line L2
    for i, task in enumerate(tasks):
        c, p, d, o = _params(task)
        r = o
        while r < horizon:
            jobs.append({"task": i, "release": r, "deadline": r + d, "work": c, "finish": None})
            r += p
    jobs.sort(key=lambda j: j["release"])
    pieces = []
    left = [j["work"] for j in jobs]
    ready = []  # heap of (rank, release, job number)
    t, nxt = 0, 0  # @line L3
    while nxt < len(jobs) or ready:  # @line L4
        if not ready:  # @line L5
            t = max(t, jobs[nxt]["release"])
        while nxt < len(jobs) and jobs[nxt]["release"] <= t:  # @line L6
            heapq.heappush(ready, (rank[jobs[nxt]["task"]], jobs[nxt]["release"], nxt))
            nxt += 1
        _, _, k = ready[0]  # @line L7
        run = left[k]  # @line L8
        if nxt < len(jobs):
            run = min(run, jobs[nxt]["release"] - t)
        if run == 0:
            pass
        elif pieces and pieces[-1][1] == t and pieces[-1][3] == k:
            pieces[-1] = (pieces[-1][0], t + run, jobs[k]["task"], k)  # @line L9
        else:
            pieces.append((t, t + run, jobs[k]["task"], k))
        t += run
        left[k] -= run
        if left[k] == 0:  # @line L10
            heapq.heappop(ready)
            jobs[k]["finish"] = t
    return [(a, b, i) for a, b, i, _ in pieces], jobs


def rate_monotonic_scheduling(tasks, horizon=None):
    """Return (pieces, missed) for rate-monotonic priorities over [0, horizon).

    The default horizon is the hyperperiod. missed lists (task, release) of
    each job that finishes after its absolute deadline.
    """
    if horizon is None:
        horizon = hyperperiod(tasks)
    pieces, jobs = fixed_priority_schedule(tasks, rate_monotonic_order(tasks), horizon)
    missed = [(j["task"], j["release"]) for j in jobs if j["finish"] > j["deadline"]]
    return pieces, missed


def simulation_test(tasks, order=None):
    """Exact test for synchronous tasks with D <= T: simulate one hyperperiod."""
    if order is None:
        order = rate_monotonic_order(tasks)
    _, jobs = fixed_priority_schedule(tasks, order, hyperperiod(tasks))
    return all(j["finish"] <= j["deadline"] for j in jobs)


def utilization(tasks):
    return sum((Fraction(task[0]) / task[1] for task in tasks), Fraction(0))


def liu_layland_test(tasks):
    """Sufficient test U <= n(2^(1/n) - 1), decided exactly.

    For U >= 0 the test is equivalent to (1 + U/n)^n <= 2, which needs no
    irrational number.
    """
    n = len(tasks)
    if n == 0:
        return True
    return (1 + utilization(tasks) / n) ** n <= 2


def hyperbolic_test(tasks):
    """Sufficient test of Bini, Buttazzo and Buttazzo: the product of (U_i + 1) is at most 2."""
    return prod((1 + Fraction(task[0]) / task[1] for task in tasks), start=Fraction(1)) <= 2
