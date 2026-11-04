# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/held-karp-algorithm/. The authors are listed in prov/X3NDEJ.jsonl.

import itertools
import random

from held_karp_algorithm import held_karp


def tour_length(d, tour):
    return sum(d[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))


def brute(d):
    n = len(d)
    return min(tour_length(d, [0] + list(p)) for p in itertools.permutations(range(1, n)))


def check(d):
    length, tour = held_karp(d)
    assert sorted(tour) == list(range(len(d)))
    assert tour[0] == 0
    assert tour_length(d, tour) == length
    assert length == brute(d)


def test_example() -> None:
    d = [[0, 2, 9, 10], [1, 0, 6, 4], [15, 7, 0, 8], [6, 3, 12, 0]]
    assert held_karp(d) == (21, [0, 2, 3, 1])


def test_small_sizes() -> None:
    assert held_karp([[0]]) == (0, [0])
    assert held_karp([[0, 3], [5, 0]]) == (8, [0, 1])
    check([[0, 1, 1], [1, 0, 1], [1, 1, 0]])


def test_equal_and_negative_weights() -> None:
    check([[0] * 5 for _ in range(5)])
    check([[0, -3, 4, 1], [2, 0, -1, 5], [-2, 7, 0, 0], [3, -4, 6, 0]])


def test_large_values() -> None:
    big = 1 << 60
    d = [[0, big, 1, big], [1, 0, big, big], [big, big, 0, 1], [big, 1, big, 0]]
    assert held_karp(d) == (4, [0, 2, 3, 1])


def test_against_brute_force() -> None:
    rng = random.Random(20240601)
    for _ in range(600):
        n = rng.randint(1, 7)
        d = [[0 if i == j else rng.randint(-5, 30) for j in range(n)] for i in range(n)]
        check(d)
