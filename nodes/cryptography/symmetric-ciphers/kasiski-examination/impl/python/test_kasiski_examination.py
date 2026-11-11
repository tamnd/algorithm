# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasiski-examination/. The authors are listed in prov/ZTGXR5.jsonl.

import random
import string

from english import SAMPLE, chi_squared, index_of_coincidence, letters
from kasiski_examination import (
    factor_counts,
    gcd_of_distances,
    kasiski_distances,
    kasiski_period,
    repeats,
)


def vigenere(text: str, key: str, sign: int = 1) -> str:
    t = letters(text)
    return "".join(chr((ord(c) - 65 + sign * (ord(key[i % len(key)]) - 65)) % 26 + 65) for i, c in enumerate(t))


def ic_period(c: str, max_period: int = 20) -> int:
    """The index of coincidence method, for the comparison: the smallest m
    whose mean column IC is at least 0.85 times the largest one."""
    ics = [sum(index_of_coincidence(c[i::m]) for i in range(m)) / m for m in range(1, max_period + 1)]
    return next(m for m in range(1, max_period + 1) if ics[m - 1] >= 0.85 * max(ics))


def oracle_distances(c: str, length: int = 3) -> list[int]:
    """Brute force: for each i, the distance to the next j > i with the same substring."""
    c = letters(c)
    out = []
    for i in range(len(c) - length + 1):
        for j in range(i + 1, len(c) - length + 1):
            if c[j : j + length] == c[i : i + length]:
                out.append(j - i)
                break
    return sorted(out)


def test_small_example() -> None:
    # THE at 0 and 12 under a key of length 4: the same ciphertext piece.
    c = vigenere("THEDOGANDCATTHE", "WXYZ")
    assert c == "PECCKDYMZZYSPEC"
    assert kasiski_distances(c) == [12]
    assert gcd_of_distances([12]) == 12


def test_edge_cases() -> None:
    assert kasiski_distances("") == []
    assert kasiski_distances("ABCDEFG") == []
    assert kasiski_period("ABCDEFG") is None
    assert kasiski_distances("AAAA") == [1]
    assert kasiski_distances("AAAAA") == [1, 1]
    assert gcd_of_distances([]) == 0


def test_lemon_on_sample() -> None:
    c = vigenere(SAMPLE, "LEMON")
    d = kasiski_distances(c)
    assert len(repeats(c)) == 32 and len(d) == 45
    assert repeats(c)["XTS"] == [6, 186, 311, 336, 391, 456]
    # Three false hits (62, 256, 261) make the gcd of all distances 1.
    assert [x for x in d if x % 5] == [62, 256, 261]
    assert gcd_of_distances(d) == 1
    assert gcd_of_distances([x for x in d if x % 5 == 0]) == 5
    counts = factor_counts(d)
    assert counts[5] == 42 and counts[10] == 20 and counts[2] == 22
    assert kasiski_period(c) == 5


def test_kasiski_and_ic_agree_then_frequency_analysis_finds_key() -> None:
    c = vigenere(SAMPLE, "LEMON")
    assert kasiski_period(c) == ic_period(c) == 5
    key = "".join(
        chr(65 + min(range(26), key=lambda s: chi_squared(vigenere(c[i::5], chr(65 + s), -1)))) for i in range(5)
    )
    assert key == "LEMON"


def test_distances_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(500):
        k = rng.randint(1, 6)
        alphabet = string.ascii_uppercase[:k]
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(60)))
        for length in (2, 3):
            assert kasiski_distances(s, length) == oracle_distances(s, length)


def test_random_keys() -> None:
    # On the 499-letter sample, Kasiski finds the least period of at least
    # 95% of random keys of length 2 to 12.
    p = letters(SAMPLE)
    rng = random.Random(2)
    ok = 0
    trials = 150
    for _ in range(trials):
        n = rng.randint(2, 12)
        key = "".join(rng.choice(string.ascii_uppercase) for _ in range(n))
        least = next(q for q in range(1, n + 1) if n % q == 0 and key == key[:q] * (n // q))
        ok += kasiski_period(vigenere(p, key)) == least
    assert ok >= 0.95 * trials
