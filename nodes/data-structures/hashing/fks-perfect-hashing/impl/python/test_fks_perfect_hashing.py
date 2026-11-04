# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fks-perfect-hashing/. The authors are listed in prov/VWBFM0.jsonl.

import random

import pytest

from fks_perfect_hashing import P61, fks_build, fks_search, h_ab

S = [10, 22, 37, 40, 52, 60, 70, 72, 75]


def test_page_example_numbers() -> None:
    p, m = 101, 9
    buckets = [[x for x in S if h_ab(3, 42, p, m, x) == j] for j in range(m)]
    assert buckets == [[10], [], [60, 72, 75], [], [], [70], [], [22, 37, 40, 52], []]
    assert sum(len(b) ** 2 for b in buckets) == 27
    assert [h_ab(3, 1, p, 9, x) for x in [60, 72, 75]] == [8, 6, 6]
    assert [h_ab(10, 18, p, 9, x) for x in [60, 72, 75]] == [3, 4, 7]
    assert [h_ab(10, 18, p, 16, x) for x in [22, 37, 40, 52]] == [4, 5, 14, 1]
    assert h_ab(3, 42, p, m, 50) == 1 and h_ab(3, 42, p, m, 13) == 0


def test_page_example_build() -> None:
    t = fks_build(S, random.Random(7), p=101)
    assert all(fks_search(t, x) for x in S)
    assert not any(fks_search(t, x) for x in range(101) if x not in S)
    assert sum(t.sizes) <= 4 * len(S)


def test_edges() -> None:
    t = fks_build([], random.Random(1))
    assert not fks_search(t, 0) and not fks_search(t, 5)
    t = fks_build([0], random.Random(1))
    assert fks_search(t, 0) and not fks_search(t, 1)
    big = [P61 - 1, 0, 2**60, 2**32 + 7]
    t = fks_build(big, random.Random(2))
    assert all(fks_search(t, x) for x in big) and not fks_search(t, 1)
    with pytest.raises(ValueError):
        fks_build([3, 3])
    with pytest.raises(ValueError):
        fks_build([P61])


def test_injective_second_level() -> None:
    rng = random.Random(3)
    keys = rng.sample(range(10**6), 300)
    t = fks_build(keys, rng)
    for j in range(t.m):
        stored = [x for x in t.slots[j] if x is not None]
        assert all(t.first(x) == j for x in stored)
        assert sorted(stored) == sorted(x for x in keys if t.first(x) == j)
    assert sum(t.sizes) <= 4 * len(keys)


def test_random_against_set() -> None:
    rng = random.Random(1984)
    for _ in range(600):
        p = rng.choice([101, 1009, P61])
        universe = min(p, 400)
        keys = rng.sample(range(universe), rng.randint(0, 40))
        t = fks_build(keys, rng, p=p)
        model = set(keys)
        assert sum(t.sizes) <= 4 * len(keys)
        for x in range(universe):
            assert fks_search(t, x) == (x in model)
