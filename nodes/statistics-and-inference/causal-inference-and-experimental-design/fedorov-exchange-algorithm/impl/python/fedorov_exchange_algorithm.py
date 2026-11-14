# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fedorov-exchange-algorithm/. The authors are listed in prov/75MV1N.jsonl.
"""Fedorov's exchange algorithm for exact D-optimal designs.

An exact design is a list of N points taken from a finite candidate list C,
repeats allowed. With regression functions f(x) in R^p, its information
matrix is M = sum_i f(x_i) f(x_i)^T. One exchange replaces a design point x_i
by a candidate x. With A = M^(-1) and d(u, v) = f(u)^T A f(v), d(u) = d(u, u),

    det M' / det M = 1 + Delta(x_i, x),
    Delta(x_i, x) = d(x) - d(x_i) - (d(x) d(x_i) - d(x, x_i)^2).

Each pass takes the exchange with the largest Delta and stops when no Delta
exceeds eps. With Fraction inputs and eps = 0 all arithmetic is exact and the
determinant rises strictly at each exchange, so the loop stops after finitely
many exchanges.
"""

from fractions import Fraction
from typing import NamedTuple


class ExchangeResult(NamedTuple):
    design: list       # indices into the candidate list, length N
    det: object        # det M of the final design
    exchanges: list    # (position, old index, new index, Delta) for each exchange


def info_matrix(rows):
    """M = sum of r r^T over the rows r."""
    p = len(rows[0])
    m = [[0] * p for _ in range(p)]
    for r in rows:
        for i in range(p):
            ri = r[i]
            for j in range(p):
                m[i][j] += ri * r[j]
    return m


def determinant(m):
    """Determinant by Gaussian elimination with partial pivoting."""
    a = [row[:] for row in m]
    n = len(a)
    d = 1
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if a[p][c] == 0:
            return 0 * d
        if p != c:
            a[c], a[p] = a[p], a[c]
            d = -d
        d = d * a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            if f != 0:
                for k in range(c, n):
                    a[r][k] -= f * a[c][k]
    return d


def inverse(m):
    """Inverse by Gauss-Jordan elimination with partial pivoting."""
    n = len(m)
    one = m[0][0] * 0 + 1
    a = [list(row) + [one if i == j else one * 0 for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if a[p][c] == 0:
            raise ValueError("singular information matrix")
        a[c], a[p] = a[p], a[c]
        pv = a[c][c]
        a[c] = [v / pv for v in a[c]]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def mat_vec(a, v):
    return [sum(ai * vi for ai, vi in zip(row, v)) for row in a]


def dot(u, v):
    return sum(ui * vi for ui, vi in zip(u, v))


def delta(a, fi, fx):
    """Delta(x_i, x) for A = M^(-1), fi = f(x_i), fx = f(x)."""
    afi = mat_vec(a, fi)
    di = dot(fi, afi)
    dx = dot(fx, mat_vec(a, fx))
    dix = dot(fx, afi)
    return dx - di - (dx * di - dix * dix)


def fedorov_exchange(candidates, start, eps=0, max_exchanges=10000):
    """Run Fedorov's exchange algorithm.

    candidates: list of regression vectors f(x) for the candidate points.
    start: list of N candidate indices whose information matrix is nonsingular.
    eps: stop when the best Delta is at most eps (use 0 with Fractions).
    """
    design = list(start)  # @line L1
    m = info_matrix([candidates[j] for j in design])  # @line L1
    if determinant(m) == 0:
        raise ValueError("the starting design has a singular information matrix")
    log = []
    while len(log) < max_exchanges:  # @line L2
        a = inverse(m)  # @line L3
        dc = [dot(fx, mat_vec(a, fx)) for fx in candidates]  # @line L4
        best = None
        for i, j0 in enumerate(design):  # @line L4
            afi = mat_vec(a, candidates[j0])
            di = dc[j0]
            for j, fx in enumerate(candidates):
                dix = dot(fx, afi)
                dl = dc[j] - di - (dc[j] * di - dix * dix)  # @line L4
                if best is None or dl > best[0]:
                    best = (dl, i, j)  # @line L5
        dl, i, j = best  # @line L5
        if dl <= eps:  # @line L6
            break
        old = design[i]
        fo, fn = candidates[old], candidates[j]
        p = len(fo)
        for r in range(p):
            for c in range(p):
                m[r][c] += fn[r] * fn[c] - fo[r] * fo[c]  # @line L7
        design[i] = j  # @line L7
        log.append((i, old, j, dl))
    return ExchangeResult(design, determinant(m), log)


def polynomial_row(x, degree):
    """f(x) = (1, x, ..., x^degree)."""
    return [x ** k for k in range(degree + 1)]


def quadratic_surface_row(x1, x2):
    """f(x) = (1, x1, x2, x1 x2, x1^2, x2^2), the second-order model in two factors."""
    return [x1 * 0 + 1, x1, x2, x1 * x2, x1 * x1, x2 * x2]


if __name__ == "__main__":
    grid = [Fraction(k, 4) for k in range(-4, 5)]
    cands = [polynomial_row(x, 2) for x in grid]
    res = fedorov_exchange(cands, [grid.index(Fraction(-1, 2)), grid.index(0), grid.index(Fraction(1, 2))])
    print("design", [str(grid[j]) for j in res.design], "det", res.det)
    for i, old, new, dl in res.exchanges:
        print("swap", grid[old], "->", grid[new], "Delta", dl)
