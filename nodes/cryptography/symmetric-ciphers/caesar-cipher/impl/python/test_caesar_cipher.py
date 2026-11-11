# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/caesar-cipher/. The authors are listed in prov/CZPQ1B.jsonl.

import random
import string

from caesar_cipher import caesar_break, caesar_decrypt, caesar_encrypt
from english import SAMPLE, letters


def oracle(text: str, k: int) -> str:
    """An independent Caesar shift built from str.maketrans."""
    up, low = string.ascii_uppercase, string.ascii_lowercase
    k %= 26
    table = str.maketrans(up + low, up[k:] + up[:k] + low[k:] + low[:k])
    return text.translate(table)


def test_suetonius_shift_of_three() -> None:
    # Suetonius: Caesar wrote D for A, that is, a shift of 3.
    assert caesar_encrypt("ABCXYZ", 3) == "DEFABC"
    assert caesar_encrypt("Veni, vidi, vici.", 3) == "Yhql, ylgl, ylfl."
    assert caesar_decrypt("Yhql, ylgl, ylfl.", 3) == "Veni, vidi, vici."


def test_edges() -> None:
    assert caesar_encrypt("", 5) == ""
    assert caesar_encrypt("12 ,.!", 5) == "12 ,.!"
    assert caesar_encrypt("Zebra", 0) == "Zebra"
    assert caesar_encrypt("Zebra", 26) == "Zebra"
    assert caesar_encrypt("abc", -1) == "zab"
    assert caesar_encrypt("abc", 27) == caesar_encrypt("abc", 1)


def test_short_text_is_ambiguous() -> None:
    # Two English words that are shifts of each other: no score can choose.
    assert caesar_encrypt("CHEER", 7) == "JOLLY"


def test_round_trip_and_oracle() -> None:
    rng = random.Random(1)
    alphabet = string.ascii_letters + " .,;!0123456789"
    for _ in range(600):
        p = "".join(rng.choice(alphabet) for _ in range(rng.randrange(30)))
        k = rng.randrange(-60, 60)
        c = caesar_encrypt(p, k)
        assert c == oracle(p, k)
        assert caesar_decrypt(c, k) == p


def test_brute_force_recovers_every_key() -> None:
    for k in range(26):
        c = caesar_encrypt(SAMPLE, k)
        ranked = caesar_break(c)
        assert len(ranked) == 26
        assert ranked[0][1] == k
        assert caesar_decrypt(c, ranked[0][1]) == SAMPLE


def test_brute_force_on_a_short_prefix() -> None:
    # 40 letters of the sample are enough for every key.
    p = letters(SAMPLE)[:40]
    for k in range(26):
        assert caesar_break(caesar_encrypt(p, k))[0][1] == k
