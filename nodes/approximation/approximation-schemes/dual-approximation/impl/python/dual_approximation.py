# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dual-approximation/. The authors are listed in prov/DPDS4B.jsonl.

"""The dual approximation framework: a binary search over sorted candidate targets with a rho-dual test."""

from typing import Callable, Optional, Sequence, TypeVar

S = TypeVar("S")


def dual_search(candidates: Sequence[int], test: Callable[[int], Optional[S]]) -> tuple[S, int, int]:
    """candidates is sorted, OPT is one of them, and test(T) returns a solution or None (a proof that OPT > T).

    Return (solution, the target it was found for, the number of calls)."""
    lo, hi = -1, len(candidates) - 1  # OPT > candidates[lo] (lo = -1 means no bound), OPT <= candidates[hi]
    best = test(candidates[hi])
    calls = 1
    if best is None:
        raise ValueError("the test rejected the largest candidate, so OPT is not among the candidates")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        s = test(candidates[mid])
        calls += 1
        if s is None:
            lo = mid
        else:
            hi, best = mid, s
    return best, candidates[hi], calls


def makespan_two_dual(p: Sequence[int], m: int, t: int) -> Optional[list[int]]:
    """A 2-dual test for P || C_max: a schedule with makespan at most 2t, or None, which proves OPT > t."""
    if max(p) > t or sum(p) > m * t:
        return None
    load = [0] * m
    machine = []
    for pj in p:
        i = min(range(m), key=lambda q: load[q])
        machine.append(i)
        load[i] += pj
    return machine


def kcenter_two_dual(dist: Sequence[Sequence[int]], k: int, r: int) -> Optional[list[int]]:
    """A 2-dual test for k-center: at most k centers within 2r of each point, or None, which proves OPT > r."""
    n = len(dist)
    centers: list[int] = []
    for v in range(n):
        if all(dist[v][c] > 2 * r for c in centers):
            centers.append(v)
            if len(centers) > k:
                return None
    return centers


def makespan_dual_approximation(p: Sequence[int], m: int) -> tuple[list[int], int, int]:
    lb = max(max(p), -(-sum(p) // m))
    return dual_search(list(range(lb, 2 * lb + 1)), lambda t: makespan_two_dual(p, m, t))


def kcenter_dual_approximation(dist: Sequence[Sequence[int]], k: int) -> tuple[list[int], int, int]:
    values = sorted({d for row in dist for d in row})
    return dual_search(values, lambda r: kcenter_two_dual(dist, k, r))
