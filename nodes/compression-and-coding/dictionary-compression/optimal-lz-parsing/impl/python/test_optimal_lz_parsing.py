# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-lz-parsing/. The authors are listed in prov/3V4KB0.jsonl.

import itertools
import random

from optimal_lz_parsing import (
    FlagModel,
    GammaModel,
    bits,
    decode,
    greedy_parse,
    matches,
    optimal_parse,
    optimal_parse_maximal,
)


def brute_min_bits(t: bytes, model, window=None, max_len=None) -> int:
    """Minimum over every parse, trying every copy length and every distance."""
    n = len(t)
    best = None
    stack = [(0, 0)]
    while stack:
        i, c = stack.pop()
        if i == n:
            best = c if best is None else min(best, c)
            continue
        stack.append((i + 1, c + model.literal(t[i])))
        lo = 0 if window is None else max(0, i - window)
        for j in range(lo, i):
            k = 0
            while i + k < n and t[j + k] == t[i + k] and (max_len is None or k < max_len):
                k += 1
                if k >= model.min_len:
                    stack.append((i + k, c + model.copy(k, i - j)))
    return best


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
    g = greedy_parse(t, GammaModel)
    assert bits(g, GammaModel) == 33
    c, p = optimal_parse(t, GammaModel)
    assert c == 32 and bits(p, GammaModel) == 32 and decode(p) == t
    assert p == [("L", 97), ("M", 1, 1), ("L", 98), ("M", 1, 1), ("M", 1, 3), ("M", 1, 1)]
    assert matches(b"abcabcab", 6) == [(1, 3), (2, 3)]
    assert matches(b"aaaaaa", 3) == [(1, 1), (2, 1), (3, 1)]

    t = b"abcabxbcab"
    assert matches(t, 6) == [(1, 2), (2, 5), (3, 5), (4, 5)]
    assert matches(t, 7) == [(1, 5), (2, 5), (3, 5)]


def test_flag_model_example() -> None:
    t = b"aabaaaa"
    g = greedy_parse(t, FlagModel)
    assert g == [("L", 97), ("L", 97), ("L", 98), ("M", 2, 3), ("M", 2, 1)]
    assert bits(g, FlagModel) == 61
    assert optimal_parse(t, FlagModel) == (53, [("L", 97), ("L", 97), ("L", 98), ("L", 97), ("M", 3, 1)])


def test_word_text() -> None:
    rng = random.Random(1)
    words = [b"the ", b"then ", b"there ", b"other ", b"them ", b"hat "]
    t = b"".join(rng.choice(words) for _ in range(150))
    assert len(t) == 752
    got = {}
    for model in (GammaModel, FlagModel):
        g = greedy_parse(t, model)
        c, p = optimal_parse(t, model)
        assert decode(p) == t and decode(g) == t
        got[model.__name__] = (bits(g, model), len(g), c, len(p))
    assert got == {"GammaModel": (1501, 85, 1364, 88), "FlagModel": (1383, 87, 1319, 87)}


def test_edges() -> None:
    for model in (GammaModel, FlagModel):
        assert optimal_parse(b"", model) == (0, [])
        assert optimal_parse(b"z", model) == (9, [("L", 122)])
    c, p = optimal_parse(b"a" * 1000, GammaModel)
    assert p == [("L", 97), ("M", 999, 1)] and c == 9 + 1 + 19 + 1
    c, p = optimal_parse(b"a" * 1000, FlagModel)
    assert decode(p) == b"a" * 1000
    assert c == 9 + 17 * 59  # 999 = 58 * 17 + 13 copies of at most 17
    rng = random.Random(0)
    t = bytes(rng.randrange(256) for _ in range(300))
    c, p = optimal_parse(t, GammaModel)
    assert decode(p) == t and c == bits(p, GammaModel)


def test_equals_brute_force_gamma() -> None:
    for n in range(0, 8):
        for s in itertools.product(b"ab", repeat=n):
            t = bytes(s)
            assert optimal_parse(t, GammaModel)[0] == brute_min_bits(t, GammaModel)
    rng = random.Random(2009)
    for t in _inputs(rng, 120, 9):
        w = rng.choice([None, 2, 3, 5])
        assert optimal_parse(t, GammaModel, window=w)[0] == brute_min_bits(t, GammaModel, window=w)


def test_equals_brute_force_flag() -> None:
    rng = random.Random(1982)
    for t in _inputs(rng, 200, 10):
        c, p = optimal_parse(t, FlagModel, window=4, max_len=3)
        assert c == brute_min_bits(t, FlagModel, window=4, max_len=3)
        assert decode(p) == t and bits(p, FlagModel) == c


def test_maximal_edges_suffice() -> None:
    rng = random.Random(2013)
    for t in _inputs(rng, 150, 60):
        w = rng.choice([None, 7, 20])
        assert optimal_parse_maximal(t, GammaModel, w)[0] == optimal_parse(t, GammaModel, w)[0]


def test_never_worse_than_greedy() -> None:
    rng = random.Random(4)
    worse = 0
    for t in _inputs(rng, 150, 60):
        for model in (GammaModel, FlagModel):
            c, p = optimal_parse(t, model)
            g = bits(greedy_parse(t, model), model)
            assert decode(p) == t and c <= g
            worse += c < g
    assert worse > 0
