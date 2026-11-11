# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vigenere-cipher/. The authors are listed in prov/11VG96.jsonl.

import random
import string

import pytest

from english import SAMPLE, index_of_coincidence, letters
from vigenere_cipher import (
    autokey_decrypt,
    autokey_encrypt,
    columns,
    estimate_period,
    friedman_estimate,
    mean_column_ic,
    vigenere_break,
    vigenere_decrypt,
    vigenere_encrypt,
)


def oracle(text: str, key: str) -> str:
    """An independent implementation: the tabula recta, row by key letter."""
    up = string.ascii_uppercase
    rows = {k: up[i:] + up[:i] for i, k in enumerate(up)}
    out, j = [], 0
    for ch in text:
        if ch.upper() in up and ch.isascii() and ch.isalpha():
            c = rows[key[j % len(key)]][up.index(ch.upper())]
            out.append(c if ch.isupper() else c.lower())
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def test_example() -> None:
    assert vigenere_encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere_decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    assert vigenere_encrypt("Attack at dawn!", "LEMON") == "Lxfopv ef rnhr!"


def test_autokey_example() -> None:
    assert autokey_encrypt("ATTACKATDAWN", "QUEENLY") == "QNXEPVYTWTWP"
    assert autokey_decrypt("QNXEPVYTWTWP", "QUEENLY") == "ATTACKATDAWN"


def test_edge_cases() -> None:
    assert vigenere_encrypt("", "KEY") == ""
    assert vigenere_encrypt("HELLO", "A") == "HELLO"
    assert vigenere_encrypt("HELLO", "D") == "KHOOR"  # one key letter is the Caesar cipher
    for key in ("", "K3Y", "two words"):
        with pytest.raises(ValueError):
            vigenere_encrypt("HELLO", key)


def test_round_trip_and_oracle() -> None:
    rng = random.Random(11)
    alphabet = string.ascii_letters + " ,.;0123"
    for _ in range(600):
        key = "".join(rng.choice(string.ascii_uppercase) for _ in range(rng.randint(1, 9)))
        p = "".join(rng.choice(alphabet) for _ in range(rng.randrange(40)))
        c = vigenere_encrypt(p, key)
        assert c == oracle(p, key)
        assert vigenere_decrypt(c, key) == p
        assert autokey_decrypt(autokey_encrypt(p, key), key) == p


def test_index_of_coincidence_finds_the_period() -> None:
    p = letters(SAMPLE)
    c = vigenere_encrypt(p, "LEMON")
    assert round(index_of_coincidence(p), 4) == 0.0747
    assert round(index_of_coincidence(c), 4) == 0.0434
    ics = {m: mean_column_ic(c, m) for m in range(1, 13)}
    assert ics[5] > 0.07 and ics[10] > 0.07
    assert all(ics[m] < 0.045 for m in ics if m % 5)
    assert estimate_period(c) == 5
    assert round(friedman_estimate(c)) == 5


def test_break_recovers_lemon() -> None:
    c = vigenere_encrypt(SAMPLE, "LEMON")
    assert vigenere_break(c) == "LEMON"
    assert [len(col) for col in columns(c, 5)] == [100, 100, 100, 100, 99]


def test_break_random_keys() -> None:
    # A heuristic: keys with repeated letters can hide the period. On the
    # 499-letter sample, at least 95% of random keys of length 1 to 12 must
    # give a key that decrypts the whole text.
    p = letters(SAMPLE)
    rng = random.Random(1)
    ok = 0
    trials = 120
    for _ in range(trials):
        key = "".join(rng.choice(string.ascii_uppercase) for _ in range(rng.randint(1, 12)))
        c = vigenere_encrypt(p, key)
        ok += vigenere_decrypt(c, vigenere_break(c)) == p
    assert ok >= 0.95 * trials
