# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-text-transform/. The authors are listed in prov/3C2Q9R.jsonl.

# Oracles: the worked example of the page, exhaustive reversibility over all
# short strings of a small alphabet that holds every flag character, random
# texts, and a check that capital conversion makes the words of a text with
# mixed capitals fall into fewer distinct forms.

import itertools
import random

from reversible_text_transform import (
    CAP,
    DESC,
    ESC,
    UPPER,
    WORD,
    cap_decode,
    cap_encode,
    decode,
    dict_decode,
    dict_encode,
    encode,
)

WORDS = ["the", "team", "a", "ab"]


def test_worked_example() -> None:
    x = "The NASA team met THE Team."
    c = cap_encode(x)
    assert c == CAP + "the " + UPPER + "nasa team met " + UPPER + "the " + CAP + "team."
    y = dict_encode(c, ["the", "team"])
    assert y == (
        CAP + WORD + "\x00 " + UPPER + "nasa " + WORD + "\x01 met "
        + UPPER + WORD + "\x00 " + CAP + WORD + "\x01."
    )
    assert decode(y, ["the", "team"]) == x


def test_edges() -> None:
    assert cap_encode("") == ""
    assert cap_encode("I") == CAP + "i"
    assert cap_encode("iPhone McDonald") == "iPhone McDonald"
    assert cap_encode(CAP) == ESC + CAP
    assert dict_encode(WORD, WORDS) == DESC + WORD
    assert dict_encode("theme", WORDS) == "theme"  # only whole words


def test_exhaustive_short_strings() -> None:
    alphabet = ["a", "b", "A", "B", " ", CAP, UPPER, ESC, WORD, DESC]
    for n in range(0, 5):
        for t in itertools.product(alphabet, repeat=n):
            x = "".join(t)
            assert cap_decode(cap_encode(x)) == x
            assert dict_decode(dict_encode(x, WORDS), WORDS) == x
            assert decode(encode(x, WORDS), WORDS) == x


def test_random_texts() -> None:
    rng = random.Random(1998)
    vocab = ["the", "The", "THE", "team", "Team", "NASA", "a", "A", "iPhone", "x", "\x01", "\x04"]
    for _ in range(500):
        x = "".join(rng.choice(vocab) + rng.choice([" ", ", ", ".\n", ""]) for _ in range(rng.randrange(0, 30)))
        assert decode(encode(x, WORDS), WORDS) == x
    for _ in range(200):
        x = "".join(chr(rng.randrange(0, 128)) for _ in range(rng.randrange(0, 60)))
        assert decode(encode(x, WORDS), WORDS) == x


def test_fewer_word_forms() -> None:
    text = "The cat. THE CAT. the Cat. Cat the cat."
    forms = {w.strip(".") for w in text.split()}
    coded = cap_encode(text)
    coded_forms = {w.strip(".").lstrip(CAP + UPPER) for w in coded.split()}
    assert len(forms) == 6 and coded_forms == {"the", "cat"}
