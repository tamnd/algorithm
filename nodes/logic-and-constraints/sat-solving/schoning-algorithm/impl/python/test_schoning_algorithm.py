# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schoning-algorithm/. The authors are listed in prov/JNC89S.jsonl.

import itertools
import random

from schoning_algorithm import _Walk, papadimitriou_2sat, schoning_algorithm, schoning_try, success_lower_bound, tries_for


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def brute_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(b)) for b in itertools.product([False, True], repeat=n))


def random_cnf(rng: random.Random, n: int, m: int, k: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]


# all 8 sign patterns over x1, x2, x3 except the clause (-x1 or x2 or x3), so 100 is the only model
EXAMPLE = [[1, 2, 3], [-1, -2, 3], [1, -2, -3], [-1, 2, -3], [1, 2, -3], [-1, -2, -3], [1, -2, 3]]


def test_example() -> None:
    models = [b for b in itertools.product([False, True], repeat=3) if satisfies(EXAMPLE, list(b))]
    assert models == [(True, False, False)]
    for seed in range(20):
        assert schoning_algorithm(3, EXAMPLE, rng=random.Random(seed)) == [True, False, False]
    # the walk of the page: 011 -> 010 -> 000 -> 100
    w = _Walk(3, EXAMPLE, [False, True, True])
    assert [EXAMPLE[j] for j in w.false_list] == [[1, -2, -3]]
    w.flip(3)
    assert [EXAMPLE[j] for j in w.false_list] == [[1, -2, 3]]
    w.flip(2)
    assert [EXAMPLE[j] for j in w.false_list] == [[1, 2, 3]]
    w.flip(1)
    assert w.false_list == []
    full = [[a, b, c] for a in (1, -1) for b in (2, -2) for c in (3, -3)]
    assert schoning_algorithm(3, full, tries=50, rng=random.Random(1)) is None


def test_edges() -> None:
    assert schoning_algorithm(0, [], tries=1) == []
    assert schoning_algorithm(2, [[]], tries=5) is None
    assert schoning_algorithm(1, [[1]], rng=random.Random(0)) == [True]
    assert schoning_algorithm(1, [[1], [-1]], tries=20, rng=random.Random(0)) is None
    x = schoning_algorithm(2, [[1, 1], [-2, -2]], rng=random.Random(0))
    assert x == [True, False]


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(600):
        n = rng.randint(3, 9)
        k = rng.choice([2, 3, 3, 4])
        m = rng.randint(1, int(4.5 * n))
        clauses = random_cnf(rng, n, m, min(k, n))
        x = schoning_algorithm(n, clauses, tries=300, rng=random.Random(rng.randrange(10**9)))
        truth = brute_sat(n, clauses)
        if x is not None:
            assert satisfies(clauses, x)  # one-sided error: every answer is a model
        if truth:
            assert x is not None  # the fixed seeds find a model in each case
            sat += 1
        else:
            assert x is None
            unsat += 1
    assert sat > 200 and unsat > 50


def test_walk_bookkeeping() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 8)
        clauses = [[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 10))]
        w = _Walk(n, clauses, [rng.random() < 0.5 for _ in range(n)])
        for _ in range(30):
            w.flip(rng.randint(1, n))
            x = w.x[1:]
            false = sorted(j for j, cl in enumerate(clauses) if not satisfies([cl], x))
            assert sorted(w.false_list) == false


def test_success_rate_above_bound() -> None:
    # measured, with a fixed seed: one try succeeds far more often than the proved bound
    rng = random.Random(77)
    n = 10
    planted = [rng.random() < 0.5 for _ in range(n)]
    clauses = [cl for cl in random_cnf(rng, n, 60, 3) if satisfies([cl], planted)]
    hits = sum(schoning_try(n, clauses, rng, 3 * n) is not None for _ in range(2000))
    assert hits / 2000 >= success_lower_bound(n, 3)
    assert tries_for(n, 3, 0.01) >= 1


def test_papadimitriou_2sat() -> None:
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(2, 10)
        clauses = random_cnf(rng, n, rng.randint(1, 2 * n), 2)
        x = papadimitriou_2sat(n, clauses, random.Random(rng.randrange(10**9)), rounds=20)
        if brute_sat(n, clauses):
            assert x is not None and satisfies(clauses, x)
        else:
            assert x is None


def test_planted_larger() -> None:
    rng = random.Random(5)
    n = 30
    planted = [rng.random() < 0.5 for _ in range(n)]
    clauses = [cl for cl in random_cnf(rng, n, 150, 3) if satisfies([cl], planted)]
    x = schoning_algorithm(n, clauses, tries=2000, rng=random.Random(6))
    assert x is not None and satisfies(clauses, x)
