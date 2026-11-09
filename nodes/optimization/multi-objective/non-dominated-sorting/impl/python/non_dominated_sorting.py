# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-dominated-sorting/. The authors are listed in prov/PQCHE1.jsonl.

"""Non-dominated sorting: split a list of objective vectors into Pareto fronts.

All objectives are minimized. A point a dominates b when a[i] <= b[i] for each
objective i and a[i] < b[i] for at least one i. Front 1 holds the points that no
point dominates. Front k holds the points that no point outside fronts 1 to k - 1
dominates. Equal points never dominate each other, so they share a front.
"""

from typing import Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for x, y in zip(a, b):
        if x > y:
            return False
        if x < y:
            strict = True
    return strict


def fast_non_dominated_sort(points: Sequence[Vector]) -> list[list[int]]:
    """Deb's fast non-dominated sort. Return the fronts as lists of indices.

    Time O(p N^2) and space O(N^2) for N points with p objectives.
    """
    n = len(points)
    dominated_by_me: list[list[int]] = [[] for _ in range(n)]  # @line L1
    count = [0] * n  # @line L1
    for i in range(n):  # @line L2
        for j in range(i + 1, n):  # @line L3
            if dominates(points[i], points[j]):  # @line L4
                dominated_by_me[i].append(j)
                count[j] += 1
            elif dominates(points[j], points[i]):  # @line L5
                dominated_by_me[j].append(i)
                count[i] += 1
    current = [i for i in range(n) if count[i] == 0]  # @line L6
    fronts: list[list[int]] = []
    while current:  # @line L7
        fronts.append(current)
        nxt: list[int] = []  # @line L8
        for i in current:  # @line L9
            for j in dominated_by_me[i]:  # @line L10
                count[j] -= 1  # @line L11
                if count[j] == 0:  # @line L12
                    nxt.append(j)
        current = nxt  # @line L13
    return fronts  # @line L14


def non_dominated_sort_2d(points: Sequence[Vector]) -> list[list[int]]:
    """Sort two-objective points into fronts in O(N log N) time.

    Visit the points in lexicographic order of (f1, f2). Each front keeps the
    last point added to it. A point goes to the first front whose last point
    does not dominate it. The predicate "the last point of front k dominates
    the new point" is true for a prefix of the fronts, so a binary search
    finds the place.
    """
    order = sorted(range(len(points)), key=lambda i: (points[i][0], points[i][1]))
    fronts: list[list[int]] = []
    last_f1: list[float] = []  # f1 of the last point of each front
    last_f2: list[float] = []  # f2 of the last point of each front
    for i in order:
        y1, y2 = points[i][0], points[i][1]
        # The last point (a, b) of a front comes before (y1, y2) in the order,
        # so a <= y1. It dominates (y1, y2) iff b < y2, or b == y2 and a < y1.
        lo, hi = 0, len(fronts)
        while lo < hi:
            mid = (lo + hi) // 2
            if last_f2[mid] < y2 or (last_f2[mid] == y2 and last_f1[mid] < y1):
                lo = mid + 1
            else:
                hi = mid
        if lo == len(fronts):
            fronts.append([])
            last_f1.append(y1)
            last_f2.append(y2)
        fronts[lo].append(i)
        last_f1[lo] = y1
        last_f2[lo] = y2
    for f in fronts:
        f.sort()
    return fronts


def ranks_from_fronts(fronts: list[list[int]], n: int) -> list[int]:
    """Return rank[i] = k when point i is in front k (fronts count from 1)."""
    rank = [0] * n
    for k, front in enumerate(fronts, start=1):
        for i in front:
            rank[i] = k
    return rank
