# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-scheduling/. The authors are listed in prov/RDGF8V.jsonl.

"""Static priority scheduling of single-burst processes on one CPU.

A smaller number means a higher priority. Ties go to the earlier arrival, then
to the smaller index. With preemptive=True, an arriving process preempts the
running one if its key is smaller; a process of equal priority does not preempt.
Times may be int or Fraction.
"""

import heapq


def priority_schedule(arrival: list, burst: list, priority: list, preemptive: bool = False) -> tuple:
    """Return (completion, slices), where slices lists (process, start, end).

    Cost: O(n log n) time, since each arrival causes at most one preemption,
    and O(n) extra space.
    """
    n = len(arrival)
    order = sorted(range(n), key=lambda i: (arrival[i], i))  # @line L1
    k, t, heap = 0, 0, []
    left = list(burst)  # @line L2
    completion = [None] * n
    slices = []
    while k < n or heap:  # @line L3
        if not heap and t < arrival[order[k]]:  # @line L4
            t = arrival[order[k]]
        while k < n and arrival[order[k]] <= t:  # @line L5
            j = order[k]
            heapq.heappush(heap, (priority[j], arrival[j], j))
            k += 1
        _, _, i = heapq.heappop(heap)  # @line L6
        if preemptive and k < n:  # @line L7
            e = min(t + left[i], arrival[order[k]])
        else:
            e = t + left[i]
        if slices and slices[-1][0] == i and slices[-1][2] == t:  # @line L8
            slices[-1] = (i, slices[-1][1], e)  # the arrival did not preempt i
        else:
            slices.append((i, t, e))
        left[i] = left[i] - (e - t)
        t = e
        if left[i] > 0:  # @line L9
            heapq.heappush(heap, (priority[i], arrival[i], i))
        else:
            completion[i] = t
    return completion, slices  # @line L10


def waiting_times(arrival: list, burst: list, priority: list, preemptive: bool = False) -> list:
    c, _ = priority_schedule(arrival, burst, priority, preemptive)
    return [ci - a - b for ci, a, b in zip(c, arrival, burst)]
