# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascade-merge-sort/. The authors are listed in prov/KG5YAF.jsonl.

import random

import pytest

from cascade_merge_sort import cascade_distribution, cascade_merge_sort


def test_example() -> None:
    f = [12, 3, 8, 1, 6, 2, 11, 9, 5, 4, 10, 7]
    assert cascade_merge_sort(f, 2, 4) == 2
    assert f == list(range(1, 13))


def test_distributions() -> None:
    assert cascade_distribution(6, 3) == (2, [3, 2, 1])
    assert cascade_distribution(100, 5) == (4, [55, 50, 41, 29, 15])
    totals = [sum(cascade_distribution(s, 5)[1]) for s in (1, 2, 6, 16, 56)]
    assert totals == [1, 5, 15, 55, 190]
    fib = [sum(cascade_distribution(s, 2)[1]) for s in (1, 2, 3, 4, 6, 9)]
    assert fib == [1, 2, 3, 5, 8, 13]


def test_edges() -> None:
    a: list[int] = []
    assert cascade_merge_sort(a) == 0 and a == []
    a = [1]
    assert cascade_merge_sort(a) == 0 and a == [1]
    a = [5] * 9
    cascade_merge_sort(a, 2, 3)
    assert a == [5] * 9
    a = list(range(40, 0, -1))
    cascade_merge_sort(a, 1, 6)
    assert a == list(range(1, 41))
    with pytest.raises(ValueError):
        cascade_merge_sort([1], 0, 4)


def test_random_against_sorted() -> None:
    rng = random.Random(1959)
    for _ in range(600):
        n = rng.randint(0, 120)
        m = rng.randint(1, 6)
        t = rng.randint(3, 9)
        f = [rng.randint(-40, 40) for _ in range(n)]
        want = sorted(f)
        passes = cascade_merge_sort(f, m, t)
        assert f == want
        s = -(-n // m)
        assert passes == (cascade_distribution(s, t - 1)[0] if s > 1 else 0)
