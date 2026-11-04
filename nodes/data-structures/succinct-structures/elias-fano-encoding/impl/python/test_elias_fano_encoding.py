# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elias-fano-encoding/. The authors are listed in prov/XGWQ3Q.jsonl.

import bisect
import random

import pytest

from elias_fano_encoding import EliasFano


def check_all(xs: list[int], u: int) -> None:
    ef = EliasFano(xs, u)
    n = len(xs)
    assert [ef.access(i) for i in range(n)] == xs
    for x in range(u):
        assert ef.next_geq(x) == bisect.bisect_left(xs, x)
    if 0 < n <= u:
        assert ef.size_in_bits() < n * ef.ell + 3 * n + 2


def test_page_example() -> None:
    xs = [3, 4, 7, 13, 14, 15, 21, 43]
    ef = EliasFano(xs, 64)
    assert ef.ell == 3
    h = "".join(str((ef.H.words[0] >> p) & 1) for p in range(16))
    assert h == "1110111010001000"
    assert ef.size_in_bits() == 40
    assert ef.access(6) == 21 and ef.access(7) == 43
    assert ef.H.select(1, 0) == 3 and ef.H.select(3, 0) == 9
    assert ef.next_geq(14) == 4
    assert ef.next_geq(30) == 7
    assert ef.next_geq(44) == 8
    check_all(xs, 64)


def test_edges() -> None:
    check_all([], 1)
    check_all([], 10)
    check_all([0], 1)
    check_all([5] * 20, 6)  # u < n, ell = 0
    check_all([0, 999], 1000)
    check_all(list(range(300)), 300)
    with pytest.raises(ValueError):
        EliasFano([3, 2], 10)
    with pytest.raises(ValueError):
        EliasFano([10], 10)
    with pytest.raises(IndexError):
        EliasFano([1], 10).access(1)


def test_random_against_bisect() -> None:
    rng = random.Random(1974)
    for _ in range(500):
        u = rng.randrange(1, 2000)
        n = rng.randrange(0, 300)
        xs = sorted(rng.randrange(u) for _ in range(n))
        ef = EliasFano(xs, u)
        assert [ef.access(i) for i in range(n)] == xs
        for _ in range(40):
            x = rng.randrange(u)
            assert ef.next_geq(x) == bisect.bisect_left(xs, x)
