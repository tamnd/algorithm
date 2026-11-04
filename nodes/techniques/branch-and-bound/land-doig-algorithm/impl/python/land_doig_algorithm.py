# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/land-doig-algorithm/. The authors are listed in prov/XVSXFR.jsonl.

import heapq
import itertools
import math
from collections.abc import Sequence
from fractions import Fraction

Num = int | Fraction


def solve_lp(c: Sequence[Num], a: Sequence[Sequence[Num]], b: Sequence[Num]) -> tuple[str, list[Fraction], Fraction]:
    """Maximise c x subject to a x <= b and x >= 0, in exact arithmetic.

    Two-phase tableau simplex with Bland's rule, so it always stops.
    Returns (status, x, value) with status "optimal", "infeasible" or
    "unbounded"; x and value are only meaningful when it is "optimal".
    """
    m, n = len(a), len(c)
    # Columns: x (n), slacks (m), artificials (one per row with b < 0).
    neg = [i for i in range(m) if b[i] < 0]
    width = n + m + len(neg)
    rows: list[list[Fraction]] = []
    basis: list[int] = []
    for i in range(m):
        sign = -1 if b[i] < 0 else 1
        row = [Fraction(sign * a[i][j]) for j in range(n)] + [Fraction(0)] * (m + len(neg)) + [Fraction(sign * b[i])]
        row[n + i] = Fraction(sign)
        if sign < 0:
            k = n + m + neg.index(i)
            row[k] = Fraction(1)
            basis.append(k)
        else:
            basis.append(n + i)
        rows.append(row)

    def pivot(r: int, col: int) -> None:
        p = rows[r][col]
        rows[r] = [v / p for v in rows[r]]
        for i in range(m):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [vi - f * vr for vi, vr in zip(rows[i], rows[r])]
        basis[r] = col

    def run(cost: list[Fraction], allowed: int) -> bool:
        # Maximise cost over the current basis; False if unbounded.
        while True:
            red = [cost[j] - sum(cost[basis[i]] * rows[i][j] for i in range(m)) for j in range(allowed)]
            enter = next((j for j in range(allowed) if red[j] > 0 and j not in basis), None)
            if enter is None:
                return True
            best: tuple[Fraction, int, int] | None = None
            for i in range(m):
                if rows[i][enter] > 0:
                    key = (rows[i][-1] / rows[i][enter], basis[i], i)
                    if best is None or key < best:
                        best = key
            if best is None:
                return False
            pivot(best[2], enter)

    if neg:
        phase1 = [Fraction(0)] * (n + m) + [Fraction(-1)] * len(neg)
        run(phase1, width)
        if any(basis[i] >= n + m and rows[i][-1] != 0 for i in range(m)):
            return "infeasible", [], Fraction(0)
        for i in range(m):
            if basis[i] >= n + m:
                col = next((j for j in range(n + m) if rows[i][j] != 0), None)
                if col is not None:
                    pivot(i, col)
    cost = [Fraction(v) for v in c] + [Fraction(0)] * (m + len(neg))
    if not run(cost, n + m):
        return "unbounded", [], Fraction(0)
    x = [Fraction(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = rows[i][-1]
    return "optimal", x, sum((Fraction(c[j]) * x[j] for j in range(n)), Fraction(0))


Fixing = tuple[tuple[int, int], ...]


def land_doig(
    c: Sequence[Num],
    a: Sequence[Sequence[Num]],
    b: Sequence[Num],
    integer: Sequence[int] | None = None,
    stats: dict[str, int] | None = None,
    trace: list[tuple[Fixing, Fraction]] | None = None,
) -> tuple[Fraction | None, list[Fraction] | None]:
    """Maximise c x subject to a x <= b, x >= 0, x_j integer for j in integer.

    Land and Doig's scheme: each node fixes some integer variables to integer
    values; its bound is the optimum of its linear program. A node with a
    fractional x_j gets two children, x_j = floor and x_j = ceil. When the
    child with x_j = v is taken from the queue, its sibling with the next
    value away from the LP value (v - 1 or v + 1) is made. The LP value is
    concave in the fixed value, so the sibling's bound is at most the child's.
    The feasible set {x >= 0 : a x <= b} must be bounded, for example because
    the constraints bound every variable. Returns (value, x), or (None, None) if
    there is no integer solution. Selection is best-first.
    """
    n = len(c)
    integer = list(range(n)) if integer is None else list(integer)
    if stats is None:
        stats = {}
    stats.update(lps=0, expanded=0)
    tick = itertools.count()

    def lp(fix: Fixing) -> tuple[list[Fraction], Fraction] | None:
        rows = [list(r) for r in a]
        rhs = list(b)
        for j, v in fix:
            e = [0] * n
            e[j] = 1
            rows.append(e)
            rhs.append(v)
            rows.append([-t for t in e])
            rhs.append(-v)
        stats["lps"] += 1
        status, x, val = solve_lp(c, rows, rhs)
        if status == "unbounded":
            raise ValueError("the linear relaxation is unbounded")
        return (x, val) if status == "optimal" else None

    Node = tuple[Fixing, list[Fraction], Fraction, tuple[Fixing, int, int, int] | None]
    heap: list[tuple[Fraction, int, Node]] = []

    def insert(fix: Fixing, sib: tuple[Fixing, int, int, int] | None, z: Fraction | None) -> None:
        r = lp(fix)
        if r is None:
            return  # infeasible: so is every value further away
        x, val = r
        if z is not None and val <= z:
            return  # fathomed: further values are no better
        heapq.heappush(heap, (-val, next(tick), (fix, x, val, sib)))

    z: Fraction | None = None  # @line L1
    best: list[Fraction] | None = None  # @line L1
    insert((), None, None)  # @line L2
    while heap:  # @line L3
        _, _, (fix, x, val, sib) = heapq.heappop(heap)  # @line L4
        if z is not None and val <= z:  # @line L5
            break
        if trace is not None:
            trace.append((fix, val))
        if sib is not None:  # @line L6
            parent, j, v, step = sib
            insert(parent + ((j, v),), (parent, j, v + step, step), z)  # @line L7
        frac = [j for j in integer if x[j].denominator != 1]  # @line L8
        if not frac:  # @line L9
            if z is None or val > z:
                z, best = val, x
            continue
        stats["expanded"] += 1
        j = frac[0]  # @line L10
        lo = math.floor(x[j])
        insert(fix + ((j, lo),), (fix, j, lo - 1, -1), z)  # @line L11
        insert(fix + ((j, lo + 1),), (fix, j, lo + 2, 1), z)  # @line L11
    return z, best  # @line L12
