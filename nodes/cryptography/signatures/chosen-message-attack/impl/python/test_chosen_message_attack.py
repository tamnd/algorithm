# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chosen-message-attack/. The authors are listed in prov/Z5A66M.jsonl.
"""Tests for the chosen-message forgeries on textbook RSA and for the e = 3
forgery against a flawed PKCS #1 v1.5 verifier. No official test vector exists
for these attacks; every forgery is checked against the local verifiers. The
DigestInfo prefix is copied from RFC 8017, Section 9.2, Note 1."""

import hashlib
import random

import pytest

from chosen_message_attack import (SHA256_DIGEST_INFO, SigningOracle, bleichenbacher_e3_forgery,
                                   directed_blinding_forgery, emsa_pkcs1_v15, flawed_pkcs1_verify,
                                   generic_product_forgery, icbrt, pkcs1_sign, pkcs1_verify,
                                   textbook_verify, toy_rsa_key)

N_TOY, E_TOY, D_TOY = 3233, 17, 2753  # p = 61, q = 53
N, E, D = toy_rsa_key(2048, 3, seed=4)  # a public test key; its factors are not secret


def test_toy_key_values() -> None:
    oracle = SigningOracle(N_TOY, D_TOY)
    m, s = generic_product_forgery(N_TOY, oracle, 2, 3)
    assert oracle.queries == [2, 3] and (m, s) == (6, 2902)
    assert textbook_verify(N_TOY, E_TOY, 6, 2902)
    oracle = SigningOracle(N_TOY, D_TOY)
    assert directed_blinding_forgery(N_TOY, E_TOY, oracle, 100, 5) == (100, 1391)
    assert oracle.queries == [1465]


def test_generated_key() -> None:
    assert N.bit_length() == 2048 and E == 3
    assert pow(pow(12345, D, N), E, N) == 12345


def test_generic_forgery_on_large_key() -> None:
    rng = random.Random(3)
    oracle = SigningOracle(N, D)
    m1, m2 = rng.randrange(2, N), rng.randrange(2, N)
    m, s = generic_product_forgery(N, oracle, m1, m2)
    assert m not in oracle.queries and textbook_verify(N, E, m, s)


def test_directed_forgery_on_large_key() -> None:
    oracle = SigningOracle(N, D)
    target = int.from_bytes(b"pay 1000 to Mallory", "big")
    m, s = directed_blinding_forgery(N, E, oracle, target, r=0x1234567)
    assert m == target and target not in oracle.queries and textbook_verify(N, E, m, s)


def test_pkcs1_round_trip_and_structure() -> None:
    em = emsa_pkcs1_v15(b"hello", 256)
    assert em[:2] == b"\x00\x01" and em[-51:-32] == SHA256_DIGEST_INFO and len(em) == 256
    s = pkcs1_sign(N, D, b"hello")
    assert pkcs1_verify(N, E, b"hello", s) and flawed_pkcs1_verify(N, E, b"hello", s)
    assert not pkcs1_verify(N, E, b"hellp", s) and not flawed_pkcs1_verify(N, E, b"hellp", s)


def test_icbrt() -> None:
    rng = random.Random(4)
    for _ in range(100):
        x = rng.getrandbits(rng.randrange(1, 2100))
        r = icbrt(x)
        assert r ** 3 <= x < (r + 1) ** 3


def test_e3_forgery_beats_only_the_flawed_verifier() -> None:
    message = b"a message the key owner never signed"
    s = bleichenbacher_e3_forgery(N, message)
    block = (s ** 3).to_bytes(256, "big")
    assert s ** 3 < N  # no reduction modulo N takes place
    assert block[4:23] == SHA256_DIGEST_INFO and block[23:55] == hashlib.sha256(message).digest()
    assert block[55:] != bytes(201)  # the garbage the flawed parser never reads
    assert flawed_pkcs1_verify(N, E, message, s)
    assert not pkcs1_verify(N, E, message, s)
    assert not flawed_pkcs1_verify(N, E, b"another message", s)


def test_e3_forgery_needs_room() -> None:
    # The forgery uses only the modulus, so any number of 1024 binary digits shows the limit.
    small_n = (1 << 1023) + 12345
    with pytest.raises(ValueError):
        bleichenbacher_e3_forgery(small_n, b"x")
