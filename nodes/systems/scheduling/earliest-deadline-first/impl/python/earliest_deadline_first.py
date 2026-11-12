# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-deadline-first/. The authors are listed in prov/20A95V.jsonl.

"""Earliest deadline first, with exact arithmetic.

A job is (release, work, deadline). A task is (C, T) or (C, T, D): the
worst-case execution time, the period and the relative deadline (default T).
Times are int or Fraction. Ties in the deadline go to the earlier release,
then to the lower job number.
"""

import heapq
from fractions import Fraction
from math import floor, lcm


def edf_jobs(jobs):
    """Preemptive EDF on one processor. Returns (pieces, finish).

    pieces is a list of (start, end, job number); finish[k] is the completion
    time of job k. Each job runs to the end, also after its deadline.
    """
    order = sorted(range(len(jobs)), key=lambda k: jobs[k][0])  # @line L1
    left = [w for _, w, _ in jobs]
    finish = [None] * len(jobs)
    pieces, ready = [], []  # ready is a heap of (deadline, release, job number)
    t, nxt = 0, 0  # @line L2
    while nxt < len(order) or ready:  # @line L3
        if not ready:  # @line L4
            t = max(t, jobs[order[nxt]][0])
        while nxt < len(order) and jobs[order[nxt]][0] <= t:  # @line L5
            k = order[nxt]
            heapq.heappush(ready, (jobs[k][2], jobs[k][0], k))
            nxt += 1
        k = ready[0][2]  # @line L6
        run = left[k]  # @line L7
        if nxt < len(order):
            run = min(run, jobs[order[nxt]][0] - t)
        if run > 0:  # @line L8
            if pieces and pieces[-1][1] == t and pieces[-1][2] == k:
                pieces[-1] = (pieces[-1][0], t + run, k)
            else:
                pieces.append((t, t + run, k))
        t += run
        left[k] -= run
        if left[k] == 0:  # @line L9
            heapq.heappop(ready)
            finish[k] = t
    return pieces, finish


def task_jobs(tasks, horizon):
    """The jobs that synchronous periodic tasks release in [0, horizon), and the task of each one."""
    jobs, owner = [], []
    for i, task in enumerate(tasks):
        c, p = task[0], task[1]
        d = task[2] if len(task) > 2 else p
        r = 0
        while r < horizon:
            jobs.append((r, c, r + d))
            owner.append(i)
            r += p
    return jobs, owner


def hyperperiod(tasks):
    return lcm(*(task[1] for task in tasks))


def earliest_deadline_first(tasks, horizon=None):
    """EDF for synchronous periodic tasks over [0, horizon) (default: the hyperperiod).

    Returns (pieces, missed), with pieces as (start, end, task) and missed as
    the list of (task, release) of each job that ends after its deadline.
    """
    if horizon is None:
        horizon = hyperperiod(tasks)
    jobs, owner = task_jobs(tasks, horizon)
    pieces, finish = edf_jobs(jobs)
    missed = [(owner[k], jobs[k][0]) for k in range(len(jobs)) if finish[k] > jobs[k][2]]
    out = []
    for a, b, k in pieces:
        if out and out[-1][1] == a and out[-1][2] == owner[k]:
            out[-1] = (out[-1][0], b, owner[k])
        else:
            out.append((a, b, owner[k]))
    return out, missed


def utilization(tasks):
    return sum((Fraction(task[0]) / task[1] for task in tasks), Fraction(0))


def demand_bound(tasks, t):
    """h(t): the work of the jobs with release and deadline in [0, t], for synchronous release."""
    total = 0
    for task in tasks:
        c, p = task[0], task[1]
        d = task[2] if len(task) > 2 else p
        if t >= d:
            total += (floor(Fraction(t - d) / p) + 1) * c
    return total


def processor_demand_test(tasks):
    """Exact EDF test for synchronous or sporadic tasks with D <= T (Baruah, Rosier and Howell 1990).

    Checks h(t) <= t at each absolute deadline t up to the bound L: the
    hyperperiod when U = 1, else the smaller of the hyperperiod and
    sum (T_i - D_i) U_i / (1 - U).
    """
    u = utilization(tasks)
    if u > 1:
        return False
    bound = hyperperiod(tasks)
    if u < 1:
        la = sum((Fraction(task[1] - (task[2] if len(task) > 2 else task[1])) * task[0] / task[1] for task in tasks), Fraction(0)) / (1 - u)
        bound = min(bound, la)
    points = set()
    for task in tasks:
        p = task[1]
        d = task[2] if len(task) > 2 else p
        while d <= bound:
            points.add(d)
            d += p
    return all(demand_bound(tasks, t) <= t for t in points)


def global_edf(jobs, m):
    """Global preemptive EDF on m identical processors. Returns the finish time of each job."""
    left = [w for _, w, _ in jobs]
    finish = [None] * len(jobs)
    t = 0
    while any(f is None for f in finish):
        ready = sorted((jobs[k][2], jobs[k][0], k) for k in range(len(jobs)) if finish[k] is None and jobs[k][0] <= t)
        running = [k for _, _, k in ready[:m]]
        future = [jobs[k][0] for k in range(len(jobs)) if jobs[k][0] > t]
        step = min([left[k] for k in running] + [r - t for r in future])
        for k in running:
            left[k] -= step
            if left[k] == 0:
                finish[k] = t + step
        t += step
    return finish
