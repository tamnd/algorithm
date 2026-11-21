# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/controlled-tabular-adjustment/. The authors are listed in prov/P26HSK.jsonl.
"""Controlled tabular adjustment (CTA) with the L1 distance.

A table is a list of n cell values a[i]. The table relations are linear equations
sum of coef * x[cell] = 0 that the table satisfies, for example a total minus its
parts. Each cell has bounds lower[i] <= x[i] <= upper[i]. A sensitive cell p has a
lower and an upper protection level (lpl, upl): the published value must be at most
a[p] - lpl or at least a[p] + upl. CTA finds the published table x that satisfies
the relations and the bounds, moves every sensitive cell out of its protection
interval, and has the least weighted L1 distance sum w[i] |x[i] - a[i]|.

The exact method tries both directions for every sensitive cell and solves one
linear program for each choice, so it takes 2^|P| LPs. The LP solver is a small
bounded-variable primal simplex with Bland's rule. With Fraction inputs and eps = 0
all arithmetic is exact; with floats, eps is the tolerance.
"""

from fractions import Fraction
from itertools import product
from typing import Optional, Sequence, Union

Number = Union[int, float, Fraction]
Relation = Sequence[tuple[int, Number]]
INF = float("inf")


def bounded_simplex(
    A: list[list[Number]], b: list[Number], c: list[Number], upper: list[Number], eps: Number = 0, max_iter: int = 10000
) -> Optional[tuple[Number, list[Number]]]:
    """Minimize c x subject to A x = b and 0 <= x <= upper (entries of upper may be inf).

    Returns (value, x), or None if the system has no solution. Raises ValueError if
    the LP is unbounded or the iteration cap is reached.
    Precondition: all rows of A have the length of c and upper.
    Cost: each pivot takes O(m (n + m)) operations for m rows and n columns; Bland's
    rule ensures termination, and the number of pivots is exponential only in the worst case.
    """
    m, n = len(A), len(c)
    # eps = 0 means exact arithmetic: work with fractions, so that no int division gives a float.
    num = Fraction if eps == 0 else float
    A = [[num(v) for v in row] for row in A]
    b = [num(v) for v in b]
    c = [num(v) for v in c]
    upper = [v if v == INF else num(v) for v in upper]
    rows = []
    rhs = []
    for i in range(m):
        sign = -1 if b[i] < 0 else 1
        rows.append([sign * v for v in A[i]] + [1 if j == i else 0 for j in range(m)])
        rhs.append(sign * b[i])
    total = n + m
    ub: list[Number] = list(upper) + [INF] * m
    basis = list(range(n, total))
    at_upper = [False] * total
    val: list[Number] = [0] * n + rhs

    def run(cost: list[Number]) -> None:
        d = [cost[j] - sum(cost[basis[i]] * rows[i][j] for i in range(m)) for j in range(total)]
        for _ in range(max_iter):
            enter = -1
            for j in range(total):
                if j in basis_set:
                    continue
                if (not at_upper[j] and d[j] < -eps and ub[j] > 0) or (at_upper[j] and d[j] > eps):
                    enter = j
                    break
            if enter < 0:
                return
            delta = -1 if at_upper[enter] else 1
            step = ub[enter]
            leave_row = -1
            leave_up = False
            for i in range(m):
                alpha = delta * rows[i][enter]
                if alpha > eps:
                    t = val[basis[i]] / alpha
                    up_side = False
                elif alpha < -eps and ub[basis[i]] != INF:
                    t = (ub[basis[i]] - val[basis[i]]) / (-alpha)
                    up_side = True
                else:
                    continue
                # The least step wins; on a tie, a bound flip of the entering variable, then
                # the basic variable with the lowest index (Bland's rule).
                if t < step or (t == step and leave_row >= 0 and basis[i] < basis[leave_row]):
                    step, leave_row, leave_up = t, i, up_side
            if step == INF:
                raise ValueError("unbounded linear program")
            for i in range(m):
                val[basis[i]] -= delta * step * rows[i][enter]
            val[enter] += delta * step
            if leave_row < 0:
                at_upper[enter] = not at_upper[enter]
                continue
            out = basis[leave_row]
            piv = rows[leave_row][enter]
            rows[leave_row] = [v / piv for v in rows[leave_row]]
            for i in range(m):
                if i != leave_row and rows[i][enter] != 0:
                    f = rows[i][enter]
                    rows[i] = [v - f * w for v, w in zip(rows[i], rows[leave_row])]
            f = d[enter]
            d[:] = [v - f * w for v, w in zip(d, rows[leave_row])]
            basis[leave_row] = enter
            basis_set.discard(out)
            basis_set.add(enter)
            at_upper[enter] = False
            at_upper[out] = leave_up
            val[out] = ub[out] if leave_up else 0
        raise ValueError("iteration cap reached")

    basis_set = set(basis)
    run([0] * n + [1] * m)
    if sum(val[n:]) > eps * (1 + m):
        return None
    for j in range(n, total):
        ub[j] = 0
    run(list(c) + [0] * m)
    x = val[:n]
    return sum(cj * xj for cj, xj in zip(c, x)), x


def cta(
    a: Sequence[Number],
    relations: Sequence[Relation],
    lower: Sequence[Number],
    upper: Sequence[Number],
    weights: Sequence[Number],
    sensitive: dict[int, tuple[Number, Number]],
    directions: Optional[dict[int, int]] = None,
    eps: Number = 1e-9,
) -> Optional[tuple[list[Number], Number, dict[int, int]]]:
    """The optimal L1 CTA over all directions, or over the given directions only.

    Returns (x, cost, chosen) where x is the published table, cost is sum w |x - a|,
    and chosen maps each sensitive cell to +1 (up) or -1 (down); or None if no
    choice of directions is feasible.
    Precondition: a satisfies every relation, lower <= a <= upper, weights >= 0, and
    the protection levels are >= 0. directions, if given, maps each sensitive cell to +1 or -1.
    Cost: 2^|P| linear programs with |relations| rows and 2n columns, or one LP if
    directions are given.
    """
    n = len(a)
    cells = sorted(sensitive)
    if directions is None:
        choices = list(product((-1, 1), repeat=len(cells)))
    else:
        choices = [tuple(directions[p] for p in cells)]
    best: Optional[tuple[list[Number], Number, dict[int, int]]] = None  # @line L1
    for choice in choices:  # @line L2
        # Columns 0 .. n-1 are z+ (x goes up), columns n .. 2n-1 are z- (x goes down).
        lo = [0] * (2 * n)
        hi = [upper[i] - a[i] for i in range(n)] + [a[i] - lower[i] for i in range(n)]  # @line L3
        for p, d in zip(cells, choice):  # @line L4
            lpl, upl = sensitive[p]
            if d > 0:
                lo[p], hi[n + p] = upl, 0
            else:
                lo[n + p], hi[p] = lpl, 0
        if any(lo[j] > hi[j] for j in range(2 * n)):
            continue
        A = []
        b = []
        for rel in relations:
            row = [0] * (2 * n)
            for cell, coef in rel:
                row[cell] += coef
                row[n + cell] -= coef
            A.append(row)
            b.append(-sum(row[j] * lo[j] for j in range(2 * n)))
        cost = [weights[i % n] for i in range(2 * n)]
        res = bounded_simplex(A, b, cost, [hi[j] - lo[j] for j in range(2 * n)], eps)  # @line L5
        if res is None:
            continue
        value, z = res
        z = [z[j] + lo[j] for j in range(2 * n)]
        value += sum(cost[j] * lo[j] for j in range(2 * n))
        if best is None or value < best[1] - eps:  # @line L6
            x = [a[i] + z[i] - z[n + i] for i in range(n)]
            best = (x, value, dict(zip(cells, choice)))
    if best is None:  # @line L7
        return None
    return best  # @line L8


def check(
    x: Sequence[Number],
    a: Sequence[Number],
    relations: Sequence[Relation],
    lower: Sequence[Number],
    upper: Sequence[Number],
    sensitive: dict[int, tuple[Number, Number]],
    eps: Number = 1e-9,
) -> bool:
    """True if x satisfies the relations and the bounds and protects every sensitive cell."""
    if any(abs(sum(coef * x[cell] for cell, coef in rel)) > eps for rel in relations):
        return False
    if any(x[i] < lower[i] - eps or x[i] > upper[i] + eps for i in range(len(x))):
        return False
    return all(x[p] <= a[p] - lpl + eps or x[p] >= a[p] + upl - eps for p, (lpl, upl) in sensitive.items())
