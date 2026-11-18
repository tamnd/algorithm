# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-larmore-algorithm/. The authors are listed in prov/HFGGSH.jsonl.

"""The least weight subsequence problem for a concave weight, in O(n log n).

F(0) = 0 and F(j) = min over 0 <= i < j of F(i) + w(i, j), for j = 1 .. n.

The weight w is concave in the sense of Hirschberg and Larmore:
w(i, j) + w(i', j') <= w(i, j') + w(i', j) for all i <= i' < j <= j'.
(This is the quadrangle inequality of a Monge array; some authors call it
convex.) Then a later candidate that is at least as good as an earlier one
at some j stays at least as good at every later j. So each candidate i is
the best one for an interval of j, and the intervals are in the order of
the candidates. A queue holds the live candidates with the first j of
their interval. A new candidate removes the candidates at the back that it
beats on their whole interval, and finds the start of its own interval by
binary search.

w may return math.inf for a pair (i, j) that is not allowed, if the pairs
with an infinite weight are closed under making the interval longer: if
w(i, j) is infinite, so is w(i', j') for all i' <= i and j' >= j. A line
that is too long for the measure is the usual case.
"""

import math
from collections import deque
from typing import Callable, List, Optional, Tuple

Weight = Callable[[int, int], float]


def lws_dp(n: int, w: Weight, stats: Optional[dict] = None) -> Tuple[List, List[int]]:
    """The O(n^2) dynamic program. Returns F[0..n] and the best predecessor P[1..n]."""
    F = [0] + [math.inf] * n
    P = [0] * (n + 1)
    evals = 0
    for j in range(1, n + 1):
        for i in range(j):
            evals += 1
            v = F[i] + w(i, j)
            if v < F[j]:
                F[j], P[j] = v, i
    if stats is not None:
        stats["evals"] = evals
    return F, P


def hirschberg_larmore(n: int, w: Weight, stats: Optional[dict] = None) -> Tuple[List, List[int]]:
    """F[0..n] and P[1..n] for a concave w, with O(n log n) evaluations of w."""
    evals = 0

    def g(i: int, j: int):
        nonlocal evals
        evals += 1
        return F[i] + w(i, j)

    F = [0] + [math.inf] * n  # @line L1
    P = [0] * (n + 1)
    Q = deque([(0, 1)])  # (candidate i, first j of its interval)  # @line L2
    for j in range(1, n + 1):  # @line L3
        while len(Q) >= 2 and Q[1][1] <= j:  # @line L4
            Q.popleft()
        i = Q[0][0]
        F[j], P[j] = g(i, j), i  # @line L5
        if j == n:
            break
        while Q:  # @line L6
            i, s = Q[-1]
            s = max(s, j + 1)
            if g(j, s) <= g(i, s):  # @line L7
                Q.pop()  # j is at least as good on all of the interval of i
                continue
            lo, hi = s + 1, n + 1  # @line L8
            while lo < hi:  # find the least c in s+1 .. n where j beats i
                mid = (lo + hi) // 2
                if g(j, mid) <= g(i, mid):
                    hi = mid
                else:
                    lo = mid + 1
            if lo <= n:
                Q.append((j, lo))  # @line L9
            break
        if not Q:
            Q.append((j, j + 1))  # @line L10
    if stats is not None:
        stats["evals"] = evals
    return F, P


def breaks(P: List[int], n: int) -> List[int]:
    """The chosen indices i_1 < ... < i_k = n, read back from the predecessors."""
    out = []
    j = n
    while j > 0:
        out.append(j)
        j = P[j]
    return out[::-1]
