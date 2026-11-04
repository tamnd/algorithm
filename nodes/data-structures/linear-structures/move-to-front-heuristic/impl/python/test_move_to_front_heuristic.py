# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/move-to-front-heuristic/. The authors are listed in prov/ADRSG4.jsonl.

import itertools
import random

import pytest

from move_to_front_heuristic import MoveToFrontList, mtf_total_cost


def test_example() -> None:
    lst = MoveToFrontList("abcde")
    costs = [lst.access(x) for x in "dbdeadb"]
    assert costs == [4, 3, 2, 5, 4, 3, 4]
    assert lst.to_list() == list("bdaec")
    assert sum(costs) == 25
    assert mtf_total_cost("abcde", "e" * 10) == 14


def test_edges() -> None:
    one = MoveToFrontList([7])
    assert one.access(7) == 1 and one.to_list() == [7]
    lst = MoveToFrontList([1, 2, 3])
    assert lst.access(1) == 1 and lst.to_list() == [1, 2, 3]
    assert lst.access(3) == 3 and lst.to_list() == [3, 1, 2]
    with pytest.raises(KeyError):
        lst.access(9)
    assert lst.to_list() == [3, 1, 2]
    with pytest.raises(ValueError):
        MoveToFrontList([1, 1])
    assert mtf_total_cost([], []) == 0


def test_random_against_python_list() -> None:
    rng = random.Random(1985)
    for _ in range(600):
        n = rng.randint(1, 9)
        keys = rng.sample(range(100), n)
        lst = MoveToFrontList(keys)
        model = list(keys)
        for _ in range(rng.randint(0, 30)):
            x = rng.choice(keys)
            want = model.index(x) + 1
            model.insert(0, model.pop(want - 1))
            assert lst.access(x) == want
            assert lst.to_list() == model


def _serve_random_algorithm(start: list[int], requests: list[int], rng: random.Random) -> tuple[int, int, int]:
    """An arbitrary algorithm A: random paid and free exchanges. Returns (C_A, X_A, F_A)."""
    a = list(start)
    c = x_paid = f_free = 0
    for x in requests:
        for _ in range(rng.randint(0, 2)):
            if len(a) > 1:
                j = rng.randrange(len(a) - 1)
                a[j], a[j + 1] = a[j + 1], a[j]
                x_paid += 1
        i = a.index(x)
        c += i + 1
        moves = rng.randint(0, i)
        for _ in range(moves):
            a[i - 1], a[i] = a[i], a[i - 1]
            i -= 1
        f_free += moves
    return c, x_paid, f_free


def test_sleator_tarjan_bound() -> None:
    rng = random.Random(28)
    for _ in range(600):
        n = rng.randint(1, 7)
        start = list(range(n))
        reqs = [rng.randrange(n) for _ in range(rng.randint(1, 25))]
        c, x_paid, f_free = _serve_random_algorithm(start, reqs, rng)
        assert mtf_total_cost(start, reqs) <= 2 * c + x_paid - f_free - len(reqs)


def test_against_every_static_order() -> None:
    rng = random.Random(202)
    for _ in range(100):
        n = rng.randint(1, 5)
        start = list(range(n))
        reqs = [rng.randrange(n) for _ in range(rng.randint(1, 15))]
        mtf = mtf_total_cost(start, reqs)
        for perm in itertools.permutations(start):
            inv = sum(1 for a, b in itertools.combinations(perm, 2) if a > b)
            static = sum(perm.index(x) + 1 for x in reqs)
            assert mtf <= 2 * static + inv - len(reqs)
