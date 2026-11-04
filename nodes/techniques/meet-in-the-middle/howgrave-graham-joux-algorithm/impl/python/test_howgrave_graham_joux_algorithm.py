# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/howgrave-graham-joux-algorithm/. The authors are listed in prov/ZVD66Y.jsonl.

import itertools
import math
import random

from howgrave_graham_joux_algorithm import _list, howgrave_graham_joux


def brute_force(a: list[int], t: int, w: int) -> bool:
    return any(sum(a[i] for i in c) == t for c in itertools.combinations(range(len(a)), w))


def is_valid(a: list[int], t: int, w: int, s: list[int] | None) -> bool:
    return (
        s is not None
        and len(s) == w
        and s == sorted(set(s))
        and all(0 <= i < len(a) for i in s)
        and sum(a[i] for i in s) == t
    )


def test_example() -> None:
    a = [31, 17, 45, 8, 26, 53, 12, 39]
    for seed in range(20):
        assert howgrave_graham_joux(a, 114, 4, rng=random.Random(seed)) == [0, 2, 4, 6]
    assert howgrave_graham_joux(a, 102, 4, rng=random.Random(0)) is None


def test_example_lists() -> None:
    a = [31, 17, 45, 8, 26, 53, 12, 39]
    left, right = [0, 1, 2, 3], [4, 5, 6, 7]
    sizes = [len(_list(a, left, 1, right, 1, r, 4)) for r in range(4)]
    assert sizes == [4, 4, 4, 4]
    sums = sorted(sum(a[p] for p in range(8) if x >> p & 1) for x in _list(a, left, 1, right, 1, 1, 4))
    assert sums == [29, 57, 57, 61]


def test_edges() -> None:
    assert howgrave_graham_joux([], 0, 0) == []
    assert howgrave_graham_joux([], 0, 1) is None
    assert howgrave_graham_joux([4], 4, 1) == [0]
    assert howgrave_graham_joux([4], 0, 0) == []
    assert howgrave_graham_joux([4], 4, 0) is None
    assert howgrave_graham_joux([1, 2], 3, 3) is None
    assert howgrave_graham_joux([1, 2], 3, -1) is None
    same = [7] * 6
    assert is_valid(same, 21, 3, howgrave_graham_joux(same, 21, 3, rng=random.Random(3)))
    assert howgrave_graham_joux(same, 20, 3, rng=random.Random(3)) is None
    big = [2**62, 2**62 - 1, 3, -(2**62), 2**61, 1, 5, 9]
    t = 2**62 + 2**61 + 3 + 9
    assert is_valid(big, t, 4, howgrave_graham_joux(big, t, 4, rng=random.Random(4)))


def test_list_against_brute_force() -> None:
    rng = random.Random(77)
    for _ in range(300):
        n = rng.randrange(0, 9)
        a = [rng.randrange(-20, 40) for _ in range(n)]
        perm = list(range(n))
        rng.shuffle(perm)
        left, right = perm[: n // 2], perm[n // 2 :]
        i, j = rng.randrange(0, 3), rng.randrange(0, 3)
        m = rng.randrange(1, 7)
        r = rng.randrange(m)
        want = sorted(
            sum(1 << p for p in x) | sum(1 << p for p in z)
            for x in itertools.combinations(left, i)
            for z in itertools.combinations(right, j)
            if (sum(a[p] for p in x) + sum(a[p] for p in z) - r) % m == 0
        )
        assert sorted(_list(a, left, i, right, j, r, m)) == want


def test_against_brute_force() -> None:
    rng = random.Random(20100530)
    for _ in range(800):
        n = rng.randrange(0, 11)
        a = [rng.randrange(-30, 60) for _ in range(n)]
        w = rng.randrange(0, n + 2)
        t = rng.randrange(-40, 200)
        got = howgrave_graham_joux(a, t, w, rng=rng)
        if brute_force(a, t, w):
            assert is_valid(a, t, w, got)
        else:
            assert got is None


def test_rounds_alone_find_planted_solutions() -> None:
    rng = random.Random(5)
    found = 0
    trials = 200
    for _ in range(trials):
        n = 12
        a = [rng.randrange(1, 2**20) for _ in range(n)]
        e = rng.sample(range(n), n // 2)
        t = sum(a[i] for i in e)
        got = howgrave_graham_joux(a, t, n // 2, rounds=40, rng=rng, fallback=False)
        if got is not None:
            assert is_valid(a, t, n // 2, got)
            found += 1
    assert found >= trials * 9 // 10
    assert math.comb(3, 1) * math.comb(3, 1) == 9
