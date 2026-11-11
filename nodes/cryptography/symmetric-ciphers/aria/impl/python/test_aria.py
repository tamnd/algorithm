# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aria/. The authors are listed in prov/8W4VPR.jsonl.

import random

from aria import SB1, SB2, SB3, SB4, decrypt_block, diffusion, encrypt_block, encryption_round_keys

PT = bytes.fromhex("00112233445566778899aabbccddeeff")


# RFC 5794 Appendix A.1, 128-bit key, with the round keys e1, e2 and e13.
def test_rfc5794_a1() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    ct = bytes.fromhex("d718fbd6ab644c739da95f3be6451778")
    ek = encryption_round_keys(key)
    assert ek[0] == 0xD415A75C794B85C5E0D2A0B3CB793BF6
    assert ek[1] == 0x369C65E4B11777AB713A3E1E6601B8F4
    assert ek[12] == 0x0F0AA16DAEE61BD7DFEE5A599970FB35
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# RFC 5794 Appendix A.2, 192-bit key.
def test_rfc5794_a2() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f1011121314151617")
    ct = bytes.fromhex("26449c1805dbe7aa25a468ce263a9e79")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# RFC 5794 Appendix A.3, 256-bit key.
def test_rfc5794_a3() -> None:
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    ct = bytes.fromhex("f92bd7c79fb72e2f2b8f80c1972d24fc")
    assert encrypt_block(key, PT) == ct
    assert decrypt_block(key, ct) == PT


# First rows of SB1, SB3 and SB4 in RFC 5794 Section 2.4.2.
def test_sbox_rows() -> None:
    assert SB1[:8] == [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5]
    assert SB3[:8] == [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38]
    assert SB4[:16] == [0x30, 0x68, 0x99, 0x1B, 0x87, 0xB9, 0x21, 0x78,
                        0x50, 0x39, 0xDB, 0xE1, 0x72, 0x09, 0x62, 0x3C]
    assert sorted(SB2) == list(range(256))


def test_diffusion_is_involution() -> None:
    rng = random.Random(3)
    for _ in range(100):
        x = rng.getrandbits(128)
        assert diffusion(diffusion(x)) == x


def test_round_trip_random() -> None:
    rng = random.Random(4)
    for n in (16, 24, 32):
        for _ in range(4):
            key, m = rng.randbytes(n), rng.randbytes(16)
            assert decrypt_block(key, encrypt_block(key, m)) == m
