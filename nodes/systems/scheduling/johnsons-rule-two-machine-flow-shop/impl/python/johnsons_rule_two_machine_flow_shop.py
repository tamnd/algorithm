# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnsons-rule-two-machine-flow-shop/. The authors are listed in prov/8HDKEZ.jsonl.

import itertools
from typing import Optional, Sequence


def johnson_smallest_time(a: Sequence[int], b: Sequence[int]) -> list[int]:
    """Johnson's 1954 procedure for F2||Cmax, in its original form.

    Look at all 2n times in increasing order. If the smallest time of a job that
    is not yet placed is its machine 1 time a[j], put the job at the front of the
    free positions; if it is its machine 2 time b[j], put the job at the back.
    Ties: smaller value first, then machine 1 before machine 2, then smaller index.
    Cost: O(n log n) time for the sort of the 2n times, O(n) space.
    """
    n = len(a)
    if len(b) != n:
        raise ValueError("a and b must have the same length")
    times = sorted([(a[j], 0, j) for j in range(n)] + [(b[j], 1, j) for j in range(n)])  # @line L1
    slots: list[Optional[int]] = [None] * n
    lo, hi = 0, n - 1  # @line L2
    placed = [False] * n
    for _, machine, j in times:  # @line L3
        if placed[j]:  # @line L4
            continue
        placed[j] = True  # @line L5
        if machine == 0:  # @line L6
            slots[lo] = j
            lo += 1
        else:  # @line L7
            slots[hi] = j
            hi -= 1
    return [j for j in slots if j is not None]  # @line L8


def makespan_of_orders(p: Sequence[Sequence[int]], orders: Sequence[Sequence[int]]) -> int:
    """The makespan of a flow shop schedule in which machine i runs the jobs in
    orders[i], each operation as early as possible.

    p[i][j] is the time of job j on machine i; every job visits machines 0, 1, ...
    in this order. Any choice of machine orders is feasible in a flow shop.
    """
    m = len(p)
    n = len(p[0]) if m else 0
    done = [0] * n  # finish time of each job on the previous machine
    end = 0
    for i in range(m):
        free = 0
        new_done = [0] * n
        for j in orders[i]:
            free = max(free, done[j]) + p[i][j]
            new_done[j] = free
        done = new_done
        end = max(end, free)
    return end


def best_permutation_makespan(p: Sequence[Sequence[int]]) -> int:
    """The least makespan over permutation schedules (the same order on every machine)."""
    n = len(p[0])
    return min(makespan_of_orders(p, [o] * len(p)) for o in itertools.permutations(range(n)))


def best_schedule_makespan(p: Sequence[Sequence[int]]) -> int:
    """The least makespan over all schedules: an independent order on each machine.
    Only for tiny instances: (n!)^m choices."""
    n = len(p[0])
    perms = list(itertools.permutations(range(n)))
    return min(makespan_of_orders(p, orders) for orders in itertools.product(perms, repeat=len(p)))
