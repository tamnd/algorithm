# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-cipher/. The authors are listed in prov/WCAD3J.jsonl.

import math
import random
import string

import pytest

from affine_cipher import (
    affine_break,
    affine_decrypt,
    affine_encrypt,
    all_keys,
    inverse_mod,
    recover_key,
)
from english import SAMPLE


def oracle(text: str, a: int, b: int) -> str:
    up, low = string.ascii_uppercase, string.ascii_lowercase
    img = "".join(up[(a * x + b) % 26] for x in range(26))
    return text.translate(str.maketrans(up + low, img + img.lower()))


def test_example() -> None:
    assert affine_encrypt("AFFINECIPHER", 5, 8) == "IHHWVCSWFRCP"
    assert affine_decrypt("IHHWVCSWFRCP", 5, 8) == "AFFINECIPHER"


def test_key_count_is_312() -> None:
    keys = all_keys()
    assert len(keys) == 312 == 12 * 26
    assert {a for a, _ in keys} == {a for a in range(26) if math.gcd(a, 26) == 1}


def test_inverse_against_pow() -> None:
    for a in range(26):
        if math.gcd(a, 26) == 1:
            assert inverse_mod(a) == pow(a, -1, 26)
        else:
            with pytest.raises(ValueError):
                inverse_mod(a)


def test_bad_key_is_rejected() -> None:
    for a in (0, 2, 13, 26):
        with pytest.raises(ValueError):
            affine_encrypt("HELLO", a, 3)


def test_caesar_is_the_case_a_equal_1() -> None:
    assert affine_encrypt("Veni, vidi, vici.", 1, 3) == "Yhql, ylgl, ylfl."


def test_round_trip_and_oracle() -> None:
    rng = random.Random(2)
    keys = all_keys()
    alphabet = string.ascii_letters + " .,!0123"
    for _ in range(600):
        a, b = rng.choice(keys)
        p = "".join(rng.choice(alphabet) for _ in range(rng.randrange(25)))
        c = affine_encrypt(p, a, b)
        assert c == oracle(p, a, b)
        assert affine_decrypt(c, a, b) == p


def test_two_pairs_recover_the_key() -> None:
    # For each key and each pair of plaintext letters, the consistent keys are
    # exactly the true key, unless x1 - x2 is 0 or 13 modulo 26.
    for a, b in all_keys():
        for x1 in range(26):
            for x2 in range(26):
                y1, y2 = (a * x1 + b) % 26, (a * x2 + b) % 26
                found = recover_key(x1, y1, x2, y2)
                if (x1 - x2) % 26 in (0, 13):
                    assert len(found) == 12 and (a, b) in found
                else:
                    assert found == [(a, b)]


def test_recover_key_against_brute_force() -> None:
    rng = random.Random(4)
    keys = all_keys()
    for _ in range(500):
        x1, y1, x2, y2 = (rng.randrange(26) for _ in range(4))
        brute = [k for k in keys if (k[0] * x1 + k[1]) % 26 == y1 and (k[0] * x2 + k[1]) % 26 == y2]
        assert recover_key(x1, y1, x2, y2) == brute


def test_known_plaintext_e_and_t() -> None:
    c = affine_encrypt("THE", 5, 8)
    # T -> c[0], E -> c[2]
    keys = recover_key(19, ord(c[0]) - 65, 4, ord(c[2]) - 65)
    assert keys == [(5, 8)]


def test_brute_force_recovers_the_key() -> None:
    rng = random.Random(3)
    for a, b in rng.sample(all_keys(), 8):
        best = affine_break(affine_encrypt(SAMPLE, a, b))[0]
        assert (best[1], best[2]) == (a, b)
