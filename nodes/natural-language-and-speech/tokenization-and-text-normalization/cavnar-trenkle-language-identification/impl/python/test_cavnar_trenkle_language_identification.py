# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cavnar-trenkle-language-identification/. The authors are listed in prov/2S4GCR.jsonl.

import random

import pytest

from cavnar_trenkle_language_identification import (
    classify,
    distances,
    ngram_counts,
    out_of_place,
    profile,
    tokens,
    train,
)

SAMPLES = {
    "en": "the cat and the dog are in the house. the children play with the ball in the garden. "
    "this is the end of the story and the start of the next one.",
    "fr": "le chat et le chien sont dans la maison. les enfants jouent avec la balle dans le jardin. "
    "ceci est la fin de l histoire et le debut de la suivante.",
    "de": "die katze und der hund sind in dem haus. die kinder spielen mit dem ball in dem garten. "
    "das ist das ende der geschichte und der anfang der naechsten.",
}


def slow_counts(text, max_n=5):
    """Count n-grams by scanning characters by hand, with the same token and padding rules."""
    words, cur = [], ""
    for ch in text + " ":
        if ch.isalpha() or ch == "'":
            cur += ch
        else:
            if cur:
                words.append(cur)
            cur = ""
    out = {}
    for w in words:
        for n in range(1, max_n + 1):
            u = w if n == 1 else "_" + w + "_" * (n - 1)
            for i in range(len(u) - n + 1):
                out[u[i : i + n]] = out.get(u[i : i + n], 0) + 1
    return out


def slow_distance(doc, cat, penalty):
    total = 0
    for r, g in enumerate(doc):
        total += abs(r - list(cat).index(g)) if g in cat else penalty
    return total


def test_paper_padding_of_text():
    c = ngram_counts("TEXT")
    two = sorted(g for g in c if len(g) == 2)
    three = sorted(g for g in c if len(g) == 3)
    four = sorted(g for g in c if len(g) == 4)
    assert two == sorted(["_T", "TE", "EX", "XT", "T_"])
    assert three == sorted(["_TE", "TEX", "EXT", "XT_", "T__"])
    assert four == sorted(["_TEX", "TEXT", "EXT_", "XT__", "T___"])
    assert all(sum(v for g, v in c.items() if len(g) == n) == 5 for n in range(2, 6))
    assert sum(v for g, v in c.items() if len(g) == 1) == 4


def test_paper_out_of_place_example():
    doc = ["TH", "ER", "ING", "ON", "ED"]
    cat = ["TH", "ER", "ON", "LE", "ED", "ING", "AND"]
    contrib = [0, 0, 3, 1, 0]
    assert out_of_place(doc, cat, penalty=7) == sum(contrib)
    assert out_of_place(["XX"], cat, penalty=7) == 7


def test_tokens():
    assert tokens("Don't stop: 42 times, ok?") == ["Don't", "stop", "times", "ok"]
    assert tokens("12 3.4 ,,") == []


def test_page_example_profile_length_six():
    p = train(SAMPLES, 6)
    assert p["en"] == ["e", "t", "h", "e_", "e__", "e___"]
    assert p["fr"] == ["e", "a", "l", "n", "_l", "t"]
    assert p["de"] == ["e", "d", "n", "_d", "i", "a"]
    assert profile("the house", 6) == ["e", "e_", "e__", "e___", "e____", "h"]
    assert distances("the house", p, 6) == {"en": 15, "fr": 30, "de": 30}
    assert classify("the house", p, 6) == "en"


def test_short_profiles_fail_long_profiles_work():
    text = "the end of the day"
    assert classify(text, train(SAMPLES, 8), 8) == "fr"
    assert distances(text, train(SAMPLES, 8), 8) == {"en": 46, "fr": 40, "de": 52}
    assert all(classify(text, train(SAMPLES, L), L) == "en" for L in range(11, 21))


def test_classify_with_default_size():
    p = train(SAMPLES)
    cases = {
        "the end of the day": "en", "in the garden": "en", "the house": "en",
        "la fin du jour": "fr", "dans la maison": "fr",
        "das ende des tages": "de", "und der hund": "de", "in dem garten": "de",
    }
    for text, lang in cases.items():
        assert classify(text, p) == lang


def test_edge_cases():
    p = train(SAMPLES, 10)
    assert profile("", 10) == []
    assert distances("123 !!", p, 10) == {"en": 0, "fr": 0, "de": 0}
    assert classify("123 !!", p, 10) == "de"
    with pytest.raises(ValueError):
        classify("abc", {})
    assert out_of_place(p["en"], p["en"]) == 0


def test_random_against_slow_versions():
    rng = random.Random(1994)
    letters = "abcde'"
    for _ in range(500):
        text = "".join(rng.choice(letters + " .1") for _ in range(rng.randint(0, 30)))
        size = rng.randint(1, 12)
        c = ngram_counts(text)
        assert c == slow_counts(text)
        p = profile(text, size)
        assert len(p) == min(size, len(c))
        for a, b in zip(p, p[1:]):
            assert c[a] > c[b] or (c[a] == c[b] and a < b)
        if len(c) > size:
            assert c[p[-1]] >= max(c[g] for g in c if g not in p)
        cats = {
            name: profile("".join(rng.choice(letters + " ") for _ in range(40)), size)
            for name in ("x", "y", "z")
        }
        ds = {name: slow_distance(p, cat, size) for name, cat in cats.items()}
        assert distances(text, cats, size) == ds
        best = min(sorted(ds), key=lambda name: ds[name])
        assert classify(text, cats, size) == best
        assert all(0 <= d <= size * len(p) for d in ds.values())
