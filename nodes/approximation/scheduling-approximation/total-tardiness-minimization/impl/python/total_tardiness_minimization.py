# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-tardiness-minimization/. The authors are listed in prov/0G2W28.jsonl.

"""1||sum T_j: Lawler's decomposition algorithm and Lawler's FPTAS by scaling."""

from fractions import Fraction
from typing import Sequence


def total_tardiness(p: Sequence, d: Sequence, order: Sequence[int], start=0):
    """Sum of max(0, C_j - d_j) when the order runs back to back from time start."""
    t, s = start, 0
    for j in order:
        t += p[j]
        if t > d[j]:
            s += t - d[j]
    return s


def lawler_decomposition(p: Sequence[int], d: Sequence, ) -> tuple[list[int], object]:
    """Exact: return (an optimal order, its total tardiness).

    Jobs are indexed in EDD order. Let k be a longest job of the current set
    (the last one in EDD order among the longest). Some optimal order puts k
    right after the jobs of the set up to position b in EDD order, for some
    b at or after the position of k, and the remaining jobs after k. The
    memo is keyed by the job set and the start time. Pseudo-polynomial.
    """
    n = len(p)
    if len(d) != n:
        raise ValueError("p and d must have the same length")
    if any(x < 0 for x in p):
        raise ValueError("processing times must be nonnegative")
    edd = tuple(sorted(range(n), key=lambda j: (d[j], j)))  # @line L1
    memo: dict = {}

    def solve(jobs: tuple, t):
        # jobs is a tuple in EDD order, t the start time
        if not jobs:  # @line L2
            return 0, ()
        key = (jobs, t)
        if key in memo:
            return memo[key]
        a = max(range(len(jobs)), key=lambda i: (p[jobs[i]], i))  # @line L3
        k = jobs[a]
        best = None
        for b in range(a, len(jobs)):  # @line L4
            before = jobs[:a] + jobs[a + 1:b + 1]
            after = jobs[b + 1:]
            ck = t + sum(p[j] for j in before) + p[k]  # @line L5
            v1, o1 = solve(before, t)
            v2, o2 = solve(after, ck)
            v = v1 + max(0, ck - d[k]) + v2  # @line L6
            if best is None or v < best[0]:
                best = (v, o1 + (k,) + o2)
        memo[key] = best
        return best  # @line L7

    value, order = solve(edd, 0)
    return list(order), value


def fptas(p: Sequence[int], d: Sequence[int], eps) -> tuple[list[int], object]:
    """Return (order, total tardiness) with total tardiness <= (1 + eps) OPT.

    Scale by K = 2 eps Tmax / (n (n + 1)), where Tmax is the largest
    tardiness in the EDD order, round the processing times down, solve the
    scaled instance exactly, and use its order for the original jobs.
    This simple version runs in time O(n^4 sum(p') ), which is not always
    polynomial; Lawler (1982) shows how to get O(n^7 / eps).
    """
    n = len(p)
    eps = Fraction(eps)
    if eps <= 0:
        raise ValueError("eps must be positive")
    edd = sorted(range(n), key=lambda j: (d[j], j))
    t, tmax = 0, 0
    for j in edd:
        t += p[j]
        tmax = max(tmax, t - d[j])
    if tmax == 0:
        return edd, 0
    K = 2 * eps * tmax / (n * (n + 1))
    if K <= 1:
        order, value = lawler_decomposition(p, d)
        return order, value
    ps = [int(Fraction(x) / K) for x in p]
    ds = [Fraction(x) / K for x in d]
    order, _ = lawler_decomposition(ps, ds)
    return order, total_tardiness(p, d, order)
