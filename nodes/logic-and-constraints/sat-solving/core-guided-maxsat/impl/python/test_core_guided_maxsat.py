# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/core-guided-maxsat/. The authors are listed in prov/D7BD01.jsonl.

import itertools
import random

from core_guided_maxsat import core_guided_maxsat, dpll, exactly_one, minimal_core


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def false_count(clauses: list[list[int]], x: list[bool]) -> int:
    return sum(not satisfies([c], x) for c in clauses)


def brute(n: int, hard: list[list[int]], soft: list[list[int]]) -> int | None:
    best = None
    for b in itertools.product([False, True], repeat=n):
        x = list(b)
        if satisfies(hard, x):
            c = false_count(soft, x)
            best = c if best is None else min(best, c)
    return best


def random_clauses(rng: random.Random, n: int, m: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), rng.randint(1, min(3, n)))] for _ in range(m)]


def test_example() -> None:
    # the page example: soft x1, x2, x3; hard: at most one of them is true
    hard = [[-1, -2], [-1, -3], [-2, -3]]
    soft = [[1], [2], [3]]
    cores: list[list[int]] = []
    cost, x = core_guided_maxsat(3, hard, soft, cores)
    assert cores == [[1, 2], [0, 1, 2]]  # x2 or x3, then all three with x2 and x3 relaxed
    assert cost == 2 and satisfies(hard, x) and false_count(soft, x) == 2
    assert x == [True, False, False]


def test_dpll_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randint(1, 8)
        cls = random_clauses(rng, n, rng.randint(0, 4 * n))
        x = dpll(n, cls)
        has = any(satisfies(cls, list(b)) for b in itertools.product([False, True], repeat=n))
        assert (x is not None) == has
        if x is not None:
            assert satisfies(cls, x)
    assert dpll(2, [[]]) is None and dpll(0, []) == []


def test_cores_are_minimal() -> None:
    rng = random.Random(2)
    for _ in range(150):
        n = rng.randint(2, 6)
        hard = random_clauses(rng, n, rng.randint(0, n))
        soft = random_clauses(rng, n, rng.randint(1, 3 * n))
        if dpll(n, hard) is None or dpll(n, hard + soft) is not None:
            continue
        k = minimal_core(n, hard, soft)
        assert k and dpll(n, hard + [soft[i] for i in k]) is None
        for i in k:
            assert dpll(n, hard + [soft[j] for j in k if j != i]) is not None


def test_exactly_one() -> None:
    cnf = exactly_one([1, 2, 3])
    for b in itertools.product([False, True], repeat=3):
        assert satisfies(cnf, list(b)) == (sum(b) == 1)


def test_edges() -> None:
    assert core_guided_maxsat(1, [[1], [-1]], [[1]]) is None
    assert core_guided_maxsat(0, [], []) == (0, [])
    assert core_guided_maxsat(1, [], [[1], [-1]])[0] == 1
    assert core_guided_maxsat(2, [], [[]])[0] == 1  # an empty soft clause is always false
    assert core_guided_maxsat(2, [[1, 2]], [[-1], [-2], [-1]])[0] == 1


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    seen = set()
    for _ in range(250):
        n = rng.randint(1, 7)
        hard = random_clauses(rng, n, rng.randint(0, n))
        soft = random_clauses(rng, n, rng.randint(0, 3 * n))
        best = brute(n, hard, soft)
        res = core_guided_maxsat(n, hard, soft)
        if best is None:
            assert res is None
            continue
        cost, x = res
        assert cost == best
        assert satisfies(hard, x) and false_count(soft, x) == cost
        seen.add(cost)
    assert len(seen) >= 4
