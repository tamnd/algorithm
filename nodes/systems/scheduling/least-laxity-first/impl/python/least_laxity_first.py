# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-laxity-first/. The authors are listed in prov/GCJJ20.jsonl.

"""Least laxity first on one processor, in unit time slots.

A job is (release, work, deadline) with integer values. At the start of each
slot t, the laxity of a released, unfinished job is deadline - t - remaining
work. LLF runs the job with the least laxity for one slot. Ties go to the job
that ran in the slot before, then to the earlier deadline, then to the lower
job number.
"""

import heapq
from math import lcm


def least_laxity_first(jobs, sticky=True):
    """Return (slots, finish): slots[t] is the job run in [t, t + 1) or None.

    With sticky=False, a tie in the laxity does not favour the running job.
    """
    left = [w for _, w, _ in jobs]
    finish = [None] * len(jobs)
    slots = []
    t, last = 0, None  # @line L1
    while any(x > 0 for x in left):  # @line L2
        ready = [k for k in range(len(jobs)) if jobs[k][0] <= t and left[k] > 0]  # @line L3
        if not ready:  # @line L4
            slots.append(None)
            last = None
            t += 1
            continue
        k = min(ready, key=lambda j: (jobs[j][2] - t - left[j], sticky and j != last, jobs[j][2], j))  # @line L5
        slots.append(k)  # @line L6
        left[k] -= 1
        t += 1
        if left[k] == 0:  # @line L7
            finish[k] = t
        last = k
    return slots, finish


def edf_slots(jobs):
    """Preemptive EDF in unit slots with the same tie rules, for comparison."""
    left = [w for _, w, _ in jobs]
    finish = [None] * len(jobs)
    slots, t, last = [], 0, None
    while any(x > 0 for x in left):
        ready = [k for k in range(len(jobs)) if jobs[k][0] <= t and left[k] > 0]
        if not ready:
            slots.append(None)
            last = None
        else:
            k = min(ready, key=lambda j: (jobs[j][2], j != last, j))
            slots.append(k)
            left[k] -= 1
            if left[k] == 0:
                finish[k] = t + 1
            last = k
        t += 1
    return slots, finish


def preemptions(slots, jobs):
    """The number of times a job stops while it still has work left."""
    total = [w for _, w, _ in jobs]
    done = [0] * len(jobs)
    count = 0
    for t, k in enumerate(slots):
        if k is not None:
            done[k] += 1
            nxt = slots[t + 1] if t + 1 < len(slots) else None
            if nxt != k and done[k] < total[k]:
                count += 1
    return count


def periodic_jobs(tasks, horizon=None):
    """Jobs of synchronous tasks (C, T) or (C, T, D) released in [0, horizon); default the hyperperiod."""
    if horizon is None:
        horizon = lcm(*(task[1] for task in tasks))
    jobs = []
    for task in tasks:
        c, p = task[0], task[1]
        d = task[2] if len(task) > 2 else p
        for r in range(0, horizon, p):
            jobs.append((r, c, r + d))
    jobs.sort()
    return jobs


def meets_deadlines(finish, jobs):
    return all(f <= d for f, (_, _, d) in zip(finish, jobs))
