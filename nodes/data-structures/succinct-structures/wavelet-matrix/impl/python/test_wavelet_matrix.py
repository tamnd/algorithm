# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavelet-matrix/. The authors are listed in prov/1R9K6G.jsonl.

import random

import pytest

from wavelet_matrix import WaveletMatrix

CODE = {"a": 0, "b": 1, "c": 2, "d": 3, "r": 4}
S = [CODE[ch] for ch in "abracadabra"]


def check_all(seq: list[int], sigma: int, rng: random.Random) -> None:
    t = WaveletMatrix(seq, sigma)
    n = len(seq)
    assert [t.access(i) for i in range(n)] == seq
    for c in range(sigma):
        r = 0
        for i in range(n + 1):
            assert t.rank(c, i) == r
            if i < n and seq[i] == c:
                r += 1
        pos = [i for i, x in enumerate(seq) if x == c]
        for j, p in enumerate(pos, 1):
            assert t.select(c, j) == p
    for _ in range(30 if n else 0):
        l = rng.randrange(n)
        r = rng.randrange(l + 1, n + 1)
        k = rng.randrange(1, r - l + 1)
        assert t.quantile(l, r, k) == sorted(seq[l:r])[k - 1]


def row(m: WaveletMatrix, level: int) -> str:
    b = m.B[level]
    return "".join(str(b.access(i)) for i in range(len(b)))


def test_page_example() -> None:
    m = WaveletMatrix(S, 5)
    assert m.L == 3
    assert [row(m, k) for k in range(3)] == ["00100000010", "00010100000", "01000100001"]
    assert m.z == [9, 9, 8]
    assert m.access(4) == CODE["c"]
    assert m.rank(CODE["a"], 7) == 3
    assert m.rank(CODE["r"], 10) == 2
    assert m.select(CODE["a"], 4) == 7
    assert m.select(CODE["r"], 2) == 9
    assert m.quantile(2, 9, 4) == CODE["b"]
    check_all(S, 5, random.Random(1))


def test_edges() -> None:
    rng = random.Random(2)
    check_all([], 1, rng)
    check_all([0], 1, rng)
    check_all([0, 0, 0], 1, rng)
    check_all([3, 3, 3], 4, rng)
    check_all(list(range(100)), 100, rng)
    check_all([1, 0] * 70, 2, rng)
    t = WaveletMatrix([0, 2], 4)
    assert t.rank(1, 2) == 0 and t.rank(3, 2) == 0
    with pytest.raises(IndexError):
        t.select(1, 1)
    with pytest.raises(ValueError):
        WaveletMatrix([4], 4)


def test_random_against_lists() -> None:
    rng = random.Random(2012)
    for _ in range(500):
        sigma = rng.randrange(1, 20)
        n = rng.randrange(0, 80)
        check_all([rng.randrange(sigma) for _ in range(n)], sigma, rng)
