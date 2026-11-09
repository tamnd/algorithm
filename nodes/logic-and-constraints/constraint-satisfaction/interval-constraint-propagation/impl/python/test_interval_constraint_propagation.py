# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-constraint-propagation/. The authors are listed in prov/34RZ0J.jsonl.

import itertools
import math
import random
from fractions import Fraction

from interval_constraint_propagation import compile_expr, hc4_revise, icp

INF = math.inf


def V(i):
    return ("var", i)


def K(c):
    return ("const", float(c))


def evaluate(expr, point):
    """Exact value of expr at a point of Fractions, by an explicit stack."""
    nodes = compile_expr(expr)
    val = []
    for node in nodes:
        op = node[0]
        if op == "var":
            val.append(point[node[1]])
        elif op == "const":
            val.append(Fraction(node[1]))
        elif op == "add":
            val.append(val[node[1]] + val[node[2]])
        elif op == "sub":
            val.append(val[node[1]] - val[node[2]])
        elif op == "mul":
            val.append(val[node[1]] * val[node[2]])
        else:
            val.append(val[node[1]] * val[node[1]])
    return val[-1]


def holds(constraints, point):
    for expr, lo, hi in constraints:
        v = evaluate(expr, point)
        if (lo != -INF and v < Fraction(lo)) or (hi != INF and v > Fraction(hi)):
            return False
    return True


def inside(box, point):
    return all(Fraction(lo) <= p <= Fraction(hi) for (lo, hi), p in zip(box, point))


def random_expr(rng, n, depth, consts):
    if depth == 0 or rng.random() < 0.3:
        if rng.random() < 0.7:
            return V(rng.randrange(n))
        return K(rng.choice(consts))
    op = rng.choice(["add", "sub", "mul", "sqr", "add", "sub"])
    if op == "sqr":
        return ("sqr", random_expr(rng, n, depth - 1, consts))
    return (op, random_expr(rng, n, depth - 1, consts), random_expr(rng, n, depth - 1, consts))


def random_constraint(rng, n, consts):
    expr = random_expr(rng, n, 3, consts)
    kind = rng.random()
    a = rng.choice(consts)
    if kind < 0.35:
        return (expr, a, a)
    if kind < 0.6:
        return (expr, -INF, a)
    if kind < 0.8:
        return (expr, a, INF)
    b = rng.choice(consts)
    return (expr, min(a, b), max(a, b))


def test_page_example():
    # x, y in [0, 10], y = x^2 and x + y = 2. The only solution is (1, 1).
    cons = [(("sub", V(1), ("sqr", V(0))), 0.0, 0.0), (("add", V(0), V(1)), 2.0, 2.0)]
    nodes = compile_expr(cons[0][0])
    first = hc4_revise(nodes, 0.0, 0.0, [(0.0, 10.0), (0.0, 10.0)])
    assert first[1] == (0.0, 10.0)
    assert math.sqrt(10.0) <= first[0][1] < math.sqrt(10.0) + 1e-12 and first[0][0] == 0.0
    box = icp([(0.0, 10.0), (0.0, 10.0)], cons, ratio=1e-9)
    for lo, hi in box:
        assert lo <= 1.0 <= hi and hi - lo < 1e-6


def test_far_from_hull():
    # x + y = 0 and x - y = 0 have the single solution (0, 0), but each
    # constraint alone removes nothing from [-1, 1]^2.
    cons = [(("add", V(0), V(1)), 0.0, 0.0), (("sub", V(0), V(1)), 0.0, 0.0)]
    assert icp([(-1.0, 1.0), (-1.0, 1.0)], cons) == [(-1.0, 1.0), (-1.0, 1.0)]
    # x^2 + y^2 = 1 and x = y: the hull of the two solutions is about
    # [-0.7071, 0.7071]^2, but propagation stops at [-1, 1]^2.
    circle = [(("add", ("sqr", V(0)), ("sqr", V(1))), 1.0, 1.0), (("sub", V(0), V(1)), 0.0, 0.0)]
    assert icp([(-2.0, 2.0), (-2.0, 2.0)], circle) == [(-1.0, 1.0), (-1.0, 1.0)]


def test_detects_empty():
    assert icp([(-1.0, 1.0)], [(("sub", V(0), V(0)), 1.0, 1.0)]) is None
    assert icp([(0.0, 1.0)], [(("sqr", V(0)), 4.0, 4.0)]) is None
    assert icp([(2.0, 1.0)], []) is None
    assert icp([(-INF, INF)], [(("sqr", V(0)), -INF, -1.0)]) is None


def test_unbounded_and_overflow():
    box = icp([(-INF, INF), (1.0, 2.0)], [(("mul", V(0), V(1)), 3.0, 4.0)])
    assert box[0][0] <= 1.5 and box[0][1] >= 4.0 and box[0][1] < 4.0 + 1e-9
    big = 1e308
    box = icp([(big, big), (big, big), (-INF, INF)], [(("sub", V(2), ("add", V(0), V(1))), 0.0, 0.0)])
    assert box[2][0] >= 1e308 and box[2][1] == INF


def test_integer_grid_no_solution_removed():
    rng = random.Random(1999)
    nonempty = 0
    for _ in range(600):
        n = rng.randint(1, 3)
        r = rng.randint(1, 4)
        box = [(float(-r), float(r))] * n
        cons = [random_constraint(rng, n, list(range(-4, 5))) for _ in range(rng.randint(1, 3))]
        grid = [p for p in itertools.product(range(-r, r + 1), repeat=n) if holds(cons, [Fraction(v) for v in p])]
        out = icp(box, cons)
        if out is None:
            assert grid == []
            continue
        nonempty += 1
        for (lo, hi), (blo, bhi) in zip(out, box):
            assert blo <= lo <= hi <= bhi
        for p in grid:
            assert inside(out, p)
    assert nonempty > 100


def test_decimal_grid_with_rounding():
    # Grid points k / 10 and constants such as 0.3 are not floats, so every
    # step rounds; no grid solution may be lost.
    rng = random.Random(2010)
    consts = [-1.5, -0.7, -0.3, 0.0, 0.1, 0.3, 0.6, 1.2, 2.5]
    with_points = 0
    for _ in range(500):
        n = rng.randint(1, 2)
        box = [(-1.0, 1.0)] * n
        cons = [random_constraint(rng, n, consts) for _ in range(rng.randint(1, 2))]
        pts = [Fraction(k, 10) for k in range(-10, 11)]
        grid = [p for p in itertools.product(pts, repeat=n) if holds(cons, list(p))]
        out = icp(box, cons)
        with_points += bool(grid)
        if out is None:
            assert grid == []
        else:
            for p in grid:
                assert inside(out, p)
    assert with_points > 150
