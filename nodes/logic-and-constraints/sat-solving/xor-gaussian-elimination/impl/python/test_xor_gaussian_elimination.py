# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-gaussian-elimination/. The authors are listed in prov/Q97DPS.jsonl.

import itertools
import random

from xor_gaussian_elimination import eliminate, xor_gaussian_elimination, xor_solution_count

Eq = tuple[list[int], int]


def holds(eqs: list[Eq], x: list[bool]) -> bool:
    return all(sum(x[v - 1] for v in vs) % 2 == b for vs, b in eqs)


def brute_count(n: int, eqs: list[Eq]) -> int:
    return sum(holds(eqs, list(bits)) for bits in itertools.product([False, True], repeat=n))


EXAMPLE: list[Eq] = [([1, 2, 3], 1), ([2, 3, 4], 0), ([1, 4, 5], 1), ([3, 5], 1)]


def test_example() -> None:
    x = xor_gaussian_elimination(5, EXAMPLE)
    assert x == [True, True, True, False, False]
    assert holds(EXAMPLE, x)
    assert xor_solution_count(5, EXAMPLE) == 2 == brute_count(5, EXAMPLE)
    _, _, pivots = eliminate(5, EXAMPLE)
    assert pivots == [0, 1, 2, 4]


def test_example_unsat() -> None:
    eqs = EXAMPLE + [([1, 4], 0)]  # rows 1 and 2 add up to x1 + x4 = 1
    assert xor_gaussian_elimination(5, eqs) is None
    assert brute_count(5, eqs) == 0


def test_edges() -> None:
    assert xor_gaussian_elimination(0, []) == []
    assert xor_gaussian_elimination(3, []) == [False, False, False]
    assert xor_solution_count(3, []) == 8
    assert xor_gaussian_elimination(1, [([], 1)]) is None  # 0 = 1
    assert xor_gaussian_elimination(1, [([], 0)]) == [False]  # 0 = 0
    assert xor_gaussian_elimination(1, [([1, 1], 1)]) is None  # x + x = 0
    assert xor_gaussian_elimination(1, [([1], 1)]) == [True]
    assert xor_gaussian_elimination(2, [([1, 2], 1), ([1, 2], 0)]) is None
    assert xor_solution_count(2, [([1, 2], 1), ([1, 2], 1)]) == 2


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    sat = unsat = 0
    for _ in range(1500):
        n = rng.randint(1, 10)
        eqs = [([rng.randint(1, n) for _ in range(rng.randint(0, 4))], rng.randint(0, 1)) for _ in range(rng.randint(0, n + 3))]
        x = xor_gaussian_elimination(n, eqs)
        count = brute_count(n, eqs)
        assert xor_solution_count(n, eqs) == count
        if x is None:
            assert count == 0
            unsat += 1
        else:
            assert holds(eqs, x)
            sat += 1
    assert sat > 300 and unsat > 300


def test_reduced_form() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 12)
        eqs = [([rng.randint(1, n) for _ in range(rng.randint(1, 5))], rng.randint(0, 1)) for _ in range(rng.randint(1, 12))]
        rows, _, pivots = eliminate(n, eqs)
        rank = len(pivots)
        assert all(rows[j] == 0 for j in range(rank, len(rows)))
        for i, col in enumerate(pivots):
            for j in range(len(rows)):
                assert bool(rows[j] >> col & 1) == (i == j)


def test_large_system() -> None:
    rng = random.Random(11)
    n = 200
    secret = [rng.random() < 0.5 for _ in range(n)]
    eqs = []
    for _ in range(300):
        vs = rng.sample(range(1, n + 1), 3)
        eqs.append((vs, sum(secret[v - 1] for v in vs) % 2))
    x = xor_gaussian_elimination(n, eqs)
    assert x is not None and holds(eqs, x)
