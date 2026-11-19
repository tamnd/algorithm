# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phrase-pair-extraction/. The authors are listed in prov/ZVR7MS.jsonl.

import random

import pytest

from phrase_pair_extraction import (
    brute_force_pairs,
    extract_phrase_pairs,
    is_consistent,
    phrase_strings,
)


def test_example_unaligned_source_word() -> None:
    f = "er geht ja nicht nach hause".split()
    e = "he does not go home".split()
    a = {(1, 1), (2, 4), (4, 2), (4, 3), (5, 5), (6, 5)}
    pairs = extract_phrase_pairs(len(f), len(e), a)
    assert len(pairs) == 10
    got = phrase_strings(f, e, pairs)
    assert ("geht ja", "go") in got
    assert ("ja nicht", "does not") in got
    assert ("nach hause", "home") in got
    assert ("nach", "home") not in got
    assert ("er geht ja nicht nach hause", "he does not go home") in got


def test_example_unaligned_target_word() -> None:
    f = "das haus ist klein".split()
    e = "the house is very small".split()
    a = {(1, 1), (2, 2), (3, 3), (4, 5)}
    pairs = extract_phrase_pairs(len(f), len(e), a)
    assert len(pairs) == 14
    got = phrase_strings(f, e, pairs)
    assert ("klein", "small") in got and ("klein", "very small") in got
    assert ("ist", "is very") in got


def test_max_len() -> None:
    f = "das haus ist klein".split()
    e = "the house is very small".split()
    a = {(1, 1), (2, 2), (3, 3), (4, 5)}
    for k in range(1, 6):
        pairs = extract_phrase_pairs(4, 5, a, max_len=k)
        assert pairs == brute_force_pairs(4, 5, a, max_len=k)
        assert all(t - s <= k and v - u <= k for (s, t), (u, v) in pairs)
    assert len(extract_phrase_pairs(4, 5, a, max_len=1)) == 4


def test_edge_cases() -> None:
    assert extract_phrase_pairs(3, 3, set()) == set()
    full = {(j, i) for j in range(1, 4) for i in range(1, 3)}
    assert extract_phrase_pairs(3, 2, full) == {((0, 3), (0, 2))}
    diag = {(j, j) for j in range(1, 5)}
    # a monotone one-to-one alignment gives one pair per pair of equal spans
    assert len(extract_phrase_pairs(4, 4, diag)) == 10
    with pytest.raises(ValueError):
        extract_phrase_pairs(2, 2, {(3, 1)})


def test_inverted_alignment() -> None:
    # a b c -> c' b' a': every span of the source pairs with the mirrored span
    a = {(1, 3), (2, 2), (3, 1)}
    pairs = extract_phrase_pairs(3, 3, a)
    assert pairs == {((s, t), (3 - t, 3 - s)) for s in range(3) for t in range(s + 1, 4)}


def test_every_pair_is_consistent() -> None:
    rng = random.Random(7)
    for _ in range(200):
        m, l = rng.randint(1, 7), rng.randint(1, 7)
        a = {(j, i) for j in range(1, m + 1) for i in range(1, l + 1) if rng.random() < 0.25}
        for p in extract_phrase_pairs(m, l, a):
            assert is_consistent(p, a)


def test_random_against_brute_force() -> None:
    rng = random.Random(2003)
    for _ in range(400):
        m, l = rng.randint(1, 9), rng.randint(1, 9)
        dens = rng.choice([0.1, 0.2, 0.35, 0.6])
        a = {(j, i) for j in range(1, m + 1) for i in range(1, l + 1) if rng.random() < dens}
        k = rng.randint(1, 8)
        assert extract_phrase_pairs(m, l, a, max_len=k) == brute_force_pairs(m, l, a, max_len=k)
