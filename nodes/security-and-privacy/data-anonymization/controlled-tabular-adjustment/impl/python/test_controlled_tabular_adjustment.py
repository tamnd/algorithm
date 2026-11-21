# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/controlled-tabular-adjustment/. The authors are listed in prov/P26HSK.jsonl.
import itertools
import random
from fractions import Fraction as F

from controlled_tabular_adjustment import bounded_simplex, check, cta


def full_table(inner):
    t = [row + [sum(row)] for row in inner]
    t.append([sum(t[r][c] for r in range(len(inner))) for c in range(len(t[0]))])
    return [v for row in t for v in row]


def relations(rows, cols):
    w = cols + 1
    rel = [[(r * w + c, 1) for c in range(cols)] + [(r * w + cols, -1)] for r in range(rows + 1)]
    rel += [[(r * w + c, 1) for r in range(rows)] + [(rows * w + c, -1)] for c in range(cols + 1)]
    return rel


PAGE = [[20, 10, 15], [5, 25, 30], [12, 18, 10]]


def page_problem():
    a = [F(v) for v in full_table(PAGE)]
    n = len(a)
    return a, relations(3, 3), [F(0)] * n, [F(10**6)] * n, [1] * n


def test_page_example() -> None:
    a, rel, lo, up, w = page_problem()
    sens = {4: (F(3), F(3)), 10: (F(2), F(2))}
    x, cost, chosen = cta(a, rel, lo, up, w, sens, eps=0)
    assert cost == 12 and chosen == {4: -1, 10: -1}
    assert check(x, a, rel, lo, up, sens, eps=0)
    y = [x[i] - a[i] for i in range(16)]
    assert y == [1, -1, 0, 0, -3, 1, 2, 0, 2, 0, -2, 0, 0, 0, 0, 0]
    costs = {}
    for d in itertools.product((-1, 1), repeat=2):
        costs[d] = cta(a, rel, lo, up, w, sens, directions={4: d[0], 10: d[1]}, eps=0)[1]
    assert costs == {(-1, -1): 12, (-1, 1): 16, (1, -1): 16, (1, 1): 12}
    one = cta(a, rel, lo, up, w, {4: (F(3), F(3))}, eps=0)
    assert one[1] == 12
    # The same problem in floats gives the same cost.
    xf, cf, _ = cta([float(v) for v in a], rel, [0.0] * 16, [1e6] * 16, w, {4: (3.0, 3.0), 10: (2.0, 2.0)})
    assert abs(cf - 12) < 1e-7


def test_infeasible() -> None:
    a = [F(v) for v in full_table([[1, 2], [3, 4]])]
    rel = relations(2, 2)
    # Every cell is fixed, so no sensitive cell can move.
    assert cta(a, rel, a, a, [1] * 9, {0: (F(1), F(1))}, eps=0) is None
    # Cell 0 may only go down to 0, which is not below 1 - 2.
    lo = [v - 1 for v in a]
    up = list(a)
    assert cta(a, rel, lo, up, [1] * 9, {0: (F(2), F(1))}, eps=0) is None


def test_simplex_small() -> None:
    # minimize -x - y with x + y + s = 4, x <= 3, y <= 3: optimum -4.
    value, x = bounded_simplex([[1, 1, 1]], [4], [-1, -1, 0], [3, 3, float("inf")], eps=0)
    assert value == -4 and x[0] + x[1] == 4
    # x + y = 5 with x, y <= 2 has no solution.
    assert bounded_simplex([[1, 1]], [5], [1, 1], [2, 2], eps=0) is None
    # A redundant row.
    value, x = bounded_simplex([[1, 1], [2, 2]], [2, 4], [1, 2], [5, 5], eps=0)
    assert value == 2 and x == [2, 0]


def brute(a, lo, up, w, sens):
    """All integer adjustments of a 2 x 2 table with totals. The table relations form a
    totally unimodular matrix, so the LP optimum of each direction is an integer point."""
    best = None
    ranges = [range(int(lo[i] - a[i]), int(up[i] - a[i]) + 1) for i in (0, 1, 3, 4)]
    for y00, y01, y10, y11 in itertools.product(*ranges):
        y = [y00, y01, y00 + y01, y10, y11, y10 + y11, y00 + y10, y01 + y11, y00 + y01 + y10 + y11]
        if any(a[i] + y[i] < lo[i] or a[i] + y[i] > up[i] for i in range(9)):
            continue
        if any(not (y[p] >= upl or y[p] <= -lpl) for p, (lpl, upl) in sens.items()):
            continue
        cost = sum(w[i] * abs(y[i]) for i in range(9))
        if best is None or cost < best:
            best = cost
    return best


def test_against_brute_force() -> None:
    rng = random.Random(2006)
    rel = relations(2, 2)
    for _ in range(500):
        a = full_table([[rng.randint(0, 6) for _ in range(2)] for _ in range(2)])
        lo = [a[i] - rng.randint(0, 2) for i in range(9)]
        up = [a[i] + rng.randint(0, 2) for i in range(9)]
        w = [rng.randint(1, 3) for _ in range(9)]
        cells = rng.sample(range(9), rng.randint(1, 2))
        sens = {p: (rng.randint(1, 2), rng.randint(1, 2)) for p in cells}
        want = brute(a, lo, up, w, sens)
        res = cta([float(v) for v in a], rel, lo, up, w, sens)
        if want is None:
            assert res is None
            continue
        x, cost, chosen = res
        assert abs(cost - want) < 1e-6
        assert check(x, a, rel, lo, up, sens, eps=1e-6)
        assert abs(sum(w[i] * abs(x[i] - a[i]) for i in range(9)) - cost) < 1e-6
        fixed = cta([float(v) for v in a], rel, lo, up, w, sens, directions={p: 1 for p in cells})
        if fixed is not None:
            assert fixed[1] >= cost - 1e-6
