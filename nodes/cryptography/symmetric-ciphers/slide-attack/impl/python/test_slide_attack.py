# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slide-attack/. The authors are listed in prov/KDTCXR.jsonl.

import random

from slide_attack import (
    PERM,
    encrypt,
    key_from_pair,
    known_pairs,
    recover_key,
    round_function,
    slide_candidates,
)


def test_perm_is_an_involution() -> None:
    assert all(PERM[PERM[x]] == x for x in range(1 << 16))


def test_key_from_pair() -> None:
    rng = random.Random(1)
    for _ in range(100):
        k, p = rng.getrandbits(16), rng.getrandbits(16)
        assert key_from_pair(p, round_function(p, k)) == k


def test_slid_pair_property() -> None:
    rng = random.Random(2)
    k = rng.getrandbits(16)
    for rounds in (1, 7, 100):
        p = rng.getrandbits(16)
        q = round_function(p, k)
        assert encrypt(q, k, rounds) == round_function(encrypt(p, k, rounds), k)


def test_recover_key_any_number_of_rounds() -> None:
    # m = 512 known pairs: about m^2 / 2^16 = 4 slid pairs are expected.
    rng = random.Random(3)
    for rounds in (16, 64, 500):
        k = rng.getrandbits(16)
        known = known_pairs(k, rounds, 512, rng)
        assert k in slide_candidates(known)
        extra = [(p, encrypt(p, k, rounds)) for p in (0x1234, 0xBEEF)]
        got = recover_key(known, lambda g: all(encrypt(p, g, rounds) == c for p, c in extra))
        assert got == k


def test_too_few_texts_usually_fail() -> None:
    # m = 32 gives about 32^2 / 2^16 = 1/64 slid pairs.
    rng = random.Random(4)
    hits = 0
    for _ in range(20):
        k = rng.getrandbits(16)
        hits += k in slide_candidates(known_pairs(k, 32, 32, rng))
    assert hits <= 3
