# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnsons-rule/. The authors are listed in prov/7Y0GYX.jsonl.

from typing import Sequence


def johnsons_rule(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """Johnson's rule for F2||Cmax.

    Job j needs a[j] on machine 1, then b[j] on machine 2. The jobs with
    a[j] <= b[j] go first, in increasing a[j]; the other jobs follow, in
    decreasing b[j]. Ties go by index. Cost: O(n log n) time, O(n) space.
    """
    if len(a) != len(b):
        raise ValueError("a and b must have the same length")
    if any(x < 0 for x in a) or any(x < 0 for x in b):
        raise ValueError("processing times must be nonnegative")
    first = [j for j in range(len(a)) if a[j] <= b[j]]  # @line L1
    last = [j for j in range(len(a)) if a[j] > b[j]]  # @line L2
    first.sort(key=lambda j: (a[j], j))  # @line L3
    last.sort(key=lambda j: (-b[j], j))  # @line L4
    return first + last  # @line L5


def makespan(a: Sequence[int], b: Sequence[int], order: Sequence[int]) -> int:
    """The makespan of the permutation schedule that runs both machines in this order
    and starts each operation as early as possible."""
    t1 = t2 = 0  # @line L6
    for j in order:  # @line L7
        t1 += a[j]  # @line L8
        t2 = max(t2, t1) + b[j]  # @line L9
    return t2  # @line L10


def gantt(a: Sequence[int], b: Sequence[int], order: Sequence[int]) -> list[tuple[int, int, int, int, int]]:
    """For each job in order: (job, start on 1, end on 1, start on 2, end on 2)."""
    rows = []
    t1 = t2 = 0
    for j in order:
        s1, t1 = t1, t1 + a[j]
        s2 = max(t2, t1)
        t2 = s2 + b[j]
        rows.append((j, s1, t1, s2, t2))
    return rows
