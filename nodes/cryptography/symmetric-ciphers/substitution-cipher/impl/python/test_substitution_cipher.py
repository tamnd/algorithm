# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-cipher/. The authors are listed in prov/QQJETY.jsonl.

import math
import random
import string

import pytest

from english import SAMPLE, letters, ngram_score
from substitution_cipher import (
    hill_climb,
    invert_key,
    key_entropy_bits,
    random_key,
    substitution_decrypt,
    substitution_encrypt,
    unicity_distance,
)

QWERTY = "QWERTYUIOPASDFGHJKLZXCVBNM"


def oracle(text: str, key: str) -> str:
    up = string.ascii_uppercase
    return text.translate(str.maketrans(up + up.lower(), key + key.lower()))


def test_example() -> None:
    assert substitution_encrypt("FLEE AT ONCE", QWERTY) == "YSTT QZ GFET"
    assert substitution_decrypt("YSTT QZ GFET", QWERTY) == "FLEE AT ONCE"


def test_bad_keys() -> None:
    for key in ("", "ABC", "A" * 26, QWERTY[:-1] + "Q"):
        with pytest.raises(ValueError):
            substitution_encrypt("HELLO", key)


def test_identity_and_caesar_keys() -> None:
    assert substitution_encrypt("Hello, World", string.ascii_uppercase) == "Hello, World"
    shift3 = string.ascii_uppercase[3:] + string.ascii_uppercase[:3]
    assert substitution_encrypt("Veni, vidi, vici.", shift3) == "Yhql, ylgl, ylfl."


def test_round_trip_and_oracle() -> None:
    rng = random.Random(5)
    alphabet = string.ascii_letters + " ,.;0123"
    for _ in range(600):
        key = random_key(rng)
        p = "".join(rng.choice(alphabet) for _ in range(rng.randrange(30)))
        c = substitution_encrypt(p, key)
        assert c == oracle(p, key)
        assert substitution_decrypt(c, key) == p
        assert invert_key(invert_key(key)) == key


def test_key_space_and_unicity_distance() -> None:
    assert math.factorial(26) == 403291461126605635584000000
    assert abs(key_entropy_bits() - math.log2(math.factorial(26))) < 1e-9
    assert 88.38 < key_entropy_bits() < 88.39
    # D = 3.2 bits per letter of redundancy gives about 28 letters.
    assert round(unicity_distance(key_entropy_bits(), 3.2)) == 28


def test_hill_climbing_recovers_most_of_the_key() -> None:
    # The threshold: at least 80% of the letters of the sample decrypt
    # correctly, and at least 17 of the 23 letters that occur are right.
    p = letters(SAMPLE)
    for seed in range(3):
        key = random_key(random.Random(100 + seed))
        c = substitution_encrypt(p, key)
        dec_key = hill_climb(c, random.Random(seed))
        d = substitution_encrypt(c, dec_key)
        right = sum(a == b for a, b in zip(d, p))
        assert right >= 0.8 * len(p)
        inv = invert_key(key)
        present = set(c)
        assert len(present) == 23
        assert sum(dec_key[ord(x) - 65] == inv[ord(x) - 65] for x in present) >= 17


def test_score_prefers_english() -> None:
    p = letters(SAMPLE)
    key = random_key(random.Random(9))
    assert ngram_score(p) > ngram_score(substitution_encrypt(p, key))
