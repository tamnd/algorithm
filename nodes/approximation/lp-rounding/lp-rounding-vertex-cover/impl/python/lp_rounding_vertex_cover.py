# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lp-rounding-vertex-cover/. The authors are listed in prov/SNS1K9.jsonl.

from fractions import Fraction
from typing import Sequence


def _simplex_max(
    c: Sequence[Fraction], a: Sequence[Sequence[Fraction]], b: Sequence[Fraction]
) -> tuple[Fraction, list[Fraction]] | None:
    """Maximize c.x subject to a x <= b and x >= 0, exactly.

    A dense two-phase tableau simplex with Bland's rule, in exact rational
    arithmetic. It returns (value, x) for an optimal basic solution, or None
    if the LP is infeasible. It is meant for small instances only: the
    number of pivots can be exponential in the worst case.
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


def solve_vertex_cover_lp(
    weights: Sequence[int | Fraction], edges: Sequence[tuple[int, int]]
) -> tuple[Fraction, list[Fraction]]:
    """Return (LP*, x): the optimum and an optimal vertex of the vertex cover LP.

    The LP is: minimize sum w(v) x_v subject to x_u + x_v >= 1 for each edge
    and x >= 0. The vertices are 0 .. n - 1 with n = len(weights).
    """
    n = len(weights)
    a = [[Fraction(-1) if j in (u, v) else Fraction(0) for j in range(n)] for u, v in edges]
    res = _simplex_max([-Fraction(w) for w in weights], a, [Fraction(-1)] * len(edges))
    if res is None:  # cannot happen: x = 1 is feasible
        raise ValueError("infeasible vertex cover LP")
    val, x = res
    return -val, x


def lp_rounding_vertex_cover(
    weights: Sequence[int | Fraction], edges: Sequence[tuple[int, int]]
) -> tuple[set[int], list[Fraction], Fraction]:
    """Return (C, x, LP*): the rounded cover, the LP solution and its value.

    Precondition: weights are non-negative, and no edge is a self-loop.
    The cover C = {v : x_v >= 1/2} has weight at most 2 LP* <= 2 OPT.
    Cost: one LP solve (here an exact simplex, for small graphs only), then
    O(n) time for the rounding.
    """
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    if any(u == v for u, v in edges):
        raise ValueError("self-loop")
    lp_value, x = solve_vertex_cover_lp(weights, edges)  # @line L1
    cover: set[int] = set()  # @line L2
    for v in range(len(weights)):  # @line L3
        if x[v] >= Fraction(1, 2):  # @line L4
            cover.add(v)
    return cover, x, lp_value  # @line L5
