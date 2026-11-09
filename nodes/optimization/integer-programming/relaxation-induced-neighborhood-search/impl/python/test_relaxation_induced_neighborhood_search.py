# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relaxation-induced-neighborhood-search/. The authors are listed in prov/6HZ5A8.jsonl.

import itertools
import random
from fractions import Fraction

import pytest
from relaxation_induced_neighborhood_search import minimize_lp, rins, solve_lp


def value(c, x) -> Fraction:
    return sum((Fraction(ci) * xi for ci, xi in zip(c, x)), Fraction(0))


def feasible(a, b, integers, x) -> bool:
    return (
        all(v >= 0 for v in x)
        and all(Fraction(x[j]).denominator == 1 for j in integers)
        and all(value(r, x) <= bi for r, bi in zip(a, b))
    )


def box_instance(rng, n, m, hi):
    a = [[rng.randint(-3, 5) for _ in range(n)] for _ in range(m)]
    b = [rng.randint(0, 12) for _ in range(m)]
    a += [[int(k == j) for k in range(n)] for j in range(n)]
    b += [hi] * n
    c = [rng.randint(-6, 3) for _ in range(n)]
    return c, a, b


def test_lp_solver_small_cases() -> None:
    assert solve_lp([1, 1], [[1, 2], [3, 1]], [4, 6]) == ("optimal", [Fraction(8, 5), Fraction(6, 5)], Fraction(14, 5))
    assert solve_lp([1], [[1], [-1]], [1, -2])[0] == "infeasible"
    assert solve_lp([1, 0], [[0, 1]], [3])[0] == "unbounded"
    with pytest.raises(ValueError):
        minimize_lp([-1], [[-1]], [0])


def test_example_of_the_page() -> None:
    w = [6, 2, 5, 7, 3]
    c = [-6, -8, -3, -7, -4]
    a = [w] + [[int(k == j) for k in range(5)] for j in range(5)]
    b = [14] + [1] * 5
    trace: list = []
    x, v, fixed, nodes = rins(c, a, b, range(5), [1, 1, 1, 0, 0], trace=trace)
    assert (x, v, fixed, nodes) == ([1, 1, 0, 0, 1], -18, [0, 1], 7)
    assert [t[0] if t[0] != "node" else t[2] for t in trace] == [
        "fix", -21, Fraction(-99, 5), -18, "improve", Fraction(-55, 3), -17, None, None
    ]
    # the global optimum is 19 (items 2, 4, 5), outside this neighborhood
    best = min(value(c, q) for q in itertools.product((0, 1), repeat=5) if feasible(a, b, range(5), q))
    assert best == -19


def test_never_worse_and_always_feasible() -> None:
    rng = random.Random(17)
    improved = 0
    for _ in range(120):
        n, m = rng.randint(2, 4), rng.randint(1, 3)
        c, a, b = box_instance(rng, n, m, 2)
        pts = [q for q in itertools.product(range(3), repeat=n) if feasible(a, b, range(n), q)]
        if not pts:
            continue
        inc = rng.choice(pts)
        x, v, fixed, _ = rins(c, a, b, list(range(n)), inc, node_limit=rng.randint(1, 6))
        assert feasible(a, b, range(n), x)
        assert v == value(c, x) <= value(c, inc)
        improved += v < value(c, inc)
    assert improved > 20


def test_full_search_solves_the_sub_mip() -> None:
    # with no node limit, RINS returns the optimum of the sub-MIP
    rng = random.Random(23)
    for _ in range(120):
        n, m = rng.randint(2, 4), rng.randint(1, 3)
        c, a, b = box_instance(rng, n, m, 2)
        pts = [q for q in itertools.product(range(3), repeat=n) if feasible(a, b, range(n), q)]
        if not pts:
            continue
        inc = rng.choice(pts)
        x, v, fixed, _ = rins(c, a, b, list(range(n)), inc, node_limit=10**6)
        sub = [q for q in pts if all(q[j] == inc[j] for j in fixed)]
        assert v == min(value(c, q) for q in sub)


def test_mixed_integer() -> None:
    rng = random.Random(31)
    for _ in range(80):
        n, m = rng.randint(2, 4), rng.randint(1, 3)
        c, a, b = box_instance(rng, n, m, 3)
        integers = sorted(rng.sample(range(n), rng.randint(1, n)))
        pts = [q for q in itertools.product(range(4), repeat=n) if feasible(a, b, integers, q)]
        if not pts:
            continue
        inc = rng.choice(pts)
        x, v, _, nodes = rins(c, a, b, integers, inc, node_limit=50)
        assert nodes <= 50
        assert feasible(a, b, integers, x)
        assert v <= value(c, inc)


def test_incumbent_already_optimal() -> None:
    c = [-1, -1]
    a = [[1, 1], [1, 0], [0, 1]]
    b = [1, 1, 1]
    x, v, _, _ = rins(c, a, b, [0, 1], [1, 0])
    assert (x, v) == ([1, 0], -1)
