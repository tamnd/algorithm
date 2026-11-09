# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gomory-cutting-plane-algorithm/. The authors are listed in prov/BP9Q4E.jsonl.

import random
from fractions import Fraction
from itertools import product

from gomory_cutting_plane_algorithm import gomory, lex_max_lp


def brute(A, b, c, box):
    """Integer optimum over the box [0, box]^n, by enumeration."""
    best = None
    for x in product(range(box + 1), repeat=len(c)):
        if all(sum(a * xi for a, xi in zip(row, x)) <= bi for row, bi in zip(A, b)):
            v = sum(ci * xi for ci, xi in zip(c, x))
            if best is None or v > best:
                best = v
    return best


def check(A, b, c, box):
    """Run gomory and compare with brute force; check every cut."""
    res = gomory(A, b, c)
    ref = brute(A, b, c, box)
    feasible = [x for x in product(range(box + 1), repeat=len(c))
                if all(sum(a * xi for a, xi in zip(row, x)) <= bi for row, bi in zip(A, b))]
    assert len(res.cuts) in (len(res.points), len(res.points) - 1)
    for (g, g0), p in zip(res.cuts, res.points):
        # the cut is valid for each integer feasible point
        assert all(sum(gk * xk for gk, xk in zip(g, x)) <= g0 for x in feasible)
        # the cut separates the LP vertex of its round
        assert sum(gk * pk for gk, pk in zip(g, p)) > g0
    if ref is None:
        assert res.status == "infeasible"
    else:
        assert res.status == "optimal"
        assert res.value == ref
        assert tuple(res.x) in feasible
        assert sum(ci * xi for ci, xi in zip(c, res.x)) == ref
    return res


def boxed(A, b, n, box):
    return [list(r) for r in A] + [[int(k == j) for k in range(n)] for j in range(n)], list(b) + [box] * n


def test_page_example() -> None:
    res = check([[3, 2], [-3, 2]], [6, 0], [0, 1], 3)
    assert res.status == "optimal" and res.x == [1, 1] and res.value == 1
    assert res.cuts == [([0, 1], 1), ([1, 1], 2)]
    assert res.points == [[Fraction(1), Fraction(3, 2)], [Fraction(4, 3), Fraction(1)], [Fraction(1), Fraction(1)]]


def test_integral_lp_needs_no_cut() -> None:
    # a totally unimodular system: the first LP vertex is integral
    res = check([[1, 1], [1, -1]], [4, 2], [2, 1], 4)
    assert res.cuts == [] and res.value == 7 and res.x == [3, 1]


def test_infeasible_parity() -> None:
    # 2x1 - 2x2 = 1 has real but no integer solutions
    A, b = boxed([[2, -2], [-2, 2]], [1, -1], 2, 3)
    res = check(A, b, [1, 1], 3)
    assert res.status == "infeasible" and len(res.cuts) >= 1


def test_infeasible_lp() -> None:
    A, b = boxed([[1, 1], [-1, -1]], [1, -3], 2, 3)
    assert lex_max_lp(A, b, [1, 0]) is None
    assert gomory(A, b, [1, 0]).status == "infeasible"


def test_degenerate() -> None:
    # three constraints through the vertex (1, 1), and a fractional optimum elsewhere
    A, b = boxed([[1, 1], [1, -1], [2, 1], [2, 2]], [2, 0, 3, 5], 2, 3)
    check(A, b, [1, 2], 3)
    check(A, b, [3, 1], 3)


def test_thin_triangle_needs_many_rounds() -> None:
    # P_t = conv{(0,0), (0,1), (t, 1/2)}: max x1 has LP value t and integer value 0
    for t in (1, 2, 3):
        A = [[1, -2 * t], [1, 2 * t]]
        b = [0, 2 * t]
        res = check(A, b, [1, 0], 2 * t)
        assert res.value == 0 and len(res.cuts) >= 2 * t


def test_random_against_brute_force() -> None:
    rng = random.Random(1958)
    for _ in range(500):
        n = rng.choice((1, 2, 2, 3))
        m = rng.randint(1, 3)
        box = 3
        A = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(m)]
        b = [rng.randint(-3, 9) for _ in range(m)]
        c = [rng.randint(-3, 5) for _ in range(n)]
        A, b = boxed(A, b, n, box)
        check(A, b, c, box)
