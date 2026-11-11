# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cbc-mac/. The authors are listed in prov/3RSETN.jsonl.

import random

import pytest

from aes import AES
from cbc_mac import (
    cbc_mac,
    cbc_mac_length_prepended,
    cbc_mac_random_iv,
    cbc_mac_random_iv_verify,
    cbc_mac_verify,
    emac,
)


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def test_aes_fips197_appendix_c1() -> None:
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    assert a.encrypt_block(bytes.fromhex("00112233445566778899aabbccddeeff")).hex() == "69c4e0d86a7b0430d8cdb78070b4c55a"


def test_derived_from_sp800_38a_f21() -> None:
    # SP 800-38A, Appendix F.2.1 (CBC-AES128.Encrypt). With a zero IV, the CBC-MAC of
    # (P1 xor IV) || P2 || ... || Pj is the ciphertext block Cj of that vector.
    # The first block below is the "Input Block #1" of F.2.1, which is P1 xor IV.
    a = AES(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
    blocks = [
        "6bc0bce12a459991e134741a7f9e1925",
        "ae2d8a571e03ac9c9eb76fac45af8e51",
        "30c81c46a35ce411e5fbc1191a0a52ef",
        "f69f2445df4f9b17ad2b417be66c3710",
    ]
    expected = [
        "7649abac8119b246cee98e9b12e9197d",
        "5086cb9b507219ee95db113a917678b2",
        "73bed6b8e3c1743b7116e69e22229516",
        "3ff1caa1681fac09120eca307586e1a7",
    ]
    for j in range(1, 5):
        m = bytes.fromhex("".join(blocks[:j]))
        assert cbc_mac(a, m).hex() == expected[j - 1]


def test_verify_accepts_and_rejects_one_changed_bit() -> None:
    rng = random.Random(1994)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    m = bytes(rng.randrange(256) for _ in range(64))
    t = cbc_mac(a, m)
    assert cbc_mac_verify(a, m, t)
    for bit in range(0, 8 * len(m), 37):
        m2 = bytearray(m)
        m2[bit // 8] ^= 1 << (bit % 8)
        assert not cbc_mac_verify(a, bytes(m2), t)
    for bit in range(128):
        t2 = bytearray(t)
        t2[bit // 8] ^= 1 << (bit % 8)
        assert not cbc_mac_verify(a, m, bytes(t2))


def test_rejects_partial_blocks() -> None:
    a = AES(bytes(16))
    with pytest.raises(ValueError):
        cbc_mac(a, b"")
    with pytest.raises(ValueError):
        cbc_mac(a, b"seventeen bytes!!")


def test_variable_length_forgery_two_one_block_messages() -> None:
    # The attacker asks for the tags of two one-block messages and forges a tag
    # for a two-block message it never asked for.
    a = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    m1, m2 = b"pay 10 EUR to A.", b"pay 99 EUR to E."
    t1, t2 = cbc_mac(a, m1), cbc_mac(a, m2)
    forged = m1 + xor(m2, t1)
    assert forged not in (m1, m2)
    assert cbc_mac_verify(a, forged, t2)


def test_variable_length_forgery_multi_block() -> None:
    # The same idea for longer messages: m || (m'_1 xor t) || m'_2 .. m'_k has the tag t' of m'.
    rng = random.Random(9797)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    for _ in range(20):
        m = bytes(rng.randrange(256) for _ in range(16 * rng.randrange(1, 5)))
        m2 = bytes(rng.randrange(256) for _ in range(16 * rng.randrange(1, 5)))
        t, t2 = cbc_mac(a, m), cbc_mac(a, m2)
        forged = m + xor(m2[:16], t) + m2[16:]
        assert cbc_mac_verify(a, forged, t2)


def test_repairs_stop_the_forgery() -> None:
    k1 = AES(bytes.fromhex("000102030405060708090a0b0c0d0e0f"))
    k2 = AES(bytes.fromhex("f0e0d0c0b0a090807060504030201000"))
    m1, m2 = b"pay 10 EUR to A.", b"pay 99 EUR to E."
    # Length prepended.
    t1, t2 = cbc_mac_length_prepended(k1, m1), cbc_mac_length_prepended(k1, m2)
    assert cbc_mac_length_prepended(k1, m1 + xor(m2, t1)) != t2
    # EMAC.
    e1, e2 = emac(k1, k2, m1), emac(k1, k2, m2)
    assert emac(k1, k2, m1 + xor(m2, e1)) != e2


def test_random_iv_variant_is_forgeable() -> None:
    # With the IV sent next to the tag, flip any bits of the first block and the same bits of the IV.
    rng = random.Random(113)
    a = AES(bytes(rng.randrange(256) for _ in range(16)))
    m = b"pay 10 EUR to A." + b"reference 000001"
    iv, t = cbc_mac_random_iv(a, m, bytes(rng.randrange(256) for _ in range(16)))
    delta = xor(b"pay 10 EUR to A.", b"pay 99 EUR to E.")
    forged = xor(m[:16], delta) + m[16:]
    assert forged[:16] == b"pay 99 EUR to E."
    assert cbc_mac_random_iv_verify(a, forged, xor(iv, delta), t)


def test_fixed_length_messages_do_not_allow_the_forgery() -> None:
    # The forged message has two blocks; when only one-block messages are tagged and
    # accepted, the splice gives no message of the allowed length.
    a = AES(bytes(range(16)))
    m1, m2 = b"A" * 16, b"B" * 16
    forged = m1 + xor(m2, cbc_mac(a, m1))
    assert len(forged) != len(m1)
