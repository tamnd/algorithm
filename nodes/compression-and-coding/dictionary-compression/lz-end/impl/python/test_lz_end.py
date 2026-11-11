# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz-end/. The authors are listed in prov/71G02H.jsonl.

import random
from bisect import bisect_left

from lz_end import decode, extract, lz77_parse, lz_end_brute, lz_end_parse, phrase_ends


def _pieces(t, phrases) -> list:
    out, s = [], 0
    for e in phrase_ends(phrases):
        out.append(t[s:e + 1])
        s = e + 1
    return out


def _check(t) -> None:
    p = lz_end_parse(t)
    assert [(length, c) for _, length, c in p] == lz_end_brute(t)
    ends = phrase_ends(p)
    assert (ends[-1] if ends else -1) == len(t) - 1
    for k, (src, length, _) in enumerate(p):
        if length:
            # The copy ends at the end of an earlier phrase and equals the text there.
            assert 0 <= src < k
            start = ends[k] - length
            assert t[ends[src] - length + 1:ends[src] + 1] == t[start:ends[k]]
        else:
            assert src == -1
    assert decode(p) == list(t)
    # The greedy LZ77 parse with copy and symbol never has more phrases.
    assert len(lz77_parse(t)) <= len(p)


def _fibonacci_word(n: int) -> str:
    a, b = "a", "ab"
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def _period_doubling(n: int) -> str:
    s = "a"
    while len(s) < n:
        s = "".join("ab" if c == "a" else "aa" for c in s)
    return s[:n]


def test_page_example() -> None:
    t = "alabaralalabarda"
    p = lz_end_parse(t)
    assert p == [(-1, 0, "a"), (-1, 0, "l"), (0, 1, "b"), (0, 1, "r"), (1, 2, "a"), (3, 5, "d"), (-1, 0, "a")]
    assert _pieces(t, p) == ["a", "l", "ab", "ar", "ala", "labard", "a"]
    assert [length for length, _ in lz77_parse(t)] == [0, 0, 1, 1, 3, 4, 0]
    t = "abcabcabcabc"
    assert _pieces(t, lz_end_parse(t)) == ["a", "b", "c", "abca", "bcab", "c"]
    assert len(lz77_parse(t)) == 4


def test_edges() -> None:
    assert lz_end_parse("") == []
    assert decode([]) == []
    assert lz_end_parse("x") == [(-1, 0, "x")]
    assert _pieces("a" * 20, lz_end_parse("a" * 20)) == ["a", "aa", "aaaa", "a" * 8, "a" * 5]
    assert len(lz77_parse("a" * 20)) == 2
    # Phrase lengths double on a run, so a run of length 2^k - 1 has k phrases.
    for k in range(1, 12):
        p = lz_end_parse("a" * (2 ** k - 1))
        assert [length + 1 for _, length, _ in p] == [2 ** m for m in range(k)]
    for t in ("ab", "aa", "abc", "abab", "a" * 30 + "b" + "a" * 30, _fibonacci_word(89), bytes(range(50))):
        _check(t)


def test_random_against_brute_force() -> None:
    rng = random.Random(2010)
    for _ in range(700):
        alphabet = rng.choice(["ab", "abc", "acgt"])
        _check("".join(rng.choice(alphabet) for _ in range(rng.randrange(45))))


def test_repetitive() -> None:
    rng = random.Random(2013)
    for _ in range(150):
        unit = "".join(rng.choice("abc") for _ in range(rng.randrange(1, 7)))
        t = (unit * 30)[: rng.randrange(1, 90)]
        if rng.random() < 0.5:
            k = rng.randrange(len(t))
            t = t[:k] + "x" + t[k + 1:]
        _check(t)


def test_extract_matches_text_and_does_one_step_per_symbol() -> None:
    rng = random.Random(239)
    texts = [_fibonacci_word(3000), _period_doubling(3000), "".join(rng.choice("ab") for _ in range(3000))]
    for t in texts:
        p = lz_end_parse(t)
        assert "".join(decode(p)) == t
        ends = phrase_ends(p)
        for _ in range(300):
            i = rng.randrange(len(t))
            j = min(len(t), i + rng.randrange(1, 60))
            steps: list[int] = []
            assert "".join(extract(p, ends, i, j, steps)) == t[i:j]
            # Work = the symbols from i up to the end of the phrase that holds t[j-1].
            assert steps == [ends[bisect_left(ends, j - 1)] - i + 1]


def test_longer_texts_against_lz77() -> None:
    rng = random.Random(77)
    cases = [
        (_fibonacci_word(4000), 22, 17),
        (_period_doubling(4000), 23, 13),
    ]
    for t, z_end, z77 in cases:
        assert len(lz_end_parse(t)) == z_end
        assert len(lz77_parse(t)) == z77
    t = "".join(rng.choice("acgt") for _ in range(200)) * 20
    p = lz_end_parse(t)
    assert "".join(decode(p)) == t
    assert len(lz77_parse(t)) <= len(p)
