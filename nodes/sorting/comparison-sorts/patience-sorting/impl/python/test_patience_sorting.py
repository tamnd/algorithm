# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patience-sorting/. The authors are listed in prov/JTB25B.jsonl.

import itertools
import random

from patience_sorting import deal, longest_nondecreasing_subsequence, patience_sorting


def test_example() -> None:
    a = [5, 1, 4, 2, 8, 3, 7, 6]
    assert deal(a) == [[5, 1], [4, 2], [8, 3], [7, 6]]
    assert longest_nondecreasing_subsequence(a) == [1, 2, 3, 6]
    patience_sorting(a)
    assert a == [1, 2, 3, 4, 5, 6, 7, 8]


def brute_longest(a: list[int]) -> int:
    best = 0
    for r in range(len(a) + 1):
        for idx in itertools.combinations(range(len(a)), r):
            if all(a[idx[t]] <= a[idx[t + 1]] for t in range(r - 1)):
                best = max(best, r)
    return best


def test_piles_equal_longest_nondecreasing() -> None:
    rng = random.Random(3)
    for _ in range(300):
        a = [rng.randint(0, 5) for _ in range(rng.randint(0, 10))]
        s = longest_nondecreasing_subsequence(a)
        assert len(deal(a)) == len(s) == brute_longest(a)
        assert all(s[t] <= s[t + 1] for t in range(len(s) - 1))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], list(range(30)), list(range(30, 0, -1))):
        b = list(a)
        patience_sorting(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(8)
    for _ in range(200):
        pairs = [(rng.randint(0, 4), i) for i in range(rng.randint(0, 30))]
        b = [Key(k, t) for k, t in pairs]
        patience_sorting(b)
        assert [(x.k, x.tag) for x in b] == sorted(pairs)


def test_random_against_sorted() -> None:
    rng = random.Random(10)
    for _ in range(100):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 300))]
        b = list(a)
        patience_sorting(b)
        assert b == sorted(a)
