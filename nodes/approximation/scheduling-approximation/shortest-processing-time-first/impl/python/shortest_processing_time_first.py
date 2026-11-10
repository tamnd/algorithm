# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-processing-time-first/. The authors are listed in prov/VXZQYC.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]


def shortest_processing_time_first(
    p: Sequence[Number], m: int = 1
) -> tuple[list[list[int]], list[Number], Number]:
    """Schedule jobs on m identical machines to minimize the total completion time.

    Job j has processing time p[j] >= 0. The jobs are sorted by processing time
    (ties by index), and the k-th job of that order goes to machine k mod m, after
    the jobs that machine already has. The result is the job list of each machine,
    the completion time C[j] of each job, and the total sum(C[j]).
    For m = 1 this is the SPT order for 1||sum C_j.

    Cost: O(n log n) for the sort and O(n) for the rest.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    n = len(p)
    order = sorted(range(n), key=lambda j: (p[j], j))  # @line L1
    load: list[Number] = [0] * m  # @line L2
    machines: list[list[int]] = [[] for _ in range(m)]
    completion: list[Number] = [0] * n
    total: Number = 0
    for k, j in enumerate(order):  # @line L3
        i = k % m  # @line L4
        load[i] = load[i] + p[j]  # @line L5
        completion[j] = load[i]
        machines[i].append(j)
        total = total + completion[j]  # @line L6
    return machines, completion, total  # @line L7


def total_completion_time(p: Sequence[Number], machines: Sequence[Sequence[int]]) -> Number:
    """Return sum(C_j) when each machine runs its list from time 0 without idle time."""
    total: Number = 0
    for jobs in machines:
        t: Number = 0
        for j in jobs:
            t = t + p[j]
            total = total + t
    return total
