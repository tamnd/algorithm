# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signature-malleability/. The authors are listed in prov/67AG3K.jsonl.
"""Tests for ECDSA malleability and the low-s rule. No official test vector
exists for malleated signatures; the secp256k1 constants are copied from
SEC 2, Section 2.4.1, and checked here by n G = O. The keys and nonces come
from a fixed seed."""

import random

from ecdsa_malleability import (SECP256K1, TOY, add, hash_to_z, is_low_s, malleate, mul, normalize_low_s,
                                on_curve, sign_z, txid, verify_z, verify_z_low_s)


def test_curves() -> None:
    for c in (TOY, SECP256K1):
        assert on_curve(c, c.g)
        assert mul(c, c.n, c.g) is None
        assert mul(c, c.n - 1, c.g) == (c.g[0], c.p - c.g[1])


def test_toy_example() -> None:
    c, d, k, z = TOY, 11, 23, 30
    Q = mul(c, d, c.g)
    assert Q == (65, 5) and mul(c, k, c.g) == (61, 28) and mul(c, c.n - k, c.g) == (61, 69)
    sig = sign_z(c, d, z, k)
    assert sig == (61, 3) and malleate(c, sig) == (61, 76)
    assert verify_z(c, Q, z, (61, 3)) and verify_z(c, Q, z, (61, 76))
    assert verify_z_low_s(c, Q, z, (61, 3)) and not verify_z_low_s(c, Q, z, (61, 76))


def test_toy_every_signature_has_a_twin() -> None:
    c, d = TOY, 11
    Q = mul(c, d, c.g)
    for k in range(1, c.n):
        for z in (0, 30, 78):
            try:
                sig = sign_z(c, d, z, k)
            except ValueError:
                continue
            twin = malleate(c, sig)
            assert twin != sig and verify_z(c, Q, z, twin)
            assert is_low_s(c, sig) != is_low_s(c, twin)  # n is odd, so s != n - s


def test_secp256k1_malleability_and_low_s() -> None:
    c, rng = SECP256K1, random.Random(146)
    d = rng.randrange(1, c.n)
    Q = mul(c, d, c.g)
    assert on_curve(c, Q)
    for i in range(3):
        z = hash_to_z(c, b"pay 1 coin to Alice, transaction %d" % i)
        sig = sign_z(c, d, z, rng.randrange(1, c.n))
        twin = malleate(c, sig)
        assert verify_z(c, Q, z, sig) and verify_z(c, Q, z, twin)
        assert txid(b"tx%d" % i, sig) != txid(b"tx%d" % i, twin)
        low = normalize_low_s(c, sig)
        assert is_low_s(c, low) and verify_z_low_s(c, Q, z, low)
        assert not verify_z_low_s(c, Q, z, malleate(c, low))
        assert not verify_z(c, Q, z ^ 1, sig)


def test_range_checks() -> None:
    c, d = TOY, 11
    Q = mul(c, d, c.g)
    assert not verify_z(c, Q, 30, (61, 3 + c.n))
    assert not verify_z(c, Q, 30, (61, 0))
    assert not verify_z(c, Q, 30, (0, 3))
    assert add(c, c.g, mul(c, c.n - 1, c.g)) is None
