# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mo-algorithm/. The authors are listed in prov/S9FYEP.jsonl.

import random

from mo_algorithm import default_block, distinct_counts, mo_algorithm


def test_example() -> None:
    a = [1, 2, 1, 3, 2, 2, 4, 1]
    qs = [(0, 4), (2, 7), (1, 3), (5, 8), (3, 6)]
    moves = []
    window: list[int] = []

    def add(i: int) -> None:
        moves.append(i)
        window.append(i)

    def remove(i: int) -> None:
        moves.append(i)
        window.remove(i)

    ans = mo_algorithm(8, qs, add, remove, lambda: len({a[i] for i in window}), 3)
    assert ans == [3, 4, 2, 3, 2]
    assert len(moves) == 17
    assert distinct_counts(a, qs, 3) == [3, 4, 2, 3, 2]


def test_edges() -> None:
    assert distinct_counts([], []) == []
    assert distinct_counts([], [(0, 0)]) == [0]
    assert distinct_counts([7], [(0, 1), (0, 0), (1, 1)]) == [1, 0, 0]
    assert distinct_counts([5, 5, 5], [(0, 3), (2, 3), (1, 1)]) == [1, 1, 0]
    assert default_block(0, 0) == 1
    assert default_block(100, 10000) == 1
    assert default_block(100, 4) == 50
    assert default_block(100, 1) == 100


def test_window_never_inverts() -> None:
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(0, 30)
        qs = []
        for _ in range(rng.randint(0, 20)):
            l = rng.randint(0, n)
            qs.append((l, rng.randint(l, n)))
        inside: set[int] = set()

        def add(i: int) -> None:
            assert i not in inside
            inside.add(i)

        def remove(i: int) -> None:
            assert i in inside
            inside.remove(i)

        got = mo_algorithm(n, qs, add, remove, lambda: frozenset(inside), rng.randint(0, 6))
        assert got == [frozenset(range(l, r)) for l, r in qs]


def test_random_against_brute_force() -> None:
    rng = random.Random(2024)
    for _ in range(600):
        n = rng.randint(0, 40)
        a = [rng.randint(0, 6) for _ in range(n)]
        qs = []
        for _ in range(rng.randint(0, 25)):
            l = rng.randint(0, n)
            qs.append((l, rng.randint(l, n)))
        expected = [len(set(a[l:r])) for l, r in qs]
        assert distinct_counts(a, qs) == expected
        assert distinct_counts(a, qs, rng.randint(1, 8)) == expected
