# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lexicographic-combinations/. The authors are listed in prov/JMPMV6.jsonl.

import itertools
import math
import random

from lexicographic_combinations import lex_combinations, next_combination, scan_steps


def test_example() -> None:
    got = list(lex_combinations(5, 3))
    assert got == [
        (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5),
        (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5),
    ]
    assert scan_steps(5, 3) == (10, 7)
    a = [1, 4, 5]
    assert next_combination(a, 5) and a == [2, 3, 4]


def test_edges() -> None:
    assert list(lex_combinations(0, 0)) == [()]
    assert list(lex_combinations(4, 0)) == [()]
    assert list(lex_combinations(4, 4)) == [(1, 2, 3, 4)]
    assert list(lex_combinations(3, 4)) == []
    assert list(lex_combinations(5, 1)) == [(1,), (2,), (3,), (4,), (5,)]
    a = [3, 4, 5]
    assert not next_combination(a, 5) and a == [3, 4, 5]


def test_against_itertools() -> None:
    for n in range(0, 11):
        for k in range(0, n + 2):
            got = list(lex_combinations(n, k))
            assert got == list(itertools.combinations(range(1, n + 1), k))
            assert len(got) == (math.comb(n, k) if k <= n else 0)


def test_scan_counts() -> None:
    for n in range(1, 13):
        for k in range(1, n + 1):
            assert scan_steps(n, k) == (math.comb(n, k - 1), math.comb(n, k - 1) - k)


def test_random_successor() -> None:
    rng = random.Random(1963)
    for _ in range(800):
        n = rng.randint(1, 14)
        k = rng.randint(1, n)
        a = sorted(rng.sample(range(1, n + 1), k))
        later = [list(c) for c in itertools.combinations(range(1, n + 1), k) if list(c) > a]
        b = list(a)
        moved = next_combination(b, n)
        if later:
            assert moved and b == min(later)
        else:
            assert not moved and b == a
