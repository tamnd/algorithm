# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timsort/. The authors are listed in prov/PM6BZ3.jsonl.

import bisect
import random

from timsort import binary_insertion_sort, count_run, gallop_left, gallop_right, min_run, timsort


class Key:
    __slots__ = ("k", "tag")

    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


def test_min_run() -> None:
    assert [min_run(n) for n in (1, 63, 64, 65, 100, 350, 2000, 10**5, 10**6)] == [1, 63, 32, 33, 50, 44, 63, 49, 62]
    for n in range(64, 5000):
        m = min_run(n)
        assert 32 <= m <= 64


def test_example_merges() -> None:
    a: list[int] = []
    base = 10**6
    for length in (120, 80, 60, 50, 40):
        base -= 1000
        a += list(range(base, base + length))
    expected = sorted(a)
    assert timsort(a) == [(80, 60), (120, 140), (50, 40), (260, 90)]
    assert a == expected


def test_count_run() -> None:
    a = [5, 4, 3, 3, 1]
    assert count_run(a, 0, 5) == 3
    assert a[:3] == [3, 4, 5]
    b = [1, 2, 2, 0]
    assert count_run(b, 0, 4) == 3


def test_binary_insertion_sort_is_stable() -> None:
    a = [Key(2, 0), Key(1, 1), Key(2, 2), Key(1, 3)]
    binary_insertion_sort(a, 0, 4, 1)
    assert [(x.k, x.tag) for x in a] == [(1, 1), (1, 3), (2, 0), (2, 2)]


def test_gallops_match_bisect() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        a = sorted(rng.randint(0, 9) for _ in range(rng.randint(1, 20)))
        pre = [rng.randint(0, 5) for _ in range(rng.randint(0, 3))]
        b = pre + a
        key = rng.randint(-1, 10)
        hint = rng.randrange(len(a))
        assert gallop_left(key, b, len(pre), len(a), hint) == bisect.bisect_left(a, key)
        assert gallop_right(key, b, len(pre), len(a), hint) == bisect.bisect_right(a, key)


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], list(range(200)), list(range(200, 0, -1))):
        b = list(a)
        timsort(b)
        assert b == sorted(a)


def patterned(rng: random.Random, n: int, mode: int) -> list[int]:
    if mode == 0:
        return [rng.randint(0, 3) for _ in range(n)]
    if mode == 1:
        return [rng.randint(0, 10**6) for _ in range(n)]
    if mode == 2:
        ks: list[int] = []
        while len(ks) < n:
            length = rng.randint(1, 200)
            block = [rng.randint(0, 100) for _ in range(length)]
            ks += sorted(block, reverse=rng.random() < 0.3)
        return ks[:n]
    half = n // 2
    return sorted(rng.randint(0, 100) for _ in range(half)) + sorted(rng.randint(0, 100) for _ in range(n - half))


def test_stable_on_patterns() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n = rng.choice([5, 63, 64, 65, 300, 1000])
        ks = patterned(rng, n, rng.randrange(4))
        b = [Key(k, i) for i, k in enumerate(ks)]
        timsort(b)
        assert [(x.k, x.tag) for x in b] == sorted((k, i) for i, k in enumerate(ks))
