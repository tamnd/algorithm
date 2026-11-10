# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-due-date-first/. The authors are listed in prov/9Q08CA.jsonl.

from fractions import Fraction
from typing import Optional, Sequence, Union

Number = Union[int, Fraction]


def earliest_due_date_first(
    p: Sequence[Number], d: Sequence[Number]
) -> tuple[list[int], list[Number], Optional[Number]]:
    """Order jobs on one machine to minimize the maximum lateness (1||Lmax).

    Job j has processing time p[j] >= 0 and due date d[j]. The jobs run back to
    back from time 0 in order of nondecreasing due date, ties by index. The result
    is the order, the completion time of each job, and Lmax = max(C[j] - d[j]),
    which is None when there are no jobs.

    Cost: O(n log n) for the sort and O(n) for the scan.
    """
    if len(p) != len(d):
        raise ValueError("p and d must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    n = len(p)
    order = sorted(range(n), key=lambda j: (d[j], j))  # @line L1
    t: Number = 0  # @line L2
    lmax: Optional[Number] = None
    completion: list[Number] = [0] * n
    for j in order:  # @line L3
        t = t + p[j]  # @line L4
        completion[j] = t
        late = t - d[j]  # @line L5
        if lmax is None or late > lmax:
            lmax = late
    return order, completion, lmax  # @line L6


def max_lateness(p: Sequence[Number], d: Sequence[Number], order: Sequence[int]) -> Optional[Number]:
    """Return Lmax of the given order run back to back from time 0."""
    t: Number = 0
    best: Optional[Number] = None
    for j in order:
        t = t + p[j]
        if best is None or t - d[j] > best:
            best = t - d[j]
    return best
