# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-processing-time-first/. The authors are listed in prov/NPZATW.jsonl.

import heapq
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


def longest_processing_time_first(p: list[Number], m: int) -> tuple[list[int], list[Number]]:
    """Graham's LPT rule for P||C_max.

    Sort the jobs by non-increasing processing time (ties keep the input
    order), then give each job to a machine of smallest current load (the
    smallest index on a tie). Precondition: m >= 1 and every p[j] >= 0.
    Returns (machine, load): machine[j] is the 0-based machine of job j, and
    load[i] is the final load of machine i. The makespan is max(load).
    Cost: O(n log n + m + n log m) time, O(n + m) space.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    order = sorted(range(len(p)), key=lambda j: -p[j])  # @line L1
    heap: list[tuple[Number, int]] = [(0, i) for i in range(m)]  # @line L2
    heapq.heapify(heap)
    machine = [-1] * len(p)
    for k in range(len(order)):  # @line L3
        j = order[k]  # @line L4
        load, i = heapq.heappop(heap)  # @line L5
        machine[j] = i  # @line L6
        heapq.heappush(heap, (load + p[j], i))  # @line L7
    loads: list[Number] = [0] * m
    for load, i in heap:  # @line L8
        loads[i] = load
    return machine, loads
