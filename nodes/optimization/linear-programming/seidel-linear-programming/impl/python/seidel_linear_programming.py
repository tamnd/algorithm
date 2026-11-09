# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seidel-linear-programming/. The authors are listed in prov/8NCQG0.jsonl.

"""Seidel's randomized incremental algorithm for linear programming in n variables.

minimize c^T x subject to a_i^T x <= b_i, in exact rational arithmetic. The constraints
are added in random order. If the current optimum satisfies the new constraint, it stays
optimal; otherwise the new optimum lies on the hyperplane of the new constraint, and a
recursive call in n - 1 variables finds it. The expected time is O(n! m).

Ties are broken lexicographically: among the optimal points, the code returns the one
with the least x_1, then the least x_2, and so on. So the optimum of every subproblem is
a unique point, which the analysis needs.

The recursion needs a bounded program, so the code adds the box -M <= x_j <= M. For
integer data, the bound M of big_box() is so large that the box changes nothing for a
bounded program, and that an unbounded program shows up as a value below -value_bound().
"""

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Sequence

Vec = list[Fraction]
Row = tuple[Vec, Fraction]  # (a, b) for the constraint a^T x <= b


@dataclass
class Result:
    status: str  # "optimal", "unbounded" or "infeasible"
    x: Optional[Vec] = None
    value: Optional[Fraction] = None
    calls: int = 0  # the number of recursive calls (line L6), over all levels


def size_bounds(a, b, c) -> tuple[int, int]:
    """(H, K): every basic solution has |x_j| <= H = (n K)^n, with K the largest |entry|."""
    n = len(c)
    k = max([1] + [abs(v) for row in a for v in row] + [abs(v) for v in b] + [abs(v) for v in c])
    return (n * k) ** n, k


def big_box(a, b, c) -> int:
    h, k = size_bounds(a, b, c)
    return 2 * len(c) * k * h * h + h + 1


def value_bound(a, b, c) -> int:
    h, k = size_bounds(a, b, c)
    return len(c) * k * h


def first_sign(objs: list[Vec], j: int) -> int:
    """The sign of the first objective that depends on x_j (0 if none does)."""
    for o in objs:
        if o[j] != 0:
            return 1 if o[j] > 0 else -1
    return 0


class Solver:
    def __init__(self, rng: random.Random, shuffle: bool):
        self.rng, self.shuffle, self.calls = rng, shuffle, 0

    def solve(self, rows: list[Row], objs: list[Vec], m: Fraction) -> Optional[Vec]:
        """The lexicographic minimum of (o^T x for o in objs) subject to rows and -m <= x_j <= m,
        or None if this set is empty."""
        n = len(objs[0])
        if n == 1:  # @line L1: an interval
            lo, hi = -m, m
            for (g,), beta in rows:
                if g > 0:
                    hi = min(hi, beta / g)
                elif g < 0:
                    lo = max(lo, beta / g)
                elif beta < 0:
                    return None
            if lo > hi:
                return None
            return [hi if first_sign(objs, 0) < 0 else lo]
        x = [m if first_sign(objs, j) < 0 else -m for j in range(n)]  # @line L2: the best corner of the box
        order = list(rows)
        if self.shuffle:
            self.rng.shuffle(order)  # @line L3
        for i, (g, beta) in enumerate(order):  # @line L4
            if sum(gj * xj for gj, xj in zip(g, x)) <= beta:  # @line L5
                continue
            if all(gj == 0 for gj in g):  # 0 <= beta is false
                return None
            x = self.on_hyperplane(order[:i], g, beta, objs, m)  # @line L6
            if x is None:  # @line L7
                return None
        return x  # @line L8

    def on_hyperplane(self, rows: list[Row], g: Vec, beta: Fraction, objs: list[Vec], m: Fraction):
        """Solve the program on the hyperplane g^T x = beta with one variable less."""
        self.calls += 1
        n = len(g)
        k = max(range(n), key=lambda j: abs(g[j]))  # x_k = (beta - sum_{j != k} g_j x_j) / g_k

        def reduce(h: Vec, t: Fraction) -> Row:
            f = h[k] / g[k]
            return [h[j] - f * g[j] for j in range(n) if j != k], t - f * beta

        sub = [reduce(h, t) for h, t in rows]
        unit = [Fraction(int(j == k)) for j in range(n)]
        sub += [reduce(unit, m), reduce([-u for u in unit], m)]  # the box on x_k
        y = self.solve(sub, [reduce(o, Fraction(0))[0] for o in objs], m)
        if y is None:
            return None
        y.insert(k, Fraction(0))
        y[k] = (beta - sum(g[j] * y[j] for j in range(n) if j != k)) / g[k]
        return y


def seidel_linear_programming(
    a: Sequence[Sequence[int]],
    b: Sequence[int],
    c: Sequence[int],
    seed: int = 0,
    box: Optional[int] = None,
    shuffle: bool = True,
) -> Result:
    """Solve min c^T x subject to A x <= b. With box=None the answer is exact for integer data;
    with a given box, the program min c^T x subject to A x <= b and |x_j| <= box is solved."""
    n = len(c)
    rows = [([Fraction(v) for v in row], Fraction(bi)) for row, bi in zip(a, b)]
    objs = [[Fraction(v) for v in c]] + [[Fraction(int(i == j)) for i in range(n)] for j in range(n)]
    m = Fraction(box if box is not None else big_box(a, b, c))
    solver = Solver(random.Random(seed), shuffle)
    x = solver.solve(rows, objs, m)
    if x is None:
        return Result("infeasible", calls=solver.calls)
    value = sum(cj * xj for cj, xj in zip(objs[0], x))
    if box is None and value < -value_bound(a, b, c):
        return Result("unbounded", calls=solver.calls)
    return Result("optimal", x, value, solver.calls)
