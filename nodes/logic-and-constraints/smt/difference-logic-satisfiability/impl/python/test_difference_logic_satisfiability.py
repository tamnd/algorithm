# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-logic-satisfiability/. The authors are listed in prov/K5P9JR.jsonl.

import itertools
import random
from fractions import Fraction

from difference_logic_satisfiability import check_cycle, check_model, solve


def brute_feasible(n: int, constraints: list[tuple]) -> bool:
    """Search the integer box [-K, 0]^n, with K the sum of the negative weights.

    If integer constraints are feasible, the shortest-path model is integer,
    lies in this box, and so the search is complete for integer weights.
    """
    k = sum(max(0, -c) for _, _, c in constraints)
    for point in itertools.product(range(-k, 1), repeat=n):
        if check_model(constraints, list(point)):
            return True
    return False


def test_page_example() -> None:
    a, b, c = 0, 1, 2
    unsat = [(a, b, 1), (b, c, -2), (c, a, 0)]
    ok, cycle = solve(3, unsat)
    assert not ok and check_cycle(unsat, cycle) and sorted(cycle) == [0, 1, 2]
    sat = [(a, b, 1), (b, c, -2), (c, a, 2)]
    ok, model = solve(3, sat)
    assert ok and model == [-1, -2, 0] and check_model(sat, model)


def test_job_shop_example() -> None:
    s0, s1, s2 = 0, 1, 2
    base = [(s0, s1, 0), (s0, s2, 0), (s1, s0, 2), (s2, s0, 2)]  # 0 <= s_i - s0 <= 2
    ok, cycle = solve(3, base + [(s1, s2, -3)])  # J1 before J2
    assert not ok and check_cycle(base + [(s1, s2, -3)], cycle)
    ok, model = solve(3, base + [(s2, s1, -2)])  # J2 before J1
    assert ok and check_model(base + [(s2, s1, -2)], model)
    assert model[s1] - model[s0] == 2 and model[s2] - model[s0] == 0


def test_edges() -> None:
    assert solve(0, []) == (True, [])
    assert solve(2, []) == (True, [0, 0])
    ok, cycle = solve(1, [(0, 0, -1)])  # x - x <= -1
    assert not ok and cycle == [0]
    ok, model = solve(1, [(0, 0, 0)])
    assert ok


def test_fractions() -> None:
    cons = [(0, 1, Fraction(1, 2)), (1, 0, Fraction(-1, 3))]
    ok, model = solve(2, cons)
    assert ok and check_model(cons, model)
    cons = [(0, 1, Fraction(1, 3)), (1, 0, Fraction(-1, 2))]
    ok, cycle = solve(2, cons)
    assert not ok and check_cycle(cons, cycle)


def test_random_against_brute_force() -> None:
    rng = random.Random(1977)
    seen = {True: 0, False: 0}
    for _ in range(1500):
        n = rng.randint(1, 4)
        m = rng.randint(1, 5)
        cons = [(rng.randrange(n), rng.randrange(n), rng.randint(-2, 2)) for _ in range(m)]
        ok, out = solve(n, cons)
        assert ok == brute_feasible(n, cons)
        seen[ok] += 1
        if ok:
            assert check_model(cons, out)
            assert all(isinstance(v, int) for v in out)  # integer weights give an integer model
        else:
            assert check_cycle(cons, out)
    assert seen[True] > 100 and seen[False] > 100


def test_larger_random_models_and_cycles() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(5, 12)
        m = rng.randint(n, 3 * n)
        cons = [(rng.randrange(n), rng.randrange(n), rng.randint(-3, 6)) for _ in range(m)]
        ok, out = solve(n, cons)
        if ok:
            assert check_model(cons, out)
        else:
            assert check_cycle(cons, out)
