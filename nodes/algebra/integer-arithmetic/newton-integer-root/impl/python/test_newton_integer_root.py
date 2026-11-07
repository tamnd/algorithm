# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-integer-root/. The authors are listed in prov/8QNZZT.jsonl.

import math
import random

import pytest

from newton_integer_root import is_perfect_power, isqrt, newton_root, root_rem


def reference_root(n: int, k: int) -> int:
    """floor(n^(1/k)) by binary search, independent of Newton's method."""
    lo, hi = 0, 1 << (n.bit_length() // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**k <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def check(n: int, k: int) -> None:
    s = newton_root(n, k)
    assert s**k <= n < (s + 1) ** k


def test_example() -> None:
    stats: list = []
    assert newton_root(814507, 2, stats) == 902 and stats == [3]
    assert root_rem(814507) == (902, 903)
    assert newton_root(814507, 3) == 93


def test_small_exhaustive() -> None:
    for k in range(1, 7):
        for n in range(0, 5000):
            assert newton_root(n, k) == reference_root(n, k)
    for n in range(0, 20000):
        assert isqrt(n) == math.isqrt(n)


def test_edges() -> None:
    for w in (4, 8):
        for j in range(1, 40):
            for n in (2 ** (w * j) - 1, 2 ** (w * j), 2 ** (w * j) + 1):
                for k in (2, 3, 4, 7):
                    check(n, k)
                assert isqrt(n) == math.isqrt(n)
    for a in (2, 3, 10, 255, 256, 2**61 - 1):
        for k in (2, 3, 5, 13):
            p = a**k
            assert newton_root(p, k) == a
            assert newton_root(p - 1, k) == a - 1
            assert newton_root(p + 1, k) == a
    assert newton_root(0, 5) == 0 and newton_root(1, 5) == 1 and newton_root(7, 1) == 7
    assert newton_root(2**100, 200) == 1
    with pytest.raises(ValueError):
        newton_root(-1, 2)
    with pytest.raises(ValueError):
        newton_root(5, 0)


def test_random() -> None:
    rng = random.Random(1669)
    for _ in range(3000):
        b = rng.randint(1, 600)
        n = rng.getrandbits(b)
        k = rng.choice((2, 2, 3, 4, 5, 6, 9, 17, 40))
        s = newton_root(n, k)
        assert s**k <= n < (s + 1) ** k
        if k == 2:
            assert s == math.isqrt(n)


def test_perfect_power() -> None:
    assert is_perfect_power(1 << 12) == (2, 12)
    assert is_perfect_power(3**10) == (3, 10)
    assert is_perfect_power(36) == (6, 2)
    assert is_perfect_power(814507) is None
    assert is_perfect_power(1) is None
    rng = random.Random(5)
    for _ in range(200):
        a, k = rng.randint(2, 1000), rng.randint(2, 9)
        r = is_perfect_power(a**k)
        assert r is not None and r[0] ** r[1] == a**k and r[1] >= k
