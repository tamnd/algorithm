# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gsat/. The authors are listed in prov/BW0R7G.jsonl.

import itertools
import random

from gsat import gsat, normalize, scores


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def count_sat(clauses: list[list[int]], x: list[bool]) -> int:
    return sum(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def brute_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(b)) for b in itertools.product([False, True], repeat=n))


def random_cnf(rng: random.Random, n: int, m: int, k: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]


EXAMPLE = [[1, 2], [-1, 3], [-3, -2], [2, 3], [-1, -2, -3]]


def test_example() -> None:
    # the page example: x = 000 has 2 false clauses, and the scores pick x3 or x2
    x = [False, False, False, False]
    make, brk = scores(3, EXAMPLE, x)
    assert [make[v] - brk[v] for v in (1, 2, 3)] == [0, 2, 1]
    x[2] = True
    assert count_sat(EXAMPLE, x[1:]) == 5
    models = [list(b) for b in itertools.product([False, True], repeat=3) if satisfies(EXAMPLE, list(b))]
    assert models == [[False, True, False], [True, False, True]]
    for seed in range(20):
        assert gsat(3, EXAMPLE, rng=random.Random(seed)) in models


def test_edges() -> None:
    assert gsat(0, []) == []
    assert gsat(2, [[]]) is None
    assert gsat(1, [[1, -1]], rng=random.Random(0)) is not None
    assert gsat(1, [[1], [-1]], rng=random.Random(0)) is None
    assert gsat(1, [[1, 1]], rng=random.Random(0)) == [True]
    assert normalize([[2, 1, 2], [3, -3]]) == [[1, 2]]


def test_score_is_change_in_satisfied_clauses() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 8)
        cls = normalize([[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 12))])
        assert cls is not None
        x = [False] + [rng.random() < 0.5 for _ in range(n)]
        make, brk = scores(n, cls, x)
        before = count_sat(cls, x[1:])
        for v in range(1, n + 1):
            y = x[:]
            y[v] = not y[v]
            assert count_sat(cls, y[1:]) - before == make[v] - brk[v]


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(500):
        n = rng.randint(3, 9)
        m = rng.randint(1, int(4.5 * n))
        clauses = random_cnf(rng, n, m, rng.choice([2, 3, 3]))
        x = gsat(n, clauses, max_tries=30, rng=random.Random(rng.randrange(10**9)))
        if x is not None:
            assert satisfies(clauses, x)  # an answer is always a model
        if brute_sat(n, clauses):
            assert x is not None  # the fixed seeds solve each satisfiable case
            sat += 1
        else:
            assert x is None
            unsat += 1
    assert sat > 200 and unsat > 50


def test_planted() -> None:
    rng = random.Random(5)
    n = 40
    planted = [rng.random() < 0.5 for _ in range(n)]
    clauses = [cl for cl in random_cnf(rng, n, 220, 3) if satisfies([cl], planted)]
    x = gsat(n, clauses, max_tries=20, max_flips=400, rng=random.Random(6))
    assert x is not None and satisfies(clauses, x)
