# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-wordpiece-tokenization/. The authors are listed in prov/PZXMS8.jsonl.

import random

import pytest

from fast_wordpiece_tokenization import (
    UNK,
    failure_table,
    lin_max_match,
    max_match,
    precompute,
    tokenize,
)

PAPER_VOCAB = {"a", "abcdx", "##b", "##c", "##cdy", "##dz"}


def brute_force_greedy(word, vocab):
    """Greedy longest match first, written as a search over all piece ends."""
    out, i = [], 0
    while i < len(word):
        ends = [j for j in range(i + 1, len(word) + 1) if (word[i:j] if i == 0 else "##" + word[i:j]) in vocab]
        if not ends:
            return [UNK]
        j = max(ends)
        out.append(word[i:j] if i == 0 else "##" + word[i:j])
        i = j
    return out


def test_failure_table_of_the_paper():
    table = failure_table(precompute(PAPER_VOCAB))
    expected = {
        "": ([], None),
        "#": ([], None),
        "##": ([], None),
        "a": (["a"], "##"),
        "ab": (["a"], "##b"),
        "abc": (["a", "##b"], "##c"),
        "abcd": (["a", "##b"], "##cd"),
        "abcdx": (["abcdx"], "##"),
        "##b": (["##b"], "##"),
        "##c": (["##c"], "##"),
        "##cd": (["##c"], "##d"),
        "##cdy": (["##cdy"], "##"),
        "##d": ([], None),
        "##dz": (["##dz"], "##"),
    }
    assert table == expected


def test_paper_examples():
    t = precompute(PAPER_VOCAB)
    stats = {}
    assert lin_max_match("abcdz", t, stats) == ["a", "##b", "##c", "##dz"]
    assert stats == {"goto": 5, "fail": 3}
    assert lin_max_match("abcz", t) == [UNK]
    assert lin_max_match("abcd", t) == [UNK]
    assert lin_max_match("abcdx", t) == ["abcdx"]
    assert lin_max_match("##bc", t) == ["##b", "##c"]
    assert lin_max_match("", t) == []


def test_bare_suffix_indicator_falls_back():
    t = precompute({"#", "a"})
    assert lin_max_match("##", t) == max_match("##", {"#", "a"}) == [UNK]
    t2 = precompute({"#", "###"})
    assert lin_max_match("##", t2) == max_match("##", {"#", "###"}) == ["#", "###"]


def test_bad_tokens_are_rejected():
    with pytest.raises(ValueError):
        precompute({"##"})
    with pytest.raises(ValueError):
        precompute({"a b"})
    with pytest.raises(ValueError):
        lin_max_match("a b", precompute({"a"}))


def test_against_brute_force_on_random_vocabularies():
    rng = random.Random(2021)
    for _ in range(400):
        vocab = {"".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 6))}
        vocab |= {"##" + "".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 7))}
        t = precompute(vocab)
        for _ in range(15):
            word = "".join(rng.choice("abc") for _ in range(rng.randint(1, 10)))
            assert lin_max_match(word, t) == brute_force_greedy(word, vocab)


def random_hash_vocab(rng):
    vocab = {"".join(rng.choice("ab#") for _ in range(rng.randint(1, 4))) for _ in range(6)}
    vocab |= {"##" + "".join(rng.choice("ab#") for _ in range(rng.randint(1, 3))) for _ in range(6)}
    vocab.discard("##")
    return vocab


def test_words_with_the_hash_character():
    # Words that do not start with ##: equal output for every vocabulary.
    rng = random.Random(5)
    for _ in range(300):
        vocab = random_hash_vocab(rng)
        t = precompute(vocab)
        for _ in range(10):
            word = "".join(rng.choice("ab#") for _ in range(rng.randint(1, 8)))
            if not word.startswith("##"):
                assert lin_max_match(word, t) == brute_force_greedy(word, vocab)


def test_words_that_start_with_the_prefix():
    # Words that start with ##: equal output when "#" is not a token.
    rng = random.Random(6)
    for _ in range(300):
        vocab = random_hash_vocab(rng)
        vocab.discard("#")
        t = precompute(vocab)
        for _ in range(10):
            word = "##" + "".join(rng.choice("ab#") for _ in range(rng.randint(0, 6)))
            assert lin_max_match(word, t) == brute_force_greedy(word, vocab)


def test_the_one_corner_case():
    # With "#" in V, a word that starts with ## can differ from the original encoder.
    vocab = {"#", "###c"}
    assert max_match("##c", vocab) == ["#", "###c"]
    assert lin_max_match("##c", precompute(vocab)) == [UNK]


def test_steps_are_linear():
    # The worst case of the original encoder: vocabulary {a, ##a, a^m b}.
    for m in (5, 20, 60):
        vocab = {"a", "##a", "a" * m + "b"}
        t = precompute(vocab)
        word = "a" * m
        stats = {}
        assert lin_max_match(word, t, stats) == ["a"] + ["##a"] * (m - 1)
        assert stats["goto"] + stats["fail"] <= 2 * len(word) + 2
    rng = random.Random(9)
    for _ in range(200):
        vocab = {"".join(rng.choice("ab") for _ in range(rng.randint(1, 6))) for _ in range(6)}
        vocab |= {"##" + "".join(rng.choice("ab") for _ in range(rng.randint(1, 6))) for _ in range(8)}
        t = precompute(vocab)
        word = "".join(rng.choice("ab") for _ in range(rng.randint(1, 30)))
        stats = {}
        lin_max_match(word, t, stats)
        assert stats["goto"] <= len(word)
        assert stats["fail"] <= stats["goto"] + 1


def test_tokenize_many_words():
    assert tokenize(["abcdz", "abcz", "a"], PAPER_VOCAB) == ["a", "##b", "##c", "##dz", UNK, "a"]
