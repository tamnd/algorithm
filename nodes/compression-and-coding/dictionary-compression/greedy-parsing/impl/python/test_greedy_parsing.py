# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-parsing/. The authors are listed in prov/08SJN4.jsonl.

import itertools
import random

from greedy_parsing import (
    bit_cost,
    decode,
    gamma,
    greedy_parse,
    greedy_parse_lz77,
    greedy_parse_static,
)


def _copy_len(t: bytes, i: int, window, cap: int) -> int:
    """Longest copy at i, by trying every source; any shorter copy is also valid."""
    lo = 0 if window is None else max(0, i - window)
    best = 0
    for j in range(lo, i):
        k = 0
        while k < cap and t[j + k] == t[i + k]:
            k += 1
        best = max(best, k)
    return best


def _all_parses(t: bytes, steps):
    """Enumerate every parse, as the list of its phrase ends, with an explicit stack."""
    stack = [(0, [])]
    while stack:
        i, ends = stack.pop()
        if i == len(t):
            yield ends
            continue
        for e in steps(i):
            stack.append((e, ends + [e]))


def brute_min_phrases(t: bytes, window=None, min_len: int = 1) -> int:
    def steps(i):
        yield i + 1  # a literal
        top = _copy_len(t, i, window, len(t) - i)
        for k in range(max(min_len, 2), top + 1):
            yield i + k
    return min(len(p) for p in _all_parses(t, steps))


def brute_min_triples(t: bytes, window=None) -> int:
    def steps(i):
        top = _copy_len(t, i, window, len(t) - i - 1)
        for k in range(top + 1):
            yield i + k + 1
    return min(len(p) for p in _all_parses(t, steps))


def brute_min_bits(t: bytes) -> int:
    """Minimum of bit_cost over all parses into literals and copies of any source."""
    n = len(t)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        c = 9 + best[i + 1]
        for j in range(i):
            k = 0
            while i + k < n and t[j + k] == t[i + k]:
                k += 1
                c = min(c, 1 + gamma(k) + gamma(i - j) + best[i + k])
        best[i] = c
    return best[0]


def _inputs(rng: random.Random, count: int, maxlen: int):
    for _ in range(count):
        n = rng.randrange(maxlen + 1)
        kind = rng.randrange(3)
        if kind == 0:
            yield bytes(rng.choice(b"ab") for _ in range(n))
        elif kind == 1:
            yield bytes(rng.choice(b"abc") for _ in range(n))
        else:
            unit = bytes(rng.choice(b"ab") for _ in range(rng.randrange(1, 4)))
            yield (unit * n)[:n]


def test_page_examples() -> None:
    t = b"aabbaa"
    g = greedy_parse(t)
    assert g == [("L", 97), ("M", 1, 1), ("L", 98), ("M", 1, 1), ("M", 2, 4)]
    assert bit_cost(g) == 33
    better = [("L", 97), ("M", 1, 1), ("L", 98), ("M", 1, 1), ("M", 1, 3), ("M", 1, 1)]
    assert decode(better) == t and bit_cost(better) == 32
    assert brute_min_bits(t) == 32

    t = b"aaabaaaaa"
    g = greedy_parse(t, min_len=3)
    assert g == [("L", 97)] * 3 + [("L", 98), ("M", 3, 4), ("L", 97), ("L", 97)]
    better = [("L", 97)] * 3 + [("L", 98), ("L", 97), ("M", 4, 1)]
    assert decode(better) == t and len(better) == 6
    assert brute_min_phrases(t, min_len=3) == 6

    d = {b"a", b"b", b"c", b"d", b"ab", b"bcd"}
    assert greedy_parse_static(b"abcd", d) == [b"ab", b"c", b"d"]
    d.add(b"bc")  # now closed under prefixes, and greedy still needs 3 phrases
    assert greedy_parse_static(b"abcd", d) == [b"ab", b"c", b"d"]


def test_triples_against_copies() -> None:
    rng = random.Random(23)
    for t in _inputs(rng, 200, 40):
        w = rng.choice([None, 4, 9])
        z_t, z_c = len(greedy_parse_lz77(t, w)), len(greedy_parse(t, w))
        assert z_t <= z_c <= 2 * z_t


def test_edges() -> None:
    assert greedy_parse(b"") == [] and greedy_parse_lz77(b"") == []
    assert greedy_parse(b"x") == [("L", 120)]
    assert greedy_parse_lz77(b"x") == [("T", 0, 0, 120)]
    assert greedy_parse(b"a" * 1000) == [("L", 97), ("M", 999, 1)]
    assert greedy_parse(b"a" * 1000, max_len=258)[:2] == [("L", 97), ("M", 258, 1)]
    assert greedy_parse_lz77(b"a" * 1000) == [("T", 0, 0, 97), ("T", 998, 1, 97)]
    for t in (b"", b"q", b"qq", b"a" * 300, b"ab" * 150, bytes(range(256))):
        assert decode(greedy_parse(t)) == t
        assert decode(greedy_parse(t, window=7, min_len=3)) == t
        assert decode(greedy_parse_lz77(t, window=5)) == t


def test_greedy_minimizes_phrase_count_exhaustive() -> None:
    for n in range(0, 10):
        for s in itertools.product(b"ab", repeat=n):
            t = bytes(s)
            assert len(greedy_parse(t)) == brute_min_phrases(t)
            assert len(greedy_parse_lz77(t)) == brute_min_triples(t)


def test_greedy_minimizes_phrase_count_with_a_window() -> None:
    rng = random.Random(1982)
    for t in _inputs(rng, 300, 11):
        w = rng.randrange(1, 6)
        assert len(greedy_parse(t, window=w)) == brute_min_phrases(t, window=w)
        assert len(greedy_parse_lz77(t, window=w)) == brute_min_triples(t, window=w)


def test_minimum_copy_length_breaks_optimality() -> None:
    rng = random.Random(3)
    worse = 0
    for t in _inputs(rng, 300, 11):
        g = len(greedy_parse(t, min_len=3))
        b = brute_min_phrases(t, min_len=3)
        assert g >= b
        worse += g > b
    assert worse > 0


def test_greedy_is_not_bit_optimal() -> None:
    rng = random.Random(8)
    worse = 0
    for t in _inputs(rng, 300, 14):
        g = bit_cost(greedy_parse(t))
        b = brute_min_bits(t)
        assert g >= b
        worse += g > b
    assert worse > 0


def test_static_dictionary() -> None:
    d = {b"a", b"b", b"ab", b"ba", b"bab", b"aab"}
    rng = random.Random(11)
    for _ in range(200):
        t = bytes(rng.choice(b"ab") for _ in range(rng.randrange(12)))
        p = greedy_parse_static(t, d)
        assert p is not None and b"".join(p) == t
        assert all(w in d for w in p)


def test_round_trip_random() -> None:
    rng = random.Random(1977)
    for _ in range(60):
        t = bytes(rng.randrange(256) for _ in range(rng.randrange(200)))
        t += t[: rng.randrange(len(t) + 1)]
        assert decode(greedy_parse(t)) == t
        assert decode(greedy_parse(t, window=16, min_len=3, max_len=10)) == t
        assert decode(greedy_parse_lz77(t)) == t
