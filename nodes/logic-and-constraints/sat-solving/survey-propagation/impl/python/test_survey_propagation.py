# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/survey-propagation/. The authors are listed in prov/VFSYED.jsonl.

import itertools
import random

from survey_propagation import Contradiction, biases, simplify, sp_decimation, survey_propagation


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def brute_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(b)) for b in itertools.product([False, True], repeat=n))


def random_cnf(rng: random.Random, n: int, m: int, k: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]


def test_warnings_follow_unit_propagation() -> None:
    # the page example: (x1) and (not x1 or x2) and (x2 or x3 or x4)
    cls = [[1], [-1, 2], [2, 3, 4]]
    eta = survey_propagation(cls, random.Random(0))
    assert eta is not None
    assert eta[0] == [1.0]  # a unit clause always sends a full warning
    assert abs(eta[1][1] - 1.0) < 1e-9  # x1 is forced true, so (not x1 or x2) warns x2
    assert eta[1][0] == 0.0  # x2 is not forced false, so no warning to x1
    assert all(e == 0.0 for e in eta[2])  # x2 is forced to satisfy the third clause
    w = biases(cls, eta)
    assert w[1] == (1.0, 0.0, 0.0) and w[2] == (1.0, 0.0, 0.0)
    assert w[3] == (0.0, 0.0, 1.0)  # x3 is free
    assert sp_decimation(4, cls, random.Random(0)) is not None


def test_contradiction() -> None:
    eta = survey_propagation([[1], [-1]], random.Random(0))
    assert eta == [[1.0], [1.0]]  # x1 is warned by both signs
    try:
        biases([[1], [-1]], eta)
    except Contradiction:
        pass
    else:
        raise AssertionError
    assert sp_decimation(1, [[1], [-1]], random.Random(0)) is None


def test_trivial_fixed_point_on_easy_formulas() -> None:
    # a tree-like formula with no forced variable converges to all-zero surveys
    cls = [[1, 2, 3], [-3, 4, 5], [-5, 6, 7]]
    eta = survey_propagation(cls, random.Random(1))
    assert eta is not None and max(max(e) for e in eta) < 1e-3


def test_simplify() -> None:
    fixed: dict[int, bool] = {}
    assert simplify([[1], [-1, 2], [-2, 3, 4]], fixed) == [[3, 4]]
    assert fixed == {1: True, 2: True}
    assert simplify([[1], [-1]], {}) is None
    assert simplify([[1, -1]], {}) == []


def test_edges() -> None:
    assert sp_decimation(0, []) == []
    assert sp_decimation(2, [[]]) is None
    x = sp_decimation(3, [[1, -1], [2]], random.Random(0))
    assert x is not None and x[1] is True


def test_small_against_brute_force() -> None:
    # answers are always models; on satisfiable formulas the success rate is measured
    rng = random.Random(2024)
    sat = solved = 0
    for _ in range(300):
        n = rng.randint(3, 10)
        m = rng.randint(1, int(4.5 * n))
        clauses = random_cnf(rng, n, m, 3)
        x = sp_decimation(n, clauses, random.Random(rng.randrange(10**9)), max_flips=2000)
        if x is not None:
            assert satisfies(clauses, x)
            solved += 1
        if brute_sat(n, clauses):
            sat += 1
        else:
            assert x is None
    assert solved >= 0.9 * sat


def test_decimation_on_a_random_formula() -> None:
    # n = 60, 250 clauses, fixed seeds: the surveys are not trivial, so decimation runs
    rng = random.Random(11)
    n = 60
    clauses = random_cnf(rng, n, 250, 3)
    eta = survey_propagation(clauses, random.Random(12))
    assert eta is not None and max(max(e) for e in eta) > 0.1
    x = sp_decimation(n, clauses, random.Random(12), max_flips=5000)
    assert x is not None and satisfies(clauses, x)
