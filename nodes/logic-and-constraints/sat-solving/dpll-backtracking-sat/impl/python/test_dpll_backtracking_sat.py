# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll-backtracking-sat/. The authors are listed in prov/EPST33.jsonl.

import itertools
import random

from dpll_backtracking_sat import dpll_backtracking_sat


def brute_force(n: int, clauses: list[list[int]]) -> list[list[int]]:
    """All models, by trying the 2^n assignments."""
    models = []
    for bits in itertools.product([False, True], repeat=n):
        if all(any(bits[abs(q) - 1] == (q > 0) for q in c) for c in clauses):
            models.append([v + 1 if bits[v] else -(v + 1) for v in range(n)])
    return models


def satisfies(model: list[int], clauses: list[list[int]]) -> bool:
    s = set(model)
    return all(any(q in s for q in c) for c in clauses)


def pigeonhole(p: int, h: int) -> tuple[int, list[list[int]]]:
    x = lambda i, j: i * h + j + 1  # noqa: E731
    cl = [[x(i, j) for j in range(h)] for i in range(p)]
    for j in range(h):
        for a in range(p):
            for b in range(a + 1, p):
                cl.append([-x(a, j), -x(b, j)])
    return p * h, cl


def test_page_example() -> None:
    f = [[1, 2], [1, -2], [-1, 3], [-2, -3]]
    log: list[tuple[int, bool, bool]] = []
    assert dpll_backtracking_sat(3, f, log) == [1, -2, 3]
    assert log == [
        (1, False, True),
        (2, False, False),
        (2, True, False),
        (1, True, True),
        (2, False, True),
        (3, False, False),
        (3, True, True),
    ]


def test_full_tree_on_a_trivial_unsat_formula() -> None:
    for n in range(1, 11):
        log: list[tuple[int, bool, bool]] = []
        assert dpll_backtracking_sat(n, [[n], [-n]], log) is None
        assert len(log) == 2 ** (n + 1) - 2


def test_hand_cases() -> None:
    assert dpll_backtracking_sat(0, []) == []
    assert dpll_backtracking_sat(0, [[]]) is None
    assert dpll_backtracking_sat(2, [[1], []]) is None
    assert dpll_backtracking_sat(3, []) == [-1, -2, -3]
    assert dpll_backtracking_sat(1, [[1], [-1]]) is None
    assert dpll_backtracking_sat(2, [[1, -1]]) == [-1, -2]
    assert dpll_backtracking_sat(2, [[1, 1, 2], [-2]]) == [1, -2]


def test_pigeonhole() -> None:
    for h in range(1, 4):
        n, f = pigeonhole(h + 1, h)
        assert dpll_backtracking_sat(n, f) is None
        n, f = pigeonhole(h, h)
        model = dpll_backtracking_sat(n, f)
        assert model is not None and satisfies(model, f)


def test_random_against_brute_force() -> None:
    rng = random.Random(1962)
    for t in range(600):
        n = rng.randint(1, 10)
        if t % 2 == 0:
            m, k = round(4.26 * n), min(3, n)
            f = [[v if rng.random() < 0.5 else -v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]
        else:
            f = []
            for _ in range(rng.randint(0, 4 * n)):
                vs = rng.sample(range(1, n + 1), rng.randint(1, min(4, n)))
                f.append([v if rng.random() < 0.5 else -v for v in vs])
        models = brute_force(n, f)
        got = dpll_backtracking_sat(n, f)
        if not models:
            assert got is None
        else:
            assert got is not None and satisfies(got, f)
            # false before true, x1 first: the answer is the first model in that order
            assert got == models[0]
