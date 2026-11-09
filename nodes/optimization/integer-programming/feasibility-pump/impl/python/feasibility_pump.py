# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feasibility-pump/. The authors are listed in prov/N3GN92.jsonl.

import random
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


def feasibility_pump(
    c: Sequence[Num],
    a: Sequence[Sequence[Num]],
    b: Sequence[Num],
    binaries: Sequence[int],
    max_iter: int = 100,
    flips: int = 20,
    restart_every: int = 100,
    seed: int = 0,
    trace: list[tuple[str, tuple[int, ...]]] | None = None,
) -> tuple[str, Vec | None, int]:
    """Look for a point with a x <= b, x >= 0 and x_j in {0, 1} for j in binaries.

    c is the cost vector (to minimize) of the first LP only. flips is the
    parameter T of the flip move, and restart_every is the parameter R of the
    random restart. Returns (status, x, iterations) where status is "feasible"
    (x is a feasible point), "infeasible" (the LP relaxation is empty) or
    "fail" (no point found within max_iter iterations; this says nothing about
    the existence of one).
    """
    n = len(c)
    rng = random.Random(seed)
    rows = [list(r) for r in a] + [[int(k == j) for k in range(n)] for j in binaries]
    rhs = list(b) + [1] * len(binaries)

    def integral(x: Vec) -> bool:
        return all(x[j].denominator == 1 for j in binaries)

    def rounded(x: Vec) -> tuple[int, ...]:
        return tuple(1 if x[j] >= Fraction(1, 2) else 0 for j in binaries)

    it = 0  # @line L1
    status, xs, _ = solve_lp([-v for v in c], rows, rhs)  # @line L1
    if status == "unbounded":
        status, xs, _ = solve_lp([0] * n, rows, rhs)
    if status == "infeasible":
        return "infeasible", None, 0
    if trace is not None:
        trace.append(("lp", tuple(xs)))
    if integral(xs):  # @line L2
        return "feasible", xs, 0
    xt = list(rounded(xs))  # @line L3
    if trace is not None:
        trace.append(("round", tuple(xt)))
    recent: list[tuple[int, ...]] = []
    while it < max_iter:  # @line L4
        it += 1  # @line L5
        recent = (recent + [tuple(xt)])[-3:]
        # distance to xt: sum of x_j where xt_j = 0, plus 1 - x_j where xt_j = 1
        dist = [Fraction(0)] * n
        for k, j in enumerate(binaries):
            dist[j] = Fraction(-1 if xt[k] == 0 else 1)
        _, xs, _ = solve_lp(dist, rows, rhs)  # @line L5
        if trace is not None:
            trace.append(("lp", tuple(xs)))
        if integral(xs):  # @line L6
            return "feasible", xs, it
        new = rounded(xs)
        gap = [abs(xs[j] - xt[k]) for k, j in enumerate(binaries)]
        if it % restart_every == 0 or (new != tuple(xt) and new in recent):  # @line L7
            for k in range(len(binaries)):  # @line L8
                rho = rng.uniform(-0.3, 0.7)
                if gap[k] + max(rho, 0.0) > 0.5:
                    xt[k] = 1 - xt[k]
            move = "restart"
        elif new != tuple(xt):  # @line L9
            xt = list(new)
            move = "round"
        else:
            tt = min(len(binaries), max(1, rng.randint(flips // 2, (3 * flips) // 2)))  # @line L10
            order = sorted(range(len(binaries)), key=lambda k: (-gap[k], k))
            for k in order[:tt]:
                xt[k] = 1 - xt[k]
            move = "flip"
        if trace is not None:
            trace.append((move, tuple(xt)))
    return "fail", None, it  # @line L11
