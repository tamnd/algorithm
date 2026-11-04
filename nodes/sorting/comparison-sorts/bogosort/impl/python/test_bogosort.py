# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bogosort/. The authors are listed in prov/YA1S1T.jsonl.

import itertools
import random
from collections import Counter

from bogosort import bogosort, is_sorted, shuffle


def test_example() -> None:
    a = [3, 1, 2]
    bogosort(a, random.Random(3))
    assert a == [1, 2, 3]


def test_edges() -> None:
    rng = random.Random(0)
    for a in ([], [1], [1, 2, 3], [2, 2, 2]):
        b = list(a)
        assert bogosort(b, rng) == 0
        assert b == a
    b = [2, 1]
    assert bogosort(b, rng) >= 1
    assert b == [1, 2]


def test_is_sorted() -> None:
    for n in range(6):
        for p in itertools.permutations(range(n)):
            assert is_sorted(list(p)) == (list(p) == sorted(p))


def test_shuffle_is_uniform() -> None:
    rng = random.Random(11)
    counts: Counter[tuple[int, ...]] = Counter()
    for _ in range(12000):
        a = [0, 1, 2]
        shuffle(a, rng)
        counts[tuple(a)] += 1
    assert len(counts) == 6
    assert all(1800 < c < 2200 for c in counts.values())


def test_mean_shuffles_is_factorial() -> None:
    rng = random.Random(5)
    total = sum(bogosort([3, 1, 2], rng) for _ in range(6000))
    assert 5.5 < total / 6000 < 6.5


def test_random_against_sorted() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        a = [rng.randint(0, 3) for _ in range(rng.randint(0, 5))]
        b = list(a)
        bogosort(b, rng)
        assert b == sorted(a)
