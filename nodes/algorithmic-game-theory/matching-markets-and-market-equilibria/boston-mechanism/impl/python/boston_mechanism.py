# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boston-mechanism/. The authors are listed in prov/GWGCR1.jsonl.
"""The Boston mechanism (immediate acceptance) for school choice.

Students are 0, ..., n - 1 and schools are 0, ..., m - 1. prefs[i] is the list of the schools
that student i reports as acceptable, best first; it may be shorter than m. priority[s] is a
ranking of all n students for school s, best first. capacity[s] is the number of seats of
school s. The result gives, for each student, the school she gets or None.
"""

from typing import Optional


def boston(
    prefs: list[tuple[int, ...]],
    priority: list[tuple[int, ...]],
    capacity: list[int],
    trace: Optional[list] = None,
) -> list[Optional[int]]:
    """Return the Boston assignment: in round k each unassigned student applies to her k-th
    choice, and each school accepts applicants by priority up to its remaining seats, for good.

    If trace is a list, the function appends, for each round k = 1, 2, ..., the dict of the
    students accepted in that round, keyed by school. O(n m + n log n) time per instance with
    the sort in line L5 done once per school and round.
    """
    n, m = len(prefs), len(capacity)
    if len(priority) != m:
        raise ValueError("one priority ranking per school")
    for s in range(m):
        if sorted(priority[s]) != list(range(n)):
            raise ValueError("a priority ranking must list every student once")
        if capacity[s] < 0:
            raise ValueError("capacities must be nonnegative")
    for lst in prefs:
        if len(set(lst)) != len(lst) or any(not 0 <= s < m for s in lst):
            raise ValueError("a preference list repeats a school or is out of range")
    rank = [[0] * n for _ in range(m)]
    for s in range(m):
        for r, i in enumerate(priority[s]):
            rank[s][i] = r
    left = list(capacity)  # @line L1
    assigned: list[Optional[int]] = [None] * n
    unassigned = set(range(n))
    for k in range(m):  # @line L2
        applicants: dict[int, list[int]] = {}
        for i in sorted(unassigned):  # @line L3
            if k < len(prefs[i]):
                applicants.setdefault(prefs[i][k], []).append(i)
        accepted_now: dict[int, list[int]] = {}
        for s, group in sorted(applicants.items()):  # @line L4
            group.sort(key=lambda i: rank[s][i])  # @line L5
            take = group[: left[s]]
            for i in take:
                assigned[i] = s
                unassigned.discard(i)
            left[s] -= len(take)  # @line L6
            if take:
                accepted_now[s] = take
        if trace is not None:
            trace.append(accepted_now)
    return assigned  # @line L7


def first_choice_count(prefs: list[tuple[int, ...]], assigned: list[Optional[int]]) -> int:
    """Return the number of students who get the first school on their reported list."""
    return sum(1 for i, s in enumerate(assigned) if s is not None and prefs[i] and prefs[i][0] == s)
