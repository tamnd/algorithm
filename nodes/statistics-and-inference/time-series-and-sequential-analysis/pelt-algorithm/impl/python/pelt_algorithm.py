# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pelt-algorithm/. The authors are listed in prov/8P0SSC.jsonl.
"""PELT: pruned exact linear time search for multiple change points.

Minimize sum over segments of C(segment) + beta * (number of change points)
over all partitions of x_1..x_n into contiguous segments. The optimal
partitioning recursion is F(0) = -beta and
F(t) = min over 0 <= s < t of F(s) + C(s+1..t) + beta. PELT keeps only the
candidates s that can still be optimal: s is dropped at time t when
F(s) + C(s+1..t) + K > F(t). With a cost that satisfies
C(a..b) + K <= C(a..s) + C(s+1..b) for all a <= s < b, a dropped candidate is
never optimal later, so PELT returns the same optimum as the full O(n^2)
recursion. Worst case O(n^2) cost evaluations; the expected linear cost holds
only under conditions on the data (Killick, Fearnhead and Eckley 2012).
"""

from collections.abc import Callable, Sequence
from fractions import Fraction
from typing import TypeVar

Num = TypeVar("Num", float, Fraction)


def rss_cost(xs: Sequence[Num]) -> Callable[[int, int], Num]:
    """C(s+1..t) = sum of (x_i - segment mean)^2 for i in s+1..t, via prefix sums. O(1) per call.

    This is twice the Gaussian negative log likelihood with unit variance, up
    to a constant per point, and it satisfies the PELT condition with K = 0.
    """
    zero = xs[0] - xs[0] if xs else 0
    s1 = [zero]
    s2 = [zero]
    for x in xs:
        s1.append(s1[-1] + x)
        s2.append(s2[-1] + x * x)

    def cost(s: int, t: int) -> Num:
        tot = s1[t] - s1[s]
        return s2[t] - s2[s] - tot * tot / (t - s)

    return cost


def pelt(n: int, cost: Callable[[int, int], Num], beta: Num, k: Num = 0,
         sizes: list[int] | None = None) -> tuple[Num, list[int]]:
    """Optimal penalized partition of 1..n. Returns (F(n), sorted change points).

    cost(s, t) is the cost of the segment x_(s+1)..x_t. A change point tau
    means a new segment starts at tau + 1. Ties choose the smallest s. If
    sizes is a list, the candidate set size at each t is appended to it.
    """
    f = [-beta] + [None] * n  # @line L1
    last = [0] * (n + 1)  # @line L1
    cand = [0]  # @line L1
    for t in range(1, n + 1):  # @line L2
        vals = [(f[s] + cost(s, t) + beta, s) for s in cand]  # @line L3
        best, arg = min(vals)
        f[t] = best  # @line L3
        last[t] = arg  # @line L4
        if sizes is not None:
            sizes.append(len(cand))
        cand = [s for v, s in vals if v - beta + k <= best] + [t]  # @line L5
    cps = []
    t = n
    while t > 0:  # @line L6
        t = last[t]
        if t > 0:
            cps.append(t)
    return f[n], sorted(cps)  # @line L6


def optimal_partitioning(n: int, cost: Callable[[int, int], Num], beta: Num) -> tuple[Num, list[int]]:
    """The full O(n^2) recursion of Jackson et al. (2005), with the same tie rule."""
    f = [-beta] + [None] * n
    last = [0] * (n + 1)
    for t in range(1, n + 1):
        f[t], last[t] = min((f[s] + cost(s, t) + beta, s) for s in range(t))
    cps = []
    t = n
    while t > 0:
        t = last[t]
        if t > 0:
            cps.append(t)
    return f[n], sorted(cps)
