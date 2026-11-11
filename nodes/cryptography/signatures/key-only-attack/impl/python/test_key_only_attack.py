# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-only-attack/. The authors are listed in prov/XJ1ZFG.jsonl.
"""Tests for the key-only forgeries. There is no official test vector for an
attack; each forgery is checked against the local verifier, and the toy keys
are textbook examples (RSA with p = 61, q = 53; ElGamal with the group of HAC
Example 11.65)."""

import random

from key_only_attack import (forge_raw_elgamal, forge_textbook_rsa, hashed_rsa_verify,
                             key_only_game, raw_elgamal_verify, textbook_rsa_verify)

N, E, D = 3233, 17, 2753  # p = 61, q = 53
P, G, X, Y = 2357, 2, 1751, 1185  # HAC Example 11.65


def test_toy_keys() -> None:
    assert 61 * 53 == N and E * D % (60 * 52) == 1
    assert pow(G, X, P) == Y


def test_textbook_rsa_forgery_values() -> None:
    assert forge_textbook_rsa(N, E, 2) == (1752, 2)
    assert forge_textbook_rsa(N, E, 1000) == (175, 1000)
    # The forged pair is exactly what the key owner would produce for m.
    assert pow(1752, D, N) == 2 and pow(175, D, N) == 1000


def test_textbook_rsa_forgery_always_verifies() -> None:
    rng = random.Random(1)
    for _ in range(200):
        m, s = forge_textbook_rsa(N, E, rng.randrange(N))
        assert textbook_rsa_verify(N, E, m, s)


def test_game_wins_without_oracle() -> None:
    assert key_only_game((N, E), textbook_rsa_verify, lambda pk: forge_textbook_rsa(*pk, 5))


def test_hash_stops_this_forgery() -> None:
    m, s = forge_textbook_rsa(N, E, 2)
    assert textbook_rsa_verify(N, E, m, s)
    # Under a hashed verifier the same pair is checked against H(message), not m.
    assert not hashed_rsa_verify(N, E, m.to_bytes(2, "big"), s)


def test_raw_elgamal_forgery_values() -> None:
    assert forge_raw_elgamal(P, G, Y, 3, 5) == (1227, (311, 409))
    assert forge_raw_elgamal(P, G, Y, 10, 7) == (1778, (1347, 1827))
    assert pow(Y, 311, P) * pow(311, 409, P) % P == pow(G, 1227, P) == 299


def test_raw_elgamal_forgery_always_verifies() -> None:
    rng = random.Random(2)
    wins = 0
    for _ in range(300):
        u, v = rng.randrange(1, P - 1), rng.randrange(1, P - 1)
        try:
            m, sig = forge_raw_elgamal(P, G, Y, u, v)
        except ValueError:
            continue
        if sig[1] == 0:  # s = 0 is outside the accepted range; pick other u, v
            continue
        assert raw_elgamal_verify(P, G, Y, m, sig)
        wins += 1
    assert wins > 50


def test_raw_elgamal_changed_message_fails() -> None:
    m, sig = forge_raw_elgamal(P, G, Y, 3, 5)
    assert not raw_elgamal_verify(P, G, Y, m + 1, sig)
