# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wavelet-tree/. The authors are listed in prov/K5P9KD.jsonl.

import random

import pytest

from wavelet_tree import WaveletTree

CODE = {"a": 0, "b": 1, "c": 2, "d": 3, "r": 4}
S = [CODE[ch] for ch in "abracadabra"]


def bits(v) -> str:
    return "".join(str(v.bits.access(i)) for i in range(len(v.bits)))


def check_all(seq: list[int], sigma: int, rng: random.Random) -> None:
    t = WaveletTree(seq, sigma)
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


def test_page_example() -> None:
    t = WaveletTree(S, 5)
    assert bits(t.root) == "00101010010"
    assert bits(t.root.left) == "0100010"
    assert bits(t.root.right) == "1011"
    assert bits(t.root.right.right) == "101"
    assert t.access(4) == CODE["c"]
    assert t.rank(CODE["a"], 7) == 3
    assert t.select(CODE["a"], 4) == 7
    assert t.rank(CODE["b"], 9) == 2
    assert t.select(CODE["r"], 2) == 9
    assert t.quantile(2, 9, 4) == CODE["b"]
    check_all(S, 5, random.Random(1))


def test_edges() -> None:
    rng = random.Random(2)
    check_all([], 1, rng)
    check_all([0], 1, rng)
    check_all([0, 0, 0], 1, rng)
    check_all([3, 3, 3], 4, rng)
    check_all(list(range(100)), 100, rng)
    check_all([1, 0] * 70, 2, rng)
    t = WaveletTree([0, 2], 4)
    assert t.rank(1, 2) == 0 and t.rank(3, 2) == 0
    with pytest.raises(IndexError):
        t.select(1, 1)
    with pytest.raises(ValueError):
        WaveletTree([4], 4)


def test_random_against_lists() -> None:
    rng = random.Random(2003)
    for _ in range(500):
        sigma = rng.randrange(1, 20)
        n = rng.randrange(0, 80)
        check_all([rng.randrange(sigma) for _ in range(n)], sigma, rng)
