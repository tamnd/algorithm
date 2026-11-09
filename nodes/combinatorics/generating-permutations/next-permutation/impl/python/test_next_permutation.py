# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-permutation/. The authors are listed in prov/V6C3MR.jsonl.

import itertools
import math
import random

from next_permutation import lexicographic_permutations, next_permutation


def test_example() -> None:
    a = [2, 6, 3, 9, 7, 5, 4, 1]
    assert next_permutation(a)
    assert a == [2, 6, 4, 1, 3, 5, 7, 9]


def test_multiset_example() -> None:
    got = ["".join(map(str, p)) for p in lexicographic_permutations([1, 1, 2, 3])]
    assert got == ["1123", "1132", "1213", "1231", "1312", "1321",
                   "2113", "2131", "2311", "3112", "3121", "3211"]


def test_edges() -> None:
    a: list[int] = []
    assert not next_permutation(a) and a == []
    a = [7]
    assert not next_permutation(a) and a == [7]
    a = [1, 2]
    assert next_permutation(a) and a == [2, 1]
    assert not next_permutation(a) and a == [1, 2]
    a = [3, 3, 3]
    assert not next_permutation(a) and a == [3, 3, 3]
    a = [3, 2, 1]
    assert not next_permutation(a) and a == [1, 2, 3]


def test_all_distinct_match_itertools() -> None:
    for n in range(0, 8):
        got = [tuple(p) for p in lexicographic_permutations(list(range(n)))]
        assert got == list(itertools.permutations(range(n)))
        assert len(got) == math.factorial(n)


def test_multisets_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(0, 7)
        items = [rng.randint(0, 3) for _ in range(n)]
        want = sorted(set(itertools.permutations(items)))
        got = [tuple(p) for p in lexicographic_permutations(items)]
        assert got == want
        count = math.factorial(n)
        for c in set(items):
            count //= math.factorial(items.count(c))
        assert len(got) == count


def test_successor_of_random_arrays() -> None:
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 6)
        a = [rng.randint(0, 4) for _ in range(n)]
        order = sorted(set(itertools.permutations(a)))
        k = order.index(tuple(a))
        b = list(a)
        ok = next_permutation(b)
        if k + 1 < len(order):
            assert ok and tuple(b) == order[k + 1]
        else:
            assert not ok and tuple(b) == order[0]


def test_strings() -> None:
    got = ["".join(p) for p in lexicographic_permutations(list("aab"))]
    assert got == ["aab", "aba", "baa"]
