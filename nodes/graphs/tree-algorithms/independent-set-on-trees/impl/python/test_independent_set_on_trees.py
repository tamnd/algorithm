# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-set-on-trees/. The authors are listed in prov/EAW1JK.jsonl.

import random

import pytest

from independent_set_on_trees import max_weight_independent_set


def edges_of(parent: list[int]) -> list[tuple[int, int]]:
    return [(v, p) for v, p in enumerate(parent) if p >= 0]


def brute(n: int, edges: list[tuple[int, int]], w: list[int]) -> int:
    best = 0
    for m in range(1 << n):
        if all(not (m >> a & 1 and m >> b & 1) for a, b in edges):
            best = max(best, sum(w[v] for v in range(n) if m >> v & 1))
    return best


def check(n: int, edges: list[tuple[int, int]], w: list[int], best: int, s: list[int]) -> None:
    chosen = set(s)
    assert all(not (a in chosen and b in chosen) for a, b in edges)
    assert sum(w[v] for v in s) == best


def test_example() -> None:
    parent = [-1, 0, 0, 1, 1, 2, 2, 4]
    w = [6, 7, 2, 3, 4, 5, 1, 8]
    best, s = max_weight_independent_set(8, edges_of(parent), w)
    assert best == 23
    assert s == [0, 3, 5, 6, 7]


def test_single_vertex() -> None:
    assert max_weight_independent_set(1, [], [5]) == (5, [0])
    assert max_weight_independent_set(1, [], [-5]) == (0, [])
    assert max_weight_independent_set(1, [], [0]) == (0, [])


def test_path_and_star() -> None:
    n = 100_000
    path = [(i, i + 1) for i in range(n - 1)]
    best, s = max_weight_independent_set(n, path, [1] * n)
    assert best == (n + 1) // 2
    check(n, path, [1] * n, best, s)
    star = [(0, i) for i in range(1, 10)]
    assert max_weight_independent_set(10, star, [100] + [1] * 9) == (100, [0])
    assert max_weight_independent_set(10, star, [5] + [1] * 9)[0] == 9
    assert max_weight_independent_set(10, star, [5] + [1] * 9, root=4)[0] == 9


def test_negative_weights() -> None:
    best, s = max_weight_independent_set(3, [(0, 1), (1, 2)], [-1, -2, -3])
    assert (best, s) == (0, [])


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        max_weight_independent_set(3, [(0, 1)], [1, 1, 1])
    with pytest.raises(ValueError):
        max_weight_independent_set(4, [(0, 1), (0, 1), (2, 3)], [1, 1, 1, 1])


def test_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(700):
        n = rng.randint(1, 12)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        edges = edges_of(parent)
        rng.shuffle(edges)
        w = [rng.randint(-5, 20) for _ in range(n)]
        root = rng.randrange(n)
        best, s = max_weight_independent_set(n, edges, w, root)
        assert best == brute(n, edges, w)
        check(n, edges, w, best, s)
