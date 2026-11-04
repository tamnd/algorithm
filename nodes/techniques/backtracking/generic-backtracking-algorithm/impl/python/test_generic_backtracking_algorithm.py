# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-backtracking-algorithm/. The authors are listed in prov/BD5KA9.jsonl.

import itertools
import random

from generic_backtracking_algorithm import backtrack, count_nodes, n_queens


def no_attack(p: tuple[int, ...]) -> bool:
    k = len(p) - 1
    return all(p[i] != p[k] and abs(p[i] - p[k]) != k - i for i in range(k))


def test_four_queens_example() -> None:
    assert n_queens(4) == [(2, 4, 1, 3), (3, 1, 4, 2)]
    assert count_nodes(4, lambda p: range(1, 5), no_attack) == [1, 4, 6, 4, 2]


def test_queens_counts() -> None:
    assert [len(n_queens(n)) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
    assert sum(count_nodes(8, lambda p: range(1, 9), no_attack)) == 2057


def test_edges() -> None:
    assert list(backtrack(0, lambda p: [1, 2], lambda p: True)) == [()]
    assert list(backtrack(2, lambda p: [], lambda p: True)) == []
    assert list(backtrack(1, lambda p: [5], lambda p: False)) == []
    assert list(backtrack(2, lambda p: [0, 1], lambda p: True)) == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_permutations() -> None:
    for n in range(6):
        got = list(backtrack(n, lambda p: range(n), lambda p: p[-1] not in p[:-1]))
        assert got == list(itertools.permutations(range(n)))


def test_subset_sum_prefix_closed() -> None:
    a = [3, 1, 4, 1, 5]
    target = 6

    def ok(p: tuple[int, ...]) -> bool:
        s = sum(b * v for b, v in zip(p, a))
        return s <= target and (len(p) < len(a) or s == target)

    got = list(backtrack(len(a), lambda p: (0, 1), ok))
    want = [p for p in itertools.product((0, 1), repeat=len(a)) if sum(b * v for b, v in zip(p, a)) == target]
    assert got == want


def test_random_against_brute_force() -> None:
    rng = random.Random(20240)
    for _ in range(600):
        n = rng.randrange(0, 5)
        m = rng.randrange(1, 4)
        bad = {tuple(rng.randrange(m) for _ in range(rng.randrange(1, n + 1))) for _ in range(rng.randrange(0, 6))} if n else set()

        def ok(p: tuple[int, ...]) -> bool:
            return p not in bad

        got = list(backtrack(n, lambda p: range(m), ok))
        want = [
            q
            for q in itertools.product(range(m), repeat=n)
            if all(q[:j] not in bad for j in range(1, n + 1))
        ]
        assert got == want


def test_output_is_a_copy() -> None:
    sols = list(backtrack(2, lambda p: (0, 1), lambda p: True))
    assert sols[0] == (0, 0) and sols[-1] == (1, 1)
