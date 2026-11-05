# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vizing-algorithm/. The authors are listed in prov/5TRSEH.jsonl.

import itertools
import random

from vizing_algorithm import vizing_algorithm


def max_degree(n: int, edges: list[tuple[int, int]]) -> int:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return max(deg, default=0)


def proper(edges: list[tuple[int, int]], col: list[int]) -> bool:
    for (e, a), (f, b) in itertools.combinations(zip(edges, col), 2):
        if a == b and set(e) & set(f):
            return False
    return True


def chromatic_index(n: int, edges: list[tuple[int, int]]) -> int:
    m = len(edges)
    for k in range(m + 1):
        for col in itertools.product(range(k), repeat=m):
            if proper(edges, list(col)):
                return k
    return m


def check(n: int, edges: list[tuple[int, int]]) -> list[int]:
    col = vizing_algorithm(n, edges)
    delta = max_degree(n, edges)
    assert len(col) == len(edges)
    assert all(1 <= c <= delta + 1 for c in col)
    assert proper(edges, col)
    return col


def complete(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def cyc(n: int) -> list[tuple[int, int]]:
    return [(i, (i + 1) % n) for i in range(n)]


PETERSEN = cyc(5) + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]

EXAMPLE = [(0, 2), (2, 3), (0, 1), (0, 3)]


def test_example() -> None:
    assert check(4, EXAMPLE) == [3, 1, 1, 2]
    other = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (0, 4)]
    assert check(5, other) == [2, 1, 3, 1, 4, 2, 4]


def test_edges() -> None:
    assert vizing_algorithm(0, []) == []
    assert vizing_algorithm(3, []) == []
    assert check(2, [(0, 1)]) == [1]
    for n in range(2, 9):
        check(n, complete(n))
    for n in (3, 5, 7):
        assert len(set(check(n, cyc(n)))) == 3
    assert len(set(check(10, PETERSEN))) == 4


def test_bipartite() -> None:
    kmn = [(i, j) for i in range(3) for j in range(3, 7)]
    check(7, kmn)
    star = [(0, i) for i in range(1, 8)]
    assert sorted(check(8, star)) == list(range(1, 8))


def test_random_against_brute_force() -> None:
    rng = random.Random(9133)
    for _ in range(600):
        n = rng.randint(0, 6)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        rng.shuffle(edges)
        edges = [(b, a) if rng.random() < 0.5 else (a, b) for a, b in edges]
        col = check(n, edges)
        if len(edges) <= 9:
            chi1 = chromatic_index(n, edges)
            assert max_degree(n, edges) <= chi1 <= max(col, default=0)


def test_random_larger() -> None:
    rng = random.Random(515)
    for _ in range(200):
        n = rng.randint(5, 40)
        p = rng.random()
        edges = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p]
        rng.shuffle(edges)
        check(n, edges)
