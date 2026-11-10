# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-scheduling/. The authors are listed in prov/D4MGPF.jsonl.

import heapq
from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


def list_scheduling(p: list[Number], m: int) -> tuple[list[int], list[Number], Number]:
    """Graham's list scheduling for independent jobs on m identical machines.

    The jobs are taken in the given order. Each job goes to a machine with
    the smallest load at that moment (the smallest index on a tie) and starts
    at that load. Precondition: m >= 1 and every p[j] >= 0.
    Returns (machine, start, makespan), with 0-based machine numbers.
    Cost: O(m + n log m) time with a binary heap, O(n + m) space.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    heap: list[tuple[Number, int]] = [(0, i) for i in range(m)]  # @line L1
    heapq.heapify(heap)
    machine: list[int] = []
    start: list[Number] = []
    for pj in p:  # @line L2
        load, i = heapq.heappop(heap)  # @line L3
        machine.append(i)  # @line L4
        start.append(load)
        heapq.heappush(heap, (load + pj, i))  # @line L5
    makespan = max(load for load, _ in heap)  # @line L6
    return machine, start, makespan


def list_scheduling_with_precedence(
    p: list[Number], m: int, prec: list[tuple[int, int]], order: list[int]
) -> tuple[list[int], list[Number], Number]:
    """Graham's list scheduling with precedence constraints.

    prec holds pairs (a, b): job b may start only after job a ends.
    order is the priority list, a permutation of range(len(p)). At each time
    when a machine is idle, the idle machines, in index order, each take the
    first job of the list that is not started and whose predecessors are all
    done. Precondition: the precedence graph is acyclic, m >= 1, p[j] >= 0.
    Returns (machine, start, makespan). Cost: O(n^2 m) time in this simple form.
    """
    n = len(p)
    preds: list[set[int]] = [set() for _ in range(n)]
    for a, b in prec:
        preds[b].add(a)
    end: dict[int, Number] = {}
    machine = [-1] * n
    start: list[Number] = [0] * n
    free: list[Number] = [0] * m
    t: Number = 0
    started = 0
    while started < n:
        progress = True
        while progress:  # repeat, because a job of length 0 frees its machine at once
            progress = False
            for i in range(m):
                if free[i] > t:
                    continue
                for j in order:
                    if machine[j] < 0 and all(q in end and end[q] <= t for q in preds[j]):
                        machine[j], start[j] = i, t
                        end[j] = t + p[j]
                        free[i] = end[j]
                        started += 1
                        progress = True
                        break
        if started == n:
            break
        later = [e for e in end.values() if e > t]
        if not later:
            raise ValueError("the precedence constraints have a cycle")
        t = min(later)
    makespan = max(end.values(), default=0)
    return machine, start, makespan
