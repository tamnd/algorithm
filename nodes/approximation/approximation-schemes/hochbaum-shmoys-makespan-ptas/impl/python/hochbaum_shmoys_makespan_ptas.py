# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hochbaum-shmoys-makespan-ptas/. The authors are listed in prov/AYZTA8.jsonl.

"""Hochbaum-Shmoys PTAS for P || C_max: a (1 + 1/k)-dual test and a binary search over the target T."""

from fractions import Fraction
from itertools import product
from typing import Optional, Sequence


def dual_test(p: Sequence[int], m: int, t: int, k: int, stats: Optional[dict] = None) -> Optional[list[int]]:
    """Return a machine for each job, with makespan at most (1 + 1/k) t, or None, which proves OPT > t."""
    n = len(p)
    if any(pj > t for pj in p):  # @line L1
        return None
    u = Fraction(t, k * k)  # @line L2
    large = [j for j in range(n) if p[j] * k > t]  # @line L3
    small = [j for j in range(n) if p[j] * k <= t]
    rounded = {j: (p[j] // u) * u for j in large}  # @line L4
    sizes = sorted(set(rounded.values()))
    index = {s: i for i, s in enumerate(sizes)}
    d = len(sizes)
    count = [0] * d
    for j in large:
        count[index[rounded[j]]] += 1
    # @line L5: the configurations are the non-empty count vectors whose rounded load is at most t
    configs = [c for c in product(*(range(ci + 1) for ci in count))
               if any(c) and sum(ci * s for ci, s in zip(c, sizes)) <= t]
    # @line L6: M[v] is the least number of machines that hold the vector v of rounded large jobs
    best: dict[tuple[int, ...], int] = {}
    choice: dict[tuple[int, ...], tuple[int, ...]] = {}
    for v in product(*(range(ci + 1) for ci in count)):
        if not any(v):
            best[v] = 0
            continue
        b = None
        for c in configs:
            if all(ci <= vi for ci, vi in zip(c, v)):
                w = tuple(vi - ci for vi, ci in zip(v, c))
                if b is None or best[w] + 1 < b:
                    b, choice[v] = best[w] + 1, c
        best[v] = b
    if stats is not None:
        stats.update(states=len(best), configs=len(configs), sizes=d, large=len(large))
    target = tuple(count)
    if best[target] > m:  # @line L7
        return None
    pools: list[list[int]] = [[] for _ in range(d)]
    for j in large:
        pools[index[rounded[j]]].append(j)
    machine = [-1] * n
    load = [0] * m
    v, i = target, 0
    while any(v):  # @line L8
        c = choice[v]
        for t_i, ct in enumerate(c):
            for _ in range(ct):
                j = pools[t_i].pop()
                machine[j] = i
                load[i] += p[j]
        v = tuple(vi - ci for vi, ci in zip(v, c))
        i += 1
    for j in small:  # @line L9
        i = min(range(m), key=lambda q: load[q])
        if load[i] > t:
            return None
        machine[j] = i
        load[i] += p[j]
    return machine  # @line L10


def makespan(p: Sequence[int], m: int, machine: Sequence[int]) -> int:
    load = [0] * m
    for j, i in enumerate(machine):
        load[i] += p[j]
    return max(load) if load else 0


def hochbaum_shmoys_makespan_ptas(p: Sequence[int], m: int, k: int) -> tuple[list[int], int]:
    """Schedule positive integer jobs on m machines with makespan at most (1 + 1/k) OPT. Return (machine of each job, calls)."""
    if not p:
        return [], 0
    lb = max(max(p), -(-sum(p) // m))  # @line B1
    lo, hi = lb - 1, 2 * lb  # @line B2: OPT > lo and OPT <= hi
    sched = dual_test(p, m, hi, k)
    calls = 1
    while hi - lo > 1:  # @line B3
        mid = (lo + hi) // 2
        s = dual_test(p, m, mid, k)
        calls += 1
        if s is None:
            lo = mid  # @line B4: OPT > mid
        else:
            hi, sched = mid, s  # @line B5
    assert sched is not None
    return sched, calls  # @line B6
