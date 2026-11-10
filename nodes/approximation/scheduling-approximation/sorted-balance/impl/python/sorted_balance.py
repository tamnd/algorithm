# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sorted-balance/. The authors are listed in prov/SYMRSF.jsonl.

from fractions import Fraction
from typing import Union

Number = Union[int, Fraction]


def sorted_balance(p: list[Number], m: int) -> tuple[list[list[int]], list[Number]]:
    """Sorted-Balance (Kleinberg and Tardos): the sorted greedy for load balancing.

    Sort the jobs by non-increasing size (ties keep the input order). Give each
    job, in that order, to a machine of smallest current load, found by a scan
    (the smallest index on a tie). Precondition: m >= 1, every p[j] >= 0.
    Returns (A, T): A[i] lists the jobs of machine i in the order they were
    assigned, T[i] is the load of machine i. The makespan is max(T).
    Cost: O(n log n + n m) time, O(n + m) space.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    order = sorted(range(len(p)), key=lambda j: -p[j])  # @line L1
    a: list[list[int]] = [[] for _ in range(m)]  # @line L2
    t: list[Number] = [0] * m
    for j in order:  # @line L3
        i = min(range(m), key=lambda k: (t[k], k))  # @line L4
        a[i].append(j)  # @line L5
        t[i] = t[i] + p[j]  # @line L6
    return a, t  # @line L7
