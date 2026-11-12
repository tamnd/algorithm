# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-executive/. The authors are listed in prov/WJY423.jsonl.

"""Frame size search and table builder of a cyclic executive.

A task is (T, C, D): an integer period T, an execution time C (an int or a
Fraction) and an integer relative deadline D. All tasks are released at
time 0. The major cycle is the hyperperiod H = lcm(T). A frame size f is
admissible when f >= max C, f divides some T (so also H), and
2f - gcd(T, f) <= D for each task. The table assigns each job in [0, H) to
one frame that lies inside the job's window [r, r + D], with total work at
most f in each frame. The assignment is a bin packing search, exponential in
the worst case; it is exact, so it finds a table whenever one exists.
"""

from fractions import Fraction
from math import gcd, lcm

Number = int | Fraction
Task = tuple[int, Number, int]


def admissible_frames(tasks: list[Task]) -> list[int]:
    """All frame sizes f that meet the three frame constraints, in increasing order."""
    h = lcm(*(t for t, _, _ in tasks))  # @line L1
    out = []
    for f in range(1, h + 1):  # @line L2
        if h % f:
            continue
        if f < max(c for _, c, _ in tasks):  # @line L3
            continue
        if all(t % f for t, _, _ in tasks):  # @line L4
            continue
        if any(2 * f - gcd(t, f) > d for t, _, d in tasks):  # @line L5
            continue
        out.append(f)
    return out


def jobs_of(tasks: list[Task]) -> list[tuple[int, int, Number, int]]:
    """The jobs (release, deadline, cost, task index) in one hyperperiod, by deadline."""
    h = lcm(*(t for t, _, _ in tasks))
    jobs = [(k * t, k * t + d, c, i) for i, (t, c, d) in enumerate(tasks) for k in range(h // t)]
    return sorted(jobs, key=lambda j: (j[1], j[0], j[3]))


def assign(jobs: list[tuple[int, int, Number, int]], f: int, frames: int) -> list[list[int]] | None:
    """Put each job in one frame inside its window; load of a frame at most f.

    Returns the list of job indices of each frame, or None. Depth-first
    search with an explicit stack; jobs are taken in deadline order and
    frames are tried from the earliest.
    """
    load: list[Number] = [0] * frames
    table: list[list[int]] = [[] for _ in range(frames)]
    choices = []
    for r, d, _, _ in jobs:
        first = -(-r // f)
        last = d // f - 1
        choices.append(list(range(first, min(last, frames - 1) + 1)))
    stack = [0]  # position in choices[i] to try next, for job i = len(stack) - 1
    while stack:
        i = len(stack) - 1
        if i == len(jobs):
            return table
        k = stack[-1]
        if k > 0:  # undo the previous choice of job i
            prev = choices[i][k - 1]
            load[prev] -= jobs[i][2]
            table[prev].pop()
        while k < len(choices[i]) and load[choices[i][k]] + jobs[i][2] > f:
            k += 1
        if k == len(choices[i]):
            stack.pop()
            continue
        fr = choices[i][k]
        load[fr] += jobs[i][2]
        table[fr].append(i)
        stack[-1] = k + 1
        stack.append(0)
    return None


def cyclic_executive_plan(tasks: list[Task]) -> tuple[int, list[list[int]], list] | None:
    """The smallest admissible frame size that has a table, with the table and the jobs."""
    if not tasks:
        raise ValueError("no tasks")
    h = lcm(*(t for t, _, _ in tasks))
    for f in admissible_frames(tasks):
        jobs = jobs_of(tasks)  # @line L6
        table = assign(jobs, f, h // f)  # @line L7
        if table is not None:
            return f, table, jobs  # @line L8
    return None  # @line L9


def run_table(f: int, table: list[list[int]], jobs: list, cycles: int = 2) -> list[tuple[Number, Number, int]]:
    """Execute the table for some major cycles: (start, end, job index) of each job run."""
    out = []
    h = f * len(table)
    for m in range(cycles):
        for k, frame in enumerate(table):
            now: Number = m * h + k * f
            for j in frame:
                out.append((now, now + jobs[j][2], j))
                now += jobs[j][2]
    return out
