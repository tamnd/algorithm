# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/horn-sat-forward-chaining/. The authors are listed in prov/JGNV5C.jsonl.

import itertools
import random

import pytest

from horn_sat_forward_chaining import horn_sat_forward_chaining


def satisfies(clauses: list[list[int]], x: list[bool]) -> bool:
    return all(any(x[abs(l) - 1] == (l > 0) for l in c) for c in clauses)


def all_models(n: int, clauses: list[list[int]]) -> list[list[bool]]:
    return [list(b) for b in itertools.product([False, True], repeat=n) if satisfies(clauses, list(b))]


# x1. x1 -> x2. x1 and x2 -> x3. x3 and x4 -> x5. x2 and x5 -> false. x4 -> x1. x3 -> x6.
EXAMPLE = [[1], [-1, 2], [-1, -2, 3], [-3, -4, 5], [-2, -5], [-4, 1], [-3, 6]]


def test_example() -> None:
    x = horn_sat_forward_chaining(6, EXAMPLE)
    assert x == [True, True, True, False, False, True]
    assert satisfies(EXAMPLE, x)


def test_example_unsat() -> None:
    f = EXAMPLE + [[4]]
    assert horn_sat_forward_chaining(6, f) is None
    assert all_models(6, f) == []


def test_edges() -> None:
    assert horn_sat_forward_chaining(0, []) == []
    assert horn_sat_forward_chaining(2, []) == [False, False]
    assert horn_sat_forward_chaining(1, [[]]) is None
    assert horn_sat_forward_chaining(1, [[-1]]) == [False]
    assert horn_sat_forward_chaining(1, [[1], [-1]]) is None
    assert horn_sat_forward_chaining(1, [[1, -1]]) == [False]  # a tautology
    assert horn_sat_forward_chaining(2, [[1], [-1, -1, 2]]) == [True, True]
    assert horn_sat_forward_chaining(1, [[1, 1]]) == [True]
    with pytest.raises(ValueError):
        horn_sat_forward_chaining(2, [[1, 2]])


def random_horn(rng: random.Random, n: int, m: int) -> list[list[int]]:
    f = []
    for _ in range(m):
        body = [-rng.randint(1, n) for _ in range(rng.randint(0, 3))]
        if rng.random() < 0.75:
            body.append(rng.randint(1, n))
        f.append(body)
    return f


def test_random_against_brute_force() -> None:
    rng = random.Random(1984)
    sat = unsat = 0
    for _ in range(1500):
        n = rng.randint(1, 10)
        f = random_horn(rng, n, rng.randint(0, 3 * n))
        x = horn_sat_forward_chaining(n, f)
        models = all_models(n, f)
        if x is None:
            assert models == []
            unsat += 1
        else:
            assert satisfies(f, x)
            # the least model: each true variable is true in every model
            for v in range(n):
                if x[v]:
                    assert all(mod[v] for mod in models)
            sat += 1
    assert sat > 300 and unsat > 300


def test_long_chain() -> None:
    n = 20000
    f = [[1]] + [[-v, v + 1] for v in range(1, n)]
    assert horn_sat_forward_chaining(n, f) == [True] * n
    assert horn_sat_forward_chaining(n, f + [[-n]]) is None
