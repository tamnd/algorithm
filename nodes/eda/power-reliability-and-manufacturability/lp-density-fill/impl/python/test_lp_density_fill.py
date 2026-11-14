# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lp-density-fill/. The authors are listed in prov/6QQEE4.jsonl.

import itertools
import random
from fractions import Fraction

from lp_density_fill import (
    build_lp,
    floating_error,
    lp_density_fill,
    simplex_max,
    window_densities,
    window_tiles,
    windows,
)


def random_instance(rng, m, tile_area, denom):
    """Feature area and slack per tile, with area + slack <= tile area."""
    area, slack = [], []
    for i in range(m):
        ra, rs = [], []
        for j in range(m):
            a = Fraction(rng.randint(0, denom), denom) * tile_area
            s = Fraction(rng.randint(0, denom), denom) * (tile_area - a)
            ra.append(a)
            rs.append(s)
        area.append(ra)
        slack.append(rs)
    return area, slack


def solve_linear(M, v):
    """Solve M x = v exactly; None if M is singular."""
    n = len(M)
    a = [list(map(Fraction, row)) + [Fraction(v[i])] for i, row in enumerate(M)]
    for col in range(n):
        piv = next((i for i in range(col, n) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(n):
            if i != col and a[i][col] != 0:
                f = a[i][col] / a[col][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[col])]
    return [a[i][n] / a[i][i] for i in range(n)]


def vertex_enumeration(c, A, b):
    """Maximum of c.x over {A x <= b, x >= 0} by trying every basis of tight constraints."""
    n = len(c)
    rows = [(list(A[i]), Fraction(b[i])) for i in range(len(A))]
    rows += [([-1 if k == j else 0 for k in range(n)], Fraction(0)) for j in range(n)]
    best = None
    for subset in itertools.combinations(range(len(rows)), n):
        x = solve_linear([rows[i][0] for i in subset], [rows[i][1] for i in subset])
        if x is None:
            continue
        if all(sum(g * xi for g, xi in zip(row, x)) <= h for row, h in rows):
            val = sum(ci * xi for ci, xi in zip(c, x))
            if best is None or val > best:
                best = val
    return best


def feasible(area, slack, p, r, U, w2):
    m = len(area)
    if any(not (0 <= p[i][j] <= slack[i][j]) for i in range(m) for j in range(m)):
        return False
    return max(window_densities(area, p, r, w2)) <= U


def test_one_tile_windows_closed_form():
    # With r = 1 every tile is a window, so each tile is filled as far as its slack and U allow.
    rng = random.Random(1)
    for trial in range(20):
        area, slack = random_instance(rng, 4, 9, 9)
        U = Fraction(rng.randint(5, 9), 9)
        if trial % 4:
            U = max(U, max(a for row in area for a in row) / 9)
        if any(a > 9 * U for row in area for a in row):
            assert lp_density_fill(area, slack, 1, U, 9) is None
            continue
        d, p = lp_density_fill(area, slack, 1, U, 9)
        expected = min(a + min(s, 9 * U - a) for ra, rs in zip(area, slack) for a, s in zip(ra, rs)) / 9
        assert d == expected
        assert feasible(area, slack, p, 1, U, 9)
        assert min(window_densities(area, p, 1, 9)) == d


def test_matches_vertex_enumeration():
    rng = random.Random(2)
    for trial in range(12):
        r = 1 + trial % 2
        area, slack = random_instance(rng, 2, 4, 8)
        U = Fraction(rng.randint(4, 8), 8)
        if lp_density_fill(area, slack, r, U, 4 * r * r) is None:
            continue
        c, A, b = build_lp(area, slack, r, U, 4 * r * r)
        value, x, _ = simplex_max(c, A, b)
        assert value == vertex_enumeration(c, A, b)


def test_dual_certificate_on_larger_grids():
    # A feasible x, a feasible dual y and equal objective values prove optimality,
    # independent of the pivoting that produced them.
    rng = random.Random(3)
    for m, r in [(5, 2), (5, 3), (6, 2)]:
        area, slack = random_instance(rng, m, 1, 10)
        U = Fraction(3, 4)
        w2 = r * r
        if lp_density_fill(area, slack, r, U, w2) is None:
            U = Fraction(1)
        c, A, b = build_lp(area, slack, r, U, w2)
        value, x, y = simplex_max(c, A, b)
        assert all(v >= 0 for v in x) and all(v >= 0 for v in y)
        for row, bi in zip(A, b):
            assert sum(a * v for a, v in zip(row, x)) <= bi
        for j in range(len(c)):
            assert sum(A[i][j] * y[i] for i in range(len(A))) >= c[j]
        assert sum(bi * yi for bi, yi in zip(b, y)) == value == sum(ci * xi for ci, xi in zip(c, x))
        d, p = lp_density_fill(area, slack, r, U, w2)
        assert feasible(area, slack, p, r, U, w2)
        assert min(window_densities(area, p, r, w2)) == d


def test_integer_fills_bracket_the_lp():
    # Brute force over integer fill amounts. The integer optimum is at most the LP
    # optimum, and rounding the LP fill down loses less than one unit per tile.
    rng = random.Random(4)
    for trial in range(6):
        m, r = 3, 2
        area = [[rng.randint(0, 3) for _ in range(m)] for _ in range(m)]
        slack = [[rng.randint(0, min(2, 4 - area[i][j])) for j in range(m)] for i in range(m)]
        U = Fraction(rng.randint(10, 14), 16)
        w2 = 16
        res = lp_density_fill(area, slack, r, U, w2)
        if res is None:
            continue
        d, p = res
        best = None
        for fill in itertools.product(*[range(slack[i][j] + 1) for i in range(m) for j in range(m)]):
            q = [[Fraction(fill[i * m + j]) for j in range(m)] for i in range(m)]
            dens = window_densities(area, q, r, w2)
            if max(dens) <= U and (best is None or min(dens) > best):
                best = min(dens)
        assert best <= d
        assert d - best < Fraction(r * r, w2)
        down = [[Fraction(int(v)) for v in row] for row in p]
        assert feasible(area, slack, down, r, U, w2)


def overlap(cell, x, y, w):
    cx, cy, h = cell
    dx = min(cx + h, x + w) - max(cx, x)
    dy = min(cy + h, y + w) - max(cy, y)
    return dx * dy if dx > 0 and dy > 0 else 0


def density(cells, x, y, w):
    return sum(overlap(c, x, y, w) for c in cells) / Fraction(w * w)


def test_floating_windows_within_fixed_bound():
    rng = random.Random(5)
    n, w = 8, 4
    h = Fraction(1, 2)
    for r in [1, 2, 4]:
        t = Fraction(w, r)
        cells = [(i * h, j * h, h) for i in range(16) for j in range(16) if rng.random() < 0.3]
        grid = [k * t for k in range(int((n - w) / t) + 1)]
        fixed = [density(cells, x, y, w) for x in grid for y in grid]
        lo, hi = min(fixed), max(fixed)
        e = floating_error(r)
        offsets = [Fraction(k, 4) for k in range(0, 17, 2)] + [Fraction(rng.randint(0, 400), 100) for _ in range(5)]
        for x in offsets:
            for y in offsets:
                d = density(cells, x, y, w)
                assert lo - e <= d <= hi + e


def test_floating_bound_is_attained():
    # Features fill the window at offset (t/2, t/2): every fixed window has density at
    # most (1 - 1/(2r))^2, while that floating window has density 1. The complement
    # layout attains the lower bound.
    for r in [1, 2, 3, 4]:
        w = 2 * r
        t = Fraction(w, r)
        n = 2 * w
        square = [(t / 2 + i, t / 2 + j, 1) for i in range(w) for j in range(w)]
        grid = [k * t for k in range(int((n - w) / t) + 1)]
        fixed = [density(square, x, y, w) for x in grid for y in grid]
        assert max(fixed) + floating_error(r) == 1 == density(square, t / 2, t / 2, w)
        half = [(i * Fraction(1, 2), j * Fraction(1, 2), Fraction(1, 2)) for i in range(2 * n) for j in range(2 * n)]
        hole = [c for c in half if overlap(c, t / 2, t / 2, w) == 0]
        fixed = [density(hole, x, y, w) for x in grid for y in grid]
        assert min(fixed) - floating_error(r) == 0 == density(hole, t / 2, t / 2, w)


def test_page_example():
    area = [[Fraction(k, 10) for k in row] for row in [[6, 2, 1], [5, 3, 0], [4, 1, 0]]]
    slack = [[Fraction(k, 10) for k in row] for row in [[1, 4, 5], [2, 3, 6], [3, 5, 2]]]
    assert window_densities(area, [[0] * 3] * 3, 2, 4) == [Fraction(2, 5), Fraction(3, 20), Fraction(13, 40), Fraction(1, 10)]
    d, p = lp_density_fill(area, slack, 2, Fraction(1, 2), 4)
    assert d == Fraction(19, 40)
    assert feasible(area, slack, p, 2, Fraction(1, 2), 4)
    mine = [[Fraction(k, 10) for k in row] for row in [[0, 1, 3], [0, 3, 6], [0, 4, 2]]]
    assert window_densities(area, mine, 2, 4) == [Fraction(1, 2), Fraction(19, 40), Fraction(1, 2), Fraction(19, 40)]
    assert lp_density_fill(area, slack, 2, Fraction(3, 10), 4) is None


def test_window_helpers():
    assert windows(3, 2) == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert window_tiles(1, 0, 2) == [(1, 0), (1, 1), (2, 0), (2, 1)]
    assert floating_error(1) == Fraction(3, 4)
