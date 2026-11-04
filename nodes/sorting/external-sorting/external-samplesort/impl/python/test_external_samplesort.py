# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-samplesort/. The authors are listed in prov/PAB348.jsonl.

import math
import random

import pytest

from external_samplesort import choose_splitters, distribute, external_samplesort

F = [14, 3, 9, 3, 17, 6, 12, 3, 20, 1, 8, 15, 3, 11, 5, 18, 7, 3, 16, 10]


def test_example_buckets() -> None:
    sample = [F[p] for p in (0, 1, 6, 10, 12, 15)]
    splitters = choose_splitters(sample, 2, 3)
    assert splitters == [3, 12]
    assert distribute(F, splitters) == [
        [1], [3, 3, 3, 3, 3], [9, 6, 8, 11, 5, 7, 10], [12], [14, 17, 20, 15, 18, 16],
    ]


def test_example_sort() -> None:
    f = F[:]
    external_samplesort(f, 12, 2, a=2)
    assert f == sorted(F)


def test_edges() -> None:
    for g in ([], [1], [7] * 200, list(range(300)), list(range(300, 0, -1))):
        f = g[:]
        external_samplesort(f, 16, 2)
        assert f == sorted(g)
    with pytest.raises(ValueError):
        external_samplesort([1], 7, 2)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(5)
    for _ in range(60):
        a = [Key(rng.randint(0, 5), i) for i in range(rng.randint(0, 200))]
        want = sorted((x.k, x.tag) for x in a)
        external_samplesort(a, 16, 2, seed=rng.randint(0, 10**6))
        assert [(x.k, x.tag) for x in a] == want


def test_bucket_bound() -> None:
    rng = random.Random(8)
    s, n = 16, 4000
    a = math.ceil(8 * math.log(s))
    limit = 2 * -(-2 * n // s)
    good = 0
    for _ in range(200):
        g = [rng.random() for _ in range(n)]
        sample = [g[rng.randrange(n)] for _ in range(a * s)]
        buckets = distribute(g, choose_splitters(sample, a, s))
        good += all(len(u) < limit for u in buckets[0::2])
    assert good >= 190


def test_random_against_sorted() -> None:
    rng = random.Random(1970)
    for _ in range(600):
        n = rng.randint(0, 150)
        b = rng.randint(1, 3)
        m = b * rng.randint(4, 8)
        f = [rng.randint(-30, 30) for _ in range(n)]
        want = sorted(f)
        ios = external_samplesort(f, m, b, seed=rng.randint(0, 10**6))
        assert f == want
        assert ios >= 2 * -(-n // b)
