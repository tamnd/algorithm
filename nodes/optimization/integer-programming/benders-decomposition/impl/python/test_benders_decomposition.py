# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benders-decomposition/. The authors are listed in prov/09SW6A.jsonl.

import itertools
import random
from fractions import Fraction

from benders_decomposition import benders, dot, solve_lp

# The example of the page: two plants with module costs 5 and 3,
# module capacities 5 and 4, unit costs 1 and 3, demand 6.
C = [5, 3]
D = [1, 3]
G = [[0, 0], [5, 0], [0, 4]]
B = [[1, 1], [-1, 0], [0, -1]]
H = [6, 0, 0]


def solve_by_gauss(rows: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction] | None:
    n = len(rows)
    m = [r[:] + [v] for r, v in zip(rows, rhs)]
    for col in range(n):
        piv = next((i for i in range(col, n) if m[i][col] != 0), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        for i in range(n):
            if i != col and m[i][col] != 0:
                f = m[i][col] / m[col][col]
                m[i] = [a - f * b for a, b in zip(m[i], m[col])]
    return [m[i][n] / m[i][i] for i in range(n)]


def lp_by_vertices(c, a, b):
    """Maximize c x over a x <= b, x >= 0 by trying every basis (bounded case)."""
    n = len(c)
    full = [list(map(Fraction, r)) for r in a] + [[Fraction(-int(i == j)) for j in range(n)] for i in range(n)]
    rhs = [Fraction(v) for v in b] + [Fraction(0)] * n
    best = None
    for rows in itertools.combinations(range(len(full)), n):
        x = solve_by_gauss([full[i] for i in rows], [rhs[i] for i in rows])
        if x is not None and all(dot(full[i], x) <= rhs[i] for i in range(len(full))):
            v = dot(c, x)
            if best is None or v > best:
                best = v
    return best


def brute(c, d, g, bmat, h, box):
    best = None
    for x in itertools.product(*(range(lo, hi + 1) for lo, hi in box)):
        r = [Fraction(h[i]) - dot(g[i], x) for i in range(len(h))]
        st, _, v = solve_lp([-t for t in d], [[-t for t in row] for row in bmat], [-t for t in r])
        if st == "unbounded":
            return "unbounded", None
        if st == "optimal":
            val = dot(c, x) - v
            if best is None or val < best:
                best = val
    return ("infeasible", None) if best is None else ("optimal", best)


def check_solution(c, d, g, bmat, h, box, val, x, y):
    assert all(lo <= xj <= hi for xj, (lo, hi) in zip(x, box))
    assert all(v >= 0 for v in y)
    for i in range(len(h)):
        assert dot(g[i], x) + dot(bmat[i], y) >= h[i]
    assert dot(c, x) + dot(d, y) == val


def test_lp_solver_against_vertices() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(1, 3)
        m = rng.randint(1, 3)
        a = [[rng.randint(-3, 4) for _ in range(n)] for _ in range(m)] + [[1] * n]
        b = [rng.randint(-2, 6) for _ in range(m)] + [rng.randint(1, 8)]
        c = [rng.randint(-4, 5) for _ in range(n)]
        st, x, v = solve_lp(c, a, b)
        want = lp_by_vertices(c, a, b)
        if want is None:
            assert st == "infeasible"
        else:
            assert st == "optimal" and v == want
            assert all(dot(r, x) <= bi for r, bi in zip(a, b)) and min(x) >= 0
    assert solve_lp([1, 1], [[1, -1]], [1])[0] == "unbounded"


def test_example_of_the_page() -> None:
    trace: list = []
    st, val, x, y = benders(C, D, G, B, H, [(0, 2), (0, 2)], trace)
    assert (st, val, x) == ("optimal", 16, (1, 1))
    assert y == [5, 1]
    assert trace == [
        ("feasibility", (0, 0), None),
        ("optimality", (0, 2), 18),
        ("optimality", (2, 0), 6),
        ("optimality", (1, 1), 8),
    ]
    assert brute(C, D, G, B, H, [(0, 2), (0, 2)]) == ("optimal", 16)


def test_infeasible_and_unbounded() -> None:
    # demand 10 is more than the total capacity 9
    assert benders(C, D, G, B, [10, 0, 0], [(0, 1), (0, 1)])[0] == "infeasible"
    # x + y >= 1 and y may grow with a negative cost: unbounded
    assert benders([1], [-1], [[1]], [[1]], [1], [(0, 2)])[0] == "unbounded"
    # every x is cut off: y <= -1 written as -y >= 1
    assert benders([1], [1], [[0]], [[-1]], [1], [(0, 3)])[0] == "infeasible"


def test_against_brute_force() -> None:
    rng = random.Random(2024)
    seen = {"optimal": 0, "infeasible": 0, "unbounded": 0}
    for _ in range(120):
        p, q, m = rng.randint(1, 2), rng.randint(1, 3), rng.randint(1, 3)
        box = [(rng.randint(-1, 0), rng.randint(0, 2)) for _ in range(p)]
        c = [rng.randint(-3, 3) for _ in range(p)]
        d = [rng.randint(-1, 4) for _ in range(q)]
        g = [[rng.randint(-3, 3) for _ in range(p)] for _ in range(m)]
        bmat = [[rng.randint(-2, 3) for _ in range(q)] for _ in range(m)]
        h = [rng.randint(-3, 4) for _ in range(m)]
        st, val, x, y = benders(c, d, g, bmat, h, box)
        want = brute(c, d, g, bmat, h, box)
        assert st == want[0]
        seen[st] += 1
        if st == "optimal":
            assert val == want[1]
            check_solution(c, d, g, bmat, h, box, val, x, y)
    assert min(seen.values()) > 0
