# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multifit-algorithm/. The authors are listed in prov/9QD5G8.jsonl.

from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]


def first_fit_decreasing(p: list[Number], c: Number, m: int) -> Optional[list[list[int]]]:
    """FFD with bin capacity c, stopped as soon as it needs more than m bins.

    The jobs are taken by non-increasing size (ties keep the input order). Each
    job goes into the first open bin where it fits; if none, a new bin opens.
    Returns the bins (lists of job indices), or None when more than m bins are
    needed or a job is larger than c. Cost: O(n log n + n m) time.
    """
    order = sorted(range(len(p)), key=lambda j: -p[j])  # @line L8
    bins: list[list[int]] = []
    fill: list[Number] = []
    for j in order:  # @line L9
        for b in range(len(bins)):  # @line L10
            if fill[b] + p[j] <= c:
                bins[b].append(j)
                fill[b] += p[j]
                break
        else:
            if len(bins) == m or p[j] > c:  # @line L11
                return None
            bins.append([j])
            fill.append(p[j])
    return bins


def multifit_algorithm(p: list[Number], m: int, k: int) -> tuple[list[int], Fraction]:
    """MULTIFIT (Coffman, Garey and Johnson 1978) for P||C_max.

    Binary search, k steps, on the bin capacity C, with FFD into m bins as
    the test. Precondition: m >= 1, k >= 0, every p[j] >= 0.
    Returns (machine, hi): machine[j] is the 0-based machine of job j, and hi
    is the final capacity; the makespan is at most hi.
    Cost: O(n log n + k n m) time (the sort can be shared), O(n + m) space.
    """
    if m < 1 or k < 0:
        raise ValueError("need m >= 1 and k >= 0")
    if not p:
        return [], Fraction(0)
    avg = Fraction(sum(p), m)  # @line L1
    lo = max(avg, Fraction(max(p)))  # @line L2
    hi = max(2 * avg, Fraction(max(p)))
    for _ in range(k):  # @line L3
        c = (lo + hi) / 2  # @line L4
        if first_fit_decreasing(p, c, m) is not None:  # @line L5
            hi = c
        else:
            lo = c  # @line L6
    bins = first_fit_decreasing(p, hi, m)  # @line L7
    assert bins is not None, "FFD fits at the upper end of the search"
    machine = [-1] * len(p)
    for i, b in enumerate(bins):
        for j in b:
            machine[j] = i
    return machine, hi
