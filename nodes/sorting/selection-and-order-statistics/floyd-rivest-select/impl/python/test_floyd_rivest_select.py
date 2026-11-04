# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-rivest-select/. The authors are listed in prov/4QBG0P.jsonl.

import random

import pytest

from floyd_rivest_select import floyd_rivest_select


def test_example() -> None:
    a = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]
    for k in range(1, 11):
        assert floyd_rivest_select(a, k, cutoff=2, rng=random.Random(k)) == sorted(a)[k - 1]
    assert a == [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]


def test_edges() -> None:
    assert floyd_rivest_select([5], 1) == 5
    assert floyd_rivest_select([4] * 50, 17, cutoff=2) == 4
    assert floyd_rivest_select([2, 1] * 40, 41, cutoff=2) == 2
    with pytest.raises(ValueError):
        floyd_rivest_select([1, 2], 0)
    with pytest.raises(ValueError):
        floyd_rivest_select([1, 2], 3)


def test_random_against_sorted() -> None:
    rng = random.Random(1975)
    for _ in range(1500):
        n = rng.randint(1, 120)
        a = [rng.randint(-30, 30) for _ in range(n)]
        k = rng.randint(1, n)
        cutoff = rng.choice([2, 3, 5, 10])
        assert floyd_rivest_select(a, k, cutoff=cutoff, rng=rng) == sorted(a)[k - 1]


def test_large_default_cutoff() -> None:
    rng = random.Random(489)
    for _ in range(5):
        a = [rng.random() for _ in range(20000)]
        k = rng.randint(1, len(a))
        assert floyd_rivest_select(a, k, rng=rng) == sorted(a)[k - 1]
