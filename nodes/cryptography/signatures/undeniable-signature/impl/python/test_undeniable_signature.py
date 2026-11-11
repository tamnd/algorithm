# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undeniable-signature/. The authors are listed in prov/PHAD4A.jsonl.
"""Tests for the Chaum-van Antwerpen undeniable signature on the toy group p = 2039."""

import random

from undeniable_signature import G, P, Q, confirm, disavow, hash_to_group, honest_signer, keygen, sign

A, Y = keygen(random.Random(1))
OTHER, _ = keygen(random.Random(2))
MSGS = [b"contract %d" % i for i in range(20)]


def test_group_and_hash() -> None:
    assert P == 2 * Q + 1 and pow(G, Q, P) == 1 and G != 1
    for m in MSGS:
        h = hash_to_group(m)
        assert h != 1 and pow(h, Q, P) == 1


def test_true_signature_confirms() -> None:
    rng = random.Random(3)
    for m in MSGS:
        s = sign(A, m)
        assert confirm(Y, m, s, honest_signer(A), rng)
        assert disavow(Y, m, s, honest_signer(A), rng) == "valid"


def test_false_signature_is_disavowed() -> None:
    rng = random.Random(4)
    for m in MSGS:
        fakes = [sign(OTHER, m), sign(A, m + b"?"), pow(G, rng.randrange(1, Q), P)]
        for s in fakes:
            assert not confirm(Y, m, s, honest_signer(A), rng)
            assert disavow(Y, m, s, honest_signer(A), rng) == "forgery"


def test_signer_cannot_deny_a_true_signature() -> None:
    """A signer that answers at random, or with the wrong key, to deny a valid
    signature is caught."""
    rng = random.Random(5)
    liar = random.Random(6)
    for m in MSGS:
        s = sign(A, m)
        assert disavow(Y, m, s, lambda c: pow(G, liar.randrange(1, Q), P), rng) == "signer cheated"
        assert disavow(Y, m, s, honest_signer(OTHER), rng) == "signer cheated"


def test_signer_cannot_confirm_a_false_signature() -> None:
    """Without knowing the exponents, a signer passes with chance 1/q per try."""
    rng = random.Random(7)
    guess = random.Random(8)
    for m in MSGS:
        s = sign(OTHER, m)
        assert not confirm(Y, m, s, lambda c: pow(G, guess.randrange(1, Q), P), rng)
        assert not confirm(Y, m, s, honest_signer(OTHER), rng)


def test_nobody_can_check_alone() -> None:
    """s is h^a: deciding if it is valid without the signer is a decisional
    Diffie-Hellman instance (g, y, h, s). Both answers occur among squares."""
    m = MSGS[0]
    s = sign(A, m)
    assert s != sign(OTHER, m) and pow(s, Q, P) == pow(sign(OTHER, m), Q, P) == 1
