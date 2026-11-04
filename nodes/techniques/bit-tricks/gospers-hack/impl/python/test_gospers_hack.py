# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gospers-hack/. The authors are listed in prov/EEBZ0F.jsonl.

import itertools
import math
import random

import pytest

from gospers_hack import gospers_hack, k_subsets


def popcount(v: int) -> int:
    return bin(v).count("1")


def brute_next(x: int, w: int) -> int | None:
    k = popcount(x)
    for y in range(x + 1, 1 << w):
        if popcount(y) == k:
            return y
    return None


def test_example() -> None:
    assert gospers_hack(92, 8) == 99
    assert list(k_subsets(5, 3)) == [7, 11, 13, 14, 19, 21, 22, 25, 26, 28]
    assert gospers_hack(28, 8) == 35


def test_exhaustive_small_words() -> None:
    for w in range(1, 13):
        for x in range(1, 1 << w):
            want = brute_next(x, w)
            got = gospers_hack(x, w)
            if want is not None:
                assert got == want
            else:
                k = popcount(x)
                assert got < x
                assert popcount(got) == max(k - 2, 0)


def test_last_combination_wraps() -> None:
    assert gospers_hack(0b11100000, 8) == 1
    assert gospers_hack(0b10000000, 8) == 0


def test_zero_is_rejected() -> None:
    with pytest.raises(ValueError):
        gospers_hack(0, 8)


def test_k_subsets_match_itertools() -> None:
    for n in range(0, 11):
        for k in range(0, n + 1):
            want = sorted(sum(1 << i for i in c) for c in itertools.combinations(range(n), k))
            got = list(k_subsets(n, k))
            assert got == want
            assert len(got) == math.comb(n, k)


def scan_next(x: int) -> int:
    """Independent oracle: scan for the lowest 1 with a 0 above it."""
    i = 0
    below = 0
    while not ((x >> i) & 1 and not (x >> (i + 1)) & 1):
        below += (x >> i) & 1
        i += 1
    high = (x >> (i + 2)) << (i + 2)
    return high | (1 << (i + 1)) | ((1 << below) - 1)


def test_random_64_bit_against_scan() -> None:
    rng = random.Random(175)
    for _ in range(3000):
        x = rng.randrange(1, 1 << 64)
        if (x + (x & -x)) >> 64:
            continue  # the last combination of its size: no answer in 64 bits
        assert gospers_hack(x, 64) == scan_next(x)
