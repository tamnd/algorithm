# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-absent-words-algorithm/. The authors are listed in prov/DEK3N2.jsonl.

import itertools
import random

from minimal_absent_words_algorithm import (
    minimal_absent_strings,
    minimal_absent_words,
    suffix_automaton,
)


def factors(y: str) -> set[str]:
    return {y[i:j] for i in range(len(y) + 1) for j in range(i, len(y) + 1)}


def brute_force(y: str, alphabet: str) -> list[str]:
    """Check the definition directly on every candidate word.

    A minimal absent word has all its proper prefixes in the factor set, so
    only words f + b with f a factor and b a letter need checking; for each,
    every proper factor is tested explicitly.
    """
    f = factors(y)
    out = set()
    for x in f:
        for b in alphabet:
            w = x + b
            if w in f:
                continue
            proper = {w[i:j] for i in range(len(w) + 1) for j in range(i, len(w) + 1)} - {w}
            if proper <= f:
                out.add(w)
    return sorted(out)


def test_example() -> None:
    assert minimal_absent_strings("abaab", "ab") == ["aaa", "aaba", "bab", "bb"]
    assert sorted(minimal_absent_words("abaab", "ab")) == [
        (1, 1, "b"),
        (1, 2, "b"),
        (2, 2, "a"),
        (2, 3, "a"),
    ]
    assert minimal_absent_strings("banana", "abn") == ["aa", "ab", "bb", "bn", "nanan", "nb", "nn"]


def test_edges() -> None:
    assert minimal_absent_strings("", "ab") == ["a", "b"]
    assert minimal_absent_strings("", "") == []
    assert minimal_absent_strings("a", "a") == ["aa"]
    assert minimal_absent_strings("aaaa", "ab") == ["aaaaa", "b"]
    assert minimal_absent_strings("abc", "abcd") == ["aa", "ac", "ba", "bb", "ca", "cb", "cc", "d"]
    assert minimal_absent_words([1, 2, 1], [1, 2]) is not None


def test_automaton_size() -> None:
    rng = random.Random(3)
    for _ in range(200):
        y = "".join(rng.choice("ab") for _ in range(rng.randrange(1, 60)))
        nxt, link, length, end = suffix_automaton(y)
        assert len(length) <= max(2, 2 * len(y) - 1)
        assert sum(len(d) for d in nxt) <= (3 * len(y) - 4 if len(y) >= 3 else 3)


def test_exhaustive_small() -> None:
    for alphabet, top in (("a", 8), ("ab", 10), ("abc", 6)):
        for n in range(top + 1):
            for t in itertools.product(alphabet, repeat=n):
                y = "".join(t)
                assert minimal_absent_strings(y, alphabet) == brute_force(y, alphabet), y


def test_random_against_brute_force() -> None:
    rng = random.Random(20261106)
    for trial in range(600):
        alphabet = "abc"[: 1 + trial % 3]
        y = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 40)))
        got = minimal_absent_strings(y, alphabet)
        assert got == brute_force(y, alphabet), y
        assert len(got) == len(set(got))
        if y:
            assert len(got) <= 2 * len(alphabet) * len(y)


def test_factors_are_words_avoiding_maws() -> None:
    rng = random.Random(11)
    for _ in range(60):
        y = "".join(rng.choice("ab") for _ in range(rng.randrange(0, 9)))
        maws = minimal_absent_strings(y, "ab")
        f = factors(y)
        for length in range(len(y) + 3):
            for t in itertools.product("ab", repeat=length):
                w = "".join(t)
                assert (w in f) == (not any(m in w for m in maws))
