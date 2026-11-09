# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benders-decomposition/. The authors are listed in prov/09SW6A.jsonl.

import itertools
from collections.abc import Sequence
from fractions import Fraction

Num = int | Fraction
Vec = list[Fraction]


def solve_lp(c: Sequence[Num], a: Sequence[Sequence[Num]], b: Sequence[Num]) -> tuple[str, Vec, Fraction]:
    """Maximize c x subject to a x <= b and x >= 0, in exact arithmetic.

    Two-phase tableau simplex with Bland's rule, so it always stops.
    Returns (status, x, value); status is "optimal", "infeasible" or
    "unbounded", and x and value are meaningful only when it is "optimal".
    """
    m, n = len(a), len(c)
    neg = [i for i in range(m) if b[i] < 0]
    width = n + m + len(neg)
    rows: list[Vec] = []
    basis: list[int] = []
    for i in range(m):
        s = -1 if b[i] < 0 else 1
        row = [Fraction(s * a[i][j]) for j in range(n)] + [Fraction(0)] * (width - n) + [Fraction(s * b[i])]
        row[n + i] = Fraction(s)
        if s < 0:
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

    def run(cost: Vec, allowed: int) -> bool:
        while True:
            enter = None
            for j in range(allowed):
                if j not in basis and cost[j] - sum(cost[basis[i]] * rows[i][j] for i in range(m)) > 0:
                    enter = j
                    break
            if enter is None:
                return True
            best = None
            for i in range(m):
                if rows[i][enter] > 0:
                    key = (rows[i][-1] / rows[i][enter], basis[i], i)
                    if best is None or key < best:
                        best = key
            if best is None:
                return False
            pivot(best[2], enter)

    if neg:
        run([Fraction(0)] * (n + m) + [Fraction(-1)] * len(neg), width)
        if any(basis[i] >= n + m and rows[i][-1] != 0 for i in range(m)):
            return "infeasible", [], Fraction(0)
        for i in range(m):
            if basis[i] >= n + m:
                col = next((j for j in range(n + m) if rows[i][j] != 0), None)
                if col is not None:
                    pivot(i, col)
    cost = [Fraction(v) for v in c] + [Fraction(0)] * (width - n)
    if not run(cost, n + m):
        return "unbounded", [], Fraction(0)
    x = [Fraction(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = rows[i][-1]
    return "optimal", x, sum((Fraction(c[j]) * x[j] for j in range(n)), Fraction(0))


def dot(u: Sequence[Num], v: Sequence[Num]) -> Fraction:
    return sum((Fraction(p) * q for p, q in zip(u, v)), Fraction(0))


def benders(
    c: Sequence[Num],
    d: Sequence[Num],
    g: Sequence[Sequence[Num]],
    bmat: Sequence[Sequence[Num]],
    h: Sequence[Num],
    box: Sequence[tuple[int, int]],
    trace: list[tuple[str, tuple[int, ...], Fraction | None]] | None = None,
) -> tuple[str, Fraction | None, tuple[int, ...] | None, Vec | None]:
    """Minimize c x + d y subject to g x + bmat y >= h, y >= 0, x integer in box.

    box[j] = (lo, hi) bounds the integer variable x_j. The master problem is
    solved by enumeration of the box, which keeps the code short; any exact
    integer programming method could take its place. Returns
    (status, value, x, y) with status "optimal", "infeasible" or "unbounded".
    """
    m, q = len(h), len(d)
    bt = [[bmat[i][k] for i in range(m)] for k in range(q)]  # B transposed, q x m
    xs = list(itertools.product(*(range(lo, hi + 1) for lo, hi in box)))

    def rhs(x: Sequence[int]) -> Vec:
        return [Fraction(h[i]) - dot(g[i], x) for i in range(m)]

    opt_cuts: list[Vec] = []  # @line L1
    feas_cuts: list[Vec] = []  # @line L1
    while True:  # @line L2
        best_x, best_val, best_eta = None, None, None
        for x in xs:  # @line L3
            r = rhs(x)
            if any(dot(f, r) > 0 for f in feas_cuts):
                continue
            eta = max((dot(u, r) for u in opt_cuts), default=None)
            val = None if eta is None else dot(c, x) + eta
            if best_x is None or (best_val is not None and (val is None or val < best_val)):
                best_x, best_val, best_eta = x, val, eta
            if val is None:
                break
        if best_x is None:  # @line L4
            return "infeasible", None, None, None
        x = best_x  # @line L5
        r = rhs(x)
        # Normalized Farkas ray: max r^T u, B^T u <= 0, sum u <= 1, u >= 0.
        _, ray, rv = solve_lp(r, bt + [[1] * m], [0] * q + [1])  # @line L6
        if rv > 0:  # @line L7
            feas_cuts.append(ray)
            if trace is not None:
                trace.append(("feasibility", x, None))
            continue
        status, u, s = solve_lp(r, bt, d)  # @line L8
        if status == "infeasible":  # @line L9
            return "unbounded", None, None, None
        if trace is not None:
            trace.append(("optimality", x, s))
        if best_eta is not None and best_eta >= s:  # @line L10
            _, y, neg = solve_lp([-v for v in d], [[-v for v in row] for row in bmat], [-v for v in r])
            return "optimal", dot(c, x) - neg, x, y
        opt_cuts.append(u)  # @line L11
