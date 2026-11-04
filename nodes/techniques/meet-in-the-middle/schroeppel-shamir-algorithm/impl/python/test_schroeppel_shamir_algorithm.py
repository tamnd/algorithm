# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schroeppel-shamir-algorithm/. The authors are listed in prov/9AEYS5.jsonl.

import itertools
import random

from schroeppel_shamir_algorithm import schroeppel_shamir


def brute_force(a: list[int], t: int) -> bool:
    return any(
        sum(c) == t
        for r in range(len(a) + 1)
        for c in itertools.combinations(a, r)
    )


def is_valid(a: list[int], t: int, s: list[int] | None) -> bool:
    return s is not None and s == sorted(set(s)) and all(0 <= p < len(a) for p in s) and sum(a[p] for p in s) == t


def test_example() -> None:
    a = [31, 17, 45, 8, 26, 53, 12, 39]
    assert schroeppel_shamir(a, 110) == [0, 4, 5]
    assert schroeppel_shamir(a, 2) is None


def test_edges() -> None:
    assert schroeppel_shamir([], 0) == []
    assert schroeppel_shamir([], 5) is None
    assert schroeppel_shamir([7], 7) == [0]
    assert schroeppel_shamir([7], 0) == []
    assert schroeppel_shamir([7], 3) is None
    assert is_valid([5, 5, 5, 5, 5], 15, schroeppel_shamir([5, 5, 5, 5, 5], 15))
    assert schroeppel_shamir([5, 5, 5, 5, 5], 7) is None
    big = [2**62, 2**62 - 1, 3, -(2**62), 2**61, 1]
    assert is_valid(big, 2**62 + 2**61 + 2, schroeppel_shamir(big, 2**62 + 2**61 + 2))


def test_against_brute_force() -> None:
    rng = random.Random(20240611)
    for _ in range(800):
        n = rng.randrange(0, 11)
        a = [rng.randrange(-30, 60) for _ in range(n)]
        t = rng.randrange(-40, 150)
        got = schroeppel_shamir(a, t)
        if brute_force(a, t):
            assert is_valid(a, t, got)
        else:
            assert got is None
