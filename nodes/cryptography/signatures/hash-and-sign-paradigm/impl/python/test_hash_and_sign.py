# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-and-sign-paradigm/. The authors are listed in prov/R0VXSE.jsonl.
"""Tests for the hash-and-sign template and Yuval's collision forgery on a
hash cut to 24 binary digits. No official vector exists for this attack; the
forgery is checked against the local verifier. The messages are fixed, so the
search is deterministic."""

import math

from hash_and_sign import (D, E, N, P, Q, SigningOracle, collision_forgery, sign, toy_hash, variants, verify,
                           yuval_collision)

FAIR = "I agree to pay Bob the sum of 100 dollars for the old bicycle he sold me on Monday this week".split()
UNFAIR = "I agree to pay Bob the sum of 9000 dollars for the old bicycle he sold me on Monday this week".split()


def test_toy_key() -> None:
    assert math.gcd(E, (P - 1) * (Q - 1)) == 1 and N > 1 << 24
    assert E * D % ((P - 1) * (Q - 1)) == 1


def test_round_trip() -> None:
    s = sign(b"hello")
    assert verify(b"hello", s) and not verify(b"hellp", s)


def test_variants_are_distinct() -> None:
    vs = list(variants(FAIR, 10))
    assert len(vs) == 1024 == len(set(vs))
    assert all(v.split() == [w.encode() for w in FAIR] for v in vs)


def test_yuval_collision_gives_forgery() -> None:
    pair = yuval_collision(variants(FAIR, 14), variants(UNFAIR, 14))
    assert pair is not None
    fair, unfair = pair
    assert b"100" in fair and b"9000" in unfair
    assert toy_hash(fair) == toy_hash(unfair) == 13065352
    oracle = SigningOracle()
    m, s = collision_forgery(oracle, fair, unfair)
    assert verify(m, s) and m not in oracle.queries and oracle.queries == [fair]


def test_birthday_count() -> None:
    # 2^14 x 2^14 pairs and 2^24 hash values: about 16 colliding pairs are expected.
    table = {}
    for m in variants(FAIR, 14):
        table.setdefault(toy_hash(m), []).append(m)
    hits = sum(len(table.get(toy_hash(m), [])) for m in variants(UNFAIR, 14))
    assert 4 <= hits <= 40


def test_longer_hash_breaks_this_pair() -> None:
    fair, unfair = yuval_collision(variants(FAIR, 14), variants(UNFAIR, 14))
    assert toy_hash(fair, 32) != toy_hash(unfair, 32)
    s = sign(fair, lambda m: toy_hash(m, 32))
    assert not verify(unfair, s, lambda m: toy_hash(m, 32))
