# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fcfs-scheduling/. The authors are listed in prov/TCCY97.jsonl.

"""First-come, first-served scheduling of single-burst processes on one CPU."""

from fractions import Fraction


def fcfs(arrival: list, burst: list) -> tuple:
    """Return (start, completion), two lists indexed like the input.

    Process i arrives at arrival[i] and needs burst[i] > 0 units of CPU. The CPU
    runs the processes in order of arrival, ties by index, each to completion,
    and is idle only when no process has arrived. Times may be int or Fraction.
    Cost: O(n log n) time for the sort, O(n) extra space.
    """
    n = len(arrival)
    queue = sorted(range(n), key=lambda i: (arrival[i], i))  # @line L1
    start = [0] * n
    completion = [0] * n
    t = 0  # @line L2
    for i in queue:  # @line L3
        if t < arrival[i]:  # @line L4
            t = arrival[i]
        start[i] = t  # @line L5
        t = t + burst[i]  # @line L6
        completion[i] = t  # @line L7
    return start, completion  # @line L8


def average_waiting(arrival: list, burst: list) -> Fraction:
    """Mean of start - arrival, which for FCFS is the mean waiting time."""
    start, _ = fcfs(arrival, burst)
    return Fraction(sum(s - a for s, a in zip(start, arrival)), len(arrival))
