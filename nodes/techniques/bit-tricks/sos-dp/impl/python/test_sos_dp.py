# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sos-dp/. The authors are listed in prov/2ABXMX.jsonl.

import random

import pytest

from sos_dp import mobius, sos_dp, sos_dp_supersets


def brute_subsets(f: list[int], n: int) -> list[int]:
    return [sum(f[s] for s in range(1 << n) if s & ~m == 0) for m in range(1 << n)]


def brute_supersets(f: list[int], n: int) -> list[int]:
    return [sum(f[s] for s in range(1 << n) if s & m == m) for m in range(1 << n)]


def test_example() -> None:
    f = [3, 1, 4, 1, 5, 9, 2, 6]
    assert sos_dp(f, 3) == [3, 4, 7, 9, 8, 18, 14, 31]
    assert sos_dp_supersets(f, 3) == [31, 17, 13, 7, 22, 15, 8, 6]
    assert mobius([3, 4, 7, 9, 8, 18, 14, 31], 3) == f
    assert sos_dp([1, 2, 3, 4], 2) == [1, 3, 4, 10]


def test_edges() -> None:
    assert sos_dp([7], 0) == [7]
    assert sos_dp([0, 0], 1) == [0, 0]
    assert sos_dp([1, 1, 1, 1], 2) == [1, 2, 2, 4]  # the wrong loop nesting gives 5 at the end
    with pytest.raises(ValueError):
        sos_dp([1, 2, 3], 2)


def test_other_monoids() -> None:
    f = [3, 1, 4, 1, 5, 9, 2, 6]
    assert sos_dp(f, 3, max) == [max(f[s] for s in range(8) if s & ~m == 0) for m in range(8)]
    assert sos_dp(f, 3, min) == [min(f[s] for s in range(8) if s & ~m == 0) for m in range(8)]


def test_or_convolution() -> None:
    rng = random.Random(7)
    for n in range(0, 6):
        a = [rng.randrange(-5, 6) for _ in range(1 << n)]
        b = [rng.randrange(-5, 6) for _ in range(1 << n)]
        za, zb = sos_dp(a, n), sos_dp(b, n)
        h = mobius([x * y for x, y in zip(za, zb)], n)
        want = [0] * (1 << n)
        for i in range(1 << n):
            for j in range(1 << n):
                want[i | j] += a[i] * b[j]
        assert h == want


def test_random_against_brute_force() -> None:
    rng = random.Random(2007)
    for _ in range(600):
        n = rng.randrange(0, 8)
        f = [rng.randrange(-10**12, 10**12) for _ in range(1 << n)]
        F = sos_dp(f, n)
        assert F == brute_subsets(f, n)
        assert sos_dp_supersets(f, n) == brute_supersets(f, n)
        assert mobius(F, n) == f
