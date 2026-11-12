# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dominant-resource-fairness/. The authors are listed in prov/DB84HW.jsonl.

from fractions import Fraction
from typing import Sequence


def dominant_unit(capacity: Sequence[int], demand: Sequence[int]) -> Fraction:
    """Dominant share of one task: max over resources of demand / capacity."""
    return max(Fraction(d, c) for d, c in zip(demand, capacity))


def drf(capacity: Sequence[int], demands: Sequence[Sequence[int]]) -> list[Fraction]:
    """Dominant resource fairness by progressive filling (Ghodsi et al., NSDI 2011).

    capacity[r] > 0 is the amount of resource r; demands[i][r] >= 0 is what
    one task of user i needs, with at least one positive entry. Tasks are
    divisible. All users that are not frozen raise their dominant shares at
    the same rate; when a resource is used up, every user that needs it is
    frozen. Return the (fractional) number of tasks of each user, exactly.
    """
    m, n = len(capacity), len(demands)
    if m == 0 or min(capacity) <= 0:
        raise ValueError("need positive capacities")
    for d in demands:
        if len(d) != m or min(d) < 0 or max(d) == 0:
            raise ValueError("each demand needs m non-negative entries, one positive")
    unit = [dominant_unit(capacity, d) for d in demands]
    tasks = [Fraction(0)] * n
    frozen = [False] * n
    level = Fraction(0)  # @line L1
    while not all(frozen):  # @line L2
        # use of resource r at level s: fixed part plus s * rate
        best, full = None, []
        for r in range(m):  # @line L3
            fixed = sum(tasks[i] * demands[i][r] for i in range(n) if frozen[i])
            rate = sum(Fraction(demands[i][r]) / unit[i] for i in range(n) if not frozen[i])
            if rate == 0:
                continue
            s = (capacity[r] - fixed) / rate
            if best is None or s < best:
                best, full = s, [r]
            elif s == best:
                full.append(r)
        level = best  # @line L4
        for i in range(n):  # @line L5
            if not frozen[i]:
                tasks[i] = level / unit[i]
                if any(demands[i][r] > 0 for r in full):  # @line L6
                    frozen[i] = True
    return tasks


def dominant_shares(capacity, demands, tasks) -> list[Fraction]:
    return [t * dominant_unit(capacity, d) for t, d in zip(tasks, demands)]


def drf_discrete(capacity: Sequence[int], demands: Sequence[Sequence[int]]) -> list[int]:
    """The paper's Algorithm 1 for whole tasks: give the next task to the
    user with the lowest dominant share (ties to the lower index), and stop
    when that task does not fit."""
    m, n = len(capacity), len(demands)
    unit = [dominant_unit(capacity, d) for d in demands]
    used = [0] * m
    tasks = [0] * n
    while n:
        i = min(range(n), key=lambda k: (tasks[k] * unit[k], k))
        if any(used[r] + demands[i][r] > capacity[r] for r in range(m)):
            return tasks
        for r in range(m):
            used[r] += demands[i][r]
        tasks[i] += 1
    return tasks
