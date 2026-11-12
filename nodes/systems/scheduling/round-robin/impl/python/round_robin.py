# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/round-robin/. The authors are listed in prov/EHJG6W.jsonl.

"""Round-robin scheduling of single-burst processes on one CPU.

Times may be int or Fraction. A process that arrives at time t joins the ready
queue before a process whose quantum ends at t. Each dispatch of a process other
than the one that has just run costs `switch` units of CPU time.
"""

from collections import deque
from fractions import Fraction


def round_robin(arrival: list, burst: list, q, switch=0) -> tuple:
    """Return (completion, slices).

    slices is a list of (process, start, end) for each run of the CPU. A process
    whose quantum ends while the ready queue is empty keeps the CPU without a
    switch, and its next run is a new slice.
    Cost: O(n log n + sum of ceil(burst / q)) time, O(n) extra space.
    """
    n = len(arrival)
    order = sorted(range(n), key=lambda i: (arrival[i], i))  # @line L1
    k, t, ready, last = 0, 0, deque(), None
    left = list(burst)  # @line L2
    completion = [None] * n
    slices = []

    def admit(now) -> None:
        nonlocal k
        while k < n and arrival[order[k]] <= now:
            ready.append(order[k])
            k += 1

    while k < n or ready:  # @line L3
        if not ready and t < arrival[order[k]]:  # @line L4
            t = arrival[order[k]]
        admit(t)  # @line L5
        i = ready.popleft()  # @line L6
        if i != last:  # @line L7
            t = t + switch
        d = min(q, left[i])  # @line L8
        slices.append((i, t, t + d))
        t = t + d  # @line L9
        left[i] = left[i] - d
        last = i
        admit(t)  # @line L10
        if left[i] > 0:  # @line L11
            ready.append(i)
        else:
            completion[i] = t
    return completion, slices  # @line L12


def waiting_times(arrival: list, burst: list, q, switch=0) -> list:
    """Waiting time C - a - b of each process."""
    c, _ = round_robin(arrival, burst, q, switch)
    return [ci - a - b for ci, a, b in zip(c, arrival, burst)]


def response_times(arrival: list, burst: list, q, switch=0) -> list:
    """Time from arrival to the first slice of each process."""
    _, slices = round_robin(arrival, burst, q, switch)
    first = {}
    for i, s, _ in slices:
        first.setdefault(i, s)
    return [first[i] - arrival[i] for i in range(len(arrival))]


def processor_sharing(burst: list) -> list:
    """Completion times under processor sharing when all processes arrive at 0.

    With bursts sorted as p(1) <= ... <= p(n), the k-th finishes at
    p(1) + ... + p(k-1) + (n - k + 1) p(k).
    """
    n = len(burst)
    order = sorted(range(n), key=lambda i: (burst[i], i))
    out = [None] * n
    done = 0
    for k, i in enumerate(order):
        out[i] = done + (n - k) * burst[i]
        done += burst[i]
    return out


def mean_turnaround(arrival: list, burst: list, q) -> Fraction:
    c, _ = round_robin(arrival, burst, q)
    return Fraction(sum(ci - a for ci, a in zip(c, arrival)), len(arrival))
