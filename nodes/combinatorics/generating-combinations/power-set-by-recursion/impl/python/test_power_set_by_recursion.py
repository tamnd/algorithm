# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-set-by-recursion/. The authors are listed in prov/198V88.jsonl.

import itertools
import random

from power_set_by_recursion import as_set, counter_writes, subsets_counter, subsets_recursive


def test_example() -> None:
    got = [as_set(x) for x in subsets_counter(3)]
    assert got == [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    assert [as_set(x) for x in subsets_recursive(3)] == got
    assert counter_writes(3) == 11


def test_edges() -> None:
    assert list(subsets_counter(0)) == [()]
    assert list(subsets_recursive(0)) == [()]
    assert list(subsets_counter(1)) == [(0,), (1,)]
    assert list(subsets_recursive(1)) == [(0,), (1,)]
    assert counter_writes(0) == 0


def test_binary_counting_order() -> None:
    for n in range(0, 11):
        a = list(subsets_counter(n))
        assert len(a) == 2**n
        assert len(set(a)) == 2**n
        assert a == list(subsets_recursive(n))
        for v, x in enumerate(a):
            assert sum(bit << j for j, bit in enumerate(x)) == v
        assert counter_writes(n) == 2 ** (n + 1) - n - 2


def test_against_itertools() -> None:
    for n in range(0, 9):
        got = sorted(tuple(as_set(x)) for x in subsets_counter(n))
        ref = sorted(c for k in range(n + 1) for c in itertools.combinations(range(1, n + 1), k))
        assert got == ref


def test_random_rank_lookup() -> None:
    rng = random.Random(198)
    lists = {n: list(subsets_counter(n)) for n in range(0, 13)}
    for _ in range(600):
        n = rng.randint(0, 12)
        s = sorted(rng.sample(range(1, n + 1), rng.randint(0, n)))
        rank = sum(1 << (e - 1) for e in s)
        assert as_set(lists[n][rank]) == s
