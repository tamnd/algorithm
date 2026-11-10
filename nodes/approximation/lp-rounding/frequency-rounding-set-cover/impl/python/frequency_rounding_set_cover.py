# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-rounding-set-cover/. The authors are listed in prov/7N315T.jsonl.

from fractions import Fraction
from typing import Iterable, Sequence


def _simplex_max(
    c: Sequence[Fraction], a: Sequence[Sequence[Fraction]], b: Sequence[Fraction]
) -> tuple[Fraction, list[Fraction]] | None:
    """Maximize c.x subject to a x <= b and x >= 0, exactly.

    A dense two-phase tableau simplex with Bland's rule, in exact rational
    arithmetic. It returns (value, x) for an optimal basic solution, or None
    if the LP is infeasible. It is meant for small instances only.
    """
    m, n = len(a), len(c)
    arts = [i for i in range(m) if b[i] < 0]
    ncol = n + m + len(arts)
    t: list[list[Fraction]] = []
    basis: list[int] = []
    for i in range(m):
        s = -1 if b[i] < 0 else 1
        row = [Fraction(s * v) for v in a[i]] + [Fraction(0)] * (m + len(arts)) + [Fraction(s * b[i])]
        row[n + i] = Fraction(s)
        if b[i] < 0:
            k = n + m + arts.index(i)
            row[k] = Fraction(1)
            basis.append(k)
        else:
            basis.append(n + i)
        t.append(row)

    def pivot(i: int, j: int) -> None:
        p = t[i][j]
        t[i] = [v / p for v in t[i]]
        for k in range(len(t)):
            if k != i and t[k][j] != 0:
                f = t[k][j]
                t[k] = [u - f * v for u, v in zip(t[k], t[i])]
        basis[i] = j

    def run(cost: list[Fraction], cols: int) -> None:
        while True:
            enter = None
            for j in range(cols):
                if j in basis:
                    continue
                z = sum(cost[basis[i]] * t[i][j] for i in range(len(t)))
                if cost[j] - z > 0:
                    enter = j
                    break
            if enter is None:
                return
            best = None
            for i in range(len(t)):
                if t[i][enter] > 0:
                    q = t[i][-1] / t[i][enter]
                    if best is None or q < best[0] or (q == best[0] and basis[i] < basis[best[1]]):
                        best = (q, i)
            if best is None:
                raise ValueError("the LP is unbounded")
            pivot(best[1], enter)

    if arts:
        cost1 = [Fraction(0)] * (n + m) + [Fraction(-1)] * len(arts)
        run(cost1, ncol)
        if sum(cost1[basis[i]] * t[i][-1] for i in range(len(t))) < 0:
            return None
        i = 0
        while i < len(t):
            if basis[i] >= n + m:
                j = next((j for j in range(n + m) if t[i][j] != 0), None)
                if j is None:
                    del t[i]
                    del basis[i]
                    continue
                pivot(i, j)
            i += 1
    cost2 = [Fraction(v) for v in c] + [Fraction(0)] * (m + len(arts))
    run(cost2, n + m)
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = t[i][-1]
    return sum((Fraction(ci) * xi for ci, xi in zip(c, x)), Fraction(0)), x


def solve_set_cover_lp(
    n: int, sets: Sequence[Iterable[int]], costs: Sequence[int | Fraction]
) -> tuple[Fraction, list[Fraction]]:
    """Return (LP*, x) for: min sum c_j x_j s.t. sum_{j : e in S_j} x_j >= 1 for each e, x >= 0."""
    members = [set(s) for s in sets]
    a = [[Fraction(-1) if e in members[j] else Fraction(0) for j in range(len(sets))] for e in range(n)]
    res = _simplex_max([-Fraction(c) for c in costs], a, [Fraction(-1)] * n)
    if res is None:
        raise ValueError("some element is in no set")
    val, x = res
    return -val, x


def frequency_rounding_set_cover(
    n: int, sets: Sequence[Iterable[int]], costs: Sequence[int | Fraction]
) -> tuple[set[int], list[Fraction], Fraction, int]:
    """Return (I, x, LP*, f): the chosen set indices, the LP solution, its value and f.

    The universe is 0 .. n - 1. Precondition: costs are non-negative and each
    element is in some set (else ValueError). f is the largest number of sets
    that hold one element. The sets with x_j >= 1/f form a cover of cost at
    most f LP* <= f OPT. Cost: one LP solve (an exact simplex here, for small
    instances only) and O(total size of the sets) other work.
    """
    members = [set(s) for s in sets]
    if any(c < 0 for c in costs):
        raise ValueError("costs must be non-negative")
    freq = [sum(1 for s in members if e in s) for e in range(n)]
    if any(k == 0 for k in freq):
        raise ValueError("some element is in no set")
    if n == 0:
        return set(), [Fraction(0)] * len(sets), Fraction(0), 0
    f = max(freq)  # @line L1
    lp_value, x = solve_set_cover_lp(n, members, costs)  # @line L2
    chosen: set[int] = set()  # @line L3
    for j in range(len(sets)):  # @line L4
        if x[j] >= Fraction(1, f):  # @line L5
            chosen.add(j)
    return chosen, x, lp_value, f  # @line L6
