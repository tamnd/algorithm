# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/halfspace-learning/. The authors are listed in prov/34Q4BF.jsonl.
"""Consistent halfspace learning by linear programming, with an exact two-phase simplex method.

Given points x_i in Q^d with labels y_i in {-1, +1}, find (w, b) with y_i (w . x_i + b) >= 1 for all i.
Such (w, b) exists exactly when the two classes are strictly separable by a hyperplane (scale any
strict separator). The LP is solved in exact rational arithmetic, with Bland's rule against cycling.
"""

import random
from fractions import Fraction
from itertools import product

Vec = list[Fraction]


class Infeasible(Exception):
    pass


class Unbounded(Exception):
    pass


def _pivot(t: list[Vec], basis: list[int], r: int, c: int) -> None:
    pv = t[r][c]
    t[r] = [v / pv for v in t[r]]
    for i in range(len(t)):
        if i != r and t[i][c] != 0:
            f = t[i][c]
            t[i] = [a - f * b for a, b in zip(t[i], t[r])]
    basis[r] = c


def _run(t: list[Vec], basis: list[int], cost: Vec, allowed: int) -> int:
    """Minimize cost . x over the tableau with Bland's rule; columns >= allowed may not enter.
    Returns the number of pivots."""
    pivots = 0
    while True:
        enter = -1
        for j in range(allowed):
            if j in basis:
                continue
            rc = cost[j] - sum(cost[basis[i]] * t[i][j] for i in range(len(t)))
            if rc < 0:
                enter = j
                break
        if enter < 0:
            return pivots
        row, best = -1, None
        for i in range(len(t)):
            if t[i][enter] > 0:
                ratio = t[i][-1] / t[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[row]):
                    row, best = i, ratio
        if row < 0:
            raise Unbounded()
        _pivot(t, basis, row, enter)
        pivots += 1


def simplex(a: list[Vec], b: Vec, c: Vec) -> tuple[Vec, int]:
    """Minimize c . x subject to A x = b, x >= 0, by the two-phase simplex method.
    Returns (x, number of pivots). Raises Infeasible or Unbounded."""
    m, n = len(a), len(c)
    t = []
    for i in range(m):
        sgn = -1 if b[i] < 0 else 1
        t.append([sgn * v for v in a[i]] + [Fraction(int(k == i)) for k in range(m)] + [sgn * b[i]])
    basis = [n + i for i in range(m)]
    # Phase 1: minimize the sum of the artificial variables.
    pivots = _run(t, basis, [Fraction(0)] * n + [Fraction(1)] * m, n)
    if sum(t[i][-1] for i in range(m) if basis[i] >= n) != 0:
        raise Infeasible()
    # Drive the artificial variables that are still basic (at value 0) out of the basis.
    i = 0
    while i < len(t):
        if basis[i] >= n:
            j = next((j for j in range(n) if t[i][j] != 0), -1)
            if j < 0:  # a redundant equation
                del t[i], basis[i]
                continue
            _pivot(t, basis, i, j)
            pivots += 1
        i += 1
    # Phase 2: the real objective; artificial columns may not enter.
    pivots += _run(t, basis, list(c) + [Fraction(0)] * m, n)
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        x[j] = t[i][-1]
    return x, pivots


def separate(xs: list[list[Fraction]], ys: list[int]) -> tuple[Vec, Fraction, int] | None:
    """A halfspace (w, b) with y_i (w . x_i + b) >= 1 for all i, minimizing |w|_1 + |b|, or None.

    Variables: w+ (d), w- (d), b+, b-, then one surplus s_i per example:
    y_i (x_i . (w+ - w-) + b+ - b-) - s_i = 1."""
    m, d = len(xs), len(xs[0]) if xs else 0
    n = 2 * d + 2 + m
    a, rhs = [], []
    for i, (x, y) in enumerate(zip(xs, ys)):
        row = [Fraction(0)] * n
        for k in range(d):
            row[k] = Fraction(y) * x[k]
            row[d + k] = -Fraction(y) * x[k]
        row[2 * d], row[2 * d + 1] = Fraction(y), Fraction(-y)
        row[2 * d + 2 + i] = Fraction(-1)
        a.append(row)
        rhs.append(Fraction(1))
    c = [Fraction(1)] * (2 * d + 2) + [Fraction(0)] * m
    try:
        x, pivots = simplex(a, rhs, c)
    except Infeasible:
        return None
    w = [x[k] - x[d + k] for k in range(d)]
    return w, x[2 * d] - x[2 * d + 1], pivots


def consistent(w: Vec, b: Fraction, xs: list[list[Fraction]], ys: list[int]) -> bool:
    return all(y * (sum(wi * xi for wi, xi in zip(w, x)) + b) >= 1 for x, y in zip(xs, ys))


def shattered(xs: list[list[Fraction]]) -> bool:
    return all(separate(xs, list(lab)) is not None for lab in product((-1, 1), repeat=len(xs)))


def random_separable(n: int, d: int, rng: random.Random) -> tuple[list[list[Fraction]], list[int], Vec, Fraction]:
    """n points with coordinates k/8 in [-1, 1], labeled by a random integer halfspace; points on it are skipped."""
    w = [Fraction(rng.randint(-3, 3)) for _ in range(d)]
    if all(v == 0 for v in w):
        w[0] = Fraction(1)
    b = Fraction(rng.randint(-2, 2), 4)
    xs, ys = [], []
    while len(xs) < n:
        x = [Fraction(rng.randint(-8, 8), 8) for _ in range(d)]
        s = sum(wi * xi for wi, xi in zip(w, x)) + b
        if s != 0:
            xs.append(x)
            ys.append(1 if s > 0 else -1)
    return xs, ys, w, b


if __name__ == "__main__":
    rng = random.Random(1)
    for n, d in ((10, 2), (30, 2), (30, 5), (60, 5)):
        xs, ys, w0, b0 = random_separable(n, d, rng)
        w, b, piv = separate(xs, ys)
        print(n, d, [str(v) for v in w0], str(b0), [str(v) for v in w], str(b), piv, consistent(w, b, xs, ys))
    f = Fraction
    print("xor", separate([[f(0), f(0)], [f(1), f(1)], [f(0), f(1)], [f(1), f(0)]], [1, 1, -1, -1]))
