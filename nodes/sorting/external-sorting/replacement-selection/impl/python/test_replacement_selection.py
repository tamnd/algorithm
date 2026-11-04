# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replacement-selection/. The authors are listed in prov/H4VBFM.jsonl.

import random

import pytest

from replacement_selection import replacement_selection


def check(f: list[int], p: int, runs: list[list[int]]) -> None:
    assert sorted(x for r in runs for x in r) == sorted(f)
    for r in runs:
        assert r and all(r[i] <= r[i + 1] for i in range(len(r) - 1))
    for r in runs[:-1]:
        assert len(r) >= p


def test_example() -> None:
    f = [5, 1, 9, 3, 7, 2, 8, 6, 4, 10, 0, 11]
    assert replacement_selection(f, 3) == [[1, 3, 5, 7, 8, 9], [2, 4, 6, 10, 11], [0]]


def test_edges() -> None:
    assert replacement_selection([], 3) == []
    assert replacement_selection([4], 3) == [[4]]
    assert replacement_selection([2, 1], 5) == [[1, 2]]
    assert replacement_selection(list(range(10)), 2) == [list(range(10))]
    assert replacement_selection(list(range(9, -1, -1)), 3) == [[7, 8, 9], [4, 5, 6], [1, 2, 3], [0]]
    assert replacement_selection([3, 2, 1], 1) == [[3], [2], [1]]
    assert replacement_selection([7] * 6, 2) == [[7] * 6]
    with pytest.raises(ValueError):
        replacement_selection([1], 0)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(5)
    for _ in range(100):
        a = [Key(rng.randint(0, 4), i) for i in range(rng.randint(0, 40))]
        runs = replacement_selection(a, rng.randint(1, 5))
        for r in runs:
            for u, v in zip(r, r[1:]):
                assert u.k < v.k or (u.k == v.k and u.tag < v.tag)
        first: dict[int, int] = {}
        for i, r in enumerate(runs):
            for x in r:
                first.setdefault(x.tag, i)
        for x in a:
            for y in a:
                if x.k == y.k and x.tag < y.tag:
                    assert first[x.tag] <= first[y.tag]


def test_random_against_sorted() -> None:
    rng = random.Random(9001)
    for _ in range(700):
        n = rng.randint(0, 80)
        p = rng.randint(1, 8)
        f = [rng.randint(-25, 25) for _ in range(n)]
        check(f, p, replacement_selection(f, p))


def test_mean_length_near_two_p() -> None:
    rng = random.Random(77)
    p, n = 50, 50000
    runs = replacement_selection([rng.random() for _ in range(n)], p)
    mean = n / len(runs)
    assert 1.9 * p < mean < 2.1 * p
