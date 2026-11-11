# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/columnar-transposition-cipher/. The authors are listed in prov/G69PV9.jsonl.

import random

from columnar_transposition_cipher import (
    break_columnar,
    columnar_decrypt,
    columnar_encrypt,
    decrypt_order,
    double_decrypt,
    double_encrypt,
    encrypt_order,
    key_order,
    multiple_anagram,
)
from english import SAMPLE, chi_squared, counts, index_of_coincidence, letters


def oracle_encrypt(plaintext: str, key: str) -> str:
    """An independent statement: sort the letter positions by (rank of column, row)."""
    t = letters(plaintext)
    k = len(key)
    rank = {c: r for r, c in enumerate(sorted(range(k), key=lambda i: key[i] + chr(65 + i)))}
    pos = sorted(range(len(t)), key=lambda i: (rank[i % k], i // k))
    return "".join(t[i] for i in pos)


def test_example() -> None:
    assert key_order("ZEBRAS") == [4, 2, 1, 3, 5, 0]
    c = columnar_encrypt("WE ARE DISCOVERED FLEE AT ONCE", "ZEBRAS")
    assert c == "EVLNACDTESEAROFODEECWIREE"
    assert columnar_decrypt(c, "ZEBRAS") == "WEAREDISCOVEREDFLEEATONCE"


def test_edge_cases() -> None:
    assert columnar_encrypt("", "KEY") == ""
    assert columnar_decrypt("", "KEY") == ""
    assert columnar_encrypt("HELLO", "A") == "HELLO"  # one column changes nothing
    assert columnar_encrypt("HI", "ZEBRAS") == "IH"  # more columns than letters
    assert columnar_decrypt("IH", "ZEBRAS") == "HI"
    assert key_order("AAB") == [0, 1, 2]  # equal letters from left to right


def test_round_trip_and_oracle() -> None:
    rng = random.Random(11)
    for _ in range(600):
        key = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(rng.randrange(1, 12)))
        p = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(rng.randrange(60)))
        c = columnar_encrypt(p, key)
        assert c == oracle_encrypt(p, key)
        assert columnar_decrypt(c, key) == p
        key2 = "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(rng.randrange(1, 12)))
        assert double_decrypt(double_encrypt(p, key, key2), key, key2) == p


def test_frequencies_are_kept() -> None:
    c = columnar_encrypt(SAMPLE, "GERMAN")
    assert c.startswith("IOFEIMEFPTOEINCCTMNASMESEHRDSNCAANTOTMNE")
    assert counts(c) == counts(SAMPLE)
    assert index_of_coincidence(c) == index_of_coincidence(SAMPLE)
    assert round(index_of_coincidence(c), 4) == 0.0747
    assert round(chi_squared(c), 1) == 39.3
    d = double_encrypt(SAMPLE, "GERMAN", "SECOND")
    assert counts(d) == counts(SAMPLE)


def test_break_by_search() -> None:
    order = key_order("GERMAN")
    assert order == [4, 1, 0, 3, 5, 2]
    c = encrypt_order(SAMPLE, order)
    found = break_columnar(c, 6)
    assert found == order
    assert decrypt_order(c, found) == letters(SAMPLE)
    # Short pieces: 60 letters are enough, 20 letters often are not.
    t = letters(SAMPLE)
    wins = {n: sum(break_columnar(encrypt_order(t[s : s + n], order), 6) == order for s in range(0, 480 - n, 40)) for n in (20, 60)}
    assert wins == {20: 4, 60: 11}


def adjacency(chain: list[int], perm: list[int]) -> float:
    """The share of links in chain that join two neighbouring plaintext positions.

    Ciphertext position j holds plaintext position perm[j].
    """
    good = sum(1 for a, b in zip(chain, chain[1:]) if perm[b] == perm[a] + 1)
    return good / (len(perm) - 1)


def multiple_messages(length: int, seed: int) -> tuple[list[str], list[int]]:
    t = letters(SAMPLE)
    msgs = [t[i : i + length] for i in range(0, len(t) - length + 1, length)]
    rng = random.Random(seed)
    perm = list(range(length))
    rng.shuffle(perm)
    return ["".join(m[p] for p in perm) for m in msgs], perm


def test_multiple_anagramming() -> None:
    assert multiple_anagram([]) == []
    # 24 messages of 20 letters: every link is right.
    cts, perm = multiple_messages(20, 1)
    assert len(cts) == 24
    chain = multiple_anagram(cts)
    assert sorted(chain) == list(range(20))
    assert adjacency(chain, perm) == 1.0
    assert [perm[j] for j in chain] == list(range(20))
    # 12 messages of 40 letters: fewer messages, longer chains, more errors.
    cts, perm = multiple_messages(40, 2)
    assert len(cts) == 12
    chain = multiple_anagram(cts)
    assert sorted(chain) == list(range(40))
    assert adjacency(chain, perm) >= 0.5
