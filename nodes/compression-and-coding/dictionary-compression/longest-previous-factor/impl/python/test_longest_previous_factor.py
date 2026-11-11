# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/longest-previous-factor/. The authors are listed in prov/H8NZFT.jsonl.

import random

from longest_previous_factor import (
    decode_factors,
    lcp_array,
    lpf_array,
    lpf_brute,
    lz_factorization,
    suffix_array,
)


def _check(t) -> None:
    lpf, prev = lpf_array(t)
    assert lpf == lpf_brute(t)
    for i in range(len(t)):
        if lpf[i]:
            assert 0 <= prev[i] < i
            assert t[prev[i]:prev[i] + lpf[i]] == t[i:i + lpf[i]]
        else:
            assert prev[i] == -1


def _fibonacci_word(n: int) -> bytes:
    a, b = b"a", b"ab"
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def test_page_example() -> None:
    t = b"abbaabbbaaabab"
    sa = suffix_array(t)
    assert sa == [8, 9, 3, 12, 10, 0, 4, 13, 7, 2, 11, 6, 1, 5]
    assert lcp_array(t, sa) == [0, 2, 3, 1, 2, 2, 3, 0, 1, 3, 2, 1, 4, 2]
    lpf, prev = lpf_array(t)
    assert lpf == [0, 0, 1, 1, 3, 2, 4, 3, 2, 3, 2, 2, 2, 1]
    assert prev == [-1, -1, 1, 0, 0, 1, 1, 2, 3, 3, 0, 2, 10, 7]
    f = lz_factorization(t)
    assert f == [(1, -1), (1, -1), (1, 1), (1, 0), (3, 0), (3, 2), (2, 0), (2, 10)]
    assert bytes(decode_factors(f, b"ab")) == t


def test_edges() -> None:
    assert lpf_array(b"") == ([], [])
    assert lpf_array(b"x") == ([0], [-1])
    n = 500
    lpf, prev = lpf_array(b"a" * n)
    assert lpf == [0] + [n - i for i in range(1, n)]
    assert all(0 <= prev[i] < i for i in range(1, n))
    assert lz_factorization(b"a" * n) == [(1, -1), (n - 1, 0)]
    assert lpf_array(bytes(range(200)))[0] == [0] * 200
    for t in (b"ab", b"aa", b"aab", b"abab", b"a" * 30 + b"b" + b"a" * 30, _fibonacci_word(89)):
        _check(t)


def test_random_against_brute_force() -> None:
    rng = random.Random(2008)
    for _ in range(800):
        alphabet = rng.choice([b"ab", b"abc", b"acgt"])
        t = bytes(rng.choice(alphabet) for _ in range(rng.randrange(50)))
        _check(t)


def test_repetitive() -> None:
    rng = random.Random(106)
    for _ in range(100):
        unit = bytes(rng.choice(b"ab") for _ in range(rng.randrange(1, 6)))
        t = (unit * 20)[: rng.randrange(1, 80)]
        if rng.random() < 0.5:
            k = rng.randrange(len(t))
            t = t[:k] + b"c" + t[k + 1:]
        _check(t)


def test_suffix_and_lcp_arrays() -> None:
    rng = random.Random(1990)
    for _ in range(300):
        t = bytes(rng.choice(b"ab") for _ in range(rng.randrange(60)))
        sa = suffix_array(t)
        assert sa == sorted(range(len(t)), key=lambda i: t[i:])
        lcp = lcp_array(t, sa)
        for r in range(1, len(t)):
            a, b = t[sa[r - 1]:], t[sa[r]:]
            k = 0
            while k < min(len(a), len(b)) and a[k] == b[k]:
                k += 1
            assert lcp[r] == k


def test_factorization_is_greedy_and_decodes() -> None:
    rng = random.Random(75)
    for _ in range(300):
        t = bytes(rng.choice(b"abc") for _ in range(rng.randrange(80)))
        f = lz_factorization(t)
        news = [t[i] for i in range(len(t)) if t[i] not in t[:i]]
        assert bytes(decode_factors(f, news)) == t
        lpf = lpf_brute(t)
        i = 0
        for length, _ in f:
            assert length == max(1, lpf[i])
            i += length
