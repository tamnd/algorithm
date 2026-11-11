# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/match-finding/. The authors are listed in prov/625H77.jsonl.

import random

from match_finding import BinaryTrees, HashChains, all_matches, longest_match_brute


def _check(t: bytes, i: int, m: tuple[int, int]) -> None:
    length, dist = m
    if length:
        assert 1 <= dist <= i
        assert all(t[i - dist + k] == t[i + k] for k in range(length))


def _inputs(rng: random.Random, count: int, maxlen: int):
    alphabets = [b"a", b"ab", b"abc", b"acgt", bytes(range(256))]
    for _ in range(count):
        n = rng.randrange(maxlen)
        kind = rng.randrange(3)
        if kind == 0:
            a = rng.choice(alphabets)
            yield bytes(rng.choice(a) for _ in range(n))
        elif kind == 1:
            unit = bytes(rng.choice(b"xyz") for _ in range(rng.randrange(1, 7)))
            yield (unit * (n + 1))[:n]
        else:
            yield bytes(rng.choice(b"ab") for _ in range(n // 2)) + b"q" * (n - n // 2)


def test_page_example() -> None:
    t = b"abcde_abcxy_abcde"
    assert longest_match_brute(t, 12, min_len=3) == (5, 12)
    assert all_matches(t, HashChains(t, max_chain=1))[12] == (3, 6)
    assert all_matches(t, HashChains(t, max_chain=2))[12] == (5, 12)
    assert all_matches(t, HashChains(t))[12] == (5, 12)
    assert all_matches(t, BinaryTrees(t))[12] == (5, 12)


def test_edges() -> None:
    for t in (b"", b"a", b"ab", b"abc", b"aaaa", b"a" * 40, b"ab" * 30):
        hc = all_matches(t, HashChains(t))
        bt = all_matches(t, BinaryTrees(t))
        for i in range(len(t)):
            assert hc[i] == longest_match_brute(t, i, 3, 258)
            assert bt[i][0] == longest_match_brute(t, i, 2, 273)[0]
    # a long run: every position after 0 copies the previous byte
    n = 600
    run = b"a" * n
    hc = all_matches(run, HashChains(run))
    bt = all_matches(run, BinaryTrees(run))
    for i in range(n):
        left = n - i
        assert hc[i] == ((min(258, left), 1) if i and left >= 3 else (0, 0))
        assert bt[i] == ((min(273, left), 1) if i and left >= 2 else (0, 0))


def test_unlimited_chains_find_a_longest_match() -> None:
    rng = random.Random(1950)
    for t in _inputs(rng, 400, 70):
        got = all_matches(t, HashChains(t))
        for i in range(len(t)):
            assert got[i] == longest_match_brute(t, i, 3, 258)


def test_binary_trees_find_a_longest_match() -> None:
    rng = random.Random(2010)
    for t in _inputs(rng, 400, 70):
        got = all_matches(t, BinaryTrees(t))
        for i in range(len(t)):
            assert got[i][0] == longest_match_brute(t, i, 2, 273)[0]
            _check(t, i, got[i])


def test_chain_limit_is_a_heuristic() -> None:
    rng = random.Random(4)
    shorter = 0
    for t in _inputs(rng, 150, 100):
        got = all_matches(t, HashChains(t, max_chain=2))
        for i in range(len(t)):
            want = longest_match_brute(t, i, 3, 258)
            _check(t, i, got[i])
            assert got[i][0] <= want[0]
            shorter += got[i][0] < want[0]
    assert shorter > 0


def test_window() -> None:
    rng = random.Random(9)
    for t in _inputs(rng, 300, 90):
        w = rng.randrange(1, 40)
        hc = all_matches(t, HashChains(t, window=w))
        bt = all_matches(t, BinaryTrees(t, window=w))
        for i in range(len(t)):
            assert hc[i] == longest_match_brute(t, i, 3, 258, window=w)
            assert bt[i][0] == longest_match_brute(t, i, 2, 273, window=w)[0]
            if bt[i][0]:
                assert bt[i][1] <= w


def test_max_len() -> None:
    t = b"ab" * 50
    for i, m in enumerate(all_matches(t, HashChains(t, max_len=7))):
        assert m == longest_match_brute(t, i, 3, 7)
