# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-parallel-merge/. The authors are listed in prov/HPT34J.jsonl.

import itertools
import math
import random

from valiant_parallel_merge import valiant_merge


def test_example() -> None:
    stats: dict = {}
    out = valiant_merge([1, 4, 6, 9], [2, 3, 7, 8, 10], stats)
    assert out == [1, 2, 3, 4, 6, 7, 8, 9, 10]
    assert stats["rounds"] == 3
    assert stats["max_per_round"] <= 9


def test_edges() -> None:
    assert valiant_merge([], []) == []
    assert valiant_merge([1], []) == [1]
    assert valiant_merge([], [1, 2]) == [1, 2]
    assert valiant_merge([2], [1]) == [1, 2]


def test_small_exhaustive_stable() -> None:
    for m in range(5):
        for n in range(5):
            for a in itertools.product(range(3), repeat=m):
                for b in itertools.product(range(3), repeat=n):
                    ta = [(x, 0, i) for i, x in enumerate(sorted(a))]
                    tb = [(x, 1, i) for i, x in enumerate(sorted(b))]
                    assert valiant_merge(ta, tb) == sorted(ta + tb)


def test_rounds_and_processors() -> None:
    rng = random.Random(11)
    for m, n in [(16, 16), (100, 100), (1000, 1000), (50, 3000), (4096, 4096)]:
        a = sorted(rng.randrange(m + n) for _ in range(m))
        b = sorted(rng.randrange(m + n) for _ in range(n))
        stats: dict = {}
        assert valiant_merge(a, b, stats) == sorted(a + b)
        assert stats["max_per_round"] <= m + n
        big = max(m, n)
        assert stats["rounds"] <= 2 * math.ceil(math.log2(math.log2(big))) + 1


def test_stable_custom_keys() -> None:
    class K:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "K") -> bool:
            return self.k < other.k

    a = [K(i // 3, f"a{i}") for i in range(9)]
    b = [K(i // 2, f"b{i}") for i in range(8)]
    out = valiant_merge(a, b)
    keys = [x.k for x in out]
    assert keys == sorted(keys)
    for k in range(4):
        tags = [x.tag for x in out if x.k == k]
        assert tags == sorted(tags, key=lambda s: (s[0], int(s[1:])))
