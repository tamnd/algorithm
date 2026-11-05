# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permutation-rank-unrank/. The authors are listed in prov/NW945N.jsonl.

import itertools
import math
import random

import pytest

from permutation_rank_unrank import lehmer_code, rank, unrank


def brute_rank(a: list[int]) -> int:
    for k, p in enumerate(itertools.permutations(sorted(a))):
        if list(p) == list(a):
            return k
    raise AssertionError


def test_example() -> None:
    assert rank([3, 1, 4, 5, 2]) == 51
    assert unrank(51, 5) == [3, 1, 4, 5, 2]
    assert lehmer_code([3, 1, 4, 5, 2]) == [2, 0, 1, 1, 0]
    assert rank([1, 3, 6, 5, 4, 2]) == 47
    assert unrank(48, 6) == [1, 4, 2, 3, 5, 6]
    assert rank([3, 1, 6, 2, 5, 4]) == 259


def test_edges() -> None:
    assert rank([]) == 0
    assert unrank(0, 0) == []
    assert rank([1]) == 0
    assert unrank(0, 1) == [1]
    assert rank(list(range(1, 11))) == 0
    assert rank(list(range(10, 0, -1))) == math.factorial(10) - 1
    assert unrank(math.factorial(10) - 1, 10) == list(range(10, 0, -1))
    with pytest.raises(ValueError):
        unrank(math.factorial(5), 5)
    with pytest.raises(ValueError):
        rank([1, 1, 2])


def test_all_small_permutations_in_order() -> None:
    for n in range(0, 7):
        for k, p in enumerate(itertools.permutations(range(1, n + 1))):
            assert rank(p) == k
            assert unrank(k, n) == list(p)


def test_big_n_exact() -> None:
    n = 60
    a = list(range(n, 0, -1))
    assert rank(a) == math.factorial(n) - 1
    assert unrank(math.factorial(n) - 1, n) == a


def test_random_against_brute_force() -> None:
    rng = random.Random(6121)
    for _ in range(600):
        n = rng.randint(0, 7)
        a = list(range(1, n + 1))
        rng.shuffle(a)
        r = rank(a)
        assert r == brute_rank(a)
        assert unrank(r, n) == a
        c = lehmer_code(a)
        assert c == [sum(1 for j in range(i + 1, n) if a[j] < a[i]) for i in range(n)]
    for _ in range(200):
        n = rng.randint(8, 80)
        r = rng.randrange(math.factorial(n))
        assert rank(unrank(r, n)) == r
