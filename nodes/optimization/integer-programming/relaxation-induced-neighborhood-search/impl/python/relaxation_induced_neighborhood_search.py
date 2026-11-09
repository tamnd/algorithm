# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxation-induced-neighborhood-search/. The authors are listed in prov/6HZ5A8.jsonl.

import math
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


def minimize_lp(c: Sequence[Num], a: Sequence[Sequence[Num]], b: Sequence[Num]) -> tuple[str, Vec, Fraction]:
    """Minimize c x subject to a x <= b and x >= 0. The LP must not be unbounded."""
    status, x, v = solve_lp([-Fraction(t) for t in c], a, b)
    if status == "unbounded":
        raise ValueError("the LP relaxation is unbounded; give bounds on the variables")
    return status, x, -v


def unit_row(n: int, j: int, s: int) -> list[int]:
    return [s if k == j else 0 for k in range(n)]


def rins(
    c: Sequence[Num],
    a: Sequence[Sequence[Num]],
    b: Sequence[Num],
    integers: Sequence[int],
    incumbent: Sequence[Num],
    node_limit: int = 1000,
    trace: list[tuple] | None = None,
) -> tuple[Vec, Fraction, list[int], int]:
    """Improve a feasible point of min c x, a x <= b, x >= 0, x_j integer (j in integers).

    incumbent must be feasible. The sub-MIP is solved by depth-first branch
    and bound with at most node_limit nodes. Returns (x, value, fixed, nodes):
    the best point found (the incumbent if no better one), its value, the
    list of fixed variables and the number of nodes used.
    """
    n = len(c)
    xbar = [Fraction(v) for v in incumbent]
    _, xstar, _ = minimize_lp(c, a, b)  # @line L1
    fixed = [j for j in integers if xstar[j] == xbar[j]]  # @line L2
    rows = [list(r) for r in a]  # @line L3
    rhs = [Fraction(v) for v in b]
    for j in fixed:
        rows += [unit_row(n, j, 1), unit_row(n, j, -1)]
        rhs += [xbar[j], -xbar[j]]
    if trace is not None:
        trace.append(("fix", tuple(fixed)))
    best = xbar  # @line L4
    best_val = sum((Fraction(c[j]) * xbar[j] for j in range(n)), Fraction(0))
    stack: list[list[tuple[list[int], Fraction]]] = [[]]
    nodes = 0
    while stack and nodes < node_limit:  # @line L5
        extra = stack.pop()  # @line L6
        nodes += 1
        status, x, v = minimize_lp(c, rows + [r for r, _ in extra], rhs + [t for _, t in extra])
        if trace is not None:
            trace.append(("node", status, None if status != "optimal" else v))
        if status == "infeasible" or v >= best_val:  # @line L7
            continue
        frac = [j for j in integers if x[j].denominator != 1]
        if not frac:  # @line L8
            best, best_val = x, v
            if trace is not None:
                trace.append(("improve", tuple(x), v))
            continue
        j = frac[0]  # @line L9
        lo, hi = math.floor(x[j]), math.ceil(x[j])
        stack.append(extra + [(unit_row(n, j, -1), Fraction(-hi))])  # @line L9
        stack.append(extra + [(unit_row(n, j, 1), Fraction(lo))])  # @line L9
    return best, best_val, fixed, nodes  # @line L10
