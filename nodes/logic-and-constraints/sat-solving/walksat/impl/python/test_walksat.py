# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/walksat/. The authors are listed in prov/T3EJBM.jsonl.

import itertools
import random

from walksat import State, normalize, pick_variable, walksat


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def count_sat(clauses: list[list[int]], x: list[bool]) -> int:
    return sum(any(x[abs(l) - 1] == (l > 0) for l in cl) for cl in clauses)


def brute_sat(n: int, clauses: list[list[int]]) -> bool:
    return any(satisfies(clauses, list(b)) for b in itertools.product([False, True], repeat=n))


def random_cnf(rng: random.Random, n: int, m: int, k: int) -> list[list[int]]:
    return [[rng.choice([1, -1]) * v for v in rng.sample(range(1, n + 1), k)] for _ in range(m)]


EXAMPLE = [[2, 3, -4], [1, 3, 4], [1, -3], [-1, 3], [-1, 2], [-3, 4]]


def test_example() -> None:
    # the page example: start at 0000
    s = State(4, EXAMPLE, [False, False, False, False])
    assert [EXAMPLE[j] for j in s.false_list] == [[1, 3, 4]]
    assert [s.break_count(v) for v in (1, 3, 4)] == [2, 2, 1]  # no freebie; the greedy move is x4
    assert pick_variable(s, [1, 3, 4], 0.0, random.Random(0)) == 4
    s.flip(4)
    assert [EXAMPLE[j] for j in s.false_list] == [[2, 3, -4]]
    assert [s.break_count(v) for v in (2, 3, 4)] == [0, 1, 1]
    for seed in range(10):
        assert pick_variable(s, [2, 3, -4], 0.5, random.Random(seed)) == 2  # the freebie move
    s.flip(2)
    assert s.false_list == []
    models = [list(b) for b in itertools.product([False, True], repeat=4) if satisfies(EXAMPLE, list(b))]
    assert models == [[False, True, False, True], [True, True, True, True]]
    for seed in range(20):
        assert walksat(4, EXAMPLE, rng=random.Random(seed)) in models


def test_edges() -> None:
    assert walksat(0, []) == []
    assert walksat(2, [[]]) is None
    assert walksat(1, [[1, -1]], rng=random.Random(0)) is not None
    assert walksat(1, [[1], [-1]], max_flips=50, rng=random.Random(0)) is None
    assert walksat(1, [[1, 1]], rng=random.Random(0)) == [True]
    assert normalize([[2, 1, 2], [3, -3]]) == [[1, 2]]


def test_state_invariants() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 8)
        cls = normalize([[rng.choice([1, -1]) * rng.randint(1, n) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 12))])
        assert cls is not None
        s = State(n, cls, [rng.random() < 0.5 for _ in range(n)])
        for _ in range(25):
            x = s.x[1:]
            assert sorted(s.false_list) == sorted(j for j, cl in enumerate(cls) if not satisfies([cl], x))
            for v in range(1, n + 1):
                y = x[:]
                y[v - 1] = not y[v - 1]
                broken = sum(1 for cl in cls if satisfies([cl], x) and not satisfies([cl], y))
                assert s.break_count(v) == broken
            s.flip(rng.randint(1, n))


def test_freebie_moves_never_lose_clauses() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(2, 8)
        cls = normalize(random_cnf(rng, n, rng.randint(2, 4 * n), 2 if n < 3 else 3))
        assert cls is not None
        s = State(n, cls, [rng.random() < 0.5 for _ in range(n)])
        if not s.false_list:
            continue
        c = cls[s.false_list[0]]
        before = count_sat(cls, s.x[1:])
        v = pick_variable(s, c, 0.0, rng)  # p = 0: freebie or greedy
        least = min(s.break_count(abs(l)) for l in c)
        assert s.break_count(v) == least
        s.flip(v)
        assert satisfies([c], s.x[1:])  # the chosen clause is now true
        if least == 0:
            assert count_sat(cls, s.x[1:]) > before


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(600):
        n = rng.randint(3, 10)
        m = rng.randint(1, int(4.5 * n))
        clauses = random_cnf(rng, n, m, rng.choice([2, 3, 3, 4]) if n >= 4 else 2)
        x = walksat(n, clauses, max_tries=5, max_flips=200, rng=random.Random(rng.randrange(10**9)))
        if x is not None:
            assert satisfies(clauses, x)
        if brute_sat(n, clauses):
            assert x is not None
            sat += 1
        else:
            assert x is None
            unsat += 1
    assert sat > 200 and unsat > 50


def test_planted() -> None:
    rng = random.Random(5)
    n = 200
    planted = [rng.random() < 0.5 for _ in range(n)]
    clauses = [cl for cl in random_cnf(rng, n, 1200, 3) if satisfies([cl], planted)]
    x = walksat(n, clauses, max_tries=3, max_flips=20000, rng=random.Random(6))
    assert x is not None and satisfies(clauses, x)
